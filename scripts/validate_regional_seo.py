from __future__ import annotations

import itertools
import json
import re
import statistics
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.praesidion.eu"

INDEXABLE_PATHS = {
    "/",
    "/beveiliging-limburg-regios/",
    "/objectbeveiliging-limburg/",
    "/evenementenbeveiliging-limburg/",
    "/receptiebeveiliging-limburg/",
    "/toegangscontrole-limburg/",
    "/mobiele-surveillance-limburg/",
    "/tijdelijke-beveiliging-limburg/",
    "/inzet-bhv-ers-limburg/",
    "/preventiemedewerkers-limburg/",
    "/special-situations-limburg/",
    "/beveiligingsbedrijf-limburg/",
    "/beveiligingsbedrijf-maastricht/",
    "/beveiligingsbedrijf-heerlen/",
    "/beveiligingsbedrijf-sittard-geleen/",
    "/beveiligingsbedrijf-roermond/",
    "/beveiligingsbedrijf-venlo/",
    "/beveiligingsbedrijf-weert/",
    "/beveiliging-aanvragen-limburg/",
    "/beveiligers-inhuren-limburg/",
    "/blog/",
    "/blog/flexibele-inzet-evenementenbeveiliging-wpbr-planning/",
    "/blog/zomerbezetting-toegangsbeheer-objectbeveiliging/",
    "/blog/kwaliteit-inhuur-beveiliging-keurmerken-processen/",
    "/blog/objectbeveiliging-zonder-ruis-roosters-overdracht/",
    "/blog/zzp-inhuur-beveiliging-planning-dossiers-rapportage/",
    "/blog/alarmopvolging-objectbeveiliging-meldkamerafspraken/",
}

PILOT_REGIONAL = {
    "/beveiligingsbedrijf-limburg/",
    "/beveiligingsbedrijf-maastricht/",
    "/beveiligingsbedrijf-heerlen/",
    "/beveiligingsbedrijf-sittard-geleen/",
    "/beveiligingsbedrijf-roermond/",
    "/beveiligingsbedrijf-venlo/",
    "/beveiligingsbedrijf-weert/",
}

REQUIRED_INDEXABLE_SNIPPETS = (
    '<link rel="canonical"',
    '<meta name="robots" content="index, follow',
    'property="og:title"',
    'property="og:description"',
    'aria-label="Breadcrumb"',
    'Laatst bijgewerkt: 2026-07-10',
    '@type":"Organization"',
    '@type":"Service"',
    '@type":"FAQPage"',
    '@type":"BreadcrumbList"',
)

FORBIDDEN_PUBLIC_TERMS = ("SEO-cluster", "AIEO", "Search Console")
NICHE_EXPECTED = {
    "zorgbeveiliging": "https://www.zorgbewaking.nl/",
    "bouwbeveiliging": "https://www.bouwbeveiligingnederland.nl/",
    "logistieke-beveiliging": "https://www.logisticsecurity.nl/",
}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key == "href" and value:
                self.hrefs.append(value)


def page_path(index_file: Path) -> str:
    if index_file == ROOT / "index.html":
        return "/"
    rel = index_file.parent.relative_to(ROOT).as_posix()
    return f"/{rel}/"


def html_files() -> list[Path]:
    return sorted(p for p in ROOT.rglob("index.html") if ".git" not in p.parts)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract(pattern: str, text: str, label: str, errors: list[str], page: str) -> str:
    match = re.search(pattern, text, re.I | re.S)
    if not match:
        errors.append(f"{page}: ontbreekt {label}")
        return ""
    return match.group(1)


def strip_tags(text: str) -> str:
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def token_set(text: str) -> set[str]:
    match = re.search(r"<h2>Regionale context</h2>(.*?)<span class=\"eyebrow\">Diensten</span>", text, re.I | re.S)
    if match:
        text = match.group(1)
    words = re.findall(r"[a-zA-ZÀ-ÿ0-9-]{4,}", strip_tags(text).lower())
    stop = {
        "praesidion",
        "security",
        "limburg",
        "beveiliging",
        "beveiligingsbedrijf",
        "vraag",
        "aanvraag",
        "deze",
        "voor",
        "naar",
        "wordt",
        "zijn",
        "niet",
        "met",
        "een",
        "het",
        "van",
        "bij",
        "die",
        "dat",
        "door",
        "op",
        "en",
    }
    return {w for w in words if w not in stop}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def validate_sitemap(errors: list[str]) -> set[str]:
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        errors.append("sitemap.xml ontbreekt")
        return set()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tree = ET.parse(sitemap)
    locs = {loc.text or "" for loc in tree.findall(".//sm:loc", ns)}
    expected = {BASE_URL + p for p in INDEXABLE_PATHS}
    if locs != expected:
        missing = sorted(expected - locs)
        extra = sorted(locs - expected)
        if missing:
            errors.append(f"sitemap mist {len(missing)} URL(s): {missing[:5]}")
        if extra:
            errors.append(f"sitemap bevat niet-indexeerbare/onverwachte URL(s): {extra[:5]}")
    return locs


def validate_links(text: str, page: str, errors: list[str]) -> None:
    parser = LinkParser()
    parser.feed(text)
    for href in parser.hrefs:
        if href.startswith(("mailto:", "tel:", "http://", "https://", "#")):
            continue
        if not href.startswith("/"):
            continue
        target = href.split("#", 1)[0].split("?", 1)[0]
        candidate = ROOT / target.lstrip("/")
        if target == "/":
            target_file = ROOT / "index.html"
        elif candidate.suffix:
            target_file = candidate
        else:
            target_file = candidate / "index.html"
        if not target_file.exists():
            errors.append(f"{page}: interne link bestaat niet: {href}")


def validate_schema(text: str, page: str, required_types: set[str], errors: list[str]) -> None:
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.I | re.S)
    seen: set[str] = set()
    for block in blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f"{page}: ongeldige JSON-LD: {exc}")
            continue
        kind = data.get("@type")
        if kind:
            seen.add(kind)
    missing = required_types - seen
    if missing:
        errors.append(f"{page}: mist schema type(s): {sorted(missing)}")


def main() -> int:
    errors: list[str] = []
    validate_sitemap(errors)

    files = html_files()
    seen_titles: dict[str, str] = {}
    seen_indexable_canonicals: dict[str, str] = {}
    indexable_count = 0
    noindex_count = 0
    regional_tokens: dict[str, set[str]] = {}

    for file in files:
        path = page_path(file)
        text = read(file)
        title = extract(r"<title>(.*?)</title>", text, "title", errors, path)
        canonical = extract(r'<link rel="canonical" href="([^"]+)"', text, "canonical", errors, path)
        robots = extract(r'<meta name="robots" content="([^"]+)"', text, "robots", errors, path)

        if title:
            if title in seen_titles:
                errors.append(f"{path}: dubbele title met {seen_titles[title]}")
            seen_titles[title] = path
        validate_links(text, path, errors)
        if any(term in text for term in FORBIDDEN_PUBLIC_TERMS):
            errors.append(f"{path}: publieke interne meta-copy gevonden")

        if path in INDEXABLE_PATHS:
            indexable_count += 1
            if canonical in seen_indexable_canonicals:
                errors.append(f"{path}: dubbele indexeerbare canonical met {seen_indexable_canonicals[canonical]}")
            seen_indexable_canonicals[canonical] = path
            for snippet in REQUIRED_INDEXABLE_SNIPPETS:
                if snippet not in text:
                    errors.append(f"{path}: mist verplicht indexeerbaar veld/snippet {snippet}")
            if canonical != BASE_URL + path:
                errors.append(f"{path}: canonical wijkt af van eigen URL: {canonical}")
            validate_schema(text, path, {"Organization", "Service", "FAQPage", "BreadcrumbList"}, errors)
            if path in PILOT_REGIONAL:
                for needle in ("Lokale risico", "Intakevragen", "Aanpak", "Veelgestelde vragen", "areaServed"):
                    if needle not in text:
                        errors.append(f"{path}: mist regionaal contentveld {needle}")
                regional_tokens[path] = token_set(text)
        else:
            if "noindex" in robots:
                noindex_count += 1
            if re.match(r"^/(zorgbeveiliging|bouwbeveiliging|logistieke-beveiliging)-", path):
                service = path.strip("/").rsplit("-", 1)[0]
                service = next((s for s in NICHE_EXPECTED if path.startswith(f"/{s}-")), "")
                expected = NICHE_EXPECTED.get(service)
                if not expected or canonical != expected:
                    errors.append(f"{path}: niche canonical fout: {canonical}")
                if expected and expected not in text:
                    errors.append(f"{path}: zichtbare niche-doorverwijzing ontbreekt")
            elif re.match(r"^/(objectbeveiliging|evenementenbeveiliging|receptiebeveiliging|toegangscontrole|mobiele-surveillance|tijdelijke-beveiliging|inzet-bhv-ers|preventiemedewerkers|special-situations)-", path):
                if "noindex" not in robots:
                    errors.append(f"{path}: legacy servicepagina mist noindex")
                if not canonical.startswith(BASE_URL + "/"):
                    errors.append(f"{path}: legacy canonical hoort intern te consolideren: {canonical}")

    missing_indexable_files = [p for p in sorted(INDEXABLE_PATHS) if not ((ROOT / "index.html") if p == "/" else (ROOT / p.strip("/") / "index.html")).exists()]
    if missing_indexable_files:
        errors.append(f"indexeerbare bestanden ontbreken: {missing_indexable_files}")

    pairs = [jaccard(regional_tokens[a], regional_tokens[b]) for a, b in itertools.combinations(sorted(regional_tokens), 2)]
    median_similarity = statistics.median(pairs) if pairs else 0.0
    if median_similarity >= 0.35:
        errors.append(f"mediane regionale token-set Jaccard te hoog: {median_similarity:.3f}")

    print(f"Indexeerbaar: {indexable_count}")
    print(f"Noindex: {noindex_count}")
    print(f"Sitemap URL's: {len(INDEXABLE_PATHS)}")
    print(f"Mediane regionale token-set Jaccard: {median_similarity:.3f}")
    if errors:
        print("VALIDATIE FOUT")
        for error in errors[:80]:
            print(f"- {error}")
        if len(errors) > 80:
            print(f"- ... plus {len(errors) - 80} extra fout(en)")
        return 1
    print("VALIDATIE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

from __future__ import annotations

import html
import json
import re
import shutil
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.praesidion.eu"
DATE = "2026-06-24"

REGIONS = [
    {"name": "Beek", "cluster": "Zuid-Limburg", "context": "bedrijven, zorglocaties, evenementen en logistieke verbindingen rond Beek en de Westelijke Mijnstreek"},
    {"name": "Beekdaelen", "cluster": "Parkstad en Heuvelland", "context": "dorpskernen, zorginstellingen, recreatie en bedrijfslocaties in Beekdaelen"},
    {"name": "Beesel", "cluster": "Noord-Limburg", "context": "mkb, retail, bedrijventerreinen en evenementen rond Beesel en Reuver"},
    {"name": "Bergen", "cluster": "Noord-Limburg", "context": "bedrijventerreinen, recreatie, zorg en buitengebied in Bergen Limburg"},
    {"name": "Brunssum", "cluster": "Parkstad", "context": "bedrijven, zorgorganisaties, instellingen en evenementen in Brunssum"},
    {"name": "Echt-Susteren", "cluster": "Midden-Limburg", "context": "industrie, logistiek, bouwplaatsen en grensregio rond Echt-Susteren"},
    {"name": "Eijsden-Margraten", "cluster": "Heuvelland", "context": "zorg, hospitality, evenementen, buitengebied en grenslocaties rond Eijsden-Margraten"},
    {"name": "Gennep", "cluster": "Noord-Limburg", "context": "zorglocaties, mkb, logistieke routes en bedrijventerreinen rond Gennep"},
    {"name": "Gulpen-Wittem", "cluster": "Heuvelland", "context": "hospitality, zorg, evenementen en recreatieve locaties in Gulpen-Wittem"},
    {"name": "Heerlen", "cluster": "Parkstad", "context": "kantoren, zorginstellingen, retail, evenementen en publieke locaties in Heerlen"},
    {"name": "Horst aan de Maas", "cluster": "Noord-Limburg", "context": "agri, logistiek, maakbedrijven, zorg en evenementen rond Horst aan de Maas"},
    {"name": "Kerkrade", "cluster": "Parkstad", "context": "zorg, evenementen, bedrijventerreinen en publieke locaties in Kerkrade"},
    {"name": "Landgraaf", "cluster": "Parkstad", "context": "evenementen, zorglocaties, retail en bedrijfsterreinen in Landgraaf"},
    {"name": "Leudal", "cluster": "Midden-Limburg", "context": "mkb, zorg, recreatie, buitengebied en bouwprojecten in Leudal"},
    {"name": "Maasgouw", "cluster": "Midden-Limburg", "context": "recreatie, jachthavens, hospitality, zorg en mkb in Maasgouw"},
    {"name": "Maastricht", "cluster": "Zuid-Limburg", "context": "kantoren, hospitality, zorg, retail, onderwijs, evenementen en internationale organisaties in Maastricht"},
    {"name": "Meerssen", "cluster": "Zuid-Limburg", "context": "mkb, zorg, hospitality en locaties tussen Maastricht en de luchthavenregio"},
    {"name": "Mook en Middelaar", "cluster": "Noord-Limburg", "context": "zorg, recreatie, mkb en grensoverschrijdende routes rond Mook en Middelaar"},
    {"name": "Nederweert", "cluster": "Midden-Limburg", "context": "industrie, agrarische bedrijven, logistieke routes, bouw en mkb rond Nederweert"},
    {"name": "Peel en Maas", "cluster": "Noord-Limburg", "context": "agri, logistiek, maakbedrijven, zorg en evenementen in Peel en Maas"},
    {"name": "Roerdalen", "cluster": "Midden-Limburg", "context": "buitengebied, zorg, recreatie, bouwprojecten en mkb in Roerdalen"},
    {"name": "Roermond", "cluster": "Midden-Limburg", "context": "retail, logistiek, hospitality, zorg, evenementen en bedrijfslocaties in Roermond"},
    {"name": "Simpelveld", "cluster": "Parkstad en Heuvelland", "context": "zorg, evenementen, recreatie en mkb in Simpelveld"},
    {"name": "Sittard-Geleen", "cluster": "Westelijke Mijnstreek", "context": "industrie, logistiek, kantoren, zorg, retail en bouwprojecten in Sittard-Geleen"},
    {"name": "Stein", "cluster": "Westelijke Mijnstreek", "context": "industrie, logistiek, mkb, zorg en grensregio rond Stein"},
    {"name": "Vaals", "cluster": "Heuvelland", "context": "hospitality, zorg, evenementen, onderwijs en grenslocaties in Vaals"},
    {"name": "Valkenburg aan de Geul", "cluster": "Heuvelland", "context": "hospitality, toerisme, evenementen, zorg en publieksstromen in Valkenburg aan de Geul"},
    {"name": "Venlo", "cluster": "Noord-Limburg", "context": "logistiek, distributiecentra, transport, industrie, retail en zorg in Venlo"},
    {"name": "Venray", "cluster": "Noord-Limburg", "context": "zorg, logistiek, maakbedrijven, retail en evenementen in Venray"},
    {"name": "Voerendaal", "cluster": "Parkstad en Heuvelland", "context": "zorg, mkb, recreatie en buitengebied in Voerendaal"},
    {"name": "Weert", "cluster": "Midden-Limburg", "context": "industrie, logistiek, zorg, retail, evenementen en bouwprojecten in Weert"},
]

SERVICES = [
    {
        "name": "Objectbeveiliging",
        "slug": "objectbeveiliging",
        "intro": "beveiligde aanwezigheid bij kantoren, bedrijfspanden, instellingen en terreinen",
        "bullets": ["postinstructies en toegangsafspraken", "rondes, sleutelbeheer en rapportage", "vaste aanspreekpunten voor opdrachtgever en locatie"],
        "faq": "Voor objectbeveiliging kijken we naar openingstijden, bezoekersstromen, kwetsbare zones, meldlijnen en de gewenste zichtbaarheid van de beveiliger.",
    },
    {
        "name": "Zorgbeveiliging",
        "slug": "zorgbeveiliging",
        "intro": "de-escalerende beveiliging voor zorginstellingen, woonzorglocaties, klinieken en opvangomgevingen",
        "bullets": ["rustige, gastvrije aanwezigheid", "afspraken over de-escalatie en escalatielijnen", "afstemming met zorgteam, receptie en facilitaire dienst"],
        "faq": "Zorgbeveiliging vraagt om zichtbaar maar zorgvuldig optreden, met respect voor cliënten, bezoekers en medewerkers.",
    },
    {
        "name": "Logistieke beveiliging",
        "slug": "logistieke-beveiliging",
        "intro": "beveiliging voor warehouses, distributiecentra, transportlocaties en bedrijventerreinen",
        "bullets": ["toegangscontrole voor chauffeurs en bezoekers", "controle op laad- en loszones", "nachtelijke rondes en incidentrapportage"],
        "faq": "Bij logistieke beveiliging sluiten instructies aan op transportbewegingen, dockplanning, terreinindeling en ketenafspraken.",
    },
    {
        "name": "Bouwbeveiliging",
        "slug": "bouwbeveiliging",
        "intro": "tijdelijke beveiliging voor bouwplaatsen, renovaties, materieel, opslag en projectlocaties",
        "bullets": ["rondes buiten werktijd", "controle op hekken, toegang en opslag", "rapportage van afwijkingen, schade of onbevoegde toegang"],
        "faq": "Bouwbeveiliging wordt ingericht op basis van fase, ligging, werktijden, waarde van materieel en bereikbaarheid voor hulpdiensten.",
    },
    {
        "name": "Inzet BHV-ers",
        "slug": "inzet-bhv-ers",
        "intro": "aanvullende veiligheidsbezetting bij evenementen, tijdelijke locaties, piekdrukte en operationele continuïteit",
        "bullets": ["aanwezigheid volgens afgesproken inzetplan", "afstemming met organisator, locatie en beveiligingsteam", "heldere meld- en escalatieroutes"],
        "faq": "BHV-inzet is maatwerk en vervangt geen formele RI&E of wettelijke beoordeling; de opdrachtgever blijft verantwoordelijk voor de juiste organisatie-eisen.",
    },
    {
        "name": "Preventiemedewerkers",
        "slug": "preventiemedewerkers",
        "intro": "preventieve aanwezigheid voor bezoekersstromen, signalering, aanspreekbaarheid en eerste opvolging",
        "bullets": ["gastvrije signalering en aanspreekpunt op locatie", "preventieve rondes en observaties", "doorzetten van meldingen volgens instructie"],
        "faq": "Preventiemedewerkers ondersteunen preventie en signalering; waar beveiligingswerkzaamheden vergunningplichtig zijn wordt de inzet daarop afgestemd.",
    },
    {
        "name": "Special Situations",
        "slug": "special-situations",
        "intro": "maatwerkbeveiliging voor gevoelige, tijdelijke of afwijkende situaties waar standaardinzet niet volstaat",
        "bullets": ["korte intake op risico, context en gevoeligheden", "discrete inzet en duidelijke mandaten", "afspraken over rapportage, bereikbaarheid en escalatie"],
        "faq": "Special Situations wordt bewust als maatwerk behandeld: eerst context en risico, daarna pas profiel, planning en instructies.",
    },
    {
        "name": "Evenementenbeveiliging",
        "slug": "evenementenbeveiliging",
        "intro": "beveiliging en publieksbegeleiding bij zakelijke events, publieksevenementen en tijdelijke drukte",
        "bullets": ["ingangen, doorstroom en publieksbewegingen", "samenwerking met organisator, locatie en hulpdiensten", "briefing, zichtbaarheid en incidentopvolging"],
        "faq": "Voor evenementenbeveiliging zijn bezoekersprofiel, locatie, vergunningseisen en draaiboek bepalend voor het inzetvoorstel.",
    },
    {
        "name": "Receptiebeveiliging",
        "slug": "receptiebeveiliging",
        "intro": "beveiligde ontvangst, bezoekersregistratie en eerste aanspreekpunt voor kantoren en instellingen",
        "bullets": ["gastvrije ontvangst met veiligheidsbewustzijn", "bezoekersregistratie en toegangsafspraken", "koppeling met facilitaire en securityprocessen"],
        "faq": "Receptiebeveiliging combineert hospitality met alertheid, instructies en duidelijke opvolging bij afwijkingen.",
    },
    {
        "name": "Toegangscontrole",
        "slug": "toegangscontrole",
        "intro": "controle van bezoekers, leveranciers, medewerkers en voertuigen op locaties met verhoogde toegangsrisico's",
        "bullets": ["controlepunten en registratieafspraken", "werkinstructies voor bezoekers en leveranciers", "opschaling bij afwijkingen of onbevoegde toegang"],
        "faq": "Toegangscontrole werkt het best met duidelijke criteria: wie mag waar naar binnen, wanneer, met welke registratie en wie beslist bij twijfel.",
    },
    {
        "name": "Mobiele surveillance",
        "slug": "mobiele-surveillance",
        "intro": "controlerondes, sleutelservice en zichtbare aanwezigheid voor meerdere locaties of risicomomenten",
        "bullets": ["preventieve en afgesproken controlerondes", "controle op afsluiting, schade en afwijkingen", "rapportage en alarmopvolging volgens afspraak"],
        "faq": "Mobiele surveillance is geschikt wanneer continue bezetting niet nodig is, maar regelmatige controle en snelle opvolging wel gewenst zijn.",
    },
    {
        "name": "Tijdelijke beveiliging",
        "slug": "tijdelijke-beveiliging",
        "intro": "snel schaalbare beveiliging bij projecten, incidenten, drukte, leegstand of overbrugging van personele capaciteit",
        "bullets": ["tijdelijk inzetplan met start- en evaluatiemoment", "duidelijke instructies voor de eerste dienst", "opschalen of afbouwen op basis van risico en behoefte"],
        "faq": "Tijdelijke beveiliging begint met een compacte intake zodat de eerste inzet praktisch, veilig en controleerbaar start.",
    },
]


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.lower().replace("&", " en ")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value


def read_style() -> str:
    text = (ROOT / "index.html").read_text(encoding="utf-8")
    start = text.index("<style>")
    end = text.index("</style>") + len("</style>")
    return text[start:end]

STYLE = read_style()
FONT = '<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&display=swap" rel="stylesheet">'


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def service_page(service: dict) -> str:
    title = f"{service['name']} Limburg | Praesidion Security"
    description = f"{service['name']} in Limburg nodig? Praesidion Security levert maatwerk voor bedrijven, instellingen en projecten met intake, instructies, rapportage en duidelijke opvolging."
    slug = f"{service['slug']}-limburg"
    canonical = f"{BASE_URL}/{slug}/"
    service_ld = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"{service['name']} Limburg",
        "provider": {"@type": "Organization", "name": "Praesidion Security B.V.", "url": BASE_URL + "/"},
        "areaServed": [r["name"] for r in REGIONS] + ["Limburg"],
        "serviceType": service["name"],
        "url": canonical,
    }
    faq_ld = faq_schema([
        (f"Wanneer kies ik voor {service['name'].lower()} in Limburg?", service["faq"]),
        ("Werkt Praesidion in heel Limburg?", "Praesidion richt zich op heel Limburg, waaronder Noord-Limburg, Midden-Limburg, Parkstad, de Westelijke Mijnstreek en Zuid-Limburg."),
        ("Kan ik direct een voorstel aanvragen?", "Ja. Stuur de locatie, gewenste tijden, risico-inschatting en contactgegevens mee; daarna volgt een passend inzetvoorstel."),
    ])
    region_links = "".join(f'<a href="/{service["slug"]}-{slugify(r["name"])}/">{esc(service["name"])} {esc(r["name"])}</a>' for r in REGIONS)
    bullets = "".join(f"<li>{esc(b)}</li>" for b in service["bullets"])
    return page_shell(title, description, canonical, service_ld, faq_ld, f"{service['name']} Limburg", f"Praesidion ondersteunt organisaties in Limburg met {service['intro']}. De inzet wordt afgestemd op locatie, risico, openingstijden en gewenste opvolging.", f"Aanvraag {service['name']} Limburg", f"{service['name']} voor heel Limburg", f"Deze pagina bundelt de regionale vraag naar {service['name'].lower()} in Limburg. Voor lokale vindbaarheid zijn er aparte pagina's per gemeente/regio, zodat zoekmachines en opdrachtgevers direct de juiste context zien.", bullets, region_links, "Lokale regio's voor deze dienst")


def combo_page(service: dict, region: dict) -> str:
    title = f"{service['name']} {region['name']} | Praesidion Security"
    description = f"{service['name']} in {region['name']} nodig? Praesidion Security levert praktische beveiligingsinzet voor {region['context']} met duidelijke instructies en rapportage."
    slug = f"{service['slug']}-{slugify(region['name'])}"
    canonical = f"{BASE_URL}/{slug}/"
    service_ld = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"{service['name']} {region['name']}",
        "provider": {"@type": "Organization", "name": "Praesidion Security B.V.", "url": BASE_URL + "/"},
        "areaServed": [region["name"], region["cluster"], "Limburg"],
        "serviceType": service["name"],
        "url": canonical,
    }
    faq_ld = faq_schema([
        (f"Wat regelt Praesidion bij {service['name'].lower()} in {region['name']}?", f"Praesidion start met intake op locatie, risico, tijden, bezoekersstromen en escalatieafspraken. Daarna volgt een praktisch inzetvoorstel voor {service['name'].lower()} in {region['name']}.") ,
        ("Is tijdelijke inzet mogelijk?", "Ja, tijdelijke inzet is mogelijk voor projecten, piekdrukte, incidenten of overbrugging. Structurele inzet kan ook na evaluatie van de locatiebehoefte."),
        ("Doet Praesidion juridische of vergunningclaims op deze pagina?", "Nee. Deze pagina is bedoeld als commerciële en operationele informatie. Specifieke wettelijke eisen worden per opdracht bron- en situatiegericht gecontroleerd."),
    ])
    related_services = "".join(f'<a href="/{s["slug"]}-{slugify(region["name"])}/">{esc(s["name"])} {esc(region["name"])}</a>' for s in SERVICES if s is not service)
    regional_peers = [r for r in REGIONS if r["cluster"] == region["cluster"] and r["name"] != region["name"]][:6]
    peer_links = "".join(f'<a href="/{service["slug"]}-{slugify(r["name"])}/">{esc(service["name"])} {esc(r["name"])}</a>' for r in regional_peers)
    bullets = "".join(f"<li>{esc(b)}</li>" for b in service["bullets"])
    extra = f"<h3>Ook rond {esc(region['cluster'])}</h3><div class=\"links\">{peer_links}</div>" if peer_links else ""
    return page_shell(title, description, canonical, service_ld, faq_ld, f"{service['name']} {region['name']}", f"Praesidion ondersteunt opdrachtgevers in {region['name']} met {service['intro']}. De aanpak past bij {region['context']}.", f"Aanvraag {service['name']} {region['name']}", f"Waarom {service['name'].lower()} in {region['name']}?", f"{region['name']} valt binnen {region['cluster']}. Beveiliging werkt daar alleen goed als postinstructies, bereikbaarheid, bezoekersstromen en lokale risico's vooraf concreet worden gemaakt.", bullets, related_services + extra, "Andere beveiligingsdiensten in deze regio")


def faq_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }


def page_shell(title, description, canonical, service_ld, faq_ld, h1, lead, subject, mid_head, mid_text, bullets, link_html, link_head):
    return f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}" />
<link rel="canonical" href="{esc(canonical)}" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(description)}" />
<meta property="og:type" content="website" />
<meta property="og:locale" content="nl_NL" />
<script type="application/ld+json">{json.dumps(service_ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
{FONT}{STYLE}
</head>
<body>
<header class="topbar"><div class="container nav"><a class="brand" href="/"><span class="mark"></span><span>Praesidion Security</span></a><nav class="links"><a href="/beveiliging-limburg-regios/">Regio's</a><a href="/#diensten">Diensten</a><a href="/#contact">Contact</a></nav></div></header>
<main>
<section class="hero"><div class="container"><span class="eyebrow">Praesidion Security · Limburg</span><h1>{esc(h1)}</h1><p class="lead">{esc(lead)}</p><div class="actions"><a class="btn primary" href="mailto:info@praesidion.nl?subject={esc(subject)}">Vraag voorstel aan</a><a class="btn secondary" href="/beveiliging-limburg-regios/">Bekijk regio-overzicht</a></div></div></section>
<section><div class="container grid"><article class="card"><h2>{esc(mid_head)}</h2><p class="muted">{esc(mid_text)}</p></article><article class="card"><h2>Wat regelen we concreet?</h2><ul>{bullets}</ul></article><article class="card"><h2>Werkwijze</h2><p class="muted">Eerst intake, daarna een voorstel met inzet, profiel, tijden, instructies, rapportage en evaluatiemoment. Geen standaardclaim, maar een praktisch beveiligingsplan per locatie.</p></article></div></section>
<section class="band"><div class="container"><h2>{esc(link_head)}</h2><p class="muted">Snel naar verwante lokale pagina's binnen het Praesidion SEO-cluster voor Limburg.</p><div class="links">{link_html}</div></div></section>
<section><div class="container"><h2>Veelgestelde vragen</h2><details><summary>Hoe start een aanvraag?</summary><p>Mail de locatie, gewenste tijden, aanleiding, bezoekers- of personeelsstromen en eventuele bijzonderheden. Daarna volgt een passende intake.</p></details><details><summary>Is dit juridisch advies?</summary><p>Nee. Deze pagina is bedoeld als commerciële en operationele informatie. Vergunningen, cao, BHV- of arbovragen worden per concrete situatie gecontroleerd.</p></details><details><summary>Kan Praesidion tijdelijk of structureel leveren?</summary><p>Beide zijn bespreekbaar. Tijdelijke inzet kan bij projecten, drukte of incidenten; structurele inzet volgt uit een afgestemd operationeel plan.</p></details></div></section>
<section id="contact"><div class="container card"><h2>Bespreek uw beveiligingsvraag</h2><p class="muted">Wilt u weten welke inzet past bij uw locatie, zorgomgeving, bouwplaats, logistieke site of bijzondere situatie? Vraag een praktisch voorstel aan.</p><a class="btn primary" href="mailto:info@praesidion.nl">Mail info@praesidion.nl</a></div></section>
</main><footer><div class="container">© Praesidion Security B.V. — specialistische beveiligingsdiensten. Informatiepagina; inzet en voorwaarden altijd op basis van intake en voorstel.</div></footer>
</body></html>
'''


def hub_page():
    title = "Beveiliging Limburg per regio en dienst | Praesidion Security"
    description = "Overzicht van Praesidion Security SEO-pagina's voor Limburg: objectbeveiliging, zorgbeveiliging, logistieke beveiliging, bouwbeveiliging, BHV-inzet, preventie en Special Situations per regio."
    canonical = f"{BASE_URL}/beveiliging-limburg-regios/"
    service_blocks = []
    for service in SERVICES:
        links = "".join(f'<a href="/{service["slug"]}-{slugify(r["name"])}/">{esc(r["name"])}</a>' for r in REGIONS)
        service_blocks.append(f'<article class="card"><h2><a href="/{service["slug"]}-limburg/">{esc(service["name"])} Limburg</a></h2><p class="muted">{esc(service["intro"])}.</p><div class="links">{links}</div></article>')
    org_ld = {"@context": "https://schema.org", "@type": "Organization", "name": "Praesidion Security B.V.", "url": BASE_URL + "/", "areaServed": ["Limburg", "Nederland"]}
    faq_ld = faq_schema([
        ("Welke regio's in Limburg bedient Praesidion?", "Dit overzicht bevat lokale pagina's voor alle Limburgse gemeenten en clusters zoals Noord-Limburg, Midden-Limburg, Parkstad, Westelijke Mijnstreek en Zuid-Limburg."),
        ("Welke beveiligingsdiensten staan in het overzicht?", "Onder meer objectbeveiliging, zorgbeveiliging, logistieke beveiliging, bouwbeveiliging, inzet BHV-ers, preventiemedewerkers, Special Situations, evenementenbeveiliging, receptiebeveiliging, toegangscontrole, mobiele surveillance en tijdelijke beveiliging."),
    ])
    return f'''<!doctype html>
<html lang="nl"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(title)}</title><meta name="description" content="{esc(description)}" /><link rel="canonical" href="{canonical}" />
<meta name="robots" content="index, follow, max-image-preview:large" /><meta property="og:title" content="{esc(title)}" /><meta property="og:description" content="{esc(description)}" /><meta property="og:type" content="website" /><meta property="og:locale" content="nl_NL" />
<script type="application/ld+json">{json.dumps(org_ld, ensure_ascii=False)}</script><script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>{FONT}{STYLE}</head>
<body><header class="topbar"><div class="container nav"><a class="brand" href="/"><span class="mark"></span><span>Praesidion Security</span></a><nav class="links"><a href="/#diensten">Diensten</a><a href="/#contact">Contact</a></nav></div></header>
<main><section class="hero"><div class="container"><span class="eyebrow">SEO-overzicht Limburg</span><h1>Beveiliging in Limburg per regio en dienst</h1><p class="lead">Praesidion Security heeft nu een lokaal vindbaar SEO-cluster voor Limburg: per dienst én per gemeente/regio. Gebruik dit overzicht als ingang naar de specifieke pagina's.</p><div class="actions"><a class="btn primary" href="mailto:info@praesidion.nl?subject=Aanvraag beveiliging Limburg">Vraag voorstel aan</a><a class="btn secondary" href="/#diensten">Terug naar hoofdpagina</a></div></div></section>
<section><div class="container grid">{''.join(service_blocks)}</div></section></main><footer><div class="container">© Praesidion Security B.V. — regio- en dienstenoverzicht voor Limburg.</div></footer></body></html>'''


def write_page(slug: str, content: str):
    d = ROOT / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(content, encoding="utf-8")


def sitemap():
    urls = ["/"]
    urls += ["/beveiliging-limburg-regios/"]
    urls += [f"/{s['slug']}-limburg/" for s in SERVICES]
    for s in SERVICES:
        for r in REGIONS:
            urls.append(f"/{s['slug']}-{slugify(r['name'])}/")
    # Preserve older existing manually-created pages not covered above.
    for idx in sorted(ROOT.glob("*/index.html")):
        slug = idx.parent.name
        path = f"/{slug}/"
        if path not in urls:
            urls.append(path)
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path in urls:
        prio = "1.0" if path == "/" else ("0.85" if path == "/beveiliging-limburg-regios/" else "0.72")
        body.append(f"  <url><loc>{BASE_URL}{path}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>{prio}</priority></url>")
    body.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(body), encoding="utf-8")


def llms():
    services = ", ".join(s["name"] for s in SERVICES)
    regions = ", ".join(r["name"] for r in REGIONS)
    content = f"""# Praesidion Security B.V. Limburg security pages

Praesidion Security B.V. provides professional security services in Limburg. This site contains service and region landing pages for: {services}.

Primary service area: Limburg, including {regions}.

Important interpretation notes:
- Pages are commercial and operational information, not legal, permit, BHV, occupational-safety or compliance advice.
- Deployment, guard profile, legal requirements and pricing depend on intake, location, risk, hours, sector and required instructions.
- Do not infer guaranteed availability, fixed pricing, customer references or legal certainty from these pages.

Canonical overview: {BASE_URL}/beveiliging-limburg-regios/
Sitemap: {BASE_URL}/sitemap.xml
Contact: info@praesidion.nl
"""
    (ROOT / "llms.txt").write_text(content, encoding="utf-8")


def update_homepage_link():
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    if "/beveiliging-limburg-regios/" in text:
        return
    marker = '<section id="contact"'
    insert = '<section class="band"><div class="container"><span class="eyebrow">Limburg SEO-cluster</span><h2>Beveiliging per regio en dienst</h2><p class="lead">Bekijk lokale Praesidion-pagina\'s voor objectbeveiliging, zorgbeveiliging, logistieke beveiliging, bouwbeveiliging, BHV-inzet, preventie en Special Situations in Limburg.</p><div class="actions"><a class="btn primary" href="/beveiliging-limburg-regios/">Bekijk alle regio\'s en diensten</a></div></div></section>'
    if marker in text:
        text = text.replace(marker, insert + marker, 1)
        path.write_text(text, encoding="utf-8")


def main():
    # Backup current sitemap once for local rollback/reference.
    if (ROOT / "sitemap.xml").exists() and not (ROOT / "sitemap.xml.before-limburg-seo").exists():
        shutil.copy2(ROOT / "sitemap.xml", ROOT / "sitemap.xml.before-limburg-seo")
    write_page("beveiliging-limburg-regios", hub_page())
    for service in SERVICES:
        write_page(f"{service['slug']}-limburg", service_page(service))
        for region in REGIONS:
            write_page(f"{service['slug']}-{slugify(region['name'])}", combo_page(service, region))
    sitemap()
    llms()
    update_homepage_link()
    print(f"Generated {1 + len(SERVICES) + len(SERVICES)*len(REGIONS)} pages, sitemap.xml and llms.txt")

if __name__ == "__main__":
    main()

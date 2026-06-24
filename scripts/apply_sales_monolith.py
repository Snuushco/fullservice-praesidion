from pathlib import Path
import json, html

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = 'https://www.praesidion.eu'
DATE = '2026-06-24'

index_path = ROOT / 'index.html'
index = index_path.read_text(encoding='utf-8')
style = index[index.index('<style>'):index.index('</style>') + len('</style>')]
font = '<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&display=swap" rel="stylesheet">'

services = [
    'Objectbeveiliging', 'Zorgbeveiliging', 'Logistieke beveiliging', 'Bouwbeveiliging',
    'BHV-ers', 'Preventiemedewerkers', 'Special Situations', 'Evenementenbeveiliging',
    'Receptiebeveiliging', 'Toegangscontrole', 'Mobiele surveillance', 'Tijdelijke beveiliging',
    'Alarmopvolging', 'Hospitality security', 'Retailbeveiliging', 'Ondersteuning bij acute risico’s',
]
sectors = [
    'zorginstellingen', 'logistiek en transport', 'bouwplaatsen', 'kantoren en bedrijfspanden',
    'retail en hospitality', 'evenementen', 'publieke en maatschappelijke locaties',
    'industrie en bedrijventerreinen', 'tijdelijke en gevoelige situaties',
]

def e(value: str) -> str:
    return html.escape(value, quote=True)

org_ld = {
    '@context': 'https://schema.org', '@type': 'Organization', 'name': 'Praesidion Security B.V.',
    'url': BASE_URL + '/', 'areaServed': ['Limburg', 'Nederland'],
    'description': 'Praesidion Security B.V. positioneert zich als één loket voor beveiligingsaanvragen in Limburg: zelf uitvoeren waar passend en anders doorzetten naar geschikte partners na intake.',
}
service_ld = {
    '@context': 'https://schema.org', '@type': 'Service', 'name': 'Beveiligingsaanvraag Limburg',
    'provider': {'@type': 'Organization', 'name': 'Praesidion Security B.V.', 'url': BASE_URL + '/'},
    'areaServed': ['Limburg', 'Noord-Limburg', 'Midden-Limburg', 'Zuid-Limburg', 'Parkstad', 'Westelijke Mijnstreek'],
    'serviceType': services, 'url': BASE_URL + '/beveiliging-aanvragen-limburg/',
}
faq_ld = {
    '@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': 'Kan Praesidion elke beveiligingsvraag aannemen?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Praesidion start met intake en beoordeelt daarna of de aanvraag zelf ingevuld kan worden. Als een andere specialist beter past, kan Praesidion de aanvraag gestructureerd doorzetten naar een passende partner.'}},
        {'@type': 'Question', 'name': 'Voor welke regio is dit bedoeld?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'De focus ligt op Limburg: Noord-Limburg, Midden-Limburg, Zuid-Limburg, Parkstad en de Westelijke Mijnstreek.'}},
        {'@type': 'Question', 'name': 'Wat moet ik meesturen bij een aanvraag?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Vermeld locatie, gewenste dagen en tijden, type object of sector, aanleiding, risico-inschatting, gewenste zichtbaarheid, startdatum en contactgegevens.'}},
    ],
}
service_cards = ''.join(
    f'<article class="card"><h3>{e(s)}</h3><p class="muted">Intake, passende inzet en waar nodig partnerroutering voor {e(s.lower())} in Limburg.</p></article>'
    for s in services
)
sector_links = ''.join(
    f'<a href="mailto:info@praesidion.nl?subject=Aanvraag beveiliging {e(s)} Limburg">{e(s)}</a>'
    for s in sectors
)
page = f'''<!doctype html>
<html lang="nl"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Beveiliging aanvragen Limburg | Eén loket via Praesidion Security</title>
<meta name="description" content="Eén loket voor beveiligingsaanvragen in Limburg. Praesidion Security beoordeelt objectbeveiliging, zorgbeveiliging, logistiek, bouw, BHV, preventie, Special Situations en partnerdoorzet." />
<link rel="canonical" href="{BASE_URL}/beveiliging-aanvragen-limburg/" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta property="og:title" content="Beveiliging aanvragen Limburg | Praesidion Security" />
<meta property="og:description" content="Alle beveiligingsvragen in Limburg via één intake: zelf invullen waar passend, anders gericht doorzetten naar geschikte partners." />
<meta property="og:type" content="website" /><meta property="og:locale" content="nl_NL" />
<script type="application/ld+json">{json.dumps(org_ld, ensure_ascii=False)}</script><script type="application/ld+json">{json.dumps(service_ld, ensure_ascii=False)}</script><script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>{font}{style}</head>
<body><header class="topbar"><div class="container nav"><a class="brand" href="/"><span class="mark"></span><span>Praesidion Security</span></a><nav class="links"><a href="/beveiliging-limburg-regios/">Regio's</a><a href="/#diensten">Diensten</a><a class="cta" href="mailto:info@praesidion.nl?subject=Beveiligingsaanvraag Limburg">Aanvraag doen</a></nav></div></header>
<main><section class="hero"><div class="container"><span class="eyebrow">Security sales monolith · Limburg</span><h1>Eén loket voor elke beveiligingsaanvraag in Limburg</h1><p class="lead">Praesidion Security wil de centrale ingang zijn voor beveiliging in Limburg. Wij vangen aanvragen breed af, kwalificeren de situatie, leveren zelf waar dat past en zetten gespecialiseerde vragen gecontroleerd door naar geschikte partners wanneer dat beter is voor de opdrachtgever.</p><div class="actions"><a class="btn primary" href="mailto:info@praesidion.nl?subject=Beveiligingsaanvraag Limburg&body=Locatie:%0D%0AType beveiliging:%0D%0AGewenste dagen/tijden:%0D%0AStartdatum:%0D%0AAanleiding/risico:%0D%0AContactgegevens:">Start intake</a><a class="btn secondary" href="/beveiliging-limburg-regios/">Bekijk alle diensten/regio's</a></div></div></section>
<section><div class="container"><div class="section-head"><span class="eyebrow">Aanvraagroutering</span><h2>Van zoekvraag naar concrete opvolging</h2><p class="lead">De pagina is gebouwd als commerciële vangnetpagina: breed genoeg voor alle security-intentie, maar concreet genoeg om aanvragen direct te triageren.</p></div><div class="grid"><article class="card"><h3>1. Intake</h3><p class="muted">Locatie, dienst, tijden, sector, risico, startdatum en gewenste zichtbaarheid worden eerst helder gemaakt.</p></article><article class="card"><h3>2. Match</h3><p class="muted">Praesidion beoordeelt of eigen inzet logisch is of dat een gespecialiseerde partner beter past.</p></article><article class="card"><h3>3. Opvolging</h3><p class="muted">De aanvraag wordt omgezet naar voorstel, intakegesprek of warme partnerdoorzet met duidelijke scope.</p></article></div></div></section>
<section class="band"><div class="container"><h2>Alles wat met beveiliging te maken heeft</h2><p class="muted">Deze commerciële hub vangt zowel directe koopintentie als oriënterende zoekvragen af. Per dienst blijven de bestaande lokale SEO-pagina's de dieptepagina's.</p><div class="grid">{service_cards}</div></div></section>
<section><div class="container grid"><article class="card"><h2>Voor welke situaties?</h2><p class="muted">Praesidion richt zich op aanvragen vanuit onder meer:</p><div class="links">{sector_links}</div></article><article class="card"><h2>Partnerdoorzet zonder gezichtsverlies</h2><p class="muted">Niet elke aanvraag hoeft door Praesidion zelf ingevuld te worden. Belangrijk is dat de lead binnenkomt, professioneel wordt gekwalificeerd en niet verloren gaat aan versnipperde aanbieders.</p></article><article class="card"><h2>Dominantie in Limburg</h2><p class="muted">De combinatie van brede vangnetpagina, dienst×regio-pagina's, monitoring en review-gated outreach maakt Praesidion vindbaar op vrijwel elke relevante beveiligingsvraag in Limburg.</p></article></div></section>
<section id="contact"><div class="container card"><h2>Leg uw beveiligingsvraag neer</h2><p class="muted">Stuur minimaal locatie, gewenste inzet, dagen/tijden, startdatum, aanleiding en contactgegevens. Dan kan de aanvraag snel worden beoordeeld.</p><a class="btn primary" href="mailto:info@praesidion.nl?subject=Beveiligingsaanvraag Limburg&body=Locatie:%0D%0AType beveiliging:%0D%0AGewenste dagen/tijden:%0D%0AStartdatum:%0D%0AAanleiding/risico:%0D%0AContactgegevens:">Mail de aanvraag</a></div></section>
</main><footer><div class="container">© Praesidion Security B.V. — één loket voor beveiligingsaanvragen in Limburg. Concrete inzet altijd op basis van intake, beschikbaarheid en passend voorstel.</div></footer></body></html>'''
page_dir = ROOT / 'beveiliging-aanvragen-limburg'
page_dir.mkdir(exist_ok=True)
(page_dir / 'index.html').write_text(page, encoding='utf-8')

if '/beveiliging-aanvragen-limburg/' not in index:
    marker = '<section id="contact"'
    insert = '<section class="band"><div class="container"><span class="eyebrow">Eén loket voor beveiliging</span><h2>Elke beveiligingsaanvraag in Limburg via Praesidion</h2><p class="lead">Object, zorg, logistiek, bouw, BHV, preventie, evenementen of een bijzondere situatie: Praesidion vangt de aanvraag af, kwalificeert de behoefte en levert zelf of routeert naar een geschikte partner.</p><div class="actions"><a class="btn primary" href="/beveiliging-aanvragen-limburg/">Beveiliging aanvragen</a></div></div></section>'
    if marker not in index:
        raise RuntimeError('contact marker not found in homepage')
    index_path.write_text(index.replace(marker, insert + marker, 1), encoding='utf-8')

sitemap_path = ROOT / 'sitemap.xml'
sitemap = sitemap_path.read_text(encoding='utf-8')
url = f'{BASE_URL}/beveiliging-aanvragen-limburg/'
if url not in sitemap:
    entry = f'  <url><loc>{url}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.92</priority></url>\n'
    sitemap_path.write_text(sitemap.replace('</urlset>', entry + '</urlset>'), encoding='utf-8')

llms_path = ROOT / 'llms.txt'
llms = llms_path.read_text(encoding='utf-8') if llms_path.exists() else ''
line = f'Commercial lead hub: {BASE_URL}/beveiliging-aanvragen-limburg/ — broad intake page for any security request in Limburg; Praesidion can self-deliver or route to suitable partners after intake.\n'
if line not in llms:
    needle = 'Canonical overview: '
    if needle in llms:
        llms = llms.replace(needle, line + needle)
    else:
        llms += '\n' + line
    llms_path.write_text(llms, encoding='utf-8')

docs = ROOT / 'docs'
docs.mkdir(exist_ok=True)
blueprint = '''# Praesidion Security — Security Sales Monolith Limburg

## Doel
Praesidion moet de centrale commerciële ingang worden voor alles wat met beveiliging in Limburg te maken heeft. Niet alleen aanvragen die direct door Praesidion zelf worden ingevuld, maar ook aanvragen die na intake beter passen bij partners.

## Positionering
- Eén loket voor beveiligingsvragen in Limburg.
- Zelf leveren waar Praesidion operationeel en commercieel goed past.
- Warm doorzetten naar geschikte partners wanneer specialistische capaciteit, locatie, schaal of vergunningstechniek daarom vraagt.
- Praesidion blijft eigenaar van de leadkwalificatie, relatie en opvolgdiscipline.

## Leadvangst-laag
1. Brede hub: `/beveiliging-aanvragen-limburg/`.
2. Dienst × regio SEO-cluster: bestaande 385 pagina's.
3. Sectorintentie: zorg, logistiek, bouw, evenementen, retail, industrie, hospitality, publieke locaties.
4. Acute vraag: tijdelijke beveiliging, incident, overbrugging, spoedbezetting.
5. Speciale vraag: Special Situations, gevoelige situaties, discrete inzet, afwijkende risico's.

## Intakevelden
- Organisatie en contactpersoon.
- Locatie(s) en regio.
- Type beveiliging of probleemomschrijving.
- Gewenste startdatum, dagen, tijden en duur.
- Aanleiding/risico: incident, preventie, structureel, vergunning, bezettingsprobleem.
- Gewenste zichtbaarheid: gastvrij, preventief, controlerend, discreet.
- Interne deadline en beslisser.
- Of partnerdoorzet akkoord is als Praesidion niet zelf de beste match is.

## Routingregels
- **Zelf oppakken:** past bij Praesidion-profiel, regio, capaciteit, kwaliteit en marge.
- **Partnerdoorzet:** specialistische inzet, schaalvraag, buiten kerncapaciteit, betere lokale partner, of lagere strategische fit.
- **Afwijzen/escaleren:** onduidelijke legaliteit, onveilige opdrachtvoorwaarden, onhaalbare start, ontbrekende mandaten of compliance-risico.

## Partnernetwerk-opzet
Minimaal registreren per partner:
- bedrijfsnaam, contactpersoon, regio's;
- diensten/specialismen;
- vergunning/status die relevant is voor het type werk;
- responstijd en capaciteit;
- marge-/fee-afspraak of wederkerigheid;
- non-solicit/klantbescherming;
- kwaliteitssignalen en incidenten;
- laatste evaluatie.

## Sales funnel
1. Zoekvraag komt binnen via hub, lokale pagina, mail, telefoon of referral.
2. Intake binnen 1 werkdag.
3. Kwalificatie: waarde, urgentie, dienst, regio, risico, fit.
4. Besluit: zelf doen / partner / afwijzen / extra info nodig.
5. Opvolging: voorstel, intakegesprek of warme overdracht.
6. CRM-status en reminder.
7. Na 7/14/30 dagen opvolging en conversiecontrole.

## Review-gates
- Geen outreach, partnerbenadering, LinkedIn-posts of e-mailcampagnes zonder Guus-approval.
- SEO/site-publicatie mag autonoom binnen bestaande Praesidion-kaders.
- Partnerclaims, vergunningclaims, klantcases en beschikbaarheid nooit verzinnen.

## Eerste 14 dagen uitvoering
1. Hub live zetten en linken vanaf homepage.
2. Leadformulier of mailto-intake vervangen door echt formulier/CRM zodra backend beschikbaar is.
3. Partnerregister opzetten.
4. Top 25 Limburgse zoekintenties selecteren voor verdiepende sectorpagina's.
5. Wekelijkse marketing monitor gebruiken om nieuwe pagina's/haakjes te bepalen.
6. SSL/custom-domain gate oplossen zodat indexatie niet wordt afgeremd.
'''
(docs / 'praesidion-security-sales-monolith.md').write_text(blueprint, encoding='utf-8')

print('created page/docs and updated homepage/sitemap/llms')
print('page bytes', (page_dir / 'index.html').stat().st_size)
print('sitemap contains hub', url in sitemap_path.read_text(encoding='utf-8'))
print('homepage contains hub', '/beveiliging-aanvragen-limburg/' in index_path.read_text(encoding='utf-8'))

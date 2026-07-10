from __future__ import annotations

import html
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.praesidion.eu"
UPDATED = "2026-07-10"

FONT = '<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&display=swap" rel="stylesheet">'

STYLE = """
<style>
:root{--ink:#f7f1e7;--ink2:#d7cbbb;--muted:#a89986;--bg:#090b0f;--panel:rgba(255,255,255,.075);--panel2:rgba(255,255,255,.11);--line:rgba(255,255,255,.16);--gold:#d8b45b;--gold2:#f3d894;--blue:#5fa8ff;--green:#42d7a3}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font-family:'DM Sans',Inter,Segoe UI,Arial,sans-serif;background:#090b0f;color:var(--ink);line-height:1.65;overflow-x:hidden}body:before{content:"";position:fixed;inset:0;z-index:-2;background:linear-gradient(135deg,#07080b 0%,#111722 48%,#0a0d12 100%)}body:after{content:"";position:fixed;inset:0;z-index:-1;opacity:.30;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:42px 42px;mask-image:linear-gradient(to bottom,black,transparent 76%)}.container{max-width:1180px;margin:0 auto;padding:0 24px}.topbar{position:sticky;top:0;z-index:30;background:rgba(9,11,15,.78);backdrop-filter:blur(20px) saturate(140%);border-bottom:1px solid var(--line)}.nav{display:flex;align-items:center;justify-content:space-between;padding:16px 24px}.brand{display:flex;gap:12px;align-items:center;color:#fff;text-decoration:none;font-weight:900}.mark{width:38px;height:38px;background:linear-gradient(135deg,var(--gold),var(--gold2));box-shadow:0 0 0 1px rgba(255,255,255,.2),0 24px 60px rgba(216,180,91,.30);clip-path:polygon(0 0,100% 0,86% 100%,0 100%)}.links{display:flex;gap:22px;align-items:center}.links a{color:var(--ink2);text-decoration:none;font-weight:750;font-size:.94rem}.links a:hover{color:#fff}.links .cta{background:var(--ink);color:#080b10;padding:11px 16px}.hero{position:relative;isolation:isolate;padding:104px 0 76px;overflow:hidden;border-bottom:1px solid var(--line)}.hero:before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(6,7,10,.96),rgba(9,14,22,.80) 56%,rgba(10,13,18,.50)),url('/static/security_at_work.webp') center/cover no-repeat;filter:saturate(.92) contrast(1.05)}.eyebrow{display:inline-flex;gap:9px;align-items:center;color:var(--gold2);border:1px solid rgba(216,180,91,.35);background:rgba(216,180,91,.10);padding:9px 12px;text-transform:uppercase;letter-spacing:.14em;font-size:.74rem;font-weight:900}.eyebrow:before{content:"";width:7px;height:7px;background:var(--green);box-shadow:0 0 20px var(--green)}h1{font-size:clamp(2.45rem,6.4vw,5.65rem);line-height:.98;margin:24px 0 20px;max-width:1010px;font-weight:900;text-transform:uppercase;overflow-wrap:anywhere}h2{font-size:clamp(1.85rem,3.5vw,3.35rem);line-height:1.05;margin:14px 0 18px}h3{margin:0 0 10px}.lead{font-size:clamp(1.06rem,2vw,1.25rem);max-width:850px;color:var(--ink2);margin:0}.actions{display:flex;flex-wrap:wrap;gap:14px;margin-top:34px}.btn{display:inline-flex;align-items:center;justify-content:center;text-decoration:none;font-weight:900;padding:15px 20px;min-height:52px;transition:.22s ease}.btn.primary{background:linear-gradient(135deg,var(--gold),var(--gold2));color:#101014;box-shadow:0 24px 58px rgba(216,180,91,.25)}.btn.primary:hover{transform:translateY(-2px)}.btn.secondary{border:1px solid rgba(255,255,255,.28);color:#fff;background:rgba(255,255,255,.06)}section:not(.hero){padding:76px 0}.section-head{max-width:860px;margin-bottom:30px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.grid.two{grid-template-columns:repeat(2,minmax(0,1fr))}.card,.panel{position:relative;overflow:hidden;border:1px solid var(--line);background:linear-gradient(180deg,var(--panel2),rgba(255,255,255,.045));padding:26px;box-shadow:0 24px 80px rgba(0,0,0,.28);backdrop-filter:blur(14px)}.card:before,.panel:before{content:"";position:absolute;left:0;top:0;right:0;height:3px;background:linear-gradient(90deg,var(--gold),rgba(95,168,255,.8),transparent)}.muted,.card p,.panel p,li{color:var(--ink2)}ul{padding-left:20px}.band{background:linear-gradient(135deg,rgba(216,180,91,.14),rgba(95,168,255,.10));border-block:1px solid var(--line)}.crumbs{font-size:.94rem;color:var(--muted);margin-bottom:18px}.crumbs a{color:var(--ink2);text-decoration:none}.crumbs a:hover{color:#fff}.linkgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.linkgrid a,.inline-links a{display:block;color:#fff;text-decoration:none;border:1px solid var(--line);background:rgba(255,255,255,.055);padding:13px 14px;font-weight:750}.inline-links{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.notice{border:1px solid rgba(216,180,91,.32);background:rgba(216,180,91,.09);padding:20px;color:var(--ink2)}details{border:1px solid var(--line);background:rgba(255,255,255,.05);padding:18px 20px;margin:12px 0}summary{cursor:pointer;color:#fff;font-weight:900}.updated{color:var(--muted);font-size:.95rem;margin-top:22px}.footer{padding:40px 0;border-top:1px solid var(--line);color:var(--muted);background:rgba(0,0,0,.22)}.footer a{color:var(--ink2)}@media (max-width:900px){.links a{display:none}.links .cta{display:inline-block;padding:9px 12px}.nav{gap:12px;padding-inline:18px}.brand{font-size:.9rem}.hero{padding:82px 0 58px}.grid,.grid.two,.linkgrid,.inline-links{grid-template-columns:1fr}section:not(.hero){padding:58px 0}h1{font-size:clamp(2.15rem,13vw,3.8rem)}}
</style>
"""


@dataclass(frozen=True)
class Region:
    name: str
    cluster: str
    profile: str
    risks: tuple[str, ...]
    intake: tuple[str, ...]
    approach: tuple[str, ...]
    areas: tuple[str, ...]
    faq: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class Service:
    name: str
    slug: str
    intent: str
    risks: tuple[str, ...]
    intake: tuple[str, ...]
    approach: tuple[str, ...]
    faq: tuple[tuple[str, str], ...]


REGIONS = [
    {"name": "Beek", "cluster": "Zuid-Limburg"},
    {"name": "Beekdaelen", "cluster": "Parkstad en Heuvelland"},
    {"name": "Beesel", "cluster": "Noord-Limburg"},
    {"name": "Bergen", "cluster": "Noord-Limburg"},
    {"name": "Brunssum", "cluster": "Parkstad"},
    {"name": "Echt-Susteren", "cluster": "Midden-Limburg"},
    {"name": "Eijsden-Margraten", "cluster": "Heuvelland"},
    {"name": "Gennep", "cluster": "Noord-Limburg"},
    {"name": "Gulpen-Wittem", "cluster": "Heuvelland"},
    {"name": "Heerlen", "cluster": "Parkstad"},
    {"name": "Horst aan de Maas", "cluster": "Noord-Limburg"},
    {"name": "Kerkrade", "cluster": "Parkstad"},
    {"name": "Landgraaf", "cluster": "Parkstad"},
    {"name": "Leudal", "cluster": "Midden-Limburg"},
    {"name": "Maasgouw", "cluster": "Midden-Limburg"},
    {"name": "Maastricht", "cluster": "Zuid-Limburg"},
    {"name": "Meerssen", "cluster": "Zuid-Limburg"},
    {"name": "Mook en Middelaar", "cluster": "Noord-Limburg"},
    {"name": "Nederweert", "cluster": "Midden-Limburg"},
    {"name": "Peel en Maas", "cluster": "Noord-Limburg"},
    {"name": "Roerdalen", "cluster": "Midden-Limburg"},
    {"name": "Roermond", "cluster": "Midden-Limburg"},
    {"name": "Simpelveld", "cluster": "Parkstad en Heuvelland"},
    {"name": "Sittard-Geleen", "cluster": "Westelijke Mijnstreek"},
    {"name": "Stein", "cluster": "Westelijke Mijnstreek"},
    {"name": "Vaals", "cluster": "Heuvelland"},
    {"name": "Valkenburg aan de Geul", "cluster": "Heuvelland"},
    {"name": "Venlo", "cluster": "Noord-Limburg"},
    {"name": "Venray", "cluster": "Noord-Limburg"},
    {"name": "Voerendaal", "cluster": "Parkstad en Heuvelland"},
    {"name": "Weert", "cluster": "Midden-Limburg"},
]

PILOT_REGIONS: dict[str, Region] = {
    "limburg": Region(
        "Limburg",
        "provincie Limburg",
        "Limburg vraagt om beveiliging die schakelt tussen grensverkeer, bedrijventerreinen, zorgvuldige ontvangst, evenementenlocaties en tijdelijke projecten. Praesidion begint daarom bij de operationele vraag en stemt daarna bezetting, taken en instructies af.",
        ("verschillende regimes per locatie, van open ontvangst tot afgesloten terrein", "wisselende drukte door events, ploegendiensten, bezoekers en leveranciers", "grensligging waardoor toegang, taal en meldlijnen vooraf helder moeten zijn", "tijdelijke projecten waarbij toezicht, sleutels en overdracht snel veranderen"),
        ("Welke locaties, zones en openingstijden vallen binnen de aanvraag?", "Welke toegangsstromen zijn er voor medewerkers, bezoekers, leveranciers en voertuigen?", "Welke meldkamer-, sleutel-, receptie- of BHV-afspraken bestaan al?", "Waar moet de beveiliger zichtbaar zijn en waar juist terughoudend?"),
        ("een compacte risico-intake per locatie of cluster", "postinstructies met taken, grenzen, rapportage en escalatie", "afstemming tussen vaste bezetting, tijdelijke inzet en mobiele controle", "evaluatie op incidenten, afwijkingen en praktische uitvoerbaarheid"),
        ("Noord-Limburg", "Midden-Limburg", "Parkstad", "Westelijke Mijnstreek", "Zuid-Limburg"),
        (("Voor welke soorten locaties is deze aanpak bedoeld?", "Voor onder meer kantoren, terreinen, publiekslocaties, evenementen en tijdelijke situaties. De precieze inzet volgt uit de locatie, risico's, openingstijden en gewenste taken."), ("Wanneer is een brede intake nodig?", "Bij meerdere locaties, wisselende openingstijden of onbekende toegangsstromen is een brede intake nodig voordat inzet verantwoord kan worden voorgesteld."), ("Waar vind ik sectorspecifieke informatie?", "Voor zorgbeveiliging, bouwbeveiliging en logistieke beveiliging kunt u terecht op de gespecialiseerde Praesidion-websites die in het regio-overzicht zijn gekoppeld.")),
    ),
    "maastricht": Region(
        "Maastricht",
        "Zuid-Limburg",
        "Maastricht combineert binnenstad, kantooromgevingen, onderwijs, hospitality, internationale bezoekersstromen en grensnabijheid. Beveiliging moet representatief blijven, maar tegelijk scherp zijn op toegang, nachtelijke rondes en afwijkende situaties.",
        ("bezoekersstromen in compacte binnenstedelijke locaties", "meertalige ontvangst en duidelijke verwijzing bij internationale gasten", "avond- en weekenddrukte rond hospitality en evenementen", "leveranciers, servicepartijen en tijdelijke badges bij kantoor- en onderwijsomgevingen"),
        ("Welke entree, balie of poort is bepalend voor de eerste controle?", "Hoe worden bezoekers, leveranciers en tijdelijke medewerkers geregistreerd?", "Zijn er piekmomenten door colleges, events, vergaderingen of publieksstromen?", "Welke talen, kledingstijl en rapportagevorm passen bij de locatie?"),
        ("receptie- en toegangsafspraken vertalen naar korte werkinstructies", "zichtbare aanwezigheid combineren met gastvrije doorverwijzing", "rondes plannen rond sluiting, leveringen en kwetsbare zones", "incidenten kort rapporteren met tijd, plek, betrokkenen en opvolging"),
        ("Centrum", "Randwyck", "Wyck", "Beatrixhaven", "Maastricht Aachen Airport-regio"),
        (("Voor welke Maastrichtse locaties is deze aanpak relevant?", "Onder meer voor kantoren, onderwijsomgevingen, hospitality, publiekslocaties en bedrijfsterreinen waar ontvangst, toegang of rondes aandacht vragen."), ("Past receptiebeveiliging bij Maastrichtse kantoren?", "Ja, wanneer ontvangst, toegangscontrole en veiligheidsbewust handelen in een functie moeten samenkomen."), ("Hoe wordt een startdatum bepaald?", "Na de intake worden taken, profiel, instructies en planning op elkaar afgestemd. Daarna kan een concrete startdatum worden voorgesteld.")),
    ),
    "heerlen": Region(
        "Heerlen",
        "Parkstad",
        "Heerlen heeft een mix van publieke functies, kantoorlocaties, retail, zorgnabije omgevingen en bedrijventerreinen. De beveiligingsvraag draait vaak om overzicht houden, aanspreekbaarheid, meldlijnen en rust rond toegankelijke gebouwen.",
        ("open gebouwen met veel verschillende bezoekers", "overgangen tussen kantooruren, avondopenstelling en sluitrondes", "onduidelijke bevoegdheden bij overlast of agressie", "parkeerterreinen, entrees en neveningangen die buiten beeld raken"),
        ("Waar ontstaan de meeste verstoringen: entree, wachtruimte, terrein of route?", "Welke partijen moeten worden gebeld bij escalatie of gebouwbeheer?", "Welke zones zijn publiek, semi-publiek of alleen voor personeel?", "Is er behoefte aan vaste post, rondes of tijdelijke extra aanwezigheid?"),
        ("rollen scheiden tussen gastvrij aanspreken, controleren en opschalen", "sluitrondes en neveningangen opnemen in de postinstructie", "rapportage laten aansluiten op facility, receptie of management", "evalueren of zichtbaarheid preventief genoeg werkt"),
        ("Heerlen-Centrum", "Hoensbroek", "Heerlerbaan", "Woonboulevard-regio", "Parkstad"),
        (("Wat is belangrijk bij beveiliging in Heerlen?", "Vooral duidelijkheid over wie aanspreekt, wie beslist en hoe meldingen worden opgevolgd bij toegankelijke locaties."), ("Is mobiele surveillance genoeg?", "Alleen als continue aanwezigheid niet nodig is. De intake bepaalt of rondes, vaste post of een combinatie logischer is."), ("Waar vind ik informatie over beveiliging in zorglocaties?", "Op zorgbewaking.nl vindt u de gespecialiseerde informatie over zorgbeveiliging, waaronder toegang, de-escalatie en nachtelijke inzet.")),
    ),
    "sittard-geleen": Region(
        "Sittard-Geleen",
        "Westelijke Mijnstreek",
        "Sittard-Geleen kent industrie, kantoren, retail, onderwijs, evenementen en logistieke bewegingen. Beveiliging moet daar omgaan met ploegwissels, leveranciers, terreinindeling en een heldere grens tussen toegang verlenen en toegang weigeren.",
        ("veel toegangsmomenten door ploegen, contractors en leveranciers", "bedrijfsterreinen met meerdere poorten of parkeerzones", "evenement- en retaildrukte rond specifieke tijdvensters", "tijdelijke werkzaamheden waardoor routes en bevoegdheden verschuiven"),
        ("Welke poorten, slagbomen, recepties of meldpunten horen bij de opdracht?", "Welke contractor- of bezoekersregels moeten beveiligers toepassen?", "Hoe lopen ploegwissels en leveringen door de dag?", "Welke rapportage is nodig voor facility, HSE of management?"),
        ("toegangscriteria vooraf scherp maken", "rondes koppelen aan terreinrisico's en afsluitmomenten", "briefing gebruiken voor tijdelijke werkzaamheden en routewijzigingen", "afwijkingen rapporteren zonder aannames over oorzaak of schuld"),
        ("Sittard", "Geleen", "Born", "Chemelot-regio", "Westelijke Mijnstreek"),
        (("Is industriebeveiliging hetzelfde als logistieke beveiliging?", "Niet altijd. Een industriële locatie kan andere zones, contractors en veiligheidsrollen hebben dan een warehouse of distributiecentrum. Voor logistieke processen vindt u meer informatie op logisticsecurity.nl."), ("Kan tijdelijke beveiliging bij werkzaamheden?", "Ja, mits planning, toegang, mandaat en evaluatiemoment vooraf duidelijk zijn."), ("Hoe wordt de inzet geëvalueerd?", "Rapportages, terugkerende afwijkingen en wijzigingen in routes of werkzaamheden worden gebruikt om taken en instructies gericht bij te stellen.")),
    ),
    "roermond": Region(
        "Roermond",
        "Midden-Limburg",
        "Roermond vraagt om beveiliging die winkel- en hospitalitydrukte, waterrecreatie, binnenstad, bedrijventerreinen en tijdelijke publieksstromen uit elkaar houdt. De aanpak moet praktisch zijn en niet zwaarder dan nodig.",
        ("drukte rond retail, parkeren en bezoekersroutes", "leveringen en servicepartijen buiten reguliere openingstijden", "horeca- en eventmomenten waarbij zichtbaarheid belangrijk is", "terreinen met meerdere toegangspunten en beperkte sociale controle"),
        ("Welke momenten veroorzaken piekdrukte of wachtrijen?", "Waar moeten bezoekers worden geholpen en waar moet toegang worden geweigerd?", "Welke routes zijn voor leveranciers en welke voor publiek?", "Wie ontvangt rapportages na sluiting, ronde of incident?"),
        ("publieksvriendelijke aanwezigheid combineren met duidelijke grenzen", "rondes afstemmen op sluiting, leveringen en kwetsbare zones", "toegangspunten benoemen in plaats van algemeen toezicht beloven", "korte evaluatie na drukke periodes of tijdelijke inzet"),
        ("Binnenstad", "Designer Outlet-regio", "Maasplassen", "Herten", "Midden-Limburg"),
        (("Waarom een aparte pagina voor Roermond?", "Omdat bezoekersdrukte, binnenstedelijke routes, horeca, retail en terreinen elk andere toegangs- en toezichtsvragen kunnen geven."), ("Kan Praesidion evenementen ondersteunen?", "Ja, na beoordeling van locatie, bezoekersprofiel, draaiboek, vergunningseisen, zones en rolverdeling."), ("Welke gebiedskenmerken worden tijdens de intake bekeken?", "Onder meer bereikbaarheid, piekmomenten, parkeer- en leveranciersroutes, sluitingstijden, neveningangen en de aanwezigheid van eigen locatiepersoneel.")),
    ),
    "venlo": Region(
        "Venlo",
        "Noord-Limburg",
        "Venlo is sterk verbonden met logistiek, transport, grensverkeer, retail en bedrijventerreinen. Op praesidion.eu blijft de vraag breed: toegangscontrole, surveillance, ontvangst, tijdelijke bezetting en escalatieafspraken voor organisaties die grip willen op hun locatie.",
        ("veel voertuig-, chauffeur- en leveranciersbewegingen", "grensoverschrijdende communicatie en uiteenlopende bezoekersprofielen", "grote terreinen waar rondes en zichtlijnen vooraf moeten worden gepland", "nacht- en weekendmomenten met minder eigen personeel"),
        ("Welke toegangspunten gelden voor voertuigen, voetgangers en bezoekers?", "Moeten beveiligers controleren, registreren, begeleiden of alleen signaleren?", "Welke talen of instructiekaarten zijn nodig bij internationale stromen?", "Hoe worden alarmen, schades en afwijkingen opgevolgd?"),
        ("toegangscontrole scheiden van logistieke procesverantwoordelijkheid", "surveillance koppelen aan tijden, zones en controlepunten", "rapportage laten aansluiten op locatiebeheer en planning", "voor warehouses, docks en chauffeursstromen de verdieping op logisticsecurity.nl gebruiken"),
        ("Trade Port", "Blerick", "Tegelen", "Venlo-Centrum", "Noord-Limburg"),
        (("Waar vind ik verdieping over logistieke beveiliging?", "Op logisticsecurity.nl vindt u specifieke informatie over warehouses, distributiecentra, transportterreinen, docks en chauffeursstromen."), ("Kan mobiele surveillance rond Venlo zinvol zijn?", "Ja, vooral wanneer meerdere controlepunten belangrijker zijn dan permanente postbezetting."), ("Hoe worden taalwensen bij grensverkeer meegenomen?", "De intake brengt bezoekers- en chauffeursprofielen in kaart. Op basis daarvan kan het gewenste taalniveau onderdeel worden van profiel en werkinstructie.")),
    ),
    "weert": Region(
        "Weert",
        "Midden-Limburg",
        "Weert ligt tussen Midden-Limburg, Brabant en Belgische routes. Beveiliging moet rekening houden met industrie, retail, evenementen, zorgnabije locaties en terreinen waar na sluiting minder toezicht is.",
        ("bedrijventerreinen met buitenopslag of meerdere entrees", "routes richting Brabant en België met wisselende leveranciers", "evenementen en piekdrukte rond tijdelijke publieksstromen", "leegstand, verbouwing of tijdelijke overbrugging van eigen bezetting"),
        ("Welke locatiezones zijn na sluiting kwetsbaar?", "Hoe worden sleutels, alarmcodes en meldingen beheerd?", "Welke piekmomenten vragen extra bezetting of preventieve aanwezigheid?", "Is de vraag tijdelijk, structureel of afhankelijk van evaluatie?"),
        ("intake richten op terreinindeling, sluitronde en opvolging", "tijdelijke inzet voorzien van eerste-dienst-instructie", "toegangsafspraken combineren met rondes en rapportage", "bij bouwintentie zichtbaar verwijzen naar bouwbeveiligingnederland.nl"),
        ("Weert-Centrum", "Kampershoek", "Leuken", "Stramproy", "Midden-Limburg"),
        (("Kan tijdelijke beveiliging in Weert?", "Ja, bijvoorbeeld bij leegstand, werkzaamheden, piekdrukte of overbrugging, na intake en planning."), ("Waar vind ik informatie over bouwplaatsbeveiliging?", "Op bouwbeveiligingnederland.nl vindt u de gespecialiseerde informatie over toegang, diefstalpreventie, nachtbewaking en tijdelijke inzet op bouwlocaties."), ("Wanneer wordt de beschikbaarheid duidelijk?", "Na ontvangst van locatie, gewenste tijden, taken en profiel kan de planning worden beoordeeld en volgt een concreet inzetvoorstel.")),
    ),
}

PILOT_SERVICE_SLUGS = (
    "objectbeveiliging",
    "evenementenbeveiliging",
    "receptiebeveiliging",
    "toegangscontrole",
    "mobiele-surveillance",
    "tijdelijke-beveiliging",
    "inzet-bhv-ers",
    "preventiemedewerkers",
    "special-situations",
)

SERVICES: dict[str, Service] = {
    "objectbeveiliging": Service("Objectbeveiliging", "objectbeveiliging", "vaste aanwezigheid bij kantoren, terreinen, instellingen en bedrijfspanden", ("ongewenste toegang via entree, leveranciersdeur of terrein", "onduidelijke sluitrondes en sleutelafspraken", "afwijkingen die niet consequent worden gerapporteerd"), ("Welke zones zijn publiek, beperkt of gesloten?", "Welke rondes, sleutels en alarmen horen bij de post?", "Wie beslist bij afwijkingen of twijfel aan toegang?"), ("postinstructies opstellen per object", "rondes en rapportage koppelen aan risicomomenten", "beveiliger zichtbaar maken waar dat preventief werkt"), (("Wanneer is objectbeveiliging passend?", "Als een locatie baat heeft bij vaste aanwezigheid, controle, rapportage en duidelijke opvolging."), ("Is objectbeveiliging altijd permanent?", "Nee. De inzet kan vast, tijdelijk of gecombineerd met mobiele surveillance zijn."))),
    "evenementenbeveiliging": Service("Evenementenbeveiliging", "evenementenbeveiliging", "begeleiding van bezoekersstromen, entrees en tijdelijke drukte", ("wachtrijen, doorstroom en toegangscontrole", "onduidelijke rolverdeling tussen organisatie, locatie en beveiliging", "incidenten zonder eenduidige meldlijn"), ("Wat is het bezoekersprofiel en de verwachte piekdrukte?", "Welke ingangen, noodroutes en zones zijn bepalend?", "Welke afspraken staan in draaiboek of vergunning?"), ("briefing op taken, zones en escalatie", "zichtbare inzet bij entree en publieksstromen", "rapportage na incidenten en evaluatiepunten"), (("Geeft Praesidion vergunningadvies?", "Nee. Vergunningen en wettelijke eisen worden per concrete situatie gecontroleerd."), ("Kan inzet tijdelijk zijn?", "Ja, evenementenbeveiliging is meestal tijdelijk en draaiboekgestuurd."))),
    "receptiebeveiliging": Service("Receptiebeveiliging", "receptiebeveiliging", "gastvrije ontvangst met veiligheidsbewust toegangsbeheer", ("bezoekers zonder juiste registratie", "spanning tussen hospitality en weigeren van toegang", "vertrouwelijke ruimtes achter een open ontvangst"), ("Welke bezoekers moeten worden geregistreerd?", "Welke huisregels en escalatielijnen gelden aan de balie?", "Welke uitstraling en taalvaardigheid zijn nodig?"), ("ontvangstproces koppelen aan securitytaken", "bezoekerstypes en uitzonderingen vooraf vastleggen", "rapportage inrichten voor receptie en facility"), (("Wat is het verschil met gewone receptie?", "Receptiebeveiliging combineert ontvangst met beveiligingsinstructies en escalatieafspraken."), ("Kan dit bij kantoorlocaties?", "Ja, vooral wanneer representativiteit en toegangscontrole samen nodig zijn."))),
    "toegangscontrole": Service("Toegangscontrole", "toegangscontrole", "controle van personen, voertuigen, leveranciers en tijdelijke toegang", ("onduidelijk wie waar naar binnen mag", "contractors of leveranciers zonder heldere registratie", "afwijkingen bij badges, sleutels of voertuigen"), ("Welke toegangspunten en criteria gelden?", "Welke gegevens worden geregistreerd en door wie?", "Wie heeft mandaat bij weigering of twijfel?"), ("criteria vertalen naar korte instructie", "controlepunten bemannen of periodiek controleren", "afwijkingen direct vastleggen en melden"), (("Wanneer werkt toegangscontrole goed?", "Als vooraf duidelijk is wie toegang heeft, onder welke voorwaarden en wie beslist bij twijfel."), ("Is technologie verplicht?", "Nee. Menselijke controle kan zelfstandig of naast systemen worden ingezet."))),
    "mobiele-surveillance": Service("Mobiele surveillance", "mobiele-surveillance", "controlerondes, sleutelservice en zichtbare aanwezigheid op risicomomenten", ("schade of inbraak buiten openingstijden", "meerdere locaties zonder permanente bezetting", "alarmopvolging zonder duidelijke locatiekennis"), ("Welke rondetijden en controlepunten zijn nodig?", "Welke sleutels, codes en meldlijnen zijn beschikbaar?", "Wat moet worden vastgelegd bij afwijkingen?"), ("rondes plannen op risico en route", "controlepunten expliciet maken", "opvolging en rapportage per ronde vastleggen"), (("Wanneer is surveillance beter dan vaste post?", "Wanneer periodieke controle volstaat en permanente aanwezigheid niet nodig is."), ("Kan surveillance met objectbeveiliging samen?", "Ja, bijvoorbeeld voor buitenrondes naast een vaste binnenpost."))),
    "tijdelijke-beveiliging": Service("Tijdelijke beveiliging", "tijdelijke-beveiliging", "schaalbare inzet bij projecten, incidenten, leegstand of piekdrukte", ("snel veranderende locatie-instructies", "onvoldoende overdracht bij de eerste dienst", "te laat afschalen na verminderd risico"), ("Wat is de aanleiding en beoogde einddatum?", "Welke instructie is nodig voor de eerste dienst?", "Wanneer evalueren we opschalen of afbouwen?"), ("compacte intake voor snelle start", "eerste-dienst-instructie vastleggen", "evaluatiemoment afspreken voor vervolg"), (("Is tijdelijke beveiliging direct beschikbaar?", "Beschikbaarheid hangt af van aanvraag, profiel en planning."), ("Wanneer stopt tijdelijke inzet?", "Dat wordt gekoppeld aan evaluatie, risico en de afgesproken opdrachtduur."))),
    "inzet-bhv-ers": Service("Inzet BHV-ers", "inzet-bhv-ers", "aanvullende veiligheidsbezetting bij evenementen, piekdrukte of tijdelijke locaties", ("onduidelijke taakafbakening tussen BHV, beveiliging en organisatie", "te weinig dekking bij piekmomenten", "melding en opvolging niet getest in de praktijk"), ("Welke BHV-organisatie en risico-inventarisatie bestaan al?", "Welke tijden, zones en aantallen zijn nodig?", "Wie heeft de leiding bij calamiteiten?"), ("aanvullende inzet afstemmen op bestaande organisatie", "meld- en escalatielijnen vooraf bevestigen", "taken begrenzen en rapporteren na inzet"), (("Vervangt deze inzet een RI&E?", "Nee. De opdrachtgever blijft verantwoordelijk voor formele organisatie-eisen."), ("Kan BHV-inzet bij evenementen?", "Ja, als aanvullende bezetting binnen een afgestemd plan."))),
    "preventiemedewerkers": Service("Preventiemedewerkers", "preventiemedewerkers", "preventieve aanwezigheid, signalering en eerste aanspreekbaarheid", ("kleine verstoringen die te laat worden gezien", "onduidelijk verschil tussen service en beveiliging", "meldingen zonder opvolgroute"), ("Waar moet preventief worden gesignaleerd?", "Welke situaties worden aangesproken en welke niet?", "Wanneer wordt beveiliging of leiding ingeschakeld?"), ("zichtbare preventieve rondes", "aanspreekregels en grenzen vastleggen", "meldingen doorzetten volgens instructie"), (("Zijn preventiemedewerkers beveiligers?", "Dat hangt af van taken en wettelijke context; vergunningplichtige werkzaamheden worden daarop afgestemd."), ("Waarvoor is preventie geschikt?", "Voor signalering, aanspreekbaarheid en het vroeg doorzetten van afwijkingen."))),
    "special-situations": Service("Special Situations", "special-situations", "maatwerk bij gevoelige, afwijkende of snel veranderende beveiligingsvragen", ("gevoelige context met beperkte informatie", "afwijkende bezoekers- of personeelsdynamiek", "mandaat en communicatie die vooraf scherp moeten zijn"), ("Wat maakt de situatie bijzonder of gevoelig?", "Wie mag informatie ontvangen en wie beslist?", "Welke zichtbaarheid, discretie en rapportage zijn gewenst?"), ("eerst context en risico, daarna profiel en planning", "mandaat, communicatie en rapportage begrenzen", "inzet evalueren zodra de situatie verandert"), (("Wat valt onder Special Situations?", "Situaties die niet goed in een standaarddienst passen en eerst inhoudelijke intake vragen."), ("Wordt discretie gegarandeerd?", "Discretie wordt als werkafspraak ingericht, maar concrete garanties volgen niet uit deze pagina."))),
    "zorgbeveiliging": Service("Zorgbeveiliging", "zorgbeveiliging", "zorgbeveiliging", (), (), (), ()),
    "bouwbeveiliging": Service("Bouwbeveiliging", "bouwbeveiliging", "bouwbeveiliging", (), (), (), ()),
    "logistieke-beveiliging": Service("Logistieke beveiliging", "logistieke-beveiliging", "logistieke beveiliging", (), (), (), ()),
}

NICHE_OWNERS = {
    "zorgbeveiliging": ("zorgbewaking.nl", "https://www.zorgbewaking.nl/"),
    "bouwbeveiliging": ("bouwbeveiligingnederland.nl", "https://www.bouwbeveiligingnederland.nl/"),
    "logistieke-beveiliging": ("logisticsecurity.nl", "https://www.logisticsecurity.nl/"),
}

BLOG_URLS = [
    "/blog/",
    "/blog/flexibele-inzet-evenementenbeveiliging-wpbr-planning/",
    "/blog/zomerbezetting-toegangsbeheer-objectbeveiliging/",
    "/blog/kwaliteit-inhuur-beveiliging-keurmerken-processen/",
    "/blog/objectbeveiliging-zonder-ruis-roosters-overdracht/",
    "/blog/zzp-inhuur-beveiliging-planning-dossiers-rapportage/",
    "/blog/alarmopvolging-objectbeveiliging-meldkamerafspraken/",
]

BLOGS = {
    "/blog/flexibele-inzet-evenementenbeveiliging-wpbr-planning/": (
        "Flexibele inzet in evenementenbeveiliging",
        "Planning, briefing en overdracht bepalen of tijdelijke evenementenbeveiliging controleerbaar blijft.",
        ("Maak bezoekersstromen, piekdrukte en zones concreet voordat het rooster wordt gevuld.", "Leg vast wie beslist bij weigering, incidenten en opschaling.", "Gebruik een korte evaluatie na afloop om draaiboek en overdracht te verbeteren."),
    ),
    "/blog/zomerbezetting-toegangsbeheer-objectbeveiliging/": (
        "Zomerbezetting en toegangsbeheer",
        "Lagere bezetting maakt toegangsafspraken kwetsbaar als bezoekers, leveranciers en tijdelijke passen niet strak zijn ingericht.",
        ("Controleer wie tijdens vakantieperiodes sleutels, badges en alarmcodes beheert.", "Plan extra aandacht voor leveranciersdeuren, neveningangen en sluitrondes.", "Laat afwijkingen kort rapporteren zodat overdracht niet afhankelijk wordt van losse berichten."),
    ),
    "/blog/kwaliteit-inhuur-beveiliging-keurmerken-processen/": (
        "Beveiliging inkopen in 2026",
        "Kwaliteit bij beveiligingsinhuur zit niet alleen in papieren eisen, maar in uitvoerbare instructies en controleerbare processen.",
        ("Vraag naar screening, planning, postinstructies en rapportage voordat u inzet bevestigt.", "Maak taken en mandaat concreet per locatie.", "Voorkom dat prijs het enige selectiecriterium wordt bij risicovolle opdrachten."),
    ),
    "/blog/objectbeveiliging-zonder-ruis-roosters-overdracht/": (
        "Objectbeveiliging zonder ruis",
        "Objectbeveiliging werkt beter wanneer roosters, overdracht en postinstructies niet afhankelijk zijn van mondelinge aannames.",
        ("Beschrijf rondes, controlepunten en uitzonderingen in de postinstructie.", "Koppel overdracht aan tijden, incidenten en openstaande acties.", "Evalueer terugkerende afwijkingen met facility of locatiebeheer."),
    ),
    "/blog/zzp-inhuur-beveiliging-planning-dossiers-rapportage/": (
        "Zzp, inhuur en beveiligingsinzet",
        "Bij ingehuurde beveiligingscapaciteit blijven planning, dossiers en rapportage bepalend voor grip op de uitvoering.",
        ("Leg vast wie instructies verstrekt en wijzigingen goedkeurt.", "Bewaar relevante inzetinformatie op een manier die overdraagbaar is.", "Gebruik rapportage om operationele bijsturing mogelijk te maken."),
    ),
    "/blog/alarmopvolging-objectbeveiliging-meldkamerafspraken/": (
        "Alarmopvolging en objectbeveiliging",
        "Alarmopvolging vraagt om heldere meldkamerafspraken, actuele sleutelgegevens en duidelijke opvolging op locatie.",
        ("Controleer of sleutel-, code- en contactgegevens actueel zijn.", "Leg vast wanneer surveillance, vaste post of locatiebeheer wordt ingeschakeld.", "Rapporteer alarmmomenten met tijd, oorzaak voor zover bekend en opvolging."),
    ),
}


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.lower().replace("&", " en ")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def url(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return BASE_URL + path


def list_items(items: tuple[str, ...]) -> str:
    return "".join(f"<li>{esc(item)}</li>" for item in items)


def faq_schema(items: tuple[tuple[str, str], ...]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }


def breadcrumb_schema(items: tuple[tuple[str, str], ...]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": pos, "name": name, "item": link}
            for pos, (name, link) in enumerate(items, start=1)
        ],
    }


def org_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Praesidion Security B.V.",
        "url": BASE_URL + "/",
        "areaServed": ["Limburg", "Nederland"],
        "email": "info@praesidion.nl",
        "telephone": "+31 46 240 2401",
    }


def service_schema(name: str, canonical: str, area: list[str], service_type: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "serviceType": service_type,
        "provider": {"@type": "Organization", "name": "Praesidion Security B.V.", "url": BASE_URL + "/"},
        "areaServed": area,
        "url": canonical,
    }


def scripts(*objects: dict) -> str:
    return "\n".join(
        f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False, separators=(",", ":"))}</script>'
        for obj in objects
    )


def header() -> str:
    return '<header class="topbar"><div class="container nav"><a class="brand" href="/"><span class="mark"></span><span>Praesidion Security</span></a><nav class="links"><a href="/beveiliging-limburg-regios/">Regio Limburg</a><a href="/beveiliging-aanvragen-limburg/">Aanvragen</a><a href="/blog/">Blog</a><a class="cta" href="mailto:info@praesidion.nl">Contact</a></nav></div></header>'


def breadcrumbs(items: tuple[tuple[str, str], ...]) -> str:
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(
        f'<a href="{esc(path)}">{esc(name)}</a>' if i < len(items) - 1 else esc(name)
        for i, (name, path) in enumerate(items)
    ) + "</nav>"


def page_shell(
    *,
    title: str,
    description: str,
    canonical_path: str,
    robots: str,
    crumbs: tuple[tuple[str, str], ...],
    eyebrow: str,
    h1: str,
    lead: str,
    body: str,
    schema_objects: tuple[dict, ...],
    cta_subject: str,
) -> str:
    canonical = url(canonical_path)
    og_url = canonical
    return f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}" />
<meta name="robots" content="{esc(robots)}" />
<link rel="canonical" href="{esc(canonical)}" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(description)}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="{esc(og_url)}" />
<meta property="og:locale" content="nl_NL" />
<meta property="og:image" content="{BASE_URL}/static/security_at_work.webp" />
<link rel="preload" as="image" href="/static/security_at_work.webp" type="image/webp" fetchpriority="high" />
{scripts(*schema_objects)}
{FONT}
{STYLE}
</head>
<body>
{header()}
<main>
<section class="hero"><div class="container">{breadcrumbs(crumbs)}<span class="eyebrow">{esc(eyebrow)}</span><h1>{esc(h1)}</h1><p class="lead">{esc(lead)}</p><div class="actions"><a class="btn primary" href="mailto:info@praesidion.nl?subject={esc(cta_subject)}">Vraag voorstel aan</a><a class="btn secondary" href="/beveiliging-limburg-regios/">Bekijk regio-overzicht</a></div><p class="updated">Laatst bijgewerkt: {UPDATED}</p></div></section>
{body}
<section id="contact" class="band"><div class="container"><div class="section-head"><span class="eyebrow">Intake</span><h2>Bespreek de beveiligingsvraag</h2><p class="lead">Stuur locatie, aanleiding, gewenste tijden, toegangsstromen en de belangrijkste risico's mee. Dan kan Praesidion bepalen welke inzet en instructies passen.</p><div class="actions"><a class="btn primary" href="mailto:info@praesidion.nl?subject={esc(cta_subject)}">Mail info@praesidion.nl</a><a class="btn secondary" href="tel:+31462402401">Bel 046 240 2401</a></div></div></div></section>
</main>
<footer class="footer"><div class="container">© Praesidion Security B.V. · <a href="/sitemap.xml">Sitemap</a> · <a href="/llms.txt">llms.txt</a></div></footer>
</body>
</html>
"""


def related_links(paths: list[tuple[str, str]]) -> str:
    return '<div class="linkgrid">' + "".join(f'<a href="{esc(path)}">{esc(label)}</a>' for label, path in paths) + "</div>"


def service_hub(service: Service) -> str:
    path = f"/{service.slug}-limburg/"
    title = f"{service.name} Limburg | Praesidion Security"
    desc = f"{service.name} in Limburg met intake, postinstructies, rapportage en duidelijke escalatieafspraken. Breed inzetbaar voor organisaties die professioneel toezicht nodig hebben."
    faq = service.faq + (
        ("Voor welke regio's is deze dienst bedoeld?", "De dienst is bedoeld voor aanvragen in heel Limburg. Op de regionale pagina's leest u meer over aandachtspunten in de verschillende Limburgse gebieden."),
        ("Waar vind ik informatie over zorg, bouw en logistiek?", "Voor deze sectoren zijn gespecialiseerde Praesidion-websites beschikbaar. Het regio-overzicht linkt rechtstreeks naar zorgbewaking.nl, bouwbeveiligingnederland.nl en logisticsecurity.nl."),
    )
    body = f"""
<section><div class="container grid"><article class="card"><h2>Wanneer deze dienst past</h2><p>{esc(service.intent.capitalize())}. De vraag wordt niet vertaald naar een standaardrooster, maar naar taken, zichtbaarheid, mandaat en rapportage.</p></article><article class="card"><h2>Risico's vooraf scherp</h2><ul>{list_items(service.risks)}</ul></article><article class="card"><h2>Intakevragen</h2><ul>{list_items(service.intake)}</ul></article></div></section>
<section class="band"><div class="container grid two"><article class="panel"><h2>Aanpak</h2><ul>{list_items(service.approach)}</ul></article><article class="panel"><h2>Afstemming op uw locatie</h2><p>De uiteindelijke inzet hangt af van locatie, openingstijden, risico, taken, gewenst profiel en bestaande voorzieningen. De intake maakt deze uitgangspunten concreet.</p></article></div></section>
<section><div class="container"><div class="section-head"><span class="eyebrow">Verwante pagina's</span><h2>Beveiliging per regio en aanvraag</h2><p class="lead">Bekijk regionale aandachtspunten of ga direct naar de aanvraagpagina die bij uw vraag past.</p></div>{related_links([("Beveiligingsbedrijf Limburg", "/beveiligingsbedrijf-limburg/"), ("Beveiliging aanvragen Limburg", "/beveiliging-aanvragen-limburg/"), ("Beveiligers inhuren Limburg", "/beveiligers-inhuren-limburg/"), ("Regio-overzicht Limburg", "/beveiliging-limburg-regios/")])}</div></section>
<section><div class="container"><h2>Veelgestelde vragen</h2>{faq_html(faq)}</div></section>
"""
    crumbs = (("Home", "/"), ("Regio Limburg", "/beveiliging-limburg-regios/"), (service.name, path))
    return page_shell(
        title=title,
        description=desc,
        canonical_path=path,
        robots="index, follow, max-image-preview:large",
        crumbs=crumbs,
        eyebrow="Diensthub Limburg",
        h1=f"{service.name} in Limburg",
        lead=f"Praesidion ondersteunt brede beveiligingsvragen in Limburg met {service.intent}. Elke aanvraag start met locatie, risico, taakafbakening en opvolging.",
        body=body,
        schema_objects=(org_schema(), service_schema(f"{service.name} Limburg", url(path), ["Limburg"], service.name), faq_schema(faq), breadcrumb_schema(tuple((n, url(p)) for n, p in crumbs))),
        cta_subject=f"Aanvraag {service.name} Limburg",
    )


def regional_page(region: Region) -> str:
    slug = "beveiligingsbedrijf-limburg" if slugify(region.name) == "limburg" else f"beveiligingsbedrijf-{slugify(region.name)}"
    path = f"/{slug}/"
    title = f"Beveiligingsbedrijf {region.name} | Praesidion Security"
    desc = f"Beveiligingsbedrijf voor {region.name}: praktische intake, lokale aandachtspunten, toegangsafspraken, rapportage en passende beveiligingsdiensten van Praesidion."
    service_links = [(SERVICES[s].name, f"/{s}-limburg/") for s in PILOT_SERVICE_SLUGS]
    peer_links = [
        ("Maastricht", "/beveiligingsbedrijf-maastricht/"),
        ("Heerlen", "/beveiligingsbedrijf-heerlen/"),
        ("Sittard-Geleen", "/beveiligingsbedrijf-sittard-geleen/"),
        ("Roermond", "/beveiligingsbedrijf-roermond/"),
        ("Venlo", "/beveiligingsbedrijf-venlo/"),
        ("Weert", "/beveiligingsbedrijf-weert/"),
    ]
    if region.name != "Limburg":
        peer_links.insert(0, ("Limburg", "/beveiligingsbedrijf-limburg/"))
    peer_links = [item for item in peer_links if item[0] != region.name]
    faq = region.faq + (
        ("Welke diensten kan ik vanaf deze pagina kiezen?", "Objectbeveiliging, evenementenbeveiliging, receptiebeveiliging, toegangscontrole, mobiele surveillance, tijdelijke beveiliging, BHV-inzet, preventiemedewerkers en Special Situations."),
        ("Welke informatie moet ik vooraf aanleveren?", "Stuur de locatie, gewenste tijden, aanleiding, bezoekers- en leveranciersstromen, bestaande maatregelen en belangrijkste risico's mee."),
    )
    body = f"""
<section><div class="container grid"><article class="card"><h2>Regionale context</h2><p>{esc(region.profile)}</p></article><article class="card"><h2>Lokale risico's om te toetsen</h2><ul>{list_items(region.risks)}</ul></article><article class="card"><h2>Intakevragen</h2><ul>{list_items(region.intake)}</ul></article></div></section>
<section class="band"><div class="container grid two"><article class="panel"><h2>Aanpak voor {esc(region.name)}</h2><ul>{list_items(region.approach)}</ul></article><article class="panel"><h2>Gebieden in de intake</h2><p>Deze gebieden helpen om route, bereikbaarheid, piekmomenten en de lokale operationele context concreet te bespreken.</p><ul>{list_items(region.areas)}</ul></article></div></section>
<section><div class="container"><div class="section-head"><span class="eyebrow">Diensten</span><h2>Kies de passende beveiligingsdienst</h2><p class="lead">Bekijk per dienst welke risico's, intakevragen, taken en rapportageafspraken een rol kunnen spelen.</p></div>{related_links(service_links)}</div></section>
<section class="band"><div class="container"><div class="section-head"><span class="eyebrow">Verwante regio's</span><h2>Beveiliging in andere Limburgse regio's</h2></div>{related_links(peer_links)}</div></section>
<section><div class="container"><h2>Veelgestelde vragen</h2>{faq_html(faq)}</div></section>
"""
    crumbs = (("Home", "/"), ("Regio Limburg", "/beveiliging-limburg-regios/"), (f"Beveiligingsbedrijf {region.name}", path))
    return page_shell(
        title=title,
        description=desc,
        canonical_path=path,
        robots="index, follow, max-image-preview:large",
        crumbs=crumbs,
        eyebrow=region.cluster,
        h1=f"Beveiligingsbedrijf {region.name}",
        lead=f"Praktische beveiliging voor organisaties in {region.name}, afgestemd op locatie, toegangsstromen, openingstijden, risico's en gewenste taken.",
        body=body,
        schema_objects=(org_schema(), service_schema(f"Beveiligingsbedrijf {region.name}", url(path), list(region.areas) + [region.name, "Limburg"], "Beveiligingsdiensten"), faq_schema(faq), breadcrumb_schema(tuple((n, url(p)) for n, p in crumbs))),
        cta_subject=f"Aanvraag beveiliging {region.name}",
    )


def faq_html(items: tuple[tuple[str, str], ...]) -> str:
    return "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in items)


def overview_page() -> str:
    service_links = [(SERVICES[s].name, f"/{s}-limburg/") for s in PILOT_SERVICE_SLUGS]
    region_links = [
        ("Beveiligingsbedrijf Limburg", "/beveiligingsbedrijf-limburg/"),
        ("Beveiligingsbedrijf Maastricht", "/beveiligingsbedrijf-maastricht/"),
        ("Beveiligingsbedrijf Heerlen", "/beveiligingsbedrijf-heerlen/"),
        ("Beveiligingsbedrijf Sittard-Geleen", "/beveiligingsbedrijf-sittard-geleen/"),
        ("Beveiligingsbedrijf Roermond", "/beveiligingsbedrijf-roermond/"),
        ("Beveiligingsbedrijf Venlo", "/beveiligingsbedrijf-venlo/"),
        ("Beveiligingsbedrijf Weert", "/beveiligingsbedrijf-weert/"),
    ]
    niche_links = [("Zorgbewaking", "https://www.zorgbewaking.nl/"), ("Bouwbeveiliging Nederland", "https://www.bouwbeveiligingnederland.nl/"), ("Logistic Security", "https://www.logisticsecurity.nl/")]
    faq = (
        ("Welke beveiligingsdiensten kan ik hier vergelijken?", "U vindt hier objectbeveiliging, evenementenbeveiliging, receptiebeveiliging, toegangscontrole, mobiele surveillance, tijdelijke beveiliging, BHV-inzet, preventiemedewerkers en Special Situations."),
        ("Waar vind ik informatie over zorg, bouw en logistiek?", "Gebruik de gespecialiseerde websites zorgbewaking.nl, bouwbeveiligingnederland.nl en logisticsecurity.nl. Vanuit dit overzicht kunt u rechtstreeks doorklikken."),
        ("Kan ik ook een aanvraag doen voor een andere Limburgse gemeente?", "Ja. Gebruik de brede aanvraagpagina en stuur locatie, gewenste tijden, aanleiding en belangrijkste risico's mee."),
    )
    body = f"""
<section><div class="container grid two"><article class="panel"><h2>Beveiligingsdiensten in Limburg</h2><p>Vergelijk per dienst de situaties waarin inzet past, de belangrijkste risico's, intakevragen en werkwijze.</p>{related_links(service_links)}</article><article class="panel"><h2>Beveiliging per regio</h2><p>Bekijk de operationele aandachtspunten voor Limburg, Maastricht, Heerlen, Sittard-Geleen, Roermond, Venlo en Weert.</p>{related_links(region_links)}</article></div></section>
<section class="band"><div class="container"><div class="section-head"><span class="eyebrow">Sectoren</span><h2>Specialistische beveiligingsvragen</h2><p class="lead">Voor zorglocaties, bouwplaatsen en logistieke processen vindt u verdiepende informatie op de gespecialiseerde Praesidion-websites.</p></div>{related_links(niche_links)}</div></section>
<section><div class="container"><h2>Veelgestelde vragen</h2>{faq_html(faq)}</div></section>
"""
    crumbs = (("Home", "/"), ("Regio Limburg", "/beveiliging-limburg-regios/"))
    return page_shell(
        title="Beveiliging Limburg per regio en dienst | Praesidion Security",
        description="Overzicht van Praesidion-beveiligingsdiensten in Limburg, met regionale aandachtspunten voor Maastricht, Heerlen, Sittard-Geleen, Roermond, Venlo en Weert.",
        canonical_path="/beveiliging-limburg-regios/",
        robots="index, follow, max-image-preview:large",
        crumbs=crumbs,
        eyebrow="Regio-overzicht",
        h1="Beveiliging in Limburg per regio en dienst",
        lead="Vergelijk beveiligingsdiensten en regionale aandachtspunten in Limburg. Van objectbeveiliging en toegangscontrole tot tijdelijke inzet en specialistische sectorvragen.",
        body=body,
        schema_objects=(org_schema(), service_schema("Beveiliging Limburg", url("/beveiliging-limburg-regios/"), ["Limburg"], "Beveiligingsdiensten"), faq_schema(faq), breadcrumb_schema(tuple((n, url(p)) for n, p in crumbs))),
        cta_subject="Aanvraag beveiliging Limburg",
    )


def request_hub(kind: str) -> str:
    is_hire = kind == "inhuren"
    path = "/beveiligers-inhuren-limburg/" if is_hire else "/beveiliging-aanvragen-limburg/"
    h1 = "Beveiligers inhuren in Limburg" if is_hire else "Beveiliging aanvragen in Limburg"
    title = f"{h1} | Praesidion Security"
    desc = "Vraag professionele beveiliging in Limburg aan met duidelijke intake over locatie, risico, tijden, profiel, rapportage en opvolging."
    faq = (
        ("Welke informatie versnelt de intake?", "Locatie, gewenste tijden, aanleiding, toegangsstromen, risico's, bestaande instructies en contactpersoon."),
        ("Krijg ik direct een prijs?", "Een voorstel hangt af van bezetting, profiel, duur, instructies en planning. Deze pagina belooft geen vaste prijs."),
        ("Waar vind ik gespecialiseerde sectorinformatie?", "Voor zorglocaties, bouwplaatsen en logistieke processen kunt u vanuit het regio-overzicht doorklikken naar de gespecialiseerde Praesidion-websites."),
    )
    body = f"""
<section><div class="container grid"><article class="card"><h2>Wat u meestuurt</h2><ul><li>adres of omschrijving van de locatie</li><li>gewenste dagen, tijden en looptijd</li><li>reden van inzet en belangrijkste risico's</li><li>bestaande toegang-, alarm-, receptie- of meldafspraken</li></ul></article><article class="card"><h2>Wat Praesidion beoordeelt</h2><ul><li>welk profiel past bij taken en omgeving</li><li>of vaste post, surveillance of tijdelijke inzet logisch is</li><li>welke instructies nodig zijn voor de eerste dienst</li><li>welke rapportage en escalatieafspraken nodig zijn</li></ul></article><article class="card"><h2>Wat het voorstel bevat</h2><p>U ontvangt een voorstel op basis van de afgesproken taken, inzetmomenten, benodigde instructies, rapportage en operationele verantwoordelijkheden.</p></article></div></section>
<section class="band"><div class="container"><div class="section-head"><span class="eyebrow">Kies richting</span><h2>Waar gaat de aanvraag over?</h2></div>{related_links([(SERVICES[s].name, f"/{s}-limburg/") for s in PILOT_SERVICE_SLUGS] + [("Beveiliging per regio", "/beveiliging-limburg-regios/")])}</div></section>
<section><div class="container"><h2>Veelgestelde vragen</h2>{faq_html(faq)}</div></section>
"""
    crumbs = (("Home", "/"), ("Regio Limburg", "/beveiliging-limburg-regios/"), (h1, path))
    return page_shell(
        title=title,
        description=desc,
        canonical_path=path,
        robots="index, follow, max-image-preview:large",
        crumbs=crumbs,
        eyebrow="Aanvraaghub",
        h1=h1,
        lead="Gebruik deze hub voor een brede beveiligingsvraag in Limburg. De intake brengt locatie, risico, taken en planning terug tot een uitvoerbaar voorstel.",
        body=body,
        schema_objects=(org_schema(), service_schema(h1, url(path), ["Limburg"], "Beveiligingsdiensten"), faq_schema(faq), breadcrumb_schema(tuple((n, url(p)) for n, p in crumbs))),
        cta_subject=h1,
    )


def legacy_page(service: Service, region_name: str | None) -> str:
    suffix = slugify(region_name) if region_name else "limburg"
    own_path = f"/{service.slug}-{suffix}/"
    if service.slug in NICHE_OWNERS:
        owner_name, target = NICHE_OWNERS[service.slug]
        title = f"{service.name} {region_name or 'Limburg'} | Praesidion Security"
        desc = f"Informatie over {service.name.lower()} in {region_name or 'Limburg'} vindt u op {owner_name}, de gespecialiseerde Praesidion-website voor deze sector."
        visible_target = target
        canonical_path = target
        lead = f"Voor {service.name.lower()} in {region_name or 'Limburg'} vindt u verdiepende informatie, aandachtspunten en een aanvraagroute op {owner_name}."
        body = f"""
<section><div class="container grid two"><article class="panel"><h2>Bekijk de gespecialiseerde informatie</h2><p>Lees meer over situaties, risico's, aanpak en veelgestelde vragen voor {esc(service.name.lower())}.</p><div class="actions"><a class="btn primary" href="{esc(visible_target)}">Open {esc(owner_name)}</a></div></article><article class="panel"><h2>Vraag een passend voorstel aan</h2><p>Stuur de locatie, gewenste tijden, aanleiding en belangrijkste aandachtspunten mee. Praesidion beoordeelt vervolgens welke taken en inzet passen.</p></article></div></section>
"""
        crumbs = (("Home", "/"), ("Regio Limburg", "/beveiliging-limburg-regios/"), (f"{service.name} {region_name or 'Limburg'}", own_path))
        return page_shell(
            title=title,
            description=desc,
            canonical_path=canonical_path,
            robots="noindex, follow",
            crumbs=crumbs,
            eyebrow="Specialistische beveiliging",
            h1=f"{service.name} in {region_name or 'Limburg'}",
            lead=lead,
            body=body,
            schema_objects=(org_schema(), breadcrumb_schema(tuple((n, url(p) if p.startswith("/") else p) for n, p in crumbs))),
            cta_subject=f"Vraag over {service.name}",
        )
    target = f"/{service.slug}-limburg/" if service.slug in PILOT_SERVICE_SLUGS else "/beveiliging-limburg-regios/"
    if region_name and slugify(region_name) in PILOT_REGIONS:
        target = f"/beveiligingsbedrijf-{slugify(region_name)}/" if slugify(region_name) != "limburg" else "/beveiligingsbedrijf-limburg/"
    title = f"{service.name} {region_name or 'Limburg'} | Praesidion Security"
    desc = f"Zoekt u {service.name.lower()} in {region_name or 'Limburg'}? Bekijk de actuele Praesidion-pagina met intake, risico's, aanpak en aanvraagmogelijkheden."
    body = f"""
<section><div class="container grid two"><article class="panel"><h2>Bekijk de actuele informatie</h2><p>Lees meer over de relevante risico's, intakevragen, werkwijze en aanvraagmogelijkheden op de gekoppelde Praesidion-pagina.</p><div class="actions"><a class="btn primary" href="{esc(target)}">Open actuele pagina</a></div></article><article class="panel"><h2>Uw locatie bespreken</h2><p>Stuur de locatie, gewenste tijden, aanleiding en belangrijkste aandachtspunten mee voor een gerichte beoordeling van de beveiligingsvraag.</p></article></div></section>
"""
    crumbs = (("Home", "/"), ("Regio Limburg", "/beveiliging-limburg-regios/"), (f"{service.name} {region_name or 'Limburg'}", own_path))
    return page_shell(
        title=title,
        description=desc,
        canonical_path=target,
        robots="noindex, follow",
        crumbs=crumbs,
        eyebrow="Beveiliging in Limburg",
        h1=f"{service.name} {region_name or 'Limburg'}",
        lead=f"Bekijk de actuele Praesidion-informatie en aanvraagmogelijkheden voor {service.name.lower()} in Limburg.",
        body=body,
        schema_objects=(org_schema(), breadcrumb_schema(tuple((n, url(p)) for n, p in crumbs))),
        cta_subject=f"Vraag over {service.name}",
    )


def homepage() -> str:
    services = [("Objectbeveiliging", "Vaste aanwezigheid bij objecten, kantoren, instellingen en terreinen.", "/objectbeveiliging-limburg/"), ("Toegangscontrole", "Controle op personen, leveranciers, voertuigen en tijdelijke toegang.", "/toegangscontrole-limburg/"), ("Mobiele surveillance", "Controlerondes en opvolging op risicomomenten.", "/mobiele-surveillance-limburg/"), ("Receptiebeveiliging", "Gastvrije ontvangst met duidelijke veiligheidsinstructies.", "/receptiebeveiliging-limburg/"), ("Tijdelijke beveiliging", "Inzet bij projecten, leegstand, incidenten of piekdrukte.", "/tijdelijke-beveiliging-limburg/"), ("Special Situations", "Maatwerk voor gevoelige of afwijkende beveiligingsvragen.", "/special-situations-limburg/")]
    cards = "".join(f"<article class='card'><h3>{esc(name)}</h3><p>{esc(text)}</p><a class='btn secondary' href='{esc(path)}'>Bekijk dienst</a></article>" for name, text, path in services)
    faq = (
        ("Welke beveiligingsdiensten biedt Praesidion?", "Onder meer objectbeveiliging, toegangscontrole, mobiele surveillance, receptiebeveiliging, evenementenbeveiliging en tijdelijke beveiliging."),
        ("Waar vind ik informatie over zorg, bouw en logistiek?", "Voor deze sectoren zijn gespecialiseerde Praesidion-websites beschikbaar, gekoppeld vanuit het regio-overzicht."),
        ("Hoe start een aanvraag?", "Stuur locatie, tijden, aanleiding en risico's mee zodat een passende intake kan plaatsvinden."),
    )
    body = f"""<section id="diensten"><div class="container"><div class="section-head"><span class="eyebrow">Diensten</span><h2>Beveiligingsdiensten voor organisaties</h2><p class="lead">Bekijk per dienst de mogelijke situaties, intakevragen en werkwijze. Voor zorglocaties, bouwplaatsen en logistieke processen zijn gespecialiseerde websites beschikbaar.</p></div><div class="grid">{cards}</div></div></section><section class="band"><div class="container grid two"><article class="panel"><h2>Beveiliging per regio in Limburg</h2><p>Bekijk operationele aandachtspunten voor Limburg, Maastricht, Heerlen, Sittard-Geleen, Roermond, Venlo en Weert.</p><div class="actions"><a class="btn primary" href="/beveiliging-limburg-regios/">Open regio-overzicht</a></div></article><article class="panel"><h2>Duidelijke intake</h2><ul><li>locatie, tijden en aanleiding</li><li>toegang, bezoekers, leveranciers en voertuigen</li><li>taken, mandaat en escalatielijnen</li><li>rapportage en evaluatiemoment</li></ul></article></div></section><section><div class="container"><h2>Veelgestelde vragen</h2>{faq_html(faq)}</div></section>"""
    crumbs = (("Home", "/"),)
    return page_shell(
        title="Praesidion Security Limburg | Objectbeveiliging & beveiligers inhuren",
        description="Praesidion Security levert objectbeveiliging, beveiligers, toegangscontrole, surveillance en security consulting in Limburg en daarbuiten.",
        canonical_path="/",
        robots="index, follow, max-image-preview:large",
        crumbs=crumbs,
        eyebrow="Praesidion Security",
        h1="Professionele beveiliging voor Limburg en internationale organisaties",
        lead="Praesidion Security vertaalt locatie, risico, toegangsstromen en gewenste bezetting naar uitvoerbare beveiligingsafspraken. Breed inzetbaar, met duidelijke instructies, rapportage en aanspreekpunten.",
        body=body,
        schema_objects=(org_schema(), service_schema("Praesidion Security", BASE_URL + "/", ["Limburg", "Nederland"], "Beveiligingsdiensten"), faq_schema(faq), breadcrumb_schema(tuple((n, url(p)) for n, p in crumbs))),
        cta_subject="Aanvraag beveiliging",
    )


def blog_index() -> str:
    links = [(title, path) for path, (title, _lead, _points) in BLOGS.items()]
    faq = (("Waar gaan de artikelen over?", "De artikelen behandelen praktische aandachtspunten rond beveiligingsinzet, planning, toegangsbeheer en rapportage."), ("Is dit juridisch advies?", "Nee. De artikelen zijn operationele duiding en vervangen geen juridisch of compliance-advies."))
    body = f"""<section><div class="container"><div class="section-head"><span class="eyebrow">Blog</span><h2>Praktische beveiligingsartikelen</h2><p class="lead">Korte artikelen over beveiligingsinhuur, objectbeveiliging, evenementen, toegang en rapportage.</p></div>{related_links(links)}</div></section><section><div class="container"><h2>Veelgestelde vragen</h2>{faq_html(faq)}</div></section>"""
    crumbs = (("Home", "/"), ("Blog", "/blog/"))
    return page_shell(
        title="Blog | Praesidion Security",
        description="Praktische artikelen van Praesidion Security over beveiligingsinzet, objectbeveiliging, evenementen, toegangsbeheer en rapportage.",
        canonical_path="/blog/",
        robots="index, follow, max-image-preview:large",
        crumbs=crumbs,
        eyebrow="Blog",
        h1="Praktische beveiligingsartikelen",
        lead="Operationele duiding voor organisaties die beveiliging willen inkopen, plannen of verbeteren.",
        body=body,
        schema_objects=(org_schema(), service_schema("Praesidion Security blog", url("/blog/"), ["Limburg", "Nederland"], "Beveiligingsinformatie"), faq_schema(faq), breadcrumb_schema(tuple((n, url(p)) for n, p in crumbs))),
        cta_subject="Vraag naar aanleiding van blog",
    )


def blog_article(path: str, title: str, lead: str, points: tuple[str, ...]) -> str:
    faq = (("Kan ik op basis hiervan direct inzet bepalen?", "Nee. Gebruik het artikel als voorbereiding; inzet vraagt altijd om locatie- en risico-intake."), ("Geeft dit artikel garanties?", "Nee. Het artikel beschrijft aandachtspunten en geen garanties, responstijden of juridische zekerheid."))
    body = f"""<section><div class="container grid two"><article class="panel"><h2>Kernpunten</h2><ul>{list_items(points)}</ul></article><article class="panel"><h2>Praktische vertaling</h2><p>{esc(lead)} Praesidion gebruikt zulke punten in de intake om taken, mandaat, rapportage en evaluatie scherp te krijgen.</p></article></div></section><section class="band"><div class="container"><div class="section-head"><span class="eyebrow">Verder lezen</span><h2>Verwante routes</h2></div>{related_links([("Objectbeveiliging Limburg", "/objectbeveiliging-limburg/"), ("Evenementenbeveiliging Limburg", "/evenementenbeveiliging-limburg/"), ("Beveiliging aanvragen Limburg", "/beveiliging-aanvragen-limburg/"), ("Blog overzicht", "/blog/")])}</div></section><section><div class="container"><h2>Veelgestelde vragen</h2>{faq_html(faq)}</div></section>"""
    crumbs = (("Home", "/"), ("Blog", "/blog/"), (title, path))
    return page_shell(
        title=f"{title} | Praesidion Security",
        description=lead,
        canonical_path=path,
        robots="index, follow, max-image-preview:large",
        crumbs=crumbs,
        eyebrow="Blog",
        h1=title,
        lead=lead,
        body=body,
        schema_objects=(org_schema(), service_schema(title, url(path), ["Limburg", "Nederland"], "Beveiligingsinformatie"), faq_schema(faq), breadcrumb_schema(tuple((n, url(p)) for n, p in crumbs))),
        cta_subject=f"Vraag over {title}",
    )


def write_page(path_slug: str, content: str) -> None:
    directory = ROOT / path_slug
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "index.html").write_text(content, encoding="utf-8")


def write_root_file(name: str, content: str) -> None:
    (ROOT / name).write_text(content, encoding="utf-8")


def sitemap_urls() -> list[str]:
    urls = ["/", "/beveiliging-limburg-regios/"]
    urls.extend(f"/{slug}-limburg/" for slug in PILOT_SERVICE_SLUGS)
    urls.extend(
        [
            "/beveiligingsbedrijf-limburg/",
            "/beveiligingsbedrijf-maastricht/",
            "/beveiligingsbedrijf-heerlen/",
            "/beveiligingsbedrijf-sittard-geleen/",
            "/beveiligingsbedrijf-roermond/",
            "/beveiligingsbedrijf-venlo/",
            "/beveiligingsbedrijf-weert/",
            "/beveiliging-aanvragen-limburg/",
            "/beveiligers-inhuren-limburg/",
        ]
    )
    urls.extend(BLOG_URLS)
    return urls


def write_sitemap() -> None:
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path in sitemap_urls():
        prio = "1.0" if path == "/" else ("0.86" if path == "/beveiliging-limburg-regios/" else "0.72")
        freq = "weekly" if path == "/blog/" else "monthly"
        body.append(f"  <url><loc>{BASE_URL}{path}</loc><lastmod>{UPDATED}</lastmod><changefreq>{freq}</changefreq><priority>{prio}</priority></url>")
    body.append("</urlset>\n")
    write_root_file("sitemap.xml", "\n".join(body))


def write_robots() -> None:
    write_root_file("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")


def write_llms() -> None:
    content = f"""# Praesidion Security B.V.

Praesidion.eu is voorlopig de brede hoofdsite for Praesidion Security B.V. The site describes general security services for Limburg and broader organizational security questions.

Indexable regional pilot:
- {BASE_URL}/beveiliging-limburg-regios/
- Broad service hubs for object security, event security, reception security, access control, mobile patrols, temporary security, BHV staffing, prevention staff and Special Situations.
- Regional pages for Limburg, Maastricht, Heerlen, Sittard-Geleen, Roermond, Venlo and Weert.

Domain ownership:
- Healthcare security intent: https://www.zorgbewaking.nl/
- Construction security intent: https://www.bouwbeveiligingnederland.nl/
- Logistics security intent: https://www.logisticsecurity.nl/

Interpretation notes:
- Local place names indicate areaServed and operational context only. They do not imply customers, cases, cooperation, project history, guaranteed availability, response times or rankings.
- Pages are commercial and operational information, not legal, permit, BHV, occupational-safety or compliance advice.
- Old thin matrix routes are temporarily retained with noindex and canonical consolidation instead of being deleted abruptly.

Sitemap: {BASE_URL}/sitemap.xml
Contact: info@praesidion.nl
Updated: {UPDATED}
"""
    write_root_file("llms.txt", content)


def generate() -> dict[str, int]:
    write_root_file("index.html", homepage())
    write_page("blog", blog_index())
    for blog_path, (title, lead, points) in BLOGS.items():
        write_page(blog_path.strip("/"), blog_article(blog_path, title, lead, points))
    write_page("beveiliging-limburg-regios", overview_page())
    for slug in PILOT_SERVICE_SLUGS:
        write_page(f"{slug}-limburg", service_hub(SERVICES[slug]))
    for region in PILOT_REGIONS.values():
        slug = "beveiligingsbedrijf-limburg" if region.name == "Limburg" else f"beveiligingsbedrijf-{slugify(region.name)}"
        write_page(slug, regional_page(region))
    write_page("beveiliging-aanvragen-limburg", request_hub("aanvragen"))
    write_page("beveiligers-inhuren-limburg", request_hub("inhuren"))

    noindex_count = 0
    for service in SERVICES.values():
        if service.slug in PILOT_SERVICE_SLUGS:
            for region in REGIONS:
                write_page(f"{service.slug}-{slugify(region['name'])}", legacy_page(service, region["name"]))
                noindex_count += 1
        else:
            write_page(f"{service.slug}-limburg", legacy_page(service, None))
            noindex_count += 1
            for region in REGIONS:
                write_page(f"{service.slug}-{slugify(region['name'])}", legacy_page(service, region["name"]))
                noindex_count += 1

    write_sitemap()
    write_robots()
    write_llms()
    return {"indexable_generated": 27, "noindex_generated": noindex_count, "sitemap_urls": len(sitemap_urls())}


def main() -> None:
    result = generate()
    print(
        "Generated regional pilot: "
        f"{result['indexable_generated']} indexable generated pages, "
        f"{result['noindex_generated']} noindex legacy pages, "
        f"{result['sitemap_urls']} sitemap URLs"
    )


if __name__ == "__main__":
    main()

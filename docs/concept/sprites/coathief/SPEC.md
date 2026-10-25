# Coathief (coati, Dark-starter fase 2): SPEC

Werkwijze: `docs/lessen/SPRITE_WERKWIJZE.md`. Basis en stijl: de goedgekeurde olinguito v2 (`../olinguito_v2/`: SPEC, referenties, `af/olinguito.png`, 3D-poppetje in `silhouet_kolibriemethode/`). Kopie van fase 1: `referenties/fase1_olinguito.png`.

## Gegeven
- **Naam: Coathief** (Jordi, 25 okt). 8 tekens, past (max. 12).
- **Lijn** (POKEMON.md, besloten): olinguito → **coati** → krabbenetende wasbeer; van kleine criminaliteit naar een nobel thema (Robin Hood). **Lange klauwen in elke vorm**, 2 per poot zoals Sandslash/Linoone (USP van de lijn).
- **Type:** de lijn is Dark; de soort staat nog niet in de repo (`src/data/pokemon/species_info/`), data volgt in een aparte taak.
- **Formaat fase 2:** 1100–1550 px, box ±47–53 (FAKEMON_CHECKLIST D1; fase 1 = 1174 px).

## Jordi's woorden (letterlijk)
- (24 okt, olinguito ronde 2) "Misschien een optie om de neus toch in te korten en pas bij de coati evolutie te vergroten."
- (23 okt, POKEMON.md) Olinguito-concept Haakstaart: "de coati-staart eindigt achter zijn rug in een grijphaak: de dief zit in de staart".
- (IDEEEN.md) "kit dat bessen pikt → tiener-bandiet met gestolen toeristentas aan de staart".

## Jordi's woorden (25 okt, stap 1, letterlijk)
- "belangrijk is de lange snuit en de staart incl patroon. Klauwen aan de poten moeten blijven. Coati's in het echt lopen rond in gangs en zijn echt irritant. Als je begint te eten rennen ze op je af en kunnen ze je naar open krabben. Tof van de olinguito moet het lichaam langer worden, de staart mag krullen, zolang het maar dit patroon heeft. We doen geeen gestolen tas oid in beeld."
- "ik neig ernaar om de kleuren van het gezicht in een soort bivakmuts patroon te maken, dus dat het hoofd aantoonbaar zwarter is (op een kring rondom de ogen na), heb 1 in een andere kleur toegevogd maar die toont wel aan hoe hij loopt."
- "Ik wil dat die in een driekwart positie naar je toeloopt alsof die een confrontatie met je aangaat, met 1 poot dus een beetje opgetild in een looppose"
- "nasua nasua doen we" · "de neus moet zwart zijn, bivakmuts idee"
- "het oog moet minder groot. zie referenties" (foto 6–8)
- "maak een A/B/C test van B1. huidige ontwerp, tegenover hoofd met natuurlijke kleuren ipv de bivak en 1 met de vlekken die je voorstelt. Het oog moet in de praktijk niet puur een rode stip zijn, want dat is niet des pokemons, maar kunnen we mogelijk zodra we gaan spriten aanpassen"
- "ik vind c wel tof! ik dacht eraan om het hele oog te omcirkelen, maar wat jij zegt klopt, dit is een echte coati vlek"
- "akkoord, laten we hiermee werken" (silhouet ronde 1)
- "ja en 1 extra keuring, we moeten kijken of de sprite sterker lijkt dan de olinguito, of het logisch is dat die in coathief evolved"
- (over kleur ronde 3b + evolutiekeuring) "vrijwel perfect, alleen de oren lijken aan de bovenkant afgeknipt he, tegenover een donkere achtergrond net wat minder, maar misschien nog een klein beetej aanpassen de oren. Lijfkleur mag warm en klauwen alleen aan de voorpoten. De olinguito heeft een groot hoofd en grote staart, maar als je het vergelijkt met zigzagoon naar linoone lijkt die niet heel gek heel toch? [...] een lachmondje wat er een beetje gek uit ziet. De klauwen idd mag nog aan gewerkt worden, en de staande voorpot ziet er een beetje gek uit. [...] Ik denk niet dat we vlekkeloos de olinguito kunnen verknleine. Kleine kleurreparaties kan je onthouden en evt later met een a/b doen"

## Referenties (`referenties/`)
- `foto1_rots_snuffelend.webp`: kleur, kopvorm, staartringen. `foto2_zijaanzicht_render.webp`: verhoudingen (lang lijf, lange poten, staart).
- `foto3_boom_frontaal.webp`: gezicht frontaal. `foto4_gang_lopend.png`: staart rechtop bij het lopen, gangs.
- `foto6_zittend_kop.png`, `foto7_kop_closeup.webp`, `foto8_zittend_kop_groot.webp`: kop en oog (klein, donker; lichte vlekken boven en onder het oog), staartringen.
- `foto5_witneus_naar_je_toe.webp`: andere soort/kleur, maar de loop naar je toe (pose) en het donkere gezicht met lichte oogkringen.

## Besloten
- Soort: rode neusbeer (*Nasua nasua*): warm roodbruin lijf, donkere onderpoten, geringde staart (licht/donker).
- Kop als **bivakmuts**: zwart, op een lichte kring rond het oog na; **neus zwart**. Oog **klein** (foto 6–8), donker roodbruin (van de olinguito).
- Lange snuit (één oog in beeld), lichaam langer dan de olinguito, staart met ringpatroon (mag krullen), 2 lange lichte klauwen per poot.
- Geen tas of ander voorwerp.
- Pose: driekwart naar de kijker toe lopen, confrontatie, één voorpoot opgetild (diagonale gang).

## Ontwerp (stap 1)
- 3D-poppetje `ontwerp/pop3d_coati.py` (op basis van het olinguito-poppetje); hoekenraster `ontwerp/hoeken.png` (lijf 30/42/54°, kop +10/+22°), Jordi koos **B1** (lijf 42°, kop 52°) als basis voor een kop-test: `ontwerp/kop_abc.png` (A bivakmuts + kring, B natuurlijke kop + vlekken, C bivakmuts + vlekken), wacht op Jordi.
- Oog bij het spriten: geen platte rode stip, maar een Pokémon-oog (bovenlid, iris donker boven/licht onder, glans).

## Bevroren
- **Hoek B1** (lijf 42°, kop 52°) en **kop C**: zwarte bivakmuts met lichte coati-vlekken boven en onder het oog, zwarte neus (Jordi, 25 okt).

## Silhouet (stap 2)
- Bij het verkleinen las de opgetilde poot als staand en verdween de verre voorpoot achter de nabije; daarom in het poppetje: kop 14° omhoog (kijkt de speler aan, poot blijft onder de kop zichtbaar), nabije voorpoot hoger (klauwen vrij van de grond), verre voorpoot en verre achterpoot naar achteren (eigen kolom). Onderlaag: `silhouet/onderlaag_b1c_256.png`.
- Ronde 1: `silhouet/ronde1.txt` / `ronde1_1x.png` / `vel_ronde1.png` (1297 px). Basis = direct verkleind (`direct.txt`, 1303 px, `silhouet_direct.py`); handreparaties alleen in zone 1 (voorpoten x 15–33, y 50–63: 2 hangende klauwen, 2 kolommen lucht tot de verre poot) en zone 2 (nabije achtervoet); 46 px gewijzigd, 0 buiten de zones (`repareer.py`).
- **Silhouet ronde 1 goedgekeurd en bevroren** (Jordi, 25 okt: "akkoord, laten we hiermee werken"): `silhouet/ronde1.txt` = `silhouet/ronde1_1x.png` (1297 px). Alle kleurrondes: alpha-diff 0 hiermee.

## Besluiten na ronde 3b (Jordi, 25 okt)
- Lijfkleur blijft warm (*Nasua nasua*). Klauwen alleen aan de voorpoten, aan **beide** voorpoten (Jordi over ronde 4: "hij heeft nu 1 poot met klauwen en 1 zonder"); silhouet ronde 3 (`silhouet/ronde3.py`, +13 px: 2 klauwtjes aan de staande voet met lucht ertussen (voorstel maker ronde 5), 1332 px).
- Formaat blijft (precedent Zigzagoon → Linoone ×0,97); olinguito niet verkleinen.
- Te doen: oren rond (niet afgeknipt), geen lachmondje, klauwen beter/langer, staande verre voorpoot natuurlijker → silhouet ronde 2 (`silhouet/ronde2.py`, 46 px in 3 zones, 1319 px) + kleur ronde 4.
- **Bewaard voor later (A/B-test):** bovenste vlek een tint terug zodat het oog het helderste punt is; frons/wenkbrauwlijn boven het oog; klauwen bijna-wit zoals de olinguito; sterkere lichtvlekken schouder/heup; familiebrug in oudroze (mondhoek of oorbinnenkant). Bron: `kleur/ronde3/EVOLUTIEKEURING.md`.

## Afgekeurd (niet herhalen)
- Lachmondje (mondhoek omhoog, ronde 3): "ziet er een beetje gek uit".
- Opgetilde voorpoot ver naar links gestrekt met de klauwen vooruit (silhouet ronde 2–3): moet zoals de onderlaag, compact onder de kin met hangende klauwen (Jordi: "nee de voorpoten zijn omgewisseld, kijk maar goed" en bij de krabbel `referenties/krabbel_jordi_voorpoten.png`: "nee dat wordt te scherp dan. [...] Misschien kan je even de twee poten opnieuw met een silhouet maken terwijl de rest hetzelfde blijft, want de rest is helemaal goed").
- **Silhouet ronde 4 goedgekeurd en bevroren** (Jordi: "ja nu klopt ie"): `silhouet/ronde4.txt` (1321 px), voorpoten zoals de onderlaag.
- Kleur ronde 6 week af van de onderlaag (Jordi: "haha maar nu doe je dus weer hetzelfde"; bij het silhouet over de onderlaag: "hier gaat ie goed"; die afbeelding kwam alleen in de chat binnen, het is `silhouet/vel_ronde4.png`, paneel 4). Daarom kleurt ronde 6b de voorpoten pixel voor pixel naar de onderlaag-indeling `silhouet/labels_voorpoten.txt` (o.a. grote crème klauwen ook aan de staande voet, naar voren op de grond).
- Ronde 6c (Jordi, krabbel `referenties/krabbel_jordi_belijning.png`): "het zit hem in de belijning. Ik heb hier een zwarte lijn getrokken die het wat dichter in de buurt doet komen van afbeelding 'onderlaag'. Daar zit de poot ook nog iets meer over de ander heen" → lijn (schaal 6x, gemeten via het oog) als omlijning tussen nabije schouder en staande poot, 7 px (`kleur/ronde6c/lijn.py`).
- Over 6c: "het sluit nog niet helemaal perfect aan. Kijk naar de non sprite. puur alleen de lijn trekken is niet voldoende, moet iets betere afwerking" → ronde 6d (maker): ronde curve, roodbruine bovenarm over de verre poot, gebogen naad naar de donkere manchet, slagschaduw (vergelijking `kleur/ronde6c/onderlaag_vs_6c_zoom.png`). Jordi erbij: "in het origineel zijn de voorpoten ook ietsje dikker" → voorpoten ±1 px dikker, nieuw silhouet `silhouet/ronde5.txt`.
- Mijn interpretaties die niet klopten: verre achterpoot schuin (`silhouet/variant_loop.*`), staande poot vóór de opgetilde (`silhouet/variant_wissel.*`).

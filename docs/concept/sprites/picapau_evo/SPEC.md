# Evolutie van Picapau (Electric/Flying, eindvorm): SPEC

Naam open (voorstel uit IDEEEN: Picaraio = *pica-pau* + *raio*). Pre-evo: `../picapau/` (af, 5 nov). Concept: `docs/concept/IDEEEN.md` (Roomkleurige specht, "Evolutie die op Raichu lijkt").
Bron: *Celeus elegans* (chestnut woodpecker): kastanjebruin met lichte kuif; de geel → oranje-kastanje stap zit in het geslacht zelf (zoals Pikachu → Raichu).

## Jordi letterlijk
- "tijd om de evolutie van picapau te maken" (5 nov)
- Eerder (IDEEEN, 5 nov): evolutie die op Raichu lijkt, "maar die lijkt minder op Raichu dan Picapau op Pikachu" (zoals Toedscruel/Tentacruel).
- Keuzes (5 nov):
  - Kleur: **kastanje + lichte kuif** (lijf oranje-kastanje zoals *Celeus elegans*, kuif en buik licht crème).
  - Tong (Raichu-staart als spechtentong met bliksempunt): **alleen in dex/move**, niet in de sprite. Jordi: "die tong is een leuk idee maar ik ben bang dat dat niet lekker te spriten is".
  - Pose: **vleugels half open** (dreigend, kuif opgezet, grotere sprite).
  - Kuif: **grote gekrulde kuif** (twee lange kuifpunten die aan de top naar buiten krullen zoals Raichu's oren; de donkere toppen van Picapau vallen weg, Raichu heeft bruine oortoppen).
- Inspiratie: "deze sprite mag als inspiratie dienen" · "uit gen 1" → `referenties/jordi_inspiratie_raichu_gen1.png` (Raichu, Gen 1-frontsprite op 16×, 64×64).
  Beschrijving (Claude): 3/4 naar links, voorovergebogen en ineengedoken; grote ronde kop als eigen vorm, één groot oog, wangvlek; lichte buik als grote ovaal; arm voor de buik, verre arm opgetrokken achter de kop; oren met gekrulde toppen naar rechtsboven; staart in een grote S-boog achter en onder het lijf langs, eindigend in de bliksempunt linksonder. Dynamisch, gespannen, vult het hele frame.
  Lezing (Claude): inspiratie voor houding en spanning (vult het frame), niet om over te nemen.
- Wat Jordi eruit wil (5 nov): **"echt zon krullende staart met een bliksemschicht"** · **"krullende oren"** (= de kuif) · **"imposant, groot, opgeblazen"**.
  → De **staart** zelf (niet de tong) wordt een lange krullende staart (S-boog zoals Raichu Gen 1) met een bliksemschicht als punt; bij een specht: de stijve steunstaart verlengd tot een krullende veerstaart/-pluim met bliksempunt. De kuifpunten krullen zoals Raichu's oren. Het lijf opgeblazen (veren opgezet, zoals een vogel die zich groot maakt), groot en imposant.

- Jordi (5 nov): **"we kunnen wel proberen zo'n tong te spriten die dan half eruit hangt, maar ik denk dat het niet lukt"** → tong half uit de snavel als **variant náást** de hoofdversie (zonder tong), niet als hoofdkeuze.
- Jordi (5 nov): **"Voor inspiratie sprites kan je kijken naar legendary vogels enzo, die hebben ook altijd wat complexere poses met dingen die om ze heen krullen. Ik wil gewoon voorkomen dat al onze vogels hetzelfde erbij staan"** → `referenties/vergelijking_vogelposes.png` (Gen 3-frontsprites op 4×: Lugia, Ho-Oh, Articuno (staart krult om het lijf), Zapdos, Moltres, Galar-vogels, Rayquaza, Yveltal, Noivern, Braviary, Staraptor, Talonflame, Corviknight, Kilowattrel). Pose moet duidelijk anders zijn dan onze eigen vogels (kolibrie, kolibrie pre-evo, Picapau: alle drie vleugels dicht/rechtop).

## Familie met Picapau (vast)
- Specht: beitelsnavel blijft, oog en kop in de lijn van Picapau, vleugels met de ronde lichte stippen (Jordi: stippen, geen Pidgey-schubben), stijve steunstaart.
- Zwaarder lijf, bolle buik (Jordi bij Picapau: "het lichaam moet echt bol, dat is juist een kenmerk van pikachu").

## Onderdelen
| onderdeel | bron | Jordi | status |
|---|---|---|---|
| kleur | *Celeus elegans* | kastanje + lichte kuif | gekozen |
| pose | Raichu Gen 1 als inspiratie | vleugels half open; "imposant, groot, opgeblazen" | gekozen, bron (model/foto) open |
| staart | Raichu Gen 1 | "echt zon krullende staart met een bliksemschicht" | gekozen |
| kuif | Raichu-oren | grote gekrulde kuif; "krullende oren" | gekozen |
| tong | spechtentong | alleen dex/move; variant met tong half uit de snavel proberen | variant |
| snavel, oog, poten | Picapau | – | open |

## Afgekeurd (niet herhalen)
- Alle lessen van Picapau (`../picapau/SPEC.md`): profielkop zonder kopdraai, dunne delen die bij het verkleinen wegvallen, model aanpassen als de sprite fout is.

## Model ronde 1 (5 nov)
- `blender/standen/` (A/B/C + tong). Claude: leest als dikke Pidgey/Fletchinder met witte ramshoorns, niet imposant; tong = worm op 1× → tong-variant vervalt.
- Jordi over de kuif in ronde 1: **"vooral de oren zijn too much"** · **"te wit, te groot"** → kuif kleiner, rustiger, subtiele krul, overwegend kastanje (hooguit lichte rand/top). Vervangt "lichte kuif" uit de kleurkeuze.
- Ronde 2 (maker): kuif zoals hierboven, imposanter (borst, kop, bredere vleugels, minder stekels, grotere stippen), staart als platte veerpluim in S met grotere bliksem, langere beitelsnavel, echte kastanje in de render.
- Jordi: **"de vleugels zijn ook iets te draconian, maar voor de rest vind ik hem wel al ergens op beginnen te lijken"** → vleugels: vogelvleugel met ronde voorrand en zachte, gesloten handpennen (geen drakenvingers); de rest van C (lijf, kop, kopdraai, pose) alleen licht bijwerken, niet herbouwen.

## Model ronde 2 (6 nov)
- `blender/r2/` (C2). Jordi: **"de oren en staart zijn geen raichu staart"**.
- Bron nu de echte Raichu: `referenties/raichu_gen3_8x.png` + Gen 1. Staart = dunne donkere koord (1–2 px) in een krul/lus met een grote platte bliksem als eind (niet de dikke pluim met kleine bliksem van C2). Kuif = Raichu-oorvorm: brede driehoek, donkere buitenkant, lichtere binnenkant, dunne krul aan de punt; maat zoals C2 ("too much", "te wit, te groot" blijven gelden). Ronde 3: alleen kuif en staart, rest van C2 bevroren.
- Jordi: **"nee de gen 1 raichu sprite moet je ook naar kijken"** → Gen 1 (`jordi_inspiratie_raichu_gen1.png`) is de hoofdbron, Gen 3 aanvulling. Gen 1-staart: brede donkere S (±3–4 px op 64) die om het lijf loopt, grote schuine bliksem linksonder; Gen 1-oren: lichte binnenkant, punt eindigt in een spiraal/krul.

## Model ronde 3 → sprite (6 nov)
- `blender/r3/` (C3): staart + bliksem lezen als Gen 1; oren = ringetjes op steeltjes ("slakkenvoelsprieten"), verre oor tegen de vleugel.
- Jordi: **"Ga een sprite bouwen. Dat is makkelijker aan te passen"** → model stopt bij C3 (bron voor massa: lijf, kop, vleugels, staart, bliksem). Sprite v1: overtrekken van de C3-render (methode Picapau sprite v2); de oren in de pixelstap naar Gen 1 (oorpunt loopt zelf uit in de krul, geen losse ring).

## Sprite r2 (6 nov)
- `sprite_v1/r2/`. Claude: schaduw met regels in code (niet met de hand), kop leest als vos.
- Jordi: **"het ding is, het is nog niet echt een vogel he. De staart mag wat dunner en wat meer vogelachtig, desnoods zwart. De oren mogen ook naar achter bewegen, zwart en meer op de raichu lijken, verder mag die wat graden naar links draaien, want nu zien we een flink stuk hoofd met het oog helemaal aan de zijkant. De vleugel mag iets vogel achtiger"**
- → pose-wijziging (draaien) in het model, dan opnieuw overtrekken; kleur daarna met de hand.
- Jordi: **"ja het lijkt nu iets meer een alien dan een vogel, en ik heb liever eigenlijk een grote vogel met raichu motief"** → koerswijziging: basis = echte grote vogel (nek, borst, schuin lijf, poten onder het zwaartepunt; Staraptor/Braviary/Talonflame/Pidgeot, grote specht *Campephilus*/*Dryocopus*); Raichu alleen als motief (zwarte gekrulde kuif, dunne staart met bliksem, kastanje + crème, wangvlek). Ei-lijf van C3 vervalt. Model r4 eerst tonen, dan pas sprite.

## Model r4 (6 nov)
- `blender/r4/` (V2 gekozen: lijf 35°, kop +5°): leest als vogel (lijster/roodborst), niet imposant; oren op 1× een zwarte vlek; poten dun en naast elkaar; staartlus + bliksem nemen veel frame. Voorstel: lijf voorover (Talonflame-diagonaal), vleugels hoger en breder, bliksem iets kleiner, grote voeten met klauwen.
- Jordi over r4: **"ja nu komen we ergens! de snavel mag open, dat geeft wat karakter. Vergeet mijn eerdere instructies over de oren, die mogen dunner en wat verder doorkrullen, iets meer zoals de onderkant van de oren van raichu"** + "ja" op de imposant-ronde → r5: voorover, vleugels hoger/breder, bliksem iets kleiner, grote klauwen; snavel open; oren dunner met doorlopende spiraal (oude maatgrens vervalt).
- Jordi: **"ja en in de pose mag de buik echt naar voren, die laten we een beetje op die gen 1 raichu pose lijken"** → grote bolle crème buik die naar voren/links uitpuilt (Gen 1-houding), lijf helt eromheen; blijft een vogel.

## Model r5 (6 nov)
- `blender/r5/` (vel_r5, closeup_r5): voorover, vleugels 1,32×, snavel open, oren dun met spiraal (±410°), bolle buik naar voren, grote voeten met klauwen. Zwak: diagonaal minder zichtbaar door de buik, verre vleugel verstopt, bliksem klein (voorstel 0,85×), staartlus breed.
- Jordi over r5: **"de buik is teveel een bulge"** → r6: buik als deel van één doorlopende lijfvorm (volle borst/buik, geen losse bol of knik); bliksem 0,85×.
- Jordi: **"maar laten we een sprite gaan maken"** · **"dat is makkelijker te editen"** → geen r6-model; sprite r3 van de r5-render, buik (geen bulge) en grotere bliksem in de sprite opgelost.

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

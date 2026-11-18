# Studie: rugsprites, icoontjes en overworldsprites (18 nov)

Vraag van Jordi: "Doe een studie naar back sprites en icoontjes (zoals in het Pokemon menu en in de overworld) en kijk hoe deze in verhouding staan tot de normale sprites, bekijk daarna wat een goede way of working zou zijn om deze te maken voor onze nieuwe designs." Aanvulling: "beperk je niet alleen tot de hoenn soorten".

Gemeten: **962 soorten van Gen 1–9** (de set die de game nu toont: DS-stijl/expansion) en apart de **385 originele GBA-sprites** (Gen 1–3, `*_gba.png`; onze nieuwe sprites zijn Gen 3-stijl, dus die set is de stijlmaat). Vormen (Alola, Mega enz.) niet meegeteld.

Vellen (3× en 4×):
- `1_vel_ingame.png`: front, rug, icoon (2 frames), overworld (6 frames) van 14 soorten uit alle generaties, in-game set.
- `2_vel_gba.png`: hetzelfde met de originele GBA-sprites (Zigzagoon, Taillow, Gastly, Seviper, Aipom, Treecko, Wailord, Ninjask, Shuppet).
- `3_icoon_vs_verkleining.png`: front, echt GBA-icoon, en de front kaal verkleind tot dezelfde hoogte; onderaan onze viscacha en Gengas kaal verkleind.

Scripts (vanuit de repo-root): `vel.py uit.png [--set gba] soort … | map/` (een eigen map met `front.png`/`back.png`/`icon.png`/`overworld.png` kan ook), `naief.py`, `meet_gba.py` + `stat_gba.py`, `meet_alle.py` (heeft een lijst `gen.txt` "soort generatie" nodig, gemaakt uit `src/data/pokemon/species_info/gen_N_families.h`).

---

## 1. Formaten in de game

| Onderdeel | Bestand | Formaat | Palet | Waar te zien |
|---|---|---|---|---|
| Front | `anim_front.png` | 64×128 (2 frames) | eigen 16 kleuren (`normal.pal`) | gevecht (tegenstander), Pokédex, samenvatting |
| Rug | `back.png` | 64×64, 1 frame (beweging komt van `backAnimId`) | **hetzelfde palet als de front** | gevecht (eigen Pokémon) |
| Icoon | `icon.png` | 32×64 (2 frames van 32×32) | één van **6 gedeelde icoonpaletten** (`icon_palettes/pal0–5.pal`, `.iconPalIndex`) | party-menu, pc-boxen, enz. |
| Overworld | `overworld.png` | 192×32 (6 frames van 32×32); 20 reuzen 384×64 (frames 64×64) | eigen 16 kleuren (`overworld_normal.pal` + `overworld_shiny.pal`) | Pokémon als NPC in de wereld (`OBJ_EVENT_GFX_SPECIES`); volgers staan uit |

Overworld-frames (uit `sAnimTable_Following`): 0–1 = naar beneden (naar de speler), 2–3 = naar boven (rug), 4–5 = naar links (opzij); naar rechts is 4–5 gespiegeld. Stilstaan = frame 0/2/4, lopen wisselt met frame 1/3/5.

**Belangrijk voor ons:**
- Overworldsprites komen alleen in de ROM voor soorten die als `OBJ_EVENT_GFX_SPECIES(...)` in een kaart/script staan (`ow_species_keep.py`). **Volgers (`OW_FOLLOWERS_ENABLED`) staan uit.** Zolang dat zo blijft, heeft een nieuwe Pokémon alleen een overworldsprite nodig als hij ergens zichtbaar in de wereld staat (statische encounter, NPC-Pokémon, legendary).
- Rug en front delen het palet: een nieuwe kleur alleen voor de rug kan niet (gemeten: mediaan 0 extra indexen in de rug). Varianten/shiny gelden dus automatisch ook voor de rug.
- Het icoon heeft géén eigen palet. Van de 6 icoonpaletten gebruiken de gewone soorten alleen 0, 1 en 2; 3–5 worden wel geladen maar alleen door 17 vormen gebruikt. Er kunnen er niet meer bij (OBJ-paletslots 0–5 zijn op schermen met iconen vol).

## 2. Verhoudingen tot de front (gemeten)

Mediaan (p10–p90). Front-hoogte/breedte = bounding box van frame 1.

| | Alle 962 (DS-set) | 385 GBA (Gen 1–3) | Per generatie |
|---|---|---|---|
| rug-breedte / front-breedte | **1,16** (0,95–1,50) | 1,11 (0,89–1,42); Gen 3: 1,17 | 1,11–1,23, geen trend |
| rug-hoogte / front-hoogte | **0,98** (0,78–1,22) | 0,98 (0,76–1,24) | 0,95–1,05 |
| icoon-hoogte / front-hoogte | **0,44** (0,37–0,52) | 0,41 (0,34–0,52) | 0,41–0,46 |
| overworld-hoogte / front-hoogte | **0,43** (0,36–0,52) | (zelfde overworldset) | 0,41–0,48 |
| overworld-hoogte / icoon-hoogte | 1,05 (0,84–1,28) | | |

De verhoudingen zijn **niet lineair**: kleine soorten krijgen een relatief grote rug en een relatief groot icoon, grote soorten lopen tegen de rand van 64 of 32 aan. Daarom een tabel op front-hoogte in plaats van één factor (mediaan per groep, DS-set):

| Front-hoogte | n | Front-breedte | **Rug b×h** | **Icoon b×h** | **Overworld b×h** |
|---|---|---|---|---|---|
| < 30 | 30 | 40 | 51×32 | 18×15 | 15×15 |
| 30–39 | 168 | 37 | 51×39 | 18×18 | 15×16 |
| 40–49 | 265 | 43 | 55×47 | 21×21 | 18×19 |
| 50–57 | 217 | 53 | 61×51 | 23×22 | 21×22 |
| 58–64 | 262 | 60 | 62×56 | 25×24 | 24×26 |

Overige vaste maten:
- **Rug:** onderkant **recht afgesneden**: de onderste rij is mediaan 86% zo breed als de breedste rij. `backPicYOffset` = het aantal lege rijen eronder (bij 130 van 131 Gen 3-soorten precies), zodat de snijlijn in het gevecht op de bovenrand van het tekstvak valt (y 112). Midden x ≈ 31,5 (net als de front). Minder kleuren gebruikt dan de front (11 tegen 13: buik, gezicht en poten zie je niet).
- **Icoon:** onderkant op **y 29** (28–30), midden x ≈ 16. ±8 kleuren (6–10). Frame 2: meestal **bovenkant 1 px lager, voeten op dezelfde rij** (ingedrukt; 195 van 385 GBA), anders 1 px hoger of verschoven; ±30% van de pixels verschilt na de beste verschuiving, dus naast het verschuiven verandert er iets kleins (poot, mond, oor).
- **Overworld:** onderkant op y 29 (28–31), 12–13 kleuren, loopframe even hoog als stilstaan (het lopen zit in de poten, niet in op-en-neer).

## 3. Wat er gebeurt behalve schalen (kijken naar de vellen)

### Rug
- **Ander standpunt, zelfde pose-idee:** van linksachter-boven, het lijf van de kijker af naar rechtsboven; de kop draait in profiel zodat vaak **één oog en de snuit/snavel** te zien zijn (Taillow, Mudbray, Feebas, Pikachu, Shuppet). Ronde/frontale soorten kijken over de schouder (Gastly: grijns aan de rechterrand) of laten alleen de achterkant zien (Seviper, Coalossal).
- **Ingezoomd:** het lijf is groter dan in de front en loopt het vak uit; staarten, vleugels en armen mogen buiten beeld vallen (Wailord: alleen de rug als heuvel; Aipom: de staarthand boven in beeld).
- Wat de rug vertelt: de **achterkant-kenmerken** (Zigzagoons zigzagrug, Seviper's rugplaten, Ninjask's vleugels en rugpatroon, Taillow's staart). Kenmerken die alleen van voren zichtbaar zijn (buikvlek, gezicht) vallen weg.
- Kenmerkende houding blijft: Treecko houdt in de rug dezelfde gespreide armen als in de front.
- Licht en selout als de front (licht linksboven), geen omlijning langs de snijlijn.

### Icoon
- **Geen verkleining maar een mini-ontwerp** (`3_icoon_vs_verkleining.png`): een kale verkleining wordt een vlek (Zigzagoon, Aipom, Sentret, en ook onze viscacha), het echte icoon niet. Wat Game Freak doet:
  - **Kop groter** (chibi), lijf korter; de kop is het grootste vlak.
  - **Eigen, eenvoudige pose**, vaak meer van opzij en naar links: Sentret staat op vier poten in plaats van op zijn staart, Aipom zit ineengedoken met de staarthand ernaast, Ninjask van opzij met één vleugel.
  - **Grote delen ingekort of weggelaten** (Ninjask's vleugels, Aipom's lange staart, Gastly's gaswolk tot een paar stipjes), het **ene herkenningsteken blijft groot** (Sentrets oren en gestreepte staart, Taillow's rode gezicht, Seviper's rode staartmes).
  - Dikke donkere omlijning (donkergrijs uit het icoonpalet, index 15 = 65,65,65), 2 tinten per kleur, nauwelijks details.
- Kijkt meestal naar links, zoals de front.

### Overworld
- **HGSS-stijl, ander standpunt dan de front:** naar beneden = **recht van voren** (niet driekwart), naar boven = recht van achteren, opzij = **profiel**. Groot hoofd, kort lijf, zwarte omlijning, eigen palet (vaak iets donkerder en verzadigder dan de front).
- Bijna iedereen 32×32 (942 van 962); alleen echt reusachtige soorten 64×64 (Wailord, Steelix, de grote legendaries).
- Er is **geen GBA-overworldset**: ook voor Gen 1–3 komen ze uit HGSS. Onze Gen 3-fronts zullen dus in elk geval naast HGSS-achtige overworldsprites staan; dat is in de game al zo voor alle bestaande soorten.

## 4. Gevolgen voor onze nieuwe designs
1. **De rug is een nieuw aanzicht**: dat staat niet in de front of het Gemini-model. Het is dus (net als de front) ontwerpwerk met een bron, geen afgeleide. Voor de rug is een model nodig.
2. **Het icoon is een mini-ontwerp**: verkleinen kan alleen als onderlaag; de keuzes (welk kenmerk groot, welke pose) zijn ontwerp.
3. **De overworld is (nog) niet nodig** behalve voor soorten die zichtbaar in de wereld staan. Gaan volgers ooit aan, dan voor alle soorten (3 aanzichten: voor, achter, opzij).
4. Kleur: rug = palet van de front (komt gratis mee), icoon = beperkt tot een gedeeld palet (0/1/2, eventueel 3–5), overworld = eigen palet, af te leiden van de front.

## 5. Voorgestelde werkwijze (nog niet getest; eerst een proef)

Algemeen, zoals bij frame 2 (`frame2_studie/STUDIE.md` §12): **per soort klein beginnen, één proef, dan voor alle soorten samen** (SPRITE_KERN regel 6). Alles bouwt op de **goedgekeurde, bevroren front**; de makerregels van SPRITE_KERN gelden ("model overnemen, nooit hertekenen", één maker per sprite, Claude vergelijkt, verse keurder, pas dan Jordi).

### A. Rugsprite (per soort, het meeste werk)
1. **Rugburen kiezen:** 2–3 echte Gen 3 (GBA-)ruggen van dezelfde bouw (viervoeter: Zigzagoon/Mightyena/Absol; vogel: Taillow/Swellow; tweevoeter: Treecko/Combusken; bol/zwevend: Gastly/Shuppet; slang: Seviper; insect: Ninjask). `vel.py --set gba` maakt het vel.
2. **Model van de rug uit Gemini**: geef de 8×-front (plus het Gemini-frontmodel als dat er is) en één rugbuur als voorbeeld, met in woorden: "dezelfde Pokémon van linksachter-boven gezien, kop in profiel over de schouder (één oog), ingezoomd, onderkant afgesneden". Eén wijziging per prompt (lessen GEMINI.md).
3. **Jordi kiest het rugmodel** (dit is de enige ontwerpkeuze: hoe ziet de achterkant eruit, wat is er van achteren te zien). Kan in batches: per keer 4–6 soorten op één vel.
4. **Overnemen naar 64×64**: grootte uit de tabel in §2 (rug ≈ 1,16× de frontbreedte, ongeveer even hoog; onderkant vlak afgesneden; niets onder de snijlijn), terugzetten met het bestaande verkleinpad (natief raster, `half2.py`-stijl), daarna **in het palet van de front** zetten (geen nieuwe indexen; script controleert).
5. Maker schoont op (oog/snuit uit de front overnemen, selout, geen lijn langs de snede), Claude vergelijkt naast de rugburen en de front, keurder, Jordi.
6. `backPicYOffset` = aantal lege rijen onder de rug; `backAnimId` kiezen bij de data-fase.

Uitzondering: **bol- en wolkvormen** (Dustly, Gengas, blobfish) kunnen misschien zonder Gemini: front 1,15× vergroten, spiegelen/verschuiven zodat het gezicht aan de rechterrand verdwijnt (Gastly-aanpak), maker maakt de achterkant. Eerst proberen op één soort.

### B. Icoon (in batches, weinig werk per soort)
1. **Onderlaag per script** (`icon_from_front.py`, nog te schrijven, staat al op de lijst in SPRITE_PLAN): front naar de doelhoogte uit §2, **kop ±1,3× vergroot**, gemapt op het best passende icoonpalet (0/1/2, anders 3–5), onderkant y 29, midden x 16.
2. **Maker tekent het icoon met de hand** op het 32×32-raster, met de onderlaag en 2–3 echte GBA-iconen van dezelfde bouw ernaast: kop groot, één herkenningsteken groot, de rest ingekort, omlijning in index 15 van het icoonpalet, ±8 kleuren. Hier mag de pose vereenvoudigd worden (dat is wat Game Freak doet), maar alleen in overleg: welk kenmerk groot blijft is een ontwerpkeuze, dus per batch één vraag aan Jordi.
3. **Frame 2 per script**: bovenkant 1 px omlaag (voeten op hun rij), daarna één klein verschil door de maker (poot, mond, oor).
4. Jordi keurt **per vel van ±10 iconen**, op 1× naast echte iconen in een party-menu-mock (of screenshot), niet los.

### C. Overworld (pas als het nodig is)
- Alleen voor soorten die in de wereld staan; anders uitstellen tot er een besluit over volgers is.
- Drie aanzichten (voor/achter/opzij, elk 2 frames), 32×32, ±1,05× zo hoog als het icoon. Het icoon is de beste onderlaag voor "opzij"; "achter" volgt de rug, "voor" is een frontaal aanzicht dat nergens anders bestaat (Gemini of hand, naar HGSS-voorbeelden van dezelfde bouw).
- Palet: front-palet donkerder/verzadigder als eigen `overworld_normal.pal`.

### Proef
Voorstel: eerst **viscacha** (heeft al frame 2, viervoeter) en **Gengas** (bol, test de uitzondering) een rug en een icoon geven. Daarna de werkwijze bijstellen en in `SPRITE_WERKWIJZE.md` zetten.

## 6. Open vragen voor Jordi
1. Volgers (Pokémon die achter je aan lopen): ooit aanzetten? Dan hebben alle ±445 soorten een overworldsprite in 3 aanzichten nodig; zo niet, alleen de paar die in de wereld staan.
2. Iconen: mag de pose vereenvoudigd/anders zijn dan de front (zoals bij Game Freak), of moet het icoon dezelfde pose houden?
3. Proef met viscacha en Gengas starten?

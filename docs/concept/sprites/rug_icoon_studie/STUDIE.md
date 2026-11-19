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
- Het icoon heeft géén eigen palet. Van de 6 icoonpaletten gebruiken bijna alle soorten 0, 1 of 2 (±1300 van de ±1340 vermeldingen); 3–5 alleen een paar tientallen (o.a. de Bulbasaur-lijn in de in-game set). Er kunnen er niet meer bij (OBJ-paletslots 0–5 zijn op schermen met iconen vol).

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

### Icoon (herzien 18 nov, na Jordi: "als je dat niet ziet was je studie nog niet goed genoeg")
Eerste versie van deze paragraaf overdreef de vrije pose (op basis van een paar uitschieters). Gemeten over alle 385 GBA-iconen (`icoon_meet.py`) en bekeken op `5_icoon_vs_front.png` (front verkleind tot icoonhoogte | icoon frame 1 | frame 2):
- **Pose = de pose van de front.** Het silhouet van de verkleinde front en het icoon overlappen mediaan 67% (IoU); bij 71% van de soorten ≥ 0,6, bij maar 4% duidelijk anders (< 0,45). Gespiegeld past zelden beter (16%). Treecko, Torchic, Taillow, Zigzagoon, Poochyena, Electrike, Spinda, Mightyena: zelfde houding.
- **Alleen als de front-pose niet compact te maken is, krijgt het icoon een eigen pose**: lange/rechtopstaande figuren of figuren met ver uitstekende delen (Sentret op zijn staart, Furret, Aipom met de staarthand, Skitty, Plusle, Linoone, Gardevoir, Dragonair, Milotic). Dan wordt het figuurtje compacter en breder (breedte/hoogte front 1,00 → icoon 1,09).
- **Het ontwerp blijft precies het ontwerp:** zelfde gezicht (oog als 1–2 px donker blokje, vaak met 1 lichte pixel), zelfde aftekeningen en kleurverdeling, niets erbij. Kleuren schuiven alleen naar het dichtstbijzijnde van het gedeelde icoonpalet (daardoor soms een tint anders: Mudkip lila-blauw, Raticate geler).
- **Verhoudingen licht chibi:** kop iets groter dan bij verkleinen (Treecko, Torchic, Mudkip, Poochyena), dunne delen dikker (poten, staart minstens 2 px), kleine details weg.
- **Tekenwijze:** dichte omlijning rondom (98–100% van de randpixels donker), **bovenkant index 15 (65,65,65), onderkant lichter grijs (98,98,90)** (gemeten: randhelderheid boven 65, onder 85); grote vlakke vlakken, 1 schaduwtint, hooguit 1–2 px hooglicht, 6–10 kleuren.
- **Frame 2:** zelfde figuur, kleine handeling: kop of lijf 1 px omlaag (ingedrukt), soms bek open, poot of staart anders (Torchic, Mudkip, Zigzagoon). In de game wisselen de frames sneller bij volle HP (elke 6 tikken) en langzamer bij weinig HP (8/14/22); flauwgevallen = alleen frame 0. Het geselecteerde icoon in het party-menu springt daarnaast op en neer (dat doet de engine, `SpriteCB_BouncePartyMonIcon`).
- **Wat Gemini r1 van de viscacha fout deed (en Claude miste):** eigen pose (zittend van opzij) terwijl onze front compact genoeg is om zijn pose te houden, en een ander ontwerp (gezicht, verhoudingen, vlekken). Toets bij een icoon dus eerst: is het silhouet de verkleinde front (of is er een reden om af te wijken), en is het gezicht/ontwerp het onze?

### Overworld
- **HGSS-stijl, ander standpunt dan de front:** naar beneden = **recht van voren** (niet driekwart), naar boven = recht van achteren, opzij = **profiel**. Groot hoofd, kort lijf, zwarte omlijning, eigen palet (vaak iets donkerder en verzadigder dan de front).
- Bijna iedereen 32×32 (942 van 962); alleen echt reusachtige soorten 64×64 (Wailord, Steelix, de grote legendaries).
- Er is **geen GBA-overworldset**: ook voor Gen 1–3 komen ze uit HGSS. Onze Gen 3-fronts zullen dus in elk geval naast HGSS-achtige overworldsprites staan; dat is in de game al zo voor alle bestaande soorten.

### Wijkt de rug af van het front-ontwerp? (Jordi, 18 nov: "In red en blue was dit overduidelijk wel, maar weet niet of dat in gen 3 ook zo is")
Alle 131 Gen 3-paren bekeken (`4_front_rug_gen3_deel1–3.png`, `front_rug_vel.py`). In Gen 3 veel minder dan in Red/Blue, maar wel:
- **Ontwerp (kleuren, kenmerken) klopt bijna altijd.** De rug laat soms iets zien dat van voren niet te zien is (Gulpins zwarte ruit, Kecleons zigzag, Swalots ruiten op de rug), maar dat hoort bij het ontwerp.
- **Pose mag vrij:** Swampert en Marshtomp met armen omhoog, Slaking en Hariyama anders gedraaid, Swellow ineengedoken.
- **Sterk ingezoomd/afgesneden:** soms is alleen een deel te zien (Lombre en Ludicolo: alleen het blad/de hoed; Wailord, Kyogre: een rug als heuvel; Blaziken: alleen kuif en schouder).
- **Een handvol wijkt echt af** van de front in vorm of kleurverdeling: Anorith (plat zijaanzicht), Armaldo, Vibrava, Dusclops, Sealeo/Spheal (vereenvoudigd tot een bol).
- Een paar zijn haast frontaal in plaats van van achteren (Kirlia, Seviper, Jirachi).
Conclusie: Gen 3 is trouw aan het ontwerp, vrij in pose en uitsnede. Voor ons: kleuren en kenmerken van de front aanhouden; pose en uitsnede mogen afwijken als het als rug beter leest.

### Icoon en overworld: vergelijkbaar en vertaalbaar? (Jordi, 18 nov)
Gemeten over 385 soorten (Gen 1–3, GBA-icoon tegen overworld) en bekeken op `6_icoon_vs_overworld.png` (front, rug, icoon 2×, overworld voor 2×, achter 2×, opzij 2×):
- **Maat: gelijk.** Overworld-hoogte (opzij) / icoon-hoogte mediaan 1,00 (0,83–1,20). Beide licht chibi, beide naar links.
- **Aanzicht: anders.** Het icoon is de front-pose (driekwart); de overworld heeft drie rechte aanzichten. Voor viervoeters en vogels die in de front al bijna van opzij staan (Zigzagoon, Electrike, Mightyena, Taillow, Raticate) lijken icoon en overworld-opzij sterk op elkaar: daar is het icoon een goede onderlaag. Bij tweevoeters die naar de kijker staan (Treecko, Pikachu) lijkt het icoon meer op overworld-voor.
- **Stijl: anders.** Overworld = HGSS: zwarte omlijning rondom, eigen palet (≤15 kleuren, dus dichter bij de front-kleuren dan het icoon), vaak verzadigder; het icoon = Gen 3-icoonstijl met gedeeld palet en grijze onderrand.
- **Overworld-achter is niet de gevechtsrug:** recht van achteren, klein, tegenover de rug van linksachter en ingezoomd. De rugsprite helpt alleen voor wat er van achteren te zien is (kleur, staart, oren).
- **Overworld-voor bestaat nergens anders**: recht van voren, het enige echt nieuwe aanzicht.
- **Jordi (18 nov):** "voor het oog lijkt het icoon meer true aan de battle sprite dan de overworld sprite, ondanks het kleurgebruik, qua vorm, silhouet etc." → het icoon is de trouwe verkleining van de front; de overworld is een eigen HGSS-tekening in andere aanzichten.
- Silhouetoverlap (IoU) zegt hier weinig: op ±20 px zijn alle aanzichten ±0,69 gelijk, dus beoordelen op het oog.

## 4. Gevolgen voor onze nieuwe designs
1. **De rug is een nieuw aanzicht**: dat staat niet in de front of het Gemini-model. Het is dus (net als de front) ontwerpwerk met een bron, geen afgeleide. Voor de rug is een model nodig.
2. **Het icoon is een mini-ontwerp**: verkleinen kan alleen als onderlaag; de keuzes (welk kenmerk groot, welke pose) zijn ontwerp.
3. **De overworld is (nog) niet nodig** behalve voor soorten die zichtbaar in de wereld staan. Gaan volgers ooit aan, dan voor alle soorten (3 aanzichten: voor, achter, opzij).
4. Kleur: rug = palet van de front (komt gratis mee), icoon = beperkt tot een gedeeld palet (0/1/2, eventueel 3–5), overworld = eigen palet, af te leiden van de front.

> **Prioriteit (Jordi, 18 nov):** "weet dat ik de iconen en de overworld sprites een stuk minder belangrijk vind dan de battle sprites, ze moeten gewoon consistent zijn, maar hoeven eecht niet hoogstondig pixel art te gaan worden". Lat voor icoon en overworld: consistent met echte Gen 3/HGSS, weinig rondes; de battle sprites (front, rug) krijgen de volle aandacht.
> **Icoonpalet:** pal2/pal5 hebben maar twee zandtinten; Game Freak maakt detail met donkergrijze binnenlijnen, niet met extra tinten.

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

### B. Icoon (herzien 18 nov)
Gemini werkte niet (r1: eigen pose en ander ontwerp; r2 met voorbeeld-icoon: verkleinde front op fijn raster). Daarom uit onze eigen front:
1. **Onderlaag per script** (`icon_onderlaag.py`): front naar de doelhoogte uit §2, gemapt op het best passende icoonpalet, onderkant y 29, midden x 16.
2. **Maker schoont op** naar de icoonregels uit §3 (pose en ontwerp van de front, kop iets groter, dunne delen ≥ 2 px, omlijning boven index 15 en onder lichter grijs, ±8 kleuren), naast echte Gen 3-iconen van dezelfde bouw. Alleen als de front-pose niet compact past een eigen pose, en dan alleen na vraag aan Jordi.
3. **Frame 2:** zelfde figuur, 1 px ingedrukt + één kleine handeling (bek, poot of staart).
4. Jordi keurt op 1× naast echte iconen.

### C. Overworld (pas als het nodig is)
- Alleen voor soorten die in de wereld staan; anders uitstellen tot er een besluit over volgers is.
- Drie aanzichten (voor/achter/opzij, elk 2 frames), 32×32, ±1,05× zo hoog als het icoon. Het icoon is de beste onderlaag voor "opzij" bij soorten die in de front al bijna van opzij staan (zoals de viscacha), omgezet naar HGSS-stijl (zwarte omlijning, eigen palet, puur profiel); "achter" haalt alleen kenmerken uit de rug; "voor" bestaat nergens anders (Gemini werkte niet bij de viscacha: werd Raichu/Pachirisu).
- Palet: front-palet donkerder/verzadigder als eigen `overworld_normal.pal`.

### Proef
Voorstel: eerst **viscacha** (heeft al frame 2, viervoeter) en **Gengas** (bol, test de uitzondering) een rug en een icoon geven. Daarna de werkwijze bijstellen en in `SPRITE_WERKWIJZE.md` zetten.

## 6. Open vragen voor Jordi
1. Volgers (Pokémon die achter je aan lopen): ooit aanzetten? Dan hebben alle ±445 soorten een overworldsprite in 3 aanzichten nodig; zo niet, alleen de paar die in de wereld staan.
2. Iconen: mag de pose vereenvoudigd/anders zijn dan de front (zoals bij Game Freak), of moet het icoon dezelfde pose houden?
3. Proef met viscacha en Gengas starten?

**Antwoorden Jordi (18 nov):**
1. "voorlopig nog niet, maar ik ga wel pokemon in de overworld plaatsen die diverse kanten op kunnen kijken." → volgers blijven uit; soorten die in de wereld geplaatst worden krijgen een overworldsprite met alle aanzichten (voor, achter, opzij).
2. "ja geen probleem, volg vooral game freak daarin" → het icoon mag een eigen, vereenvoudigde pose hebben, zoals bij Game Freak.
3. "kan je dat?" → iconen: ja, zelf (script-onderlaag + maker). Ruggen: Claude schrijft de Gemini-prompts (`viscacha/rug/PROMPT_RUG.md`, `gengas/rug/PROMPT_RUG.md`), Jordi plakt ze in Gemini en kiest.

## 7. Externe hulpmiddelen (18 nov)
Jordi: "Wat betreft de externe tools, alleen als ze gratis zijn wil ik dat doen".
- **PixelLab** (pixel-art-AI, 4/8 kijkrichtingen, draaien van een figuur, API/MCP): alleen een gratis proef met een beperkt aantal generaties (bronnen noemen ±40, daarna een paar per dag); verder betaald. Bruikbaar als gratis test voor de overworld van één soort, niet voor de hele dex.
- **Image-to-3D, gratis demo's op Hugging Face** (TRELLIS.2 van Microsoft, Hunyuan3D van Tencent, open gewichten): front → 3D-model → in Blender (gratis) renderen vanuit elk aanzicht als onderlaag. Gratis Spaces kunnen traag zijn of slapen. Een render blijft een onderlaag, nooit het eindresultaat.
- Lokaal draaien kan hier niet (geen GPU in de container).

## 8. Proef viscacha (18 nov)
**Rug: geslaagd** (`viscacha/rug/af/rug.png`; Jordi: "backsprites lukken iig, dat is geslaagd"). Werkwijze die werkte:
1. Gemini, nieuw gesprek, **alleen onze 8×-front als bijlage**; het standpunt in woorden ("seen from behind and slightly above on the left … head turned in profile over its shoulder … bottom cut off by a straight line"). Een echte rug als voorbeeld (Raticate) liep erin door (kleur, vacht, oren); bijsturen in hetzelfde gesprek tekende alles opnieuw als front.
2. Jordi kiest uit een paar pogingen (hier zijn eigen poging zonder Raticate).
3. Gemini tekende op een exact 16-px raster: kale 1-op-1-reductie naar 64×64 in het frontpalet.
4. Varianten voor de echte keuzes (A model / B kop +21% → "b lijkt opgeblazen"; vier ogen → oog 4), daarna alleen technische reparaties: oog uit de front, selout aan de lichtkant (keurder: zwart → index 2), schaduwsikkel. ±5 rondes, 2 keuringen.
**Icoon: moeizaam** (zie `viscacha/icoon/PROMPT_ICOON.md`): Gemini ontwerpt zelf (r1) of verkleint de front (r2 met voorbeeld); de verkleinde front + opschonen gaf de juiste pose maar was "plat van kleur", te groot en zonder perspectief.
**Overworld:** Gemini maakte een Raichu/Pachirisu; nog open.

## 9. Proef overworld viscacha (19 nov)
Meetstudie in `overworld/` (`ow_meet.py`, `ow_kleur.py`, `loop_vel.py`; handmeting onderdelen in `overworld/meting_onderdelen/RESULTAAT.md`). Correcties op §3: opzij is altijd een echt profiel; het overworldpalet is níet donkerder/verzadigder dan de front (hoofdvlak dL 0, dS 0), alleen eigen kleuren; omlijning onder zwart, boven een donkere vachttint; lopen = alleen voeten, geen op-en-neer (88%).
Twee routes naast elkaar: A Gemini (front + rug als bijlage, bouw in woorden) en B eigen methode (front/icoon/rug + rekenregels). Jordi: "dit is no contest" · "Gemini is echt zeer goed" · "en de eigen route echt heel matig". Werkwijze: `docs/lessen/OVERWORLD_WERKWIJZE.md`.

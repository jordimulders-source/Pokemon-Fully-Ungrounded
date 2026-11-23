# Pinsir-evolutie v2, frontsprite r1 (23 nov)

Model: `referenties/model_v2_r4.webp` (bevroren, Jordi: "probeer 1 maar"). Opnieuw bouwen vanuit `docs/concept/sprites/pinsir_evo/`:
`python3 sprite_v2/natief_meet.py && python3 sprite_v2/bouw.py`. Er is niets uit sprite_r1..r11 overgenomen.

## Werkwijze (geen tekenwerk)
1. **Natief raster**: pitch 10,24 px, fase 9,25 (zelfde Gemini-raster als het oude model). Per cel de mediaan van het midden (6×6), dus geen webp-ruis → `natief_ruw.png`. Per cel een klasse: zwart, bruin in 5 banden, room 2, rood 2, oog (alleen op de oogplek) → `natief.png` (schoon, in de modelkleuren). Figuur 91×78 cellen.
2. **Reductie** 91 → 64 kolommen (schaal 64/91, de breedte bepaalt het): elke spritepixel = 1, 2 of 4 hele modelcellen, nooit een gemiddelde kleur. Meerderheid wint (bij gelijke stand: de eerste cel = naaste buur). Figuur onderaan (y 9–63), x 0–63. Kale versie (alle modellijnen, modelkleuren) → `kaal.png`.
3. **Lijnen**: alleen de lange modellijnen uit de opdracht, als lijst met zaadcellen in `bouw.py` (`HOUD`): kopschildrand, schouderkoepel, buikrand, rechterarm/klauw + dijvoorkant (Z18), linkerarm/klauw, knieën (ook de kniecirkel), dij/staartgrens, staartsegmenten, voetklauwen, rug: lijn onder de rugstekels en achterste plaatrand. Van het rugkrasjesnet B19 alleen het langste doorlopende pad (de hoofdplaatlijn). Alle andere binnenlijnen (nekkrasjes, rugkrasjes, korte streepjes) vervallen; die cellen krijgen de modeltint van hun buren. Binnenlijnen in de donkere bruintint (L 35), niet zwart; gezicht houdt zijn zwarte modellijnen.
4. **Buitenlijn**: 1 px, kleur per pixel uit het model: zwart waar het model zwart is (248 px), donkerrood langs de buitenkant van de kaken (model heeft daar geen zwart maar `r`-cellen) en bruine lijntint op een paar plekken zonder zwart (samen 36 px).
5. **Kleur**: tinten gecentreerd op de modeltinten en naar buiten gespreid tot Gen 3-stappen (Pinsir 213/175/127/69, Tyranitar 221/192/143/71):
   bruin 35 / 74 / 107 / 147 / 190 (lijn, schaduw, midden, licht, hooglicht = buikschaduw), room 226, rood 38 / 70 / 115, oog (248,236,160), zwart. 12 kleuren incl. transparant (index 0).

## Pixels die niet 1-op-1 uit de reductie komen (zie `afwijkingen.txt`)
- **Rug (toegestaan door Jordi)**: rugzone = bruin achter de nek boven dij/staart, zonder arm en schouderkoepel. Vlakjes < 8 px opgeslokt (16 px), daarna elke plaat tussen de gehouden lijnen gevuld met 3 tinten via de eigen plaatvorm, licht linksboven en schaduw rechtsonder (169 px). Geen nieuwe lijnen of vormen; de rij rugstekels staat op de modelplekken (±6 stekels, x 41–56).
- **Opschonen**: tintvlakjes < 3 px (bruin < 5 px) nemen de buurtint van dezelfde kleurgroep (156 px); gezicht uitgezonderd. Daarna nog 15 px losse vlekjes (bruin buiten gezicht/stekels/buik, rood in de kaken).
- **Gezicht**: = model, niet opgeschoond. Ogen cel voor cel het model: linkeroog driehoek met verticale buitenkant, rechteroog gespiegeld met de zwarte pupilstreep en het smalle stukje oog ervoor (zoals het model); beide kijken dezelfde kant op, niet naar het midden. 4 px oogrand/pupil van lijntint naar zwart (model: zwart). Mond: verticale zwarte spleet met losse tanden links en rechts; 3 tandpixels van hooglicht naar room (model: roomkleurig).
- **Stekels**: flanken zoals het model (`-O#`: donker links, licht rechts; 1 px brede stekel = licht), 6 px. Stekelpunt 1 px: 5 px van een platte top `##` transparant gemaakt (silhouet verder gelijk aan de kale reductie; rugzone telt een stekelcel al bij ¼ dekking mee zodat de punten niet wegvallen).
- **Buiklijnen**: tan-op-room cellen in de buik tellen als lijn (anders wint de room en verdwijnen ze), kleur bruin licht (model L 127).

## Zelf gezien / zwakke punten
- Het onderlijf (dij, knie, staartbasis) blijft lijnrijker dan Tyranitar/Aggron: dat zijn de lange plaatlijnen van het model zelf.
- De rechterklauw (roomvingers x 35–36, y 42–44) ligt tegen de roomkleurige buik en leest op 1× zwak; in het model is hij ook maar ±1 px per vinger.
- De rugplaten zijn grote vlakken (licht linksboven, schaduw rechtsonder); het model heeft veel kleinere plaatjes. Zo gevraagd, maar Jordi ziet het verschil in `rug_8x.png`.
- Figuur gebruikt de volle 64 px breedte (kaakpunt x 0, staartpunt x 63).
- Geen verse keurder gebruikt (opdracht: maker; keuring door Claude/keurder hierna).

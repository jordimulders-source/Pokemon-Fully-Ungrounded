# Sapa Inca – ronde 11 (kleur naar latere generaties, gouden staf, kop/ogen groter)

Basis: `ronde10/sapa_inca.png`. `sapa_inca.txt` = dat volledige raster met het nieuwe palet en onderaan het blok "ronde 11", geschreven door `reparatie11.py`.
Bestanden:
- `sapa_inca.png/.txt`, `reparatie11.py`
- `bouw.py` (controle: K/d/p overal, de lichte selout l en de rode selout r alleen aan de lichtkant)
- `vel.py` → `vel.png` (4× en 1× licht/donker naast ronde 10; 4× naast Armarouge, Corviknight, Kilowattrel; kop 8× en staf 8× naast ronde 10)
- `kijk.py`

Jordi: "ik twijfel om de gloed van de staf, vergelijk die eens met ander sprite werk. 1. [kop/ogen groter] ja, zolang de verhoudingen goed blijven. 2. [klauwen] nee hoeft niet 3. [vleugelpunt] van een afstandje merk je dat bijna niet 4. [kroononderrand] merk je ook amper 5. [kleurbalans] is prima. Ik zou eerder nog net wat meer naar het kleurgebruik, de schaduw etc tov andere pokemon kijken. Vooral de latere generaties, omdat dit een wat complexer design is, wat je in latere gens wat meer ziet dan in gen 3".

## Studie (8×, normal.pal)
| Soort | Groep | Tinten (donker → licht) | Hoe de schaduw verschuift |
|---|---|---|---|
| Armarouge | goud | 106,63,3 → 198,120,27 → 241,163,41 → 254,250,98 (+ 255,252,199 glans) | schaduw naar oranje/bruin, licht naar bleekgeel; glans kort en klein |
| Aegislash | goud (metaal) | 72,56,48 → 144,128,80 → 176,160,88 → 232,224,128 | donkerste tint bruin; licht alleen in korte stukken aan de lichtkant |
| Kingambit | goud (kling) | 136,104,32 → 200,152,72 → 248,216,104 | lichte lijn langs één kant, niet in het midden |
| Corviknight | donker lijf | 24,16,56 → 40,40,88 → 64,64,112 → 96,104,168 | donker lijf met groot waardebereik; schaduw koel (blauwpaars), lichte veren als banden |
| Kilowattrel | donker + geel | 24,24,24 → 48,56,56 → 72,88,96; geel 120,92,32 → 192,144,40 → 248,204,48 | veren als heldere vlakken; geel met bruine schaduw |
| Decidueye / Delphox | warm | schaduw rood naar donkerrood/paarsbruin, licht warm crème | gekleurde lichte rand aan de lichtkant, zwart alleen aan de schaduwkant |

## Palet voor (ronde 10) en na (ronde 11)
| | ronde 10 | ronde 11 | waarom |
|---|---|---|---|
| K | 24,16,20 | 22,14,26 | iets paars |
| d | 52,38,36 | 46,30,50 | lijfschaduw koel paarsbruin (Psychic, echo van de kroonrand) |
| m | 88,66,58 | 98,66,64 | basis lijf |
| l | 136,104,86 | 172,120,98 | lichte selout warmer en lichter: groter waardebereik |
| r | 186,54,34 | 178,46,46 | roodschaduw iets koeler |
| R, o | 238,98,48 / 250,162,92 | gelijk | |
| p, v | 116,90,172 / 184,166,236 | 112,86,172 / 186,168,238 | nagenoeg gelijk |
| a | 172,104,34 | 206,110,30 | goudschaduw oranje (Armarouge) |
| g | 230,172,58 | 242,180,54 | goud basis |
| y | 250,226,132 | 254,240,156 | goud licht bleekgeel |
| b, w | 112,128,152 / 210,222,234 | 106,120,150 / 224,232,240 | snavel iets meer contrast |
| t | 162,82,42 | 128,62,44 | donker oker: schaduwkant van de staf en de vaan |

## Wat er veranderde
1. **Staf zonder gloed** (21 px): basis g, schaduwkant t (donker oker), omlijning links d en rechts K. De lichte tint y alleen in korte stukjes links (rij 30–31, 34, 38). Op de stafkop één glanspixel (w) linksboven in de ruit; de punt is g/a. Geen doorlopende lichtgele middenlijn meer. Vorm en roestbruine vaan (rij 26–28) gebleven.
2. **Kop en ogen groter** (50 px; silhouet +7): het rode masker is 1 kolom breder links (x21) en 1 rij langer (tot rij 27), dus de kop zonder kroon is ±13×10.
   - Ogen 2 rijen hoog: vlak donker lid (d), gouden iris hoog onder het lid, zwarte pupil.
   - Nabij oog: glans (w) aan de lichtkant links van de pupil. Verre oog: iris + pupil, zonder glans.
   - Snavel: bleke rug over 5 rijen schuin naar linksonder, donkere haakpunt op (23–24,27–28).
   - Oorschijf: 2×3 goud met een zwarte rand aan de schaduwkant.
   - De kroon is niet aangeraakt.
3. **Kleur en schaduw:**
   - **Palet:** zie de tabel hierboven.
   - **Lichte selout** (27 px): aan de lichtkant van lijf, hals, linkervleugel en opgeheven vleugel is de donkerbruine rand van ronde 10 weer een warme lichte selout (l). Zwart staat alleen aan de schaduwkant.
   - **Ongemoeid gebleven:** het kroonpatroon (v3) is per veer identiek; de kleurbalans, de pose, de vleugelpunt, de kroononderrand en de klauwen zijn niet aangeraakt.
- Totaal: 98 px veranderd + het palet. 0 open randen volgens de aangepaste regel (lichte selout aan de lichtkant toegestaan). 15 kleuren + transparant.

## Zelf gekeken (4× en 1× naast ronde 10 en naast Armarouge/Corviknight/Kilowattrel; kop en staf 8×)
- De staf leest nu als goud (zoals Aegislash/Kingambit) en niet meer als gloeiend. Het lijf heeft een lichtere, warme rand aan de lichtkant en een koelere paarsbruine schaduw. Het gezicht is groter: de ogen zijn gouden ogen met pupil, de snavel is langer.

## Eerlijk: wat nog niet klopt
- **Waardebereik lijf:** het donkere lijf heeft nog maar 3 tinten (d, m, l) plus zwart. Corviknight gebruikt er 4–5 met lichte veerbanden; bij ons is de verbetering vooral de rand en de koelere schaduw, en het binnenvlak blijft vrij vlak. Een vierde lijftint past niet zonder een andere kleur op te geven.
- **Veervormen:** die heb ik niet als aparte heldere vlakken uitgewerkt (Kilowattrel/Decidueye). De pennen van de vleugels hebben dezelfde opbouw als in ronde 10.
- **Snavel:** op 1× is het nog steeds vooral een bleke streep in het rode masker, al is hij langer en heeft hij een donkere punt.
- **Staf:** de schaduwkant t (donker roestbruin) leest op 8× als bruin-rood naast het goud. Dat is minder metaalachtig dan de bruine schaduw van Aegislash.
- **Rood iets koeler** (r): de kroon is daardoor aan de schaduwkant iets donkerder dan in ronde 10.

## Lessen
- Een "gloed" ontstaat als de lichtste tint een doorlopende middenlijn is; goud leest als metaal met licht in korte stukken aan één kant en een bruine schaduwkant.
- Bij een strenge open-randregel altijd een uitzondering maken voor de lichte gekleurde selout aan de lichtkant (Game Freak doet dat zo), anders wordt de sprite donker en vlak (ronde 10).

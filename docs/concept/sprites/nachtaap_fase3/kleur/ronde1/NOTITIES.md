# Nachtaap fase 3: kleurronde 1 (5 nov)

Bestanden: `nachtaap_fase3.png` (64×64, geïndexeerd, index 0 transparant), `normal.pal` (JASC), `raster.txt` (één teken per paletindex), `vel.png`.
Bron: `bron/delen.txt` (met de hand geschreven rijen `y x pixels`, absolute x, later overschrijft eerder) → `bron/bouw.py` (raster + png + pal, controleert tegen het silhouet) → `bron/check.py` (open randen, losse pixels, alpha-diff, telling) → `bron/vel.py`.

## Game Freak-studie (bovenste frame, 8×)
| Sprite | Tinten per groep | Omlijning | Licht | Gezicht / ogen / handen |
|---|---|---|---|---|
| Aipom (paarse aap) | paars 4 (d583ff, b462e6, 8b39b4, 52206a), crème 4, zwart | 52206a (donkerste paars) aan de lichtkant, zwart onder/rechts | linksboven, hooglicht als band over kop en armen | ogen: klein, wit + zwart, ingebed in crème gezichtsvlak; staarthand: 3 dikke vingers als bolletjes met omlijning ertussen |
| Primeape | vacht 4 (ffe6b4…7b5a29), bruin 4, zwart | zwart rondom, binnenrand vachttint; gekartelde schaduwgrens | linksboven | ogen: zwart streepje + wit; vuisten = bollen met 1 groefje |
| Medicham | rood 4, crème 4, zwart | gekleurd (7b524a) aan de lichte kant | linksboven, grote kernschaduw op de bollen | handen: gesloten, vingers alleen als 1-px groef |
| Alakazam | geel 4, bruin 4, 101010 | bijna-zwart rondom; geel krijgt binnenrand d5b400 | linksboven | handen open naar de kijker met lepel; vingers 2 px met donkere lijn ertussen |
| Slaking | bruin 5, wit 3, roze 3, **geen puur zwart** (100000) | donkerbruin aan de lichtkant | linksboven | gezicht donker met lichte snuit; kleine ogen in een donkere oogkas |
| Reuniclus / Duosion (gloed) | gel 3 groen: 306040 (omlijning), 408858 (band), 58b078 (vlak) + licht d0e8c0 | gel heeft **eigen donkere omlijning**, band vlak | glans alleen als enkele lichte vlekken | gel = vlakke band van 2–4 px met eigen omlijning; geen verloop |

Conclusies voor deze sprite: 4 vachttinten + omlijning (K) ; omlijningsbasis (D) aan de lichte kant (linksboven), K rechts/onder; gloed als vlakke band met eigen omlijning (Reuniclus), geen verloop; handen: vingers 2 px met een donkere lijn ertussen (Alakazam/Aipom).

## Palet (`normal.pal`)
| idx | teken | kleur | gebruik |
|---|---|---|---|
| 0 | `.` | 152 208 160 | transparant |
| 1 | K | 28 20 40 | omlijning (schaduwkant), mond, lid, gaten |
| 2 | D | 50 48 98 | vacht-omlijningsbasis (lichtkant), vingerlijnen, kreukels |
| 3 | S | 80 82 150 | vacht schaduw |
| 4 | V | 114 118 190 | vacht basis = model T2 #7276BE |
| 5 | L | 156 162 222 | vacht licht |
| 6 | F | 72 56 100 | gezicht (kale huid) |
| 7 | f | 44 34 64 | gezicht schaduw, wenkbrauwlijn, kin, oogkas, zool |
| 8 | P | 214 170 204 | snuit lila-roze |
| 9 | p | 166 122 166 | snuit schaduw, neusrug |
| 10 | B | 184 230 255 | lichtblauw licht (oog onder, gloedband lichtkant) |
| 11 | b | 104 176 236 | lichtblauw (iris, gloedband schaduwkant) |
| 12 | G | 40 98 176 | gloedomlijning |
| 13 | M | 228 221 240 | maanzilver (#E4DDF0): hand, maan, wiggen |
| 14 | m | 170 164 198 | maanzilver schaduw |
| 15 | W | 252 252 252 | wit: maankern, glans in de ogen |

Hergebruik: maanzilver (M/m) is één groep voor hand, maan en wiggen (Mama Killa-motief); de zool deelt `f` met het gezicht.

## Per onderdeel
- **Kop:** volgt het model: donker gezichtsschild (F/f) links in de kop (driekwart), vacht als lijst eromheen, breder aan de rechterkant; rechte wenkbrauwlijn (rij 35, `f`), daaronder per oog een K-lid; ogen 2×2 (glans W linksboven, iris b, lichte reflectie B tegenover de glans), oogkas `f` eromheen, verre oog iets anders gekleurd (geen kopie); neusrug `p` van tussen de ogen, snuit P/p breder naar onder met twee neusgaten (`f`) bovenaan, rechte mond (K, rij 44), lip, donkere kin. Geen oren.
- **Maan:** sikkel met de punten omlaag op de kruin, 10 px breed (x5–14) × 5 rijen, midden 3 px dik (W), hoorns M/m, linkerhoorn (nabije kant) langer dan de rechter; 1 rij vacht tussen maan en kopomtrek, geen glans erboven (L op rij 29 weggehaald). Groter dan in het model (model ±9×2 px op spritemaat).
- **Vuistarm:** vuist met drie knokkelgroeven (S/D), armrug licht (L), onderkant S/K; lijn K waar de arm achter de kop langs gaat.
- **Healerhand:** maanzilver, palm naar de kijker, 4 vingers van 2 px (M licht, m schaduw) met D-lijnen ertussen tot rij 53, middelvinger en ringvinger het hoogst, pink 1 px; duim linksonder met een schuine naad; pols in lichaamskleur rechtsonder ("randje van de pols mag de lichaamskleur").
- **Gloed:** vlakke band (B aan de lichtkant links/boven, b rechts/onder) met eigen omlijning G, volgt de vingertoppen; boven sluit hij aan op de K-omlijning van de kin.
- **Rugpatroon:** drie getrapte wiggen in maanzilver (M, schaduwrand m), **verplaatst van het achterwerk (model, x33–38) naar de rug** tussen kop en dij (x20–32, rij 34–41), elk vanaf de ruglijn schuin naar linksonder (loodrecht op de ruggengraat, mee met de 40°-pose), lengtes 4 / 7 / 6 rijen, 3 px breed bovenaan, één trede per 2 rijen.
- **Benen:** bovenste been = cilinder (L links, S rechts), voet als want (alleen buitenkant, vachtkleur, schuine teenkreukel rechts); onderste been: dij als grote bol met kreukel naar de romp, onderbeen met hooglichtband, voet met de donkere kale zool (`f`) rechtsonder zichtbaar.
- **Staart:** spiraal met één lijn (K) tussen de windingen: van de inkeping onderaan langs links omhoog, over de bovenkant, rechts omlaag en eindigend tegen het gat; gat met eigen rand (K boven/links, D rechts/onder, hoeken D).

## Controles (script `bron/check.py`)
- Alpha-diff met `silhouet/ronde1.txt`: **0** (1796 px). Geen afwijking nodig voor de maan of de gloed.
- Open randen (randpixel zonder K/D/G): **0**.
- Losse pixels: 28, allemaal bewust (ogen, glans, neusgaten, lip, knokkelgroeven, pinkje, pols, randhoeken).
- Zwart-aandeel van de omtrek 0,50 (Gen 3: 0,35–0,6).

## §0-checklist
1. 3/4 links-voor: kop driekwart (gezicht links), lijf 40° – ok (pose uit het model).
2. Alle ledematen geteld (2 armen, 2 benen, staart), verbonden – ok.
3. Geen rechte lijnen waar het rond is: wenkbrauwlijn bewust recht (Jordi); rechterkant gloed 8 px recht (het model ook) – zie zwak.
4. Ogen geïntegreerd (lid, iris donker boven/licht onder, glans) – ok.
5. Silhouet bevroren – ok.
6. Formaat 1796 px (eindvorm; Alakazam 1388, Slaking 2264) – ok.
7. Pose niet stijf – ok (model).

## Eerlijk: wat nog zwak is
- **Kop leest als helm/ruimtehelm** (ronde vachtring om een donker vizier + witte boog bovenop). Komt deels uit het model, maar de witte maan versterkt het: op 1× en 3× leest de maan eerder als glimlicht op een helm dan als maansikkel.
- **Healerhand leest als een ovenwant/handschoen**: vier rechte vingers van gelijke vorm met rechte lijnen ertussen, geen ronde toppen; de vingers lezen op 3×, op 1× is het een lichte vlek met streepjes. Palm vrij vlak.
- **Spiraal leest als lus met een vierkant gat** (gat 3×4 uit het bevroren silhouet); op 1× wel een krul, maar niet zo vloeiend als het model.
- **Lijf is vlak** vergeleken met Primeape/Slaking: grote vlakken V zonder kernschaduw; de dij en romp missen volume.
- **Wiggen** lezen op 1× als drie lichte schuine strepen op schouder/rug (klauwkrassen?); de trede is op 1× niet te zien. Plek: ik heb de rug geïnterpreteerd als het vlak tussen kop en dij; of dat voor Jordi "de rug" is, moet blijken.
- Gezicht: ogen + snuit lezen, maar het geheel is minder expressief dan het model; de kin onder de mond is erg donker.

## Lessen
- Een 64-px-raster als zone-kaart uit de onderlaag halen (gemiddelde kleur per pixel, ingedeeld in licht/basis/schaduw/gezicht/snuit/gloed) en dan per rij met de hand schrijven ging snel; de builder die elke rij tegen het silhouet toetst ving de enige fout (staart 1 px verschoven) direct.
- Een maan van gelijke dikte die de kopomtrek volgt leest als glimlicht; een sikkel heeft een dik midden (3 px) en spitse hoorns nodig, en geen lichte vacht erboven.
- Een palmhand in een gloed heeft aan de silhouetrand 3 px nodig (G + band + handomlijning); waar dat er niet is, de band één rij overslaan in plaats van de hand smaller te maken.

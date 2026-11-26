# Regionale Poliwhirl: eindkeuring + eindronde (25 nov)

Invoer: `../sprite_r6/poliwhirl_regional_r6_B.png` (Jordi: "B correct"). Uit: `poliwhirl_regional_ek.png` (+ `_8x`), `vel.png` (ek | r6_B | model op 8×, 1× licht/donker, 4× naast de regionale Poliwag, Poliwhirl/Poliwrath `_gba` en de vier maatstaf-sprites).
Opdracht (Jordi, 24 nov): eindkeuring = schaduw + belijning + kleurtinten, met een verplichte omlijningsronde volgens Dragonfly Cave. Er is niets getekend: alleen lijnpixels → outline base van het eigen materiaal, en geel 6 → geel 7 binnen de schaduwzone van het model.

Scripts: `meet.py` (modelhelderheid geel per spritepixel → `ylum.npy`), `zones.py` (bevroren zones), `lijn.py` (normaal + eigen materiaal per buitenlijnpixel), `maak.py` (lijnronde + schaduw, varianten V1–V3, eindversie), `controle.py` → `controle.txt`, `vel.py`.

## Gidsregels die ik toepas (Dragonfly Cave, letterlijk)
- r. 89–91: "The "outline shadows" are always black (or ever-so-slightly off-black) on Pokémon sprites".
- r. 106–109 (regel 3): "The outline base and outline highlight colors are also colors. When you're recoloring, you must also recolor the outlines."
- r. 111–116 (regel 4): "The outlines must be reasonably dark. [...] you should either stick with the outline base color in all but the very lightest areas or create a separate outline highlight color that's darker than the shadow color."
- r. 96–99 (regel 1): "the relative luminosity of the shades on the original sprite should always be maintained on the new one."
- r. 425–428: "we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."
- r. 431–434: "lighter pixels on the inside of the outline are a far better idea and can make the sprite look smoother against dark backgrounds".
- r. 440–446: "the R/S one seems overall lighter. [...] The R/S Scyther, on the other hand, has a whole lot of the highlighting color all over the place."
- r. 450–453: "Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts [...] place pixels of the outline highlight color on the inside of the outline rather than the outside."

## 1. Belijning
**Vóór (r6_B): BIJNA.** Het geel had overal een zwarte buitenlijn (geel 7, de outline base van het geel, kwam alleen voor in de neusgaten en de tenen), dus ook aan de lichtkant: "very 2D and cartoony" (gids r. 422). IJs was al goed (b links/boven, f/zwart rechts/onder), behalve de linkerkant van de rechterhandschoen (zwart aan de lichtkant). Zwart patroon: lijn 1 rondom, zoals de regionale Poliwag (outline base van een bijna zwart materiaal = zwart). Binnenlijnen: geen zwarte binnenlijnen buiten de pupillen (bevroren) en de okselkier (22,30).
**Ronde (`lijn.py`):** per buitenlijnpixel (zwart, grenst aan lucht) het eigen materiaal (meerderheid van de buren) en de normaal naar de lucht; lichtkant = normaal met nx+ny < 0 (licht linksboven). Lichtkant → outline base van het eigen materiaal: geel → 7, ijs → b. Schaduwkant en diagonale twijfelgevallen blijven zwart. Eén handmatige pixel: (20,48) → 7, de holle knie links van het linkerbeen (de normaalregel gaf zwart tussen twee 7-pixels = zwart/donkergeel om en om; regel uit Gnomad r10).
- Geel 1 → 7: 27 px: kopkruin (27,14); bovenkant linkerarm (15,30), (14,31); linkerrand buik (22,31), (22,36); linkerkant linkerbeen (20,44)–(20,51) incl. knie (20,48); bovenkant linkervoet (16..19,52), (15,53), (15,54); rechterbeen/-voet (40,48), (41,53), (40,54), (40,55), (41,56), (41,57), (47,54), (48,54).
- IJs 1 → b: 5 px: linkerkant rechterhandschoen (47,34), (47,35), (46,40), (46,41) en linkerkant linkerhandschoen (7,40); kristallen al goed.
- 1 px breed gebleven, geen nieuwe clusters, geen lichte kleur buiten de lijn.
- Zwart (index 1): 185 → 153 px = 12,2 % van 1250 (maatstaf: Dundragoon 13,7 %, Skinguin 14,3 %, Princadee 13,8 %, Zapacha 17,5 %).
- Outline highlights (r. 450–453): niet apart gezet; het geel heeft al veel 5 direct binnen de lijn (kop, armen, dijen), en volgens regel 4 blijft een licht materiaal bij zijn outline base.
**Na: PASS.**

## 2. Schaduw
**Vóór: FAIL (vlak, "2 kleuren effen").** Geel = 5 (150 px, 38 %) + 6 (239 px, 60 %) + 7 (7 px, alleen neusgaten/tenen): geen schaduwtint, het zwarte patroon deed al het volume.
**Meting model (`meet.py`):** het Gemini-geel heeft twee niveaus: licht ±207–219 (kruin, bovenbuik, dijen) en schaduw ±176–186 (onderkop, rechterhelft lijf, onderbenen, voeten); r6 had dat al als 5 / 6. Een derde, donkerder niveau bestaat in het model niet (alleen losse randpixels < 176).
**Varianten (`maak.py`):**
- V1: 7 alleen op modelpixels < 176 → losse vlekjes, geen sikkel. Afgewezen.
- V2: modelschaduw volledig → 7 (zoals de Poliwag-kop) → onderkop en onderbenen olijfgroen en modderig, een rechte band onder de mond, veel donkerder dan de maatstaf ("R/S ... overall lighter", r. 440). Afgewezen.
- **V3 (gekozen):** 5/6 blijven zoals het model ze geeft; alleen binnen de schaduwzone van het model (< 196) wordt de gele pixel 7 als zijn rechterbuur zwart of donker patroon is, of als er zwarte buitenlijn onder/rechtsonder ligt. Dat geeft een 1–2 px sikkel die de vorm volgt (rechterkant van de kop langs het patroon, rechterflank van de buik, onderkant armen, rechterkant benen, onderkant voeten). Een kleurgrens onder de mond (geel boven zwart patroon) telt niet als vormschaduw: daar zou het een rechte band worden.
- Geel 6 → 7: 45 px. Geel nu 5: 150 / 6: 194 / 7: 78 (+27 lijn) ≈ 36 / 46 / 18 %.
- Kleine 7-stukjes zijn diagonale ketens (sikkel van 1 px, zoals Gen 3) of lijnpixels; geen losse tintvlakjes midden in een vlak.
- Rest: de rechterflank van de buik (x 38, r 30–37) is een 1 px rechte 7-strook, omdat de grens met het (bevroren) zwarte patroon daar recht is.
**Na: PASS** (volume leest op 1× en 4× naast Poliwag en de maatstaf; licht linksboven consistent).

## 3. Kleurtinten
Palet ongewijzigd = palet van de regionale Poliwag (Jordi: kleur voor de hele lijn gelijk). Helderheid (0,299/0,587/0,114):
- Geel 229 / 194 / 132 (stappen 35, 62; maatstaf Dundragoon-geel 238/218/178/109, Skinguin 204/181/154/71): de onderste stap is groot, maar dezelfde als bij de Poliwag en de 7 werkt ook als outline base (regel 4: "reasonably dark"). Hue shift naar olijf in de schaduw: ok.
- IJs 245 / 217 / 179 / 125 (b) / 80 (f): ok, outline base b, schaduwlijn f zoals de Poliwag-kristallen.
- Rood 153 / 106 / 68, zwart patroon 16 / 41 / 59 / 90: ok.
- Regel 1 (relatieve helderheid behouden): ja. Regel 2 (één hue per materiaal): ja.
**Vóór: PASS, na: PASS** (geen tint aangepast; alleen de verdeling van 6/7 veranderde).

## Bevroren zones: diffbewijs (`controle.txt`)
- Silhouet/alpha-diff: **0**.
- Bevroren masker (`zones.py`, 339 px): beide oogzones incl. omlijning (x 19–26 en 32–40, r 12–20), neusgaten, al het rood (mond, spiraal, kristalkernen) en de hele spiraal-bbox incl. het geel ertussen: **0 px anders**.
- Linkeroog los gecontroleerd: (20,15)=1, (20,16)=8, (20,17)=8, (20,18)=1, gelijk aan r6_B ("B correct").
- Materiaalvormen (kristallen, handschoenen, mond, voeten, geel/zwart-patroon): **0** materiaalwissels; alleen zwart → outline base van het eigen materiaal en geel 6 → geel 7.
- Totaal gewijzigd: **77 px** (kop r12–29: 11, romp/armen r30–42: 27, benen/voeten r43–58: 39); 1→7: 27, 1→b: 5, 6→7: 45.
- Kleuren: 16/16 incl. transparant, palet byte-gelijk aan r6_B.

## Checklist E (FAKEMON_CHECKLIST)
E1 verre kant donkerder: rechterbeen/rechterarm grotendeels in zwart patroon, ok. E2 overlap met omlijning: n.v.t. (geen nieuwe overlappen). E3 donker aandeel 12,2 % zwart (+ zwart patroon als materiaal, zoals de Poliwag): binnen de band.

## Ter info voor Jordi (niet uitgevoerd)
- De buik binnen de spiraal is licht geel 5 met rood (bevroren); daardoor heeft de buik zelf geen sikkel in het midden, alleen rechts tegen het patroon.
- Het zwarte patroon is vrijwel effen 2 met wat 3/4; meer volume daarin (tint 3/4 op de bollingen) kan, maar dan per vlak naar het model; niet gedaan omdat het patroon bevroren is en het model daar effen zwart is.
- Kristal-schaduwlijn is f (donker ijsblauw) i.p.v. zwart, gelijk aan de goedgekeurde Poliwag; bewust zo gelaten (consistentie met de lijn).

# Onweerswolk-Altaria frontsprite, ronde 8 (nieuw opgebouwd vanaf het model)

Jordi (21 nov, over r4–r7): "ik vind de wolken nog niet zo'n issue. Alleen beetje te weinig static toch wel. het zit vooral in kleurgebruik/schaduw/tinten waardoor de wolken wat minder duidelijk zijn, de hoeveelheid is het issue niet De voelsprieten mogen ook wat meer definitie en kleur in en het hofod is nog wat blurry ook wederom, werk maar door. Houd zoveel mogelijk het model aan voor de wolken, al mag er wat extra static bij, maar kijk voor inpsiratie ook naar het model, niks zelf tekenen".

Bouwen vanuit `altaria/`: `python3 sprite_r8/bouw.py && python3 sprite_r8/vel.py && python3 sprite_r8/controle.py`.
Bestanden: `altaria_r8.png` (64×64, geïndexeerd, index 0 transparant, 14 kleuren incl. transparant), `altaria_r8_8x.png` (wit), `vel.png` (r8 | r5-proef | model op 8×; kop+kuif en een stuk wolk op 16× naast het model; 1× op wit/crème/grijsblauw/zwart + model en r5-proef op 1×), `bouw.py`, `controle.py`, hulpjes `raster.py` (model met blokraster = spritepixels), `zoom.py`, `naast.py`, `vel.py`.

## Oorzaak van de onduidelijke wolken in r4–r7 (gemeten)
Het model heeft vier wolktonen (L46 / 75 / 124 / 185) + zwarte lijnen. r5 gebruikte L54 / 73 / **95** / 122 / 177: de meeste wolkpixels (498) stonden in L95, een tussentint die in het model niet voorkomt. Daardoor waren licht en schaduw vlak en modderig. r8 gebruikt de modeltonen zelf en laat per spritepixel de modelband met de meeste stemmen winnen (geen gemiddelde).

## Palet (14 incl. transparant; wolk- en violettinten = mediaan van de modelpixels per band)
| index | kleur | L | herkomst |
|---|---|---|---|
| 0 | transparant | | |
| 1 | (7,12,30) | 12 | model-zwart; alleen de 5 pupilpixels |
| 2 | (20,36,64) | 34 | wolk-selout: donkere navy (buitenlijn, lijnen tussen de bollen, snavelrand); niet zwart |
| 3 | (29,50,81) | 46 | model wolk navy (L<60) |
| 4 | (50,82,116) | 75 | model wolk donker teal (L60–100) |
| 5 | (87,137,171) | 124 | model wolk teal (L100–155) |
| 6 | (144,205,223) | 185 | model wolk licht cyaan kap (L≥155) |
| 7 | (188,224,238) | 215 | model-static (cyaanwit) |
| 8 | (36,34,92) | 39 | violet-selout (donker violet, niet zwart) |
| 9 | (54,58,124) | 63 | model violet donker (L<85) |
| 10 | (94,98,210) | 107 | model violet midden (L85–130) |
| 11 | (128,132,236) | 143 | model violet licht (L130–160) |
| 12 | (160,166,239) | 172 | model violet hooglicht (L160–195: koplicht linksboven) |
| 13 | (202,208,249) | 207 | model lavendelwit (L≥195: kuifglanzen, oogglans) |
Stappen wolk: 34 → 46 → 75 → 124 → 185 (+ static 215); kop: 39 → 107 → 143 → 172 (+ glans 207).

## Kale reductie (stap 1)
Silhouet = r5-proef (alpha-diff 0). Per spritepixel stemmen de 9 natieve pixels van het 3×3-blok op hun modelband (wolk of violet volgens het materiaal van de proef); een zwarte modelpixel telt 1,5 (lijnen zijn 1 natieve px). Dunne modelvormen: navy + lijn wint al bij ≥4/9 als dat meer is dan teal + cyaan (navy rand onder een bol), cyaan bij ≥4/9 als dat meer is dan navy + lijn (kleine kap). Dat is `kaal` in `bouw.py`.

## Afwijkingen van de kale reductie: 480 px, per zone
- **Buitenrand wolk/hals: 102 van 169**: buitenlijn → wolk-selout 2 (wolk) of violet-selout 8 (hals/kop). De static-boogjes buiten de linkervleugel uit r5 (6 px, x4–5) blijven static.
- **Static: 105 px** (r5: 69). Alle op de modelplekken: blok met ≥2 static-modelpixels (`statisch()` uit `gereedschap/klassen.py`: de cyaanwitte kern + de dunne lichte knetterlijntjes), plus blokken met 1 die aan zo'n blok grenzen (modellijntjes lopen schuin door de blokken); uitgedund tot 1 px (Zhang-Suen), L-hoekjes weg, stukjes < 3 px weg. Niet op de buitenrand, niet in de kop. Niets bijgetekend: de "extra" static t.o.v. r4–r7 zijn de kortere modelstukjes die toen bij ≥10 px wegvielen.
- **Wolk binnen: 171 van 1346**:
  - lijnen (40): blok met ≥2 zwarte modelpixels, als samenhangend stuk ≥3 px, gedund tot 1 px → wolk-selout 2 (de modellijnen tussen de bollen, gekleurd, niet zwart); selout-meerderheidspixels die niet op zo'n lijn liggen → wolkband van hun blok.
  - ontkorrelen (129): tintvlakjes < 3 px (cyaan en selout < 2) → meest voorkomende wolkbuur; 1-px-uitsteeksels (3 van 4 buren één andere vultint) → die tint. Alleen naar een tint die er al naast ligt.
- **Kuif: 63 van 172** (silhouet gelijk): onderkant van een streng (lucht eronder) → violet-selout 8 (de donkere violetrand van het model); bovenkant/twijg → lichtste modelband met ≥2 stemmen, aan de buitenrand begrensd op violet licht 11 (geen lichte buitenrand); binnenin een streng de lichtste band met ≥3 stemmen: zo staan de lavendelwitte en hooglicht-glanzen van het model op hun plek (o.a. (29–35,8–10) en (35–38,14–15)). Per soort: m→l 14, m→selout 11, selout→v 10, w→l 7 (rand), h→l 3, l→h 2, l→w 2, m→w 1, v→w 1, overige 12.
- **Kop: 39 van 145** (`KOPGRID`, X19–33, Y18–28; gelezen uit `raster.py` = het model met blokraster):
  - kop 3 tinten + selout: hooglicht 12 linksboven (Y18–20, X22–25, model L172), licht 11 midden, midden 10 rechts (model L118), violet-selout 8 rechts en links (model-zwart → gekleurd). Afwijkend: (27,18) m→l, (30,18) selout→m, (21,21) l→m (lichtkant-selout), (32,20) (33,22–25) m→selout (rechterrand, model K op X33–34), (20,22) m→selout, (21,22) (21,23) → m (lijn | kopkleur | oog), (30,24) l→m.
  - ogen uit r5: ver oog (22,22–23), nabij oog (28,22) (27–28,23) + glans (27,22) in lavendelwit 13 (r5: wit). Ver oog 1 px rechts van het model, zoals in r3–r5.
  - snavel in de wolktinten van het model: bovenrand (23–25,24) selout (model: zwarte rand), (21–22,24) licht violet (model: kop), Y25 cyaan met teal (24,25), Y26 teal/cyaan met mondlijn navy (24–26,26) (model navy), onderkaak (22–23,27) cyaan en (24–25,27) teal, rand (19,26) (20–21,27) (22–23,28) (26,27) selout.
  - wang (29–31,25) cyaan, (28,26) cyaan, (29–31,26) teal, onderrand (28–30,27) selout (model K); (28,25) (27,27) (31–32,27) (26–27,28) violet midden (model: violet tussen snavel en wang / hals); (27,26) selout (model K tussen snavel en wang).

## Controle (`controle.py`)
14 kleuren incl. transparant; alpha-diff met de r5-proef 0; zwart alleen de 5 pupilpixels; lichte pixels (L≥150) op de buitenrand: alleen de 6 static-boogjes links (static, zoals r5). Pixels zonder 8-buur van dezelfde tint: 36, waarvan 30 kuiftwijgjes/-glanzen en oogglans, de rest snavelrand en halsrand. Aandeel wolk: selout 236, navy ±360, donker teal ±490, teal ±225, cyaan ±160 (model /9: K 153, 440, 551, 258, 193).

## Eerlijke twijfels
- De bollen lezen nu door licht/schaduw (cyaan kap linksboven, navy onder) en enkele modellijnen; ze zijn op 1/3 hoekiger dan de zachte modelbollen. Meer modellijnen kwamen niet boven de drempel (het model scheidt veel bollen met 1 natieve px zwart); die heb ik niet bijgetekend.
- Static is duidelijk aanwezig (105 px, 1 px dik); de lange lijn langs de rechtervleugelrand en de Z-vorm rechts in het lijf (X40–46, Y44–48) zijn modelplekken maar vallen op.
- Kuif: de rechterhelft van de bovenste streng (X33–41, Y10–12) is donker, zoals in het model; de glanzen zitten vooral in de linkerhelft en de onderste streng.

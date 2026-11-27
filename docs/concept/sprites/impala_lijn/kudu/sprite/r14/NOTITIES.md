# Kudu r14: eindkeuring DC (alleen uitvoering)
Uitgangspunt: `r13/kudu_r13.png` (Jordi 27 nov: "linkerstuk van r10 b6a en rechterstuk van r12 van de maan ... en dan naar eindkeuring").
Script: `sprite/r14.py` (elke pixel met reden in `pixels.txt`), controle `sprite/r14_check.py` (`telling.txt`), vel `sprite/vel14.py` (`vel.png`).
Lever: `kudu_r14.png` (P-modus, index 0 = transparant, 14 kleuren + transparant), `kudu_r14_8x.png`, `normal.pal`.

Naast elkaar bekeken: impala (`impala/af/`), skinguin, dundragoon, viscacha, awki, en Gen 3 `anim_front_gba` van stantler (zelfde goudvacht) en arcanine (manen over lijf).

## Gidsregels (letterlijk, `dragonflycave_spriting_guide.txt`)
- r. 96–97: "The "outline shadows" are always black (or ever-so-slightly off-black) on Pokémon sprites".
- r. 112–113: "The outline base and outline highlight colors are also colors. When you're recoloring, you must also recolor the outlines."
- r. 117–119: "The outlines must be reasonably dark. If you're recoloring a sprite in a relatively light color, be careful to make the outline base color sufficiently dark to make the outlines clear."
- r. 106–107: "the relative luminosity of the shades on the original sprite should always be maintained".
- r. 419–422: "With the outlining all-black, it looks very 2D and cartoony ... we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."
- r. 427–428: "lighter pixels on the inside of the outline are a far better idea" / r. 452–453: "Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts".

## 1. Belijning (het hoofdpunt)
r13 had een vrijwel overal zwarte lijn (301 px `#302418`), terwijl de impala en de maatstaf-sprites een gekleurde lijn aan de lichtkant hebben ("looks very 2D and cartoony").
- **Buitenlijn lichtkant -> lijnbasis.** Per lijnpixel de normaal naar buiten gemeten; links/boven (35°–215°) krijgt de lijnbasis van het eigen onderdeel, rechts/onder blijft zwart (outline shadow). Een pixel waarvan beide buren op de rand de andere klasse hebben volgt de buren (geen zwart/donker om en om).
  - goud (vacht én manen): `K` = **#6E4614** (warm donkerbruin, lum 76; zelfde rol en helderheid als Stantlers lijnbasis `#7B4100`, lum 75). Eerst `d` (manen-donker) geprobeerd voor de manen: te licht als lijn (stap 45 op `m`), manen vloeiden weg in hals en lijf; daarom één lijnbasis voor al het goud, zoals Stantler.
  - staal: `A` (#4A4A52), bestond al aan de linkerkant van de hoorns; nu ook de hoorntoppen en de lichtkant van de linkerhoorn (x11–13 y4–6).
- **Binnenlijnen niet zwart:** franje/manen over hals, borst en lijf (x18 y29–37, onderrand manen y38–41, achterrand x32 y30–41) -> `K`; hoorn over kop/oor (onderlijn rechterhoorn y15 x24–26, hoornvoeten (15,16–17), (20–21,19)) -> `A`; oortop rechts onder de hoorn (y16 x24–29, lag dubbel zwart met de hoornonderlijn) -> `K`, dus nu 1 px staal + 1 px oorrand i.p.v. 2 px zwart.
- **Schoft x34–39 y29–31** (overgang manen -> rug, uit r12): het mengsel 0/D/d is één vachtlijn `K` geworden met de oorspronkelijke D-plukjes ertussen; manenpunt (35,29) `K`.
- **Open randen dicht (2 px):** (10,25) snuitrug en (22,18) kop tussen hoorn en oor stonden als M op de buitenrand -> `K`.
- **Bewust gelaten:** de D-lijnstukken van r13 op de rugtop (y31 x40–46), het linkeroor en de nabije achterpoot (outline highlights op de meest belichte plekken, zoals Stantler zijn `4`); zwart onder buik, kin, hoeven, rechts van poten, romp en hoorns; neus/mond (x8–12 y25–29) en oog: niet aangeraakt.
- Resultaat: zwart 301 -> 169 px; aandeel zeer donker (0+K) 0,231 -> 0,224 (E3-band 0,10–0,25).

## 2. Schaduw
Getoetst tegen de toonkaart van `model_A3.png` (cellen 16 px, x-offset 6): lijf licht op de rugtop (L x40–50 y32–35), donker achter de manen (slagschaduw D x33–35), buik + verre achterpoot D, sikkel D op de romp rechts (x51–53 y38–42); borst L op de lichtkant; manen l linksboven -> m-sikkel rechtsonder; hoorns W-slijprand + 4/3 + A. Dat volgt het model en de Gen 3-opbouw (licht linksboven, sikkel rechtsonder, geen pillow shading). **Niets veranderd** aan de schaduwvlakken: elke ingreep zou verzonnen schaduw zijn (kernles "schaduw uit de modelhelderheid").
- Ter info: de bovenrand van de buikschaduw (y44 x35–44) is 10 px recht. Het model heeft daar ook een band (m bij y43–45); de witte strepen eindigen erin (x37, x40, x44), dus hij leest niet als losse band. Niet aangepast.

## 3. Kleurtinten
| groep | tinten (lum) | stappen | hue |
|---|---|---|---|
| vacht | L F8D888 (216) · M D8A850 (172) · D **A87432** (124) + lijn K 6E4614 (76) | 44 · 48 | 43° -> 39° -> 34° -> 33° (naar rood in de schaduw) |
| manen | l D8AC30 (171) · m B08824 (137) · d 7C5A10 (92) + lijn K | 34 · 45 | 44° -> 43° -> 41° |
| staal | W FFFFFF · 4 C8C8CC (200) · 3 8A8A92 (139) + lijn A 4A4A52 (75) | koel blauwgrijs, duidelijk anders dan het goud, witte slijprand | |
| oor | R E0A090 (177) · r B06A58 (125) | 52 | |
- **D: A07030 -> A87432** (lum 119 -> 124): stap M->D was 53, nu 48 (= Stantler 3->4, 49). Zelfde rol, alle D-pixels blijven D.
- **K: 5C4434 -> 6E4614**: was grijsbruin, nu warm donkerbruin (lijnbasis van het goud). K is ook de donkere rand van oog K4 (Bidoof-bron (64,48,16), dus nu dichter bij de bron) en de hoeven/neus; alleen de tint wisselt, posities 0 px anders.
- Goud warm en mat: M heeft middelmatige verzadiging; manen-goud is verzadigder en lijkt daardoor op mosterd/oker, apart van de vacht (Jordi's keuze, niet aangeraakt).

## Bevroren zones: diff-bewijs (`telling.txt`)
- silhouet (alpha): **0 px**
- oogvlak K4 x15–19 y21–24 (letters): **0 px** (alleen de K-tint, zie boven)
- W-pixels (strepen, slijprand, snuit): **0 px**; hoornvulling 3/4/W: **0 px**
- vulpixels die van letter veranderen: **2** (de twee open randen M -> K); verder alleen lijnpixels 0 -> K (120) en 0 -> A (12). Manenomtrek, halsstrook (x19–20), hoornvorm en strepen zijn dus positioneel ongewijzigd.
- per zone: hoorns 7 · kop/oren 11 · manen+franje+halsstrook 56 · lijf/staart 9 · poten 41 · hoornvoet/oortop rechts 10 = 134 px.

## FAKEMON_CHECKLIST E (alleen uitvoering)
E1 ok (verre poten D, verre oor in schaduw) · E2 ok (overlaplijnen nu in lijnbasis K/A, niet zwart) · E3 ok (0,224).

## Ter info voor Jordi (niet uitgevoerd)
- De hals tussen franje en manen wordt nu door bruine i.p.v. zwarte lijnen begrensd; hij blijft zichtbaar (stap 96 op M), maar iets minder hard dan in r13. Zo doen Stantler en Arcanine het ook.
- Oortop rechts + hoornonderlijn blijven 2 px donker (staal + bruin) omdat de vormen bevroren zijn.
- Palet: 14 kleuren + transparant, 1 plek vrij (index 15).

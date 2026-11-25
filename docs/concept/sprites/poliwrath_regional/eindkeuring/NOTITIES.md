# Regionale Poliwrath: eindkeuring + eindronde (25 nov)

Invoer: `../sprite_r2/poliwrath_regional_r2_E2M1.png` (Jordi: "linksonder heeft alles het beste"; spiraal = modelspiraal, "fantastico"). Uit: `poliwrath_regional_ek.png` (+ `_8x`), `vel.png` (ek | r2_E2M1 | model op spritemaat op 8×, 1× licht/donker, 4× naast de regionale Poliwhirl, Poliwrath `_gba` en de vier maatstaf-sprites).
Opdracht (Jordi, 24 nov): eindkeuring = schaduw + belijning + kleurtinten, met verplichte omlijningsronde volgens Dragonfly Cave. Alleen uitvoering: er is niets getekend. Alleen lijnpixels → outline base van het eigen materiaal, en geel een tint donkerder als sikkel aan de schaduwkant.
Aanpak = die van de regionale Poliwhirl (`../../poliwhirl_regional/eindkeuring/`).

Scripts: `meet.py` (modelhelderheid per spritepixel uit het gespiegelde, geschrapte model `../sprite_r1/geschrapt.npz`, dat in de sprite op x+1, y+2 staat; silhouetdiff 14 px = alleen de oogbulten → `mlum.npy`), `zones.py` (bevroren zones), `lijn.py` (normaal + eigen materiaal per buitenlijnpixel; = Poliwhirl-script), `maak.py` (lijnronde, sikkel, opschonen, eindversie; log in `maak_log.txt`), `controle.py` → `controle.txt`, `vel.py`.

## Gidsregels die ik toepas (Dragonfly Cave, `docs/lessen/bronnen/dragonflycave_spriting_guide.txt`, letterlijk)
- r. 96–98: "The "outline shadows" are always black (or ever-so-slightly off-black) on Pokémon sprites".
- r. 102–107 (regel 1): "Do not recolor two different shades with the same shade [...] the relative luminosity of the shades on the original sprite should always be maintained on the new one."
- r. 109–110 (regel 2): "There is a reason all the shades on the main body are green, too. Don't make the highlights blue and the base color red".
- r. 112–115 (regel 3): "The outline base and outline highlight colors are also colors. When you're recoloring, you must also recolor the outlines."
- r. 117–123 (regel 4): "The outlines must be reasonably dark. [...] you should either stick with the outline base color in all but the very lightest areas or create a separate outline highlight color that's darker than the shadow color."
- r. 373–377: "don't stick to the possible manual anti-aliasing on the outside edges of the outline [...] this results in very visible, horrendously ugly colored "dots" around the outline."
- r. 419–423: "With the outlining all-black, it looks very 2D and cartoony [...] we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."
- r. 427–433: "lighter pixels on the inside of the outline are a far better idea and can make the sprite look smoother against dark backgrounds".
- r. 444–450: "the R/S one seems overall lighter. [...] The R/S Scyther, on the other hand, has a whole lot of the highlighting color all over the place."
- r. 452–455: "Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts [...] place pixels of the outline highlight color on the inside of the outline rather than the outside."

## 1. Belijning
**Vóór (r2_E2M1): BIJNA.** Het geel had aan de lichtkant op de meeste plekken zwart (linkerrand buik, bovenrand linkerdij, rechterknie): "very 2D and cartoony" (r. 419). De linkerhandschoen had aan de bovenkant/linkerkant zwart (lichtkant) terwijl de rest b was; het schouderkristal links ook. IJskristallen al goed (b lichtkant, f schaduwkant). Donker lijf: lijn 1 rondom, zoals de regionale Poliwag/Poliwhirl (outline base van een bijna zwart materiaal = zwart). Geen zwarte binnenlijnen buiten de ogen (bevroren; ook de onderrand van beide ogen, rij 12–13).
**Ronde (`lijn.py`, `maak.py stap_lijn`):** per buitenlijnpixel (zwart, grenst aan lucht) het eigen materiaal (meerderheid van de buren) en de normaal naar de lucht; lichtkant = nx+ny < 0 (licht linksboven). Lichtkant → outline base van het eigen materiaal: geel → 7, ijs → b; donker lijf blijft 1; diagonale twijfelgevallen blijven zwart.
Uitzondering volgens regel 4 ("reasonably dark", r. 117): is het eigen vlak naast de lijn al de donkerste tint (geel 7 / ijs b), dan valt een outline base weg in het vlak → zwart. Daarna om-en-om opgelost (SPRITE_KERN: nooit zwart en outline base om en om op één rand):
- Geel 1 → 7 (8 px): kleine gele schouder links (11,21); linkerrand buik (20,26), (20,27), (21,28); bovenrand linkerdij (21,40), (19,41), (18,42); rechterknie (44,47).
- IJs 1 → b (7 px): schouderkristal (9,21); linkerhandschoen boven/links (3,24), (2,25), (1,26), (1,27), (1,33), (2,34).
- Bewust zwart gebleven: beide voeten rondom (vlak is 6/7, de donkerste geeltinten; een 7-lijn verdween in het vlak en gaf om-en-om met zwart): (18,52), (16,53), (17,53), (13–15,54), (9,55), (8,56), (48,54), (48,56), (48,57), (47,58), (47,60), (56,57). Rechterkopflank (45,10): enige outline-base-pixel tussen zwart en de ijslijn → 1. Spiraaleinde aan de buikrand (21,29): rood eigen materiaal, maar zwart gelaten (spiraal bevroren; een donkerrode randpixel zou de spiraal 1 px verlengen).
- 1 px breed gebleven, geen clusters, geen lichte kleur buiten de lijn (r. 373–377): 0 lichte pixels op de buitenrand.
- Zwart (index 1): 258 → 243 px = 11,2 % van 2171 (Poliwhirl ek 12,2 %; maatstaf Dundragoon 13,7 %, Skinguin 14,3 %, Princadee 13,8 %, Zapacha 17,5 %; het zwart-blauwe lijf doet hier, net als bij de Poliwhirl, een deel van het donker).
- Outline highlights (r. 452–455): niet apart gezet; het geel heeft al 5 direct binnen de lijn (kop links, bovenbuik, dijen) en volgens regel 4 blijft een licht materiaal bij zijn outline base.
**Na: PASS** (controle: 0 om-en-om, 0 zwarte binnenpixels buiten de ogen).

## 2. Schaduw
**Meting model (`meet.py`):** het Gemini-geel van kop en buik is **één vlakke tint**: lum 201–209 (mediaan 201,6, p90 204,4), geen verloop van linksboven naar rechtsonder. Schaduw bestaat in het model alleen als olijfcellen < 190: onder/naast de ogen, de streep links van de kopband (26,7–9), rechtsonder de kaak (x 34–37, r 21–22), onderbuik (r 37–40), dijen, voeten. r2 had die al als 6/7; het kopgeel was 5 omdat het model daar vlak is.
**Eerlijk per kleurzone, vóór: FAIL (geel), PASS (ijs), BIJNA (donker lijf).**
- Geel kop: effen 5-vlak, ±26 × 8 px tussen kopband en kin, alleen onderbroken door mond, neusgaatjes en de modelolijf onder de ogen. Effen: ja.
- Geel buik: 5 rond de spiraal, rechterflank zonder sikkel (alleen r33+ 6/7 uit het model). Effen: grotendeels.
- Geel dijen/armen/voeten: 5/6/7 uit het model, leest met volume.
- IJs (kristallen, handschoenen): 4 tinten + b/f-lijn, facetten uit het model: niet effen.
- Donker lijf: hoofdzakelijk 3 met 2-binnenlijnen en 4 op kopband/schouders; het model is daar effen zwart. Zie "ter info".
**Ronde (`maak.py sikkel`), zelfde regel als Poliwhirl V3:** een gele pixel 5/6 met aan de schaduwkant (rechts, onder, rechtsonder) zwart of donker lijf wordt een tint donkerder als sikkel die de vorm volgt: binnen de modelschaduwzone (lum < 190) → 7, in de vlakke modelzone 5 → 6. Alleen waar de vorm aan de lichtkant doorloopt (links resp. boven ook geel), zodat een strook van 1 px (tenen linkervoet r56) zijn hooglicht houdt. Daarna nieuwe tintgroepjes < 3 px terug (SPRITE_KERN "geen tintvlakjes < 3 px"): 15 px teruggezet (`maak_log.txt`). Twee handmatige pixels: (55,23) 5 → 6 (enige 5 tussen sikkel 6-6 en 7 op de rechterbovenarm), (21,41) 6 → 7 (losse 6 tussen 7-en op de linkerdij).
- Geel 5 → 6 (41 px): rechterkopflank (45,11), (44,14)–(44,17), (43,17); kin onderrand (24..33,22), (37,21), (38,21); rechterbovenarm (52,21), (54,22), (53..55,23); rechterflank buik (39,25)–(39,28), (40,29), (40,30), (41,31); rechterdij (45,41), (45,42), (44,43), (47,49); linkerdij (18,46); voeten (16,56), (17,56), (49,58), (55,58), (56,58), (49,59).
- Geel 5 → 7 (5 px, modelschaduw): olijfstreep naast de kopband (26,7), (26,8), (26,9); rechterknie (45,47), (46,48).
- Geel 6 → 7 (33 px, modelschaduw): kin rechtsonder (34..37,22); rechterflank onderbuik (42,33), (41,34), (40,35), (40,36), (39,37); onderbuik (33,41); linkerdij (21,41), (22,41), (20..23,42), (20,43), (20,44), (21,45), (20,46), (15,47), (17,47), (18,47), (16,48), (17,48); voeten (15,56), (15,57), (53,56), (48,60), (49,60), (52..54,60).
- Geel nu 5: 334 / 6: 200 / 7: 118 (was 380 / 192 / 72).
- Afgewezen variant V5 (proef): tweede sikkelrij in de kaak rechts (r21 x 29–39) en de rechterkopflank (x 42, r17–18). Leest op 8× als een rechte dubbele band onder de mond (SPRITE_KERN: "geen banding", "rechte tintgrenzen" = vast foutpatroon) en heeft geen grond in het model. Niet gedaan.
**Na: geel BIJNA → PASS voor de lijn.** Kin, rechterkopflank, rechterflank buik, dijen en voeten hebben nu een sikkel rechtsonder; licht linksboven consistent. Eerlijk: het gezicht tussen neusgaatjes en mond en de kaak blijven een groot licht 5-vlak, omdat het model daar vlak is. Dat is hetzelfde als de goedgekeurde regionale Poliwhirl ek (gezicht 5, sikkel rechts/onder); naast de Poliwhirl op 4× is de lijn consistent, de Poliwrath-kop is alleen groter en dus iets lichter in totaal (r. 444: "the R/S one seems overall lighter"). IJs: PASS (ongewijzigd). Donker lijf: ongewijzigd, zie ter info.

## 3. Kleurtinten
Palet ongewijzigd en byte-gelijk aan de regionale Poliwhirl `af/` (Jordi: "kleur zou ik voor de hele lijn hetzelfde blijven houden"); indexrollen gelijk: 1 lijn · 2/3/4 lijf · 5/6/7 geel · 8/9/a/b/f ijs · c/d/e rood. Helderheid (0,299/0,587/0,114):
- Geel 230 / 195 / 133 (stappen 35, 62): zelfde als Poliwag/Poliwhirl; 7 is ook de outline base ("reasonably dark", regel 4). Hue shift naar olijf in de schaduw.
- IJs 246 / 217 / 179 / 125 (b) / 81 (f): outline base b, schaduwlijn f zoals de Poliwag-/Poliwhirl-kristallen.
- Rood 154 / 106 / 68, donker lijf 41 / 60 / 90, lijn 17.
- Regel 1 (relatieve helderheid behouden): ja. Regel 2 (één hue per materiaal): ja.
**Vóór: PASS, na: PASS** (geen tint aangepast; alleen de verdeling binnen het geel en de lijnkleur veranderde).

## Bevroren zones: diffbewijs (`controle.txt`)
- Silhouet/alpha-diff: **0**.
- Bevroren masker (`zones.py`, 664 px): beide ogen E2 incl. lid, omlijning en onderrand (x 14–25 en 31–44, r 0–13), neusgaatjes (23,15), (27,15), mond M1 (al het rood r16–19), al het rood (spiraal, kristalkernen) en de hele spiraal-bbox x 22–38, r 27–40 incl. het geel ertussen: **0 px anders**.
- Materiaalvormen (kristallen, handschoenen, mond, spiraal, geel/donker-patroon): **0** materiaalwissels; alleen zwart → outline base van het eigen materiaal en geel een tint donkerder.
- Totaal gewijzigd: **94 px** (kop r0–22: 29, romp/armen r23–40: 25, benen/voeten r41–63: 40); 1→7: 8, 1→b: 7, 5→6: 41, 5→7: 5, 6→7: 33.
- Kleuren: 16/16 incl. transparant. Lichte pixels op de buitenrand: 0. Eenlingen: 73 → 67 (allemaal facetten in kristallen/handschoenen en modellijntjes, al in r2; de ronde voegt er geen toe behalve de 7-lijnpixel (11,21) van het kleine gele schoudervlekje). Nieuwe tintgroepjes < 3 px: geen (de gemelde 6 op (45,11) hangt vast aan het 6-vlak in de bevroren oogzone).

## Checklist E (FAKEMON_CHECKLIST)
E1 verre kant donkerder: rechterflank kop/buik/dij met sikkel, rechterbeen grotendeels donker lijf: ok. E2 overlap met omlijning: n.v.t. (geen nieuwe overlappen). E3 donker aandeel: 11,2 % zwart (+ zwart-blauw lijf als materiaal, zoals Poliwag/Poliwhirl): binnen de band.

## Ter info voor Jordi (niet uitgevoerd)
- **Kopvlak:** het model heeft op kop en buik geen schaduw (één tint). Wil je de kop ronder (zoals de Gen 3-Poliwrath met een donkere rechterkant), dan is dat een eigen schaduwkeuze die niet uit het model komt; een tweede sikkelrij is geprobeerd en leest als een rechte band. Alleen op jouw woord.
- **Donker lijf:** vrijwel effen 3 met 2/4; het model is daar effen zwart. Meer volume (4 op de bollingen, 2 als sikkel) kan, maar is niet gedaan voor de consistentie met de goedgekeurde Poliwhirl (zelfde keuze daar).
- **Voeten:** rondom zwart (geen 7-selout), omdat het voetvlak zelf al 6/7 is.
- **Spiraaleinde (21,29):** raakt de buikrand; de randpixel is zwart gebleven.

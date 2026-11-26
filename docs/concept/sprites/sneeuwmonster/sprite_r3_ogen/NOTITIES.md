# Sneeuwmonster r3_ogen: alleen de ogen rond (Jordi: "probeer de ogen rond te maken")
Basis r2; buiten de oogvakken (x21–26/y21–27 en x29–34/y22–28) pixeldiff 0 (assert in `bouw.py`); lijfvolume = r2.
Bestanden: `oog_R_<links>_<glans>.png` voor links a / a1 / b / c en glans lb (linksboven) / onder, `sneeuwmonster_r3.png` (= gekozen a1 + lb), `vel.png` (alle combinaties 12× naast r2 en het model, de gekozen combinatie 8× naast het model en 1× op vier achtergronden), `bouw.py` (maakt alles).

## Pixelpatroon uit echte Gen 3-sprites (_gba)
Ronde stipogen 4×4 (Lickitung (38,21), Politoed (32,19), Delcatty dichtbij-oog (31,24), Dewgong (19,16)): `.XX. / XGXX / XXXX / .XX.`
Ver oog 3×4 (Delcatty ver-oog (23,24)): `XX. / XGX / XXX / .XX`
In alle vier staat de glans G linksboven binnen het oog (kolom 1, rij 1); dat is ook de modelplek. Wynaut, Snorunt, Spheal en Castform hebben geen ronde stipogen (dichte streepjes of andere vormen), dus die zijn niet gebruikt.
Tinten per pixel uit het 1024-model (< 48 zwart, < 76 steen donker, anders steen midden); een verschoven oog neemt de tint van dezelfde patroonplek op de modelpositie.

## Varianten
- Rechteroog (alle): 4×4 rond op x30–33, y23–26; glans (31,24) = modelplek; "onder" = (31,25).
- Linkeroog:
  - a: 3×4 op x22–24 (modelpositie), **raakt de gezichtsrand**.
  - a1 (extra): a 1 px naar rechts (x23–25), raakt de rand niet; tussenruimte tussen de ogen 4 px zoals in het model. **Gekozen.**
  - b: 4×4 op x22–25, **raakt de gezichtsrand**.
  - c: b 1 px naar rechts (x23–26), raakt de rand niet; tussenruimte 3 px (model ±4).
- Glans "onder" (SPRITE_KERN, vuurduivel): zelfde kolom, één rij lager, op een pixel die niet aan de rand grenst.
Diff t.o.v. r2 (alleen oogvakken): a 6/10, a1 14/15, b 8/12, c 17/18 px (glans lb/onder).

## Twijfels
- a1 is een ovaal, rond als het Delcatty-ver-oog. Als Jordi echt twee gelijke rondjes wil, is c de ronde versie zonder randcontact (ogen dan 1 px dichter bij elkaar dan in het model).
- Met de glans helemaal omsloten leest het rechteroog op 12× als een ringetje, net als Lickitung en Politoed. Op 1× leest het als een glanzend steentje.

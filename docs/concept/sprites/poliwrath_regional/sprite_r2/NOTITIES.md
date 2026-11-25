# Regionale Poliwrath – sprite r2 (maker)

Basis = r1 met spiraal S1 (`../sprite_r1/`, gespiegeld model, 62×60 op x 1–62, y 2–61; zelfde palet). `varianten.py` laadt de r1-basis en zet alleen ogen en mond erop.
Uitvoer: `poliwrath_regional_r2_{E1,E2}{M1,M2,M3}.png`, `vel.png` (6× op 8× + model, kop 12× naast de modelkop en naast de Gen 3-Poliwrath-ogen, 1× licht/donker).

## Bewijs (`uitvoer.py`)
Ten opzichte van r1 O1S1 alleen verschillen in de oogzone (rij 0–12, x 12–45) en de mondzone (rij 12–18, x 13–43): **0 px erbuiten** voor alle zes. Silhouet: E1 +2 px, E2 +14 px (de oogbulten steken boven de modelkop uit), niets weg.

## Ogen (Jordi: "de hele ronde vorm van poliwraths ogen ..., incl ooglid, gekleurd naar het model, en geschaald naar de passende grootte")
- Bron: `graphics/pokemon/poliwrath/anim_front_gba.png` frame 1, de hele oogbult van de top (rij 9) tot de onderrand van het oog (rij 19): links x 19–30 (12×11), rechts x 37–49 (13×11). Ongespiegeld (links op links, rechts op rechts).
- Verhouding: Poliwrath kop/lijf op ooghoogte (rij 16) x 19–51 = **33 px**; kop hier op ooghoogte (rij 7) x 15–43 = **29 px** → factor 0,879. Oogbult links 12·0,879 = 10,5 → 11, rechts 13·0,879 = 11,4 → 11, hoogte 11·0,879 = 9,7 → 10.
- **E1** (berekende verhouding): links 11×10 (bronkolom 6 en bronrij 3 van het venster geschrapt), rechts 11×10 (kolommen 6 en 10, rij 5). Geschrapt = kolom/rij die het meest op zijn buur lijkt, niet door de pupil en niet de buitenste: geen schaling met resampling.
- **E2** (één stap groter): het oog ongeschaald, links 12×11, rechts 13×11 (+1 / +2 px).
- Kleur: lijn e en a → 1, oogwit 1 → 8, grijs 2/3 → 9, pupil a → 1. De blauwe Poliwrath-tinten b/c/d (licht/midden/donker) → kop-tint van het model **op die pixel** (`mat.py` van het gespiegelde, geschrapte model): geel → 5/6/7, zwarte band → 4/3/2. Valt een pixel buiten de modelkop (lucht/ijs), dan het materiaal van de dichtstbijzijnde kopcel.
- Plek: buitenrand van het oogwit op de buitenrand van het modeloogwit (links x 17, rechts x 39), onderste wit-rij op de onderste rij van het modeloog (rij 10). E1: links x 14–24 / y 2–11, rechts x 32–42 / y 2–11. E2: links x 14–25 / y 1–11, rechts x 31–43 / y 1–11.
- Opgeschoonde schaalrand (lidtint die na het plakken op de silhouetrand staat → omlijning 1): E1 (18,2), (14,6); E2 (18,1), (14,6), (34,1), (35,1). Verder geen pixels aangepast.

## Mond (Jordi: "kijken hoe een lijn van 1 pixel er netjes uit kan zien"; niet recht, geen glimlach)
Modelglimlach → geel uit de kop (zoals r1). Rode lijn (13), 1 px, plek/breedte van de modelmond x 15–41, middenstuk op rij 15 (2 rijen onder de neusgaatjes), mondhoeken omlaag. Regelmatige trapjes volgens de DC-gids (segmentlengtes lopen gelijkmatig op/af, diagonaal alleen via hoekjes):
- **M1 boog**: segmenten 2-4-15-4-2 (rij 17-16-15-16-17).
- **M2 recht midden met geknikte mondhoeken**: 1-1-23-1-1 (hoeken 1:1 omlaag).
- **M3 golf**: 1-4-6-5-6-4-1 (twee lage bulten, midden 1 rij lager, hoeken omlaag).

## Eigen zwakke punten
1. De oogbulten liggen deels in de zwarte modelband; per pixel gekleurd geeft dat in de linkerbult gele lidstreepjes binnen zwart en in de rechterbult een bijna zwarte bult. Dat is letterlijk het model op die plek, maar het leest drukker dan het Poliwrath-oog in één kleur.
2. Poliwraths lidlijnen (e) worden zwart (1); in de zwarte band vallen ze bijna weg.
3. M2 leest op 1× bijna als een rechte lijn (de hoeken zijn 1 px).
4. Pupil = Poliwraths ene zwarte pixel; de grijze 2-tinten werden 9 (ijsblauw), het palet heeft geen neutraal grijs.

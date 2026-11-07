# Hatun runa – kleur ronde 1

**Bestanden:** `hatun_runa.png` (64×64, geïndexeerd, index 0 transparant), `normal.pal` (JASC, 16), `raster.txt` (handraster, 0–F per pixel), `vel.png` (sprite | model op 8×, close-ups kop en vleugel 12×, 1× en 2× op licht/donker + model 1×).
**Gereedschap** (`stappen/`): `tl.py` (gedeelde helpers; model-bbox x108 y104, schaal 16.875, top 19, left 8 zoals `silhouet/sil.py`), `rgb.py` (mediaan van het model per spritepixel → paletkleur, alleen als onderlaag: `stappen/onder3.txt`), `meet.py` (modelhelderheid per spritepixel), `klas.py`, `zie.py` (sprite | model met raster), `ed.py`/`zet.py` (handmatige rijsegmenten/pixels; melden silhouetafwijking), `controle.py` (clusters < 3 px), `rand.py` (lichte kleuren op de buitenrand), `toon.py` (helderheid sprite vs model per zone), `vel.py`. Handwerk per onderdeel in `stappen/e_*.txt` (rijen, x-start = tekens).

## Werkwijze
1. Onderlaag: modelmediaan (midden 60 % van elk modelvak) naar het palet (`onder3.txt`). Alleen als positiegids.
2. Per onderdeel met de hand herschreven op 12–26× naast het model, elke lijn/grens op gemeten modelpixels (`meet.py`, kwart-pixelkaart van het oog):
   - **Kop** (`e_kop.txt` + reparaties): kruin rij 43–44 met goudvlekje (17,44)/(18,44); wenkbrauwstreep rij 45 x17–24, rij 46 x15–25, voorkant rij 47 x14–16 (gemeten: wit rij 46 vanaf x15, rij 47 x15–17); masker rij 47–49 tot x25; oog gemeten: donker (18–19, 47–48), glans (18,48) (model 18.6/48.0), witte sikkel (20,47–48) (model x20.0–20.5, y47.6–49.0), bruine iris (18–19,49); bovensnavel grijs met lichte bovenkant (C) en selout B, punt (9,50); open bek: donkerrood/zalm (14–16, 51–53), grijze onderkaak schuin (17,51)→(13,55); witte keel x18–23 rij 51–53 met grijze schaduw rij 53, zwarte lijn onder het masker rij 50.
   - **Nabije vleugel** (`e_nv.txt`): goudgele onderkant x30–35 (gemeten rij 29–45), lichtbruine voorrand (5) met selout 3; bruine slagpennen met 8 scheidingslijnen precies op de donkere modelpixels (L1 (37,23)→(35,28), L2 (40,25)→(36,30), L3 (41,29)→(38,32), L4 (41,32)→(37,35), L5 (40,35)→(37,37), L6–L8 onderaan). **Geen zebra:** lijnen taps (2 bij de inkeping, 3 naar binnen), vulling 4, licht (5) alleen op voorrand en veerpunten.
   - **Verre vleugel** (`e_vv.txt`): lange veren schuin naar rechtsonder met 3 scheidingen (S1 x10→15, S2 x16→19, S3 x20→22) i.p.v. de 5–6 dunne modellijnen (minder, grotere vormen op de modelplekken); donkere dekveren (2) eronder met één lichtere veer (3) rechts (rij 37–41).
   - **Staart** (`e_st.txt`): bovenrand selout 3, lichte veren 5/4, twee scheidingen op de modelpixels ((52,34)→(46,40) en (53,38)→(50,40)), donkere basis 2.
   - **Rug, buik, pootjes** (`e_lijf.txt`, `e_r7.txt`): donkerbruine rug x39–45, buik 8 (links/midden) → 7 (rechts) → schaduwsikkel 6 rechtsonder; verre poot donker (2), nabije poot met 3-highlight.
3. Controle: silhouet-diff **0** (971 px), geen lichte kleur op de buitenrand (`rand.py`: 0), kleine clusters alleen lijnen, veerpunten, glans en oog.

## Palet (16)
0 transparant · 1 omlijning (32,22,22) · bruin 2/3/4/5 · goud 6/7/8 · wit 9/A · snavel B/C · bek D/E · F maskerzwart (50,50,56) (model: masker 45,45,47 lichter dan de lijn 30,20,22).

## Afwijkingen van het model
- Verre vleugel: 3 scheidingen i.p.v. ±5 dunne lijnen (opdracht: geen zebra, minder en grotere vormen op de modelplekken).
- Nabije vleugel: lijnen in donkerbruin (2/3, taps) i.p.v. bijna zwart; zelfde plekken.
- Bovensnavel: buitenrand in donkergrijs (B, selout) en zwart aan de onderkant; het model heeft overal zwart. Snavel blijft grijs lezen.
- Toon: sprite gemiddeld 7–12 helderheid donkerder dan het verkleinde model (vleugels/staart; `toon.py`), deels omdat het model per vak lijn+vulling middelt.

## Open zwakke punten (voor ronde 2)
- Staart en verre vleugel iets te donker t.o.v. het model (toon.py: staart 79 vs 91, verre vleugel 66 vs 76).
- Bek: rood iets kleiner dan in het model; controleren op 1×.

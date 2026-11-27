# Guaraná fase 2, ronde 13 (start r12): omlijnde ogen rond, als opengebarsten vrucht aan de tros

Jordi (letterlijk, bij `sprite_r12/jordi_vierkanten.png`): "je maakt er een zooitje van, alles wat ik omlijnd heb zijn vierkanten, waarom? Fix dat,
en blijf telkens kijken naar de verhouding, zodat het een stuk fruit aan de tros lijkt".

Bestanden: `guarana2_r13.png`, `normal.pal` (= r12), `voor_jordi_r13_8x.png` (fase 1 | r13 | r12, 8×), `afstand.png` (fase 1 | r13 | r12 op 1× en 2×),
`closeups.png` (per oog r12 | r13, 12×). Bouwen vanuit `guarana_fase2/`: `python3 sprite_r13/bouw13.py && python3 sprite_r13/vel13.py`.
`kader.py SPRITE` = rechte donkere stukken ≥ 3 px die oogwit raken, per oogvak.

## Omlijningen terugrekenen
jordi_vierkanten.png = r12 op ±13,2× (x = (X−19,4)/13,2, y = (Y+36)/13,2; geijkt op oog L1 en het bovenste oog rechts). Rode lijnen geclusterd:
| omlijning (beeld) | sprite | oog |
|---|---|---|
| X423–484 Y117–181 | x31–35 y12–16 | M1 middelste tros rechtsboven |
| X280–413 Y160–260 (2 omlijningen samen) | x20–30 y15–22 | H1 half dicht oog midden + M2 links ervan |
| X185–248/181–189 Y252–299 | x12–17 y22–25 | L2 linkertros boven |
| X113–196 Y303–353 | x7–13 y26–29 | L1 linkertros links |
| X213–288 Y396–451 | x15–20 y33–37 | L5 linkertros onder |
| X634–697 Y244–295 | x47–51 y21–25 | RT rechtertros boven |
| X719–790 Y238–300 | x53–58 y21–25 | R2 rechtertros rechtsboven |
| X583–647 Y392–434 | x43–47 y32–36 | R5 rechtertros linksonder |
| (coördinator: "kleine oog links-midden") | x42–45 y25–28 | R1 rechtertros |

## Werkwijze (per oog, `bouw13.py`)
- Oog rond in plaats van een rechte rij wit in een rechthoekige rand:
  - open: wit 2-4-2 (`..LL.. / .LWWL. / LWKWWK / .LKWK. / ..KK..`), pupil 2 px linksonder, schil lijnrood links/boven, zwart rechts/onder (fase 1);
  - half dicht (H1): gebogen lid van vruchthuid met lijnrode boog (`..LL.. / .LMML.`), daaronder wit met pupil, onderkant rond;
  - klein (M2, R1, weinig plek): wit 3 px met pupil 1 px (`.LL. / LWWK / LKWK / .KK.`).
- Rondom het oog een ring vrucht (licht linksboven, midden, schaduw rechtsonder), daarbuiten een ronde naad (lijnrood, hoeken afgesneden):
  rondom rood, de vrucht duidelijk groter dan het oog. Tegen achtergrond/blad wordt de ring buitenlijn, behalve naast de bovenschil van een oog
  (anders een rechte bovenlijn over het oog).
- Oud wit van het omlijnde oog dat buiten het nieuwe oog valt → vrucht. Ogen die niet omlijnd zijn (L3, L4, M3, R4) en pixels die die raken: niet aangeraakt.
- 216 px anders dan r12; groen 0 px; silhouet +1 ((44,36), onderkant oog R5).

## Roodverdeling (lijnrood / schaduw / midden / licht)
fase 1 39/17/34/11 · r12 39,7/17,6/34,1/8,6 · **r13 41,3/16,9/31,8/10,0** (binnen ±3 van 40/15/35/10).

## Zelf bekeken
- 2× en 8× naast fase 1 en r12: de omlijnde ogen lezen als ronde ogen/dichte ooglid-vrucht in een rode vrucht, geen vierkantjes meer.
  De ogen zijn kleiner dan in r12 (wit 6 px i.p.v. 8), want rondom moet rood blijven; de trossen worden wat drukker door de naden.
- `kader.py`: nog donkere stukjes van 3 px: pupil + onderschil verticaal onder elkaar (L2, L1, L5, RT, R2, M1) en op de bovenrand (L2, RT, R2:
  buitenlijn + bovenschil). Geen rechthoekige kaders meer. Niet keurder-getoetst.

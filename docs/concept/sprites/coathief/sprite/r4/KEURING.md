# Controlekeuring Coathief r4 (schaduw, kleur, belijning)

Gekeurd: `coathief_r4.png` (`r4.txt` + `palet.txt`) op 8× en 1×, wit en donker, naast r3 en Mightyena, Linoone en Poochyena (eerste frame `anim_front_gba.png`). Silhouet, onderdelen, oog, crème aftekening, zwarte oren en ringvolgorde bevroren en niet gekeurd. Diff r3→r4 nagemeten: 69 px, precies de lijst uit `r3/KEURING_DFC.md` (21× 1→2, 20× 8→D, 16× 3→2, 7× 3→4, 4× 6→7, 1× 7→5); alpha/vorm identiek.

## Oordeel: BIJNA (één regelbreuk van 5 px; verder PASS)

r4 is beter dan r3 en een nette Gen 3-sprite:
- Zwart heeft nu een echte ramp (L 16/33/58/91, stappen ±25–33); dat is vrijwel Mightyena's donkere ramp (32/49/74–82). Kop leest als zwart/antraciet, niet grijs of blauw (3 = (56,58,62) is nauwelijks koeler dan r3).
- Schaduwsikkel wang → kaak is zichtbaar en volgt de vorm; schedel en snuitrug blijven licht. Op 1× leest de kop nu als volume i.p.v. vlak.
- Crème-omlijning D (120,96,68, L≈100) zit tussen Linoone's selouts (131,115,90 / 139,98,65); niet te donker, staart en tenen krijgen een zachte lichte rand i.p.v. een bruine vlek. Crème-stappen 153/195/237 gelijkmatig.
- Bruin hue-shift: warm roodbruin, rustiger schaduw. Vachtgrens rug gekarteld, nabije voorpoot heeft nu de lichtrand (`1 4 3 2 2 2 1`, zelfde profiel als de achterpoot).
- Geen nieuwe losse pixels: de eilandjes < 3 px zijn diagonale lijnstukjes, oog/aftekening (bevroren) of tintpixels in de pootprofielen.

Wat de reparatie liet liggen:
1. **Bovenrand kop wisselt selout en zwart om en om.** Van oortip tot verre oor: (15,30)=2, (16,29)(17,29)=1, (18,30)(19,30)=2, (20–22,30)=1, (23,31)=2. Het automatische criterium in `dfc_reparaties.py` (alleen lijnpixels boven 4) sloeg de oortip en de pixels boven 3 over. Klein contrast (L33 tegen 16), maar het is precies de harde regel "nooit om en om op één rand".
2. **Crème-omlijning niet overal doorgevoerd** (zelfde oorzaak: alleen pixels die 8 waren): (50,23) is 1 aan de lichtkant van een crème ring (rijen 20–22 erboven zijn D); de linkerrand van de nabije voorpoottenen (16,53)(16,54) is 1, terwijl de tenen van de achterpoot D kregen.

## MOET (geen vormwijziging; in een kopie gesimuleerd en bekeken)
| pixel (x,y) | nu | wordt | waarom |
|---|---|---|---|
| (16,29) (17,29) | 1 | **2** | oortip in dezelfde selout als de flanken |
| (20,30) (21,30) (22,30) | 1 | **2** | schedelrand tussen de oren doorlopend selout tot (23,31) |
| (50,23) | 1 | **D** | lichtkant crème ring, sluit aan op (51,20–22) |
| (16,53) (16,54) | 1 | **D** | lichtkant crème tenen voorpoot, zoals de achterpoot |

Verre oor (24,30)(25,29)(26,29)(27,30) blijft 1 (achter, schaduw). Onder- en rechterranden blijven 1.

## MAG
- (45,7) 1 → D: linkerrand van het hangende staartpuntje, maakt de kolom (45,5–7) D.
- Zwarte staartringen aan de licht-/bovenkant ((50–52,2), (53,3), (54,3), linkerrand x52 rijen 8–11 en 16–19) 1 → 2 voor consistentie met de kop. Op 1× nauwelijks zichtbaar; alleen als de kopregel ook voor de staart moet gelden.
- Poten blijven parallelle strepen (`1 4 3 2 2 2 1`); bij een rechte cilinder is dat normaal (Mightyena-poten), geen actie nodig.

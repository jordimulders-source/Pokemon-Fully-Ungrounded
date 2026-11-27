# Guaraná fase 2, ronde 15 (start r14)

Jordi (letterlijk): "nu weer geen enkel oog dat de goede kant op kijkt, blijven in rondjes gaan. de tros rechts is ook geen geheel meer"
+ "er moeten tenminste een paar ogen naar linksonder kijken zoals in fase 1" / "heb ik toch al gezegd"
+ "de vormen van links en midden zijn verder oke, al heeft links onderin een heel verlept stukje fruit ipv recht en is midden op plekken iets te hard belijnd".
Getoetst aan "VASTE REGELS SPRITE" onderaan SPEC.md.

Bestanden: `guarana2_r15.png`, `normal.pal` (= r14 = fase 1-palet; 11 kleuren), `voor_jordi_r15_8x.png` (fase 1 | r15 | r14), `afstand.png` (1× en 2×).
Bouwen vanuit `guarana_fase2/`: `python3 sprite_r15/bouw15.py && python3 sprite_r15/vel15.py`. Controle: `oogtabel.py` (tabel hieronder),
`controle.py` (diff met r13, ruimte tussen trossen, roodverdeling), `recht.py` (rechte stukken + horizontale lijnen), `lijnen.py` (binnenlijnen r14 vs r15).

## Wat er veranderd is t.o.v. r14
1. **Ogen fase 1, pixel voor pixel** (sjablonen `OOG` in bouw15.py; `P` = pupil):
   - `F1A` = bovenste oog fase 1 (guarana/af/guarana.png x16–22, y17–23), `F1B` = onderste oog fase 1 (x14–20, y27–33): wit, pupil en schil exact
     gekopieerd (ook het zwart rechts/onder van de fase 1-schil). **F1A: D (linkertros) en RT (rechtertros); F1B: M1 (midden) en R5 (rechtertros).**
   - De andere open ogen volgens regel 5/6 (schil lijnrood rondom): L2 en R2 `MIDDEN` (wit 2-4-4-2, pupil 2×2 precies in het midden);
     F `O45` (0 links, ½ onder); e `O54` (½ links, 0 onder); andere kant zoals fase 1: s rechtsonder, C (klein) links, R1 (klein) rechts.
     Half dicht (A, H1, M2): gebogen lid van vruchthuid met lijnrode rand, pupil links tegen het lid.
   - Offset in de tabel = pupilmidden − witmidden (wit-bbox = wit + pupil). Bij een wit van 5 breed kan een 2×2-pupil niet precies in het midden;
     fase 1 zet hem op (−0,5;+0,5): één kolom wit links ervan en één rij wit eronder. Dat is de "linksonder" van F1A/F1B.
   - Oog op het midden van de vrucht; raakt of overlapt het een ander oog, dan max. 1 px opgeschoven binnen de eigen vrucht (zodat er geen dikke dubbele
     oogranden ontstaan). Alle ogen staan ongeschonden in de sprite (laatste kolom), M2 op 1 px na (half dicht, lid valt over de rand).
   - Let op: regel 6 (oogrand rechts/onder lijnrood) en de opdracht "schil exact kopiëren" spreken elkaar tegen bij F1A/F1B; daar is fase 1 exact
     gevolgd (zwart rechts/onder), bij de andere ogen regel 6. Aan Jordi/coördinator om te kiezen.
2. **Rechtertros één geheel:** spreiding om de takpunt 1,3 → 1,1, vruchtmaat gelijk (×1,6). Geen achtergrondgaten meer tussen de vruchten (gecontroleerd
   voor alle drie de trossen: geen achtergrondpixel met tros binnen 3 px links, rechts, boven én onder).
3. **Linkertros onderaan:** H (onderste vrucht, was een spitse, hangende peer: "verlept") is nu een volle ronde vrucht van dezelfde maat als de andere
   (9 px, hooglicht, sikkel). G (linksonder) hangt nu vóór E en is daardoor een hele ronde vrucht i.p.v. een sikkel. Verder geen vormen veranderd.
4. **Binnenlijnen (midden te hard belijnd):** zwart binnen een tros → lijnrood; twee lijnpixels van verschillende vruchten naast elkaar → de achterste
   wordt vrucht (midden of schaduw); lijnrood dat tegen een oogrand ligt → vrucht. Binnen links/midden (buiten de ogen) r14 → r15: zwart 5/1 → 0/0,
   lijnrood 27/28 → 16/21, 2×2-lijnklonten 6/8 → 0/0. Tintgrenzen tussen vruchten blijven (geen blur).

## Oogtabel
| tros | oog | sjabloon | wit-bbox (x0,y0)-(x1,y1) | pupil-bbox | offset (dx,dy) | in sprite |
|---|---|---|---|---|---|---|
| L | C | KL_L | (13,27)-(16,29) | (13,28)-(13,28) | (-1.5,+0.0) | 18/18 px |
| L | A | HALF7 | (1,26)-(5,27) | (1,26)-(2,26) | (-1.5,-0.5) | 23/23 px |
| L | B (L2) | MIDDEN | (9,23)-(12,26) | (10,24)-(11,25) | (+0.0,+0.0) | 24/24 px |
| L | D | F1A | (6,29)-(10,33) | (7,31)-(8,32) | (-0.5,+0.5) | 38/38 px |
| L | F | O45 | (12,33)-(15,37) | (13,35)-(14,36) | (+0.0,+0.5) | 30/30 px |
| M | M2 | HALF6 | (21,20)-(24,21) | (21,20)-(22,20) | (-1.0,-0.5) | 17/18 px |
| M | a (H1) | HALF7 | (24,16)-(28,17) | (24,16)-(25,16) | (-1.5,-0.5) | 23/23 px |
| M | b (M1) | F1B | (32,13)-(36,17) | (33,15)-(34,16) | (-0.5,+0.5) | 39/39 px |
| M | e | O54 | (30,21)-(34,24) | (31,22)-(32,23) | (-0.5,+0.0) | 30/30 px |
| R | r (R1) | KL_R | (42,26)-(45,28) | (45,27)-(45,27) | (+1.5,+0.0) | 18/18 px |
| R | p (RT) | F1A | (46,22)-(50,26) | (47,24)-(48,25) | (-0.5,+0.5) | 38/38 px |
| R | q (R2) | MIDDEN | (53,25)-(56,28) | (54,26)-(55,27) | (+0.0,+0.0) | 24/24 px |
| R | s | ORO | (48,29)-(51,32) | (50,31)-(51,32) | (+1.0,+1.0) | 24/24 px |
| R | u (R5) | F1B | (43,32)-(47,36) | (44,34)-(45,35) | (-0.5,+0.5) | 39/39 px |

## Controle
- Liaan/blad: 0 px anders buiten de trossen en de oude trosplek (t.o.v. r13). Ruimte links–midden 2 px, midden–rechts 5 px. Kader x0–62, y1–51.
- Rood lijn/schaduw/midden/licht: **42,5/14,5/33,0/10,0** (doel 40/15/35/10 ±3).
- `recht.py`: rechte buitenranden 4–6 px alleen aan de bovenkant tegen het blad en bij x0; horizontale lijnen ≥ 5 in de trossen alleen bovenaan
  (trostop tegen blad/lus) en bij twee oogranden in de rechtertros (RT/R1 onderrand, R5-bovenrand + naad).
- Zelf bekeken op 1×, 2× en 8× naast fase 1: de vier fase 1-ogen kijken linksonder zoals fase 1; de rechtertros hangt als één tros. Niet keurder-getoetst.

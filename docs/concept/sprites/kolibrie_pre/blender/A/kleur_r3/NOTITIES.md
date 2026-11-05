# Kolibrie pre-evo – kleur r3 (maker): reparaties keuring r2

Bron: `../kleur_r2/raster.txt` + `reparaties.py` (alle pixels met coördinaat, met de hand gekozen) → `raster.txt`; `palet.py` → `kolibrie_pre.png`/`normal.pal`; `controle.py`; `vel.py` → `vel.png` (r3 naast r2); `silhouet_r3.txt` (identiek aan `silhouet_r2.txt`).

## Controles
- alpha-diff met `kleur_r2/silhouet_r2.txt`: **0** (603 px); `cmp` silhouet_r3 = silhouet_r2.
- 33 px gewijzigd t.o.v. r2. Open randen (licht vlak naast transparant): 0.
- Niet-zwarte schaduwrand: (33,23) bovenrand nek, (41,32) `E` (bewuste zachte trap in de rug), teentjes (27,44),(29,44),(32,44) (dunne delen, zie FAIL 9/14).
- Losse pixels: alleen bedoelde enkelingen (oog-omgeving, vleugelrand-diagonaal, staarttop (41,35), vleugelpunt).
- Oog (x21–25, y17–21): 0 px gewijzigd. Snavelvorm: 0 px gewijzigd; alleen de gaapkleur (15,18),(16,19).

## Palet
Index `9` (keelopening, 150,40,84) is vrijgekomen (gaap nu `1`) en hergebruikt als **verre poot, donker warm (176,98,40)**. Rest gelijk aan r2.

## Per FAIL
| # | wat gedaan |
|---|---|
| 3 kop-over-rug | (30,25) `2`→`3`; over blijft één taps lijntje (29,26)(28,26)(27,27) langs de kinrand. |
| 4 kap-banding | (29–30, 19–21) en (29,22) `E`→`B`; `E` alleen nog (30,22),(30,23),(31,23): de schaduw wordt naar onder breder. |
| 5 vleugel binnenrand | (36,28),(33,30),(32,31),(32,32) `4`→`B`; (35,29) `B`→`4`: één vlekje `4` op (34–35, 28–29). Voorrand `E` y28–32 blijft. |
| 7 jaggies rug | (41,32) `1`→`E` (zachte trap in kleur; omtrek gelijk). Linksonder (22,39) niet verplaatst (zou silhouetwijziging zijn). |
| 9 open randen | gaap (15,18),(16,19) → `1` (omlijningskleur, vorm gelijk). Teen (28,44) `F`→`1`. |
| 10 losse pixels | (30,45) is nu de klauwpunt onder het verre teentje (30,44) i.p.v. een los pixel. (45,42) blijft `1` (zie hieronder). |
| 11 leesbaarheid 1× | warme pootjes geven een accent; op 1× zie je nu twee oranje stipjes onder de buik. |
| 14 pootjes | nabije poot (28–29,43) `C`/`D` met teentjes (27,44),(29,44) `D`; verre poot (31–32,43) `D`/`9` met teentjes (30,44),(32,44) `9`, klauwpunt (30,45); (30,43) `1` scheidt de pootjes. |
| 15 staart | lob in schaduw: (41,36),(42,36),(42,37) `3`, (43,37),(42,38),(42,39),(42,40),(43,40) `2`; alleen de top (41,35) `4`. |

## Eerlijke resterende zwakke punten
1. **(45,42) spijkertje:** kan alleen weg met een silhouetwijziging van 1 px (pixel weghalen). Kleur verandert er niets aan; het blijft een punt onder de staarttip. Voorstel: die ene pixel uit het silhouet halen (vraag aan Jordi/coördinator).
2. **Teentjes aan de onderrand** zijn gekleurd naast transparant: het silhouet heeft onder de pootjes geen rij voor een zwarte omlijning (Taillow/Starly hebben 3–4 rijen poot). Dunne delen zonder omlijning mag volgens de gids, maar het is geen echte Gen 3-poot met zwarte rand. Een echte oplossing vraagt 1–2 rijen silhouetgroei onder de pootjes.
3. **Staart** leest door de schaduw nu als een donker stompje achter de vleugel; op 1× valt het weg tegen de vleugel (`2`/`3` naast `E`).
4. **Linksonder** (x22, y38–39) blijft run 1-1-2-1-1 (silhouet).
5. Oog en snavel bevroren; de punten uit §4 van de keuring (oog als "0", snavel als sprietjes op 1×) liggen bij Jordi.

## Lessen
- Een vrijgekomen paletindex (hier `9` na het dichten van de gaap) is de goedkoopste manier om een accentkleur toe te voegen zonder palet te verruimen.
- Pootjes van een zittend vogeltje hebben in het silhouet minstens 2 rijen onder de buik nodig voor een zwarte onderrand; plan dat bij het silhouet, niet in de kleurronde.

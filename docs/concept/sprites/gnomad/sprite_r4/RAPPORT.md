# Gnomad – sprite r4 (maker-agent, 22 nov)

Basis: r3-A. De riem blijft de bruine Machoke-riem van r3. Alleen de gesp is nieuw: in de vorm van Jordi's foto van een kabouterriem ("qua vorm"), in de kleuren van r3-A.
Script: `r4.py`. Het gebruikt r3-B (riem zonder gesp) als basis en zet daar de gesp op. Een assert bewaakt de diff van 0 buiten de gesp.

## Gesp
- Groot vierkant van 8×7 inclusief zwarte omlijning, op x21–28, y43–49. Hij steekt 1 px boven en 1 px onder de band uit.
- Vlak crème schaduw (218,198,158), met een glanspixel crème licht (248,242,222) linksboven.
- Schaduw rechts en onder in lichtbruin (174,130,90).
- In het midden een staand gat van 2×3 (x24–25, y45–47) waar de donkerbruine band (104,68,48) doorheen zichtbaar is.
- Geen pin, geen details. Geen nieuwe kleuren (16, niets opgeofferd).

## Diff t.o.v. r3-A
| zone | px |
|---|---|
| gesp | 40 |
| riem, neus, rest | 0 |

Controle: geen lichte kleur op de buitenrand, geen losse zwarte pixels. Zwart is 21,7 % van de figuur (r3: 21,4 %; Gen 3 ±12–19 %, komt door de zwarte riemlijnen).

Bestanden: `gnomad.png`, `gnomad_8x.png`, `vel.png` (r4 | r3-A op 8×, met 1× op licht/donker).
(Een eerste versie met zwarte riem en gele gesp is na de correctie "qua vorm" overschreven.)

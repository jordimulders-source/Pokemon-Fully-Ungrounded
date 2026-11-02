# Wasbeer silhouet ronde 13: alleen de armzone (maker-agent, 2 nov)

Jordi over r12: "je hebt nog steeds zon gekke streep links van het hoofd die ik meermaals al benoemd heb. Verder staan de armen heel gek, alsof ze uit zijn buik groeien".
Bestanden: `ronde13.txt` (armzone met de hand als tekst gelegd, rest = r12), `ronde13_1x.png`, `vel_ronde13.png` (r13 4x, omtrek over onderlaag, r12 vs r13, Gumshoos/Weavile/Sneasel, 1x, zoom 8x kop+armen, foto 10/11/15), `vel_r13.py` (maakt ook het diffbewijs).

## Bevroren: diffbewijs
Armzone = kolom 0–14, rij 22–43. `python3 vel_r13.py`: **146 px gewijzigd binnen de armzone, 0 erbuiten** (kop, lijf, buidel, benen, staart gelijk aan r12). 1421 px, bbox 60x55.

## Wat er veranderd is
- **Streep weg:** de lange dunne verre arm die op kinhoogte 13 px naar links stak, is weg. Links van de kop (boven rij 22) staat niets meer.
- **Nabije arm (laag):** schouder direct onder de kin (rij 22–24), bovenarm 4 px dik recht omlaag vóór de borst met een kolom lucht ertussen (rij 25–31), elleboog (rij 30–31), onderarm schuin vooruit-omlaag naar een vuist van 5–6 px (rij 34–37). Koevoet: 2 klauwen samen = steel van 3 px dik omlaag, bocht vooruit, eindstuk, gespleten punt (V op (1,41)).
- **Verre arm (hoger, actief):** vuist opgeheven op borsthoogte (rij 23–26, kolom 3–9), komt van achter de nabije schouder (bovenarm valt achter de nabije arm, zoals bij Weavile's verre arm). Koevoet hangt eraan: steel 3 px dik omlaag, bocht vooruit, punt gespleten (V op (1,30)).
- Armen reiken tot kolom 1 (r12 ook), maar als korte vuist + klauw, niet als lange onderarm.

## Check
| punt | oordeel |
|---|---|
| Geen streep/lange dunne lijn links van de kop | ok |
| Armen vanaf de schouder, niet uit de buik | ok: beide wortels op rij 22–25, direct onder de kin; nabije bovenarm met lucht langs de borst |
| Beide armen zichtbaar, één hoger | ok: verre vuist rij 23–26, nabije vuist rij 34–37 |
| Stevig (≥3 px), compact | ok: bovenarm 4, onderarm 5, vuisten 5–6, klauwsteel 3 |
| Koevoetklauwen Sneasel-maat | ok: ±3x5 px per klauwpaar; de V-inkeping leest pas op 4x |
| Leest op 1x | redelijk: twee vuisten met haken vóór de borst; de lucht van 1 kolom langs de nabije bovenarm valt op 1x bijna weg (in kleur scheidt de donkere onderarm hem van de geelbruine borst) |

## Open
- Bij de verre arm zijn geen bovenarm en elleboog te zien (die liggen achter de nabije arm, wat voor de verre kant klopt). Wil Jordi ze zien, dan moet de verre arm opzij of achter het lijf, en dat raakt de bevroren romp.
- Beide koevoeten lijken op 1x een beetje op de haak van de staart (drie haken). Een alternatief is de nabije klauw recht vooruit met de bocht omlaag; dat is nog niet gemaakt.

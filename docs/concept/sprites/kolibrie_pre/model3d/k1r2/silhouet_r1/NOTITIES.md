# Kolibrie pre-evo – silhouet r1 (K1 kop 47°, lijf R2)

Bron: `../silhouet_direct.txt` (656 px). Reparaties letterlijk als pixels in `maak.py`; `controle.py` (losse pixels, uitsteeksels, spleten); `vel.py` → `vel.png` (onderlaag | silhouet | overlay 4×, 2× en 1×, naast Taillow, Starly en het oude B2 r1).

**Resultaat: 656 px** (direct 656). Eén deel, geen gaten.

## Diff per zone (t.o.v. silhouet_direct.txt)
| zone | rechthoek | erbij | eraf |
|---|---|---|---|
| bekje | (13,13)–(19,20) | 3 | 2 |
| kin | (17,23)–(21,27) | 0 | 2 |
| pootjes | (23,42)–(36,46) | 5 | 4 |
| staartstompje | (37,41)–(46,46) | 0 | 0 |
| gladmaken ±1 px | (17,33) en (43,38) | 1 | 1 |
| **buiten** | | **0** | **0** |

Gladmaken: twee artefacten van de verkleining, buiten de opgegeven zones maar binnen de regel "±1 px aan de rand": een uitsteeksel van 1 px op de borst (17,33) weg, een inkeping van 1 px in de rug (43,38) dicht. Wil Claude strikt 0 buiten de vier zones, dan zijn dit de enige twee pixels om terug te zetten.

## Wat ik deed
1. **Bekje** (linkerrand per rij y14–19: 15-16-18-17-15-15): bovensnavel dun en schuin naar links (punt (15,14), 2 px dik op x16–17); open V aan de voorkant 3 rijen hoog (x15) en 2 rijen (x16), top op (17,16); ondersnavel groter, met een punt van 2×2 op x15–16, y18–19, en een wig tot x17 op y17. Punten op de plek van de render (bovensnavel x15, ondersnavel x15). Steekt 2–3 px voor de kop uit, vergelijkbaar met Starly (die steekt ±2–3 px uit, met een trede).
2. **Kin:** inham onder de kopbol 1 px dieper op y24–25 (linkerrand 17-17-18-20-20-19-18), zodat de kopbol loskomt van de borst. De ronding van de kop (y11–23) is niet aangeraakt.
3. **Pootjes:** nabije poot = stam 3 px (y42–43, x26–28) + teenrij 5 px naar links (y44, x24–28), op de plek van de render (zelfde massa: 11 px). Het hangende buikrandje (x30–34, y42) is het verre stompje geworden: 3×2 op x31–33, y42–43. Twee kolommen lucht tussen de poten; onder de buik verder leeg.
4. **Staartstompje:** de render is al rond (6-5-3 px), zonder losse pixel of trapje: niets veranderd ("stompje is prima").

## Checklist
- 3/4 links-voor: kop 47° naar de kijker, lijf 32°. ok.
- Kop: ronde bol, niet afgevlakt (geen pixel in de kop buiten het bekje veranderd).
- Lijf niet dikker: 656 = 656.
- Losse pixels: geen. Uitsteeksels van 1 px alleen de bovensnavelpunt (15,14) en het teenpuntje (24,44), bewust. 1-px "spleet" (17,16) is de top van de V.

## Zelf nog zwak (eerlijk)
- **Bekje op 1×**: het leest als een klein open "<", maar de opening aan de voorkant is maar 2–3 px hoog; op 1× is het net zo klein als het bekje van Starly en het leest vooral door de inkeping, dus de kleur (oranje ondersnavel, donkere mond) moet het af maken.
- **Kopbol en borst**: de inham is ondiep (2–3 px ten opzichte van kop en borst); op 1× is de kop een eigen bol, maar de overgang naar de borst is zacht. Dieper maken zou de borstronding aantasten.
- **Verre stompje** zit in de render niet als poot (daar is het een buikrandje); als stompje klopt het met de pose, maar het is mijn interpretatie.
- **Totaal 656 px** is aan de kleine kant naast Starly (767) en Taillow (838); bewust niet vergroot (massa heilig).

## Lessen
- Een render waarin de snavel binnen de kopomtrek valt, geeft na verkleinen een bultje: de snavelpunten van de render aanhouden en de V met de hand uitsnijden, zonder de snavel verder naar voren te trekken dan de render (overlay checken).

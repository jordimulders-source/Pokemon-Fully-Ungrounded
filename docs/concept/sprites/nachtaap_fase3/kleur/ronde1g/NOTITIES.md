# Nachtaap fase 3: kleurronde 1g (5 nov), vuistarm + lijf afronden op v7

Basis: `../ronde1f/v7/` (been +7 px, gekozen door Jordi). Bron: `bron/ronde1g.txt` (regels `y x tekens`, bovenop v7) → `bron/bouw.py`; `bron/check.py` (bevroren delen, diff per zone, open randen, losse pixels); `bron/vel.py`; `bron/zoom.py` (uitsnede naast v7, met rooster). Palet gelijk aan v7.
Volgorde van Jordi: eerst de vuistarm, daarna het lijf afronden. Geen strepen of rugpatroon.

## Bevroren: 0 px diff met v7 (check.py)
| deel | masker | diff |
|---|---|---|
| kop, gezicht, maan | x0–20 rij 29–47, plus x0–13 rij 27–28 | 0 |
| hand, gloed, gezicht en maan (alle pixels met kleur FfPpBbGMmW in v7) | per kleur | 0 |
| staart (spiraal + stam) | x≥44 rij 0–38, plus x≥49 rij 39–41 | 0 |
| opgeheven been (vorm, dij, onderbeen, want-voet) | x28–44 rij 0–30, plus de buitenomtrek van de dij rij 31–35 | 0 |

Het hand-/gloedvak (x6–21, rij 44–63) heeft 1 px diff: (21,47) V→L. Dat is een armpixel (in v7 V, geen gloed): de lichtband van de onderarm.

## Per zone (diff met v7: 226 px in totaal; buitenomtrek 25 px)
- **Vuistarm (37 px, waarvan 15 omtrek):** `later_vuistarm.txt` toegepast, met deze correcties:
  - Rij 26–28 zelf hersteld: het bestand gaf een gat op (14,27) en een losse K op (14,26).
  - De onderkant van de vuist is rond (rij 21–22) in plaats van 5 px recht.
  - De spleet tussen arm en kruin eindigt zonder inkeping van 1 px (26,11 K).
  - Resultaat: de arm is horizontaal 8 px breed, haaks ±5,5 px, en wordt taps achter de kop. Er zit lucht tussen de arm en de kruin (rij 25–26, x8–11). Cilinder: K-onderrand, S-schaduwband, V, L-band, D-bovenrand.
- **Rugrand (rij 29–35, 40 px, waarvan 2 omtrek):**
  - De rug loopt van schouder naar dij in segmenten van 2–3–5 px (rij 32: x21–22, rij 31: x23–25, rij 30: x26–30). De segmenten worden geleidelijk langer: een bolle boog zonder rechte stukken van 5–6 px halverwege.
  - Daaronder ligt een L-lichtband van 2 rijen.
  - De lichte vlekken van de oude dijwortel zijn weg: de L op x37–40 rij 32–35 aan de schaduwkant is nu V/S.
  - De lichtband van de dij stopt op rij 33. Het buiklicht is een eigen vlak linksboven op de romp (x29–33, rij 35–38).
- **Heup/bil (rij 36–46, x≥36, 67 px, waarvan 8 omtrek):**
  - De naden tussen dij, staartwortel en bil zijn weg: rij 36 x39–43, rij 38 x37–42, de dubbele rand x43/x45 op rij 39–41 en de lijn op rij 45–46 x40–48. De dij gaat nu in één heup op, en de staart komt uit de rechterkant van die heup.
  - Omtrek: de rechterrand loopt van de staartwortel in een rustige holle boog (x47-47-46-46-46-47-48) naar de bovenrand van het onderbeen. Er is geen hoek of bult meer.
  - Schaduw: de rechter- en onderkant zijn S, met D langs de rand.
- **Volume (82 px):**
  - Nabije arm als cilinder: S slagschaduw van de kop op x21, een L-band op x22–23 die met de arm taps naar x24 loopt, V, en S aan de rompkant.
  - Romp: grote vlakken. Licht linksboven, V in het midden, en een terminator die van rechtsboven naar linksonder loopt (S).
  - Dij van het onderbeen (de lob onder het lijf): V linksboven, S-kern, D/K-onderrand.
  - De D-kniestreep (x43–46, rij 46–51) tussen lob en onderbeen is S geworden.
  - De omtrek van het onderbeen en de voet is niet veranderd.

## Controle
- Open randen: 0.
- korrel.py: 0 uitsteeksels, 27 inkepingen en 1 tand (x44,y34). Dat is precies gelijk aan v7: de bewuste spiraalspleet en de lucht tussen dij en staart.
- Losse pixels: geen nieuwe. De 2 in de buurt van mijn wijzigingen, (20,32) en (21,45), staan zo in v7 en liggen buiten mijn regels.
- Totaal 1820 px (v7: 1825).

## §0 en de norm
1. 3/4: ongewijzigd, ok.
2. Ledematen: alle 4 plus de staart tellen en zijn verbonden, ok.
3. Rechte lijnen: de vuistonderkant is rond gemaakt. Wat nog over is, staat hieronder bij "zwak".
4. Ogen en gezicht: 0 px diff.
5. Silhouet leest: ok.
6. Formaat: −5 px.
7. Pose: bevroren.
- Omlijning: D aan de lichte kant, K aan de schaduwkant, ok.
- Licht: linksboven, ok.

## Eerlijk: zwak
- **Romp is rustiger, maar wat vlak:** het middenvlak V is groot. Het model laat meer ronding zien, met een donkerdere buikonderkant en een sterkere kernschaduw. Op 1× leest het lijf wel als één vorm, maar minder bol dan het model.
- **Rug–dij-overgang:** het laatste stuk van de rugrand (rij 30, x26–30, 5 px) gaat met een holle hoek over in de voorrand van het been. Die hoek kon ik niet afronden zonder beenpixels te veranderen: (29,29)/(30,30) horen bij het bevroren been.
- **Knie:** zonder de D-streep scheiden alleen de inkeping onderaan en de lichtband van het onderbeen de lob van het onderbeen. Op 1× leest het als één gebogen been, maar de lob blijft een vrij grote donkere massa onder het lijf.
- **Staartwortel/heup:** de staartwortel is bevroren (S), dus de rechterkant van de heup is een doorlopende donkere band van de staart tot het onderbeen. Dat klopt als schaduwkant, maar het is zwaar naast de lichte dij.
- De onderlaag in het vel toont het been nog op de oude plek (model niet aangepast).

## Lessen
- `later_vuistarm.txt` was niet bouwklaar (gat en losse K op rij 26–27). Lees bewaarde stukjes altijd eerst in op een kopie en zoom in vóór je ze overneemt.
- Bevroren delen ook als kleurmasker controleren (FfPpBbGMmW uit de basis), niet alleen als rechthoeken. Een rechthoek rond de gloed vangt anders armpixels.

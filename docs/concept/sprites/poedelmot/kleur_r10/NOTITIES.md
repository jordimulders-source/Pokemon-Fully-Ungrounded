# Poedelmot: kleur r10 (maker, zuinig)

Maatstaven (Jordi): heel accuraat op het model, en een Gen 3-sprite volgens onze eisen. Gebouwd vanaf r9 (r9 ongewijzigd). Hersteld: precies de zwakke punten die ik in r9 zelf noemde. Lagen: `stappen/bouw10.sh` (nieuw: `k_poten10.py`, `k_naad10.py`, `k_dun10.py`, `k_eind10.py`; aangepast: `k_modlijn.py`).

## Gedaan
1. **Poten**:
   - Per pluim een eigen ronde omtrek: ovalen met middelpunt en straal met de hand gemeten op het model (12×).
   - Een 1 px lijn `3` alleen waar een pluim over de pluim erachter of het middenstuk valt; dubbele lijnen zijn naar 1 px teruggebracht.
   - Volgorde van achter naar voor: E, D, B, A, B2, C.
   - De extra klauwgroep (22–24,55–56) is weg (pluimkleur; de rand krijgt lijntint).
   - Vijf klauwgroepen zoals het model, elk met 2 schuine klauwtjes `2` en `3` ertussen.
   - Middenstuk: tan platen `6` (licht `7` linksboven) met twee gebogen naden `3`.
2. **Vleugelnaad**: overal 1 px. Waar de naad 2 px dik was, is per kolom alleen de onderste pixel gebleven.
3. **Kopomtrek rechts**: doorlopende lijn `3` van (36,34) naar (42,46), zoals het model.
4. **Reparatie van een fout in r9**: de glans in beide ogen was door de modellijn-laag verdwenen (en is in r9 dus ook weg). De ogen zijn nu beschermd en de glans is terug: nabij (27–28,34–35), ver (17,34–35).

## Poten: model vs r10
| Pluim | Model (positie, vorm, klauwtjes) | r10 |
|---|---|---|
| A, links voor | x15–22, y48–56; ronde hangende pluim, vóór B; klauwtjes (18–20,55–57), 2 schuin | ovaal (18,5; 52) 3,6×4,3; klauwgroep (18–20,55–57), 2 klauwtjes. Klopt. |
| B, links midden | x22–31, y48–56; ronde pluim achter A; geen klauwtjes eronder | ovaal (26,5; 52) 4,5×4,0; geen klauwtjes (extra groep weg). Klopt. |
| B2, onder B | x25–30, y55–59; kleine pluim; klauwtjes (24–26,58–59) | ovaal (27,5; 57,3) 2,9×2,1; klauwgroep (24–26,58–59). Klopt. |
| Middenstuk | x30–43, y47–56; tan platen met donkere lijnen, achter de pluimen; klauwtjes (32–33,57–58) | tan platen met twee gebogen naden; klauwgroep (32–33,57–58). Klopt in plek. |
| C, midden voor | x34–41, y54–61; ronde pluim vóór alles; klauwtjes (35–39,60–61), 2 | ovaal (37,6; 57,4) 3,7×3,9; klauwgroep (35–39,60–61), 2 klauwtjes. Klopt. |
| D, rechts midden | x41–47, y52–58; ovaal achter C; klauwtjes (43–46,58–59), 2 | ovaal (44,2; 55) 3,2×3,6; klauwgroep (43–46,58–59), 2. Klopt. |
| E, rechts achter | x44–54, y46–56; grootste pluim, achteraan; geen klauwtjes | ovaal (49; 51) 5×5; geen klauwtjes. Klopt. |

In het model: 6 pluimen, middenstuk, 5 klauwgroepen. In r10 hetzelfde.

## Controle
- Alpha-diff 0. Open randen 0.
- Selout: 3 reeksen zonder afwisseling.
- Losse pixels 0, clusters < 3 px 0.
- Donker-aandeel 0,228.

## Zelf nagelopen (8× naast het model)
- **Kop/ogen**: zwart amandeloog met glans, ver oog smal, kinboog vloeiend, kopomtrek rechts doorlopend.
- **Kraag**: plukjes en onderrand over de pluimen; minder pluizig dan het model (het silhouet ligt vast).
- **Vleugels**: wit-crème met liggende tan schubbogen en een 1 px naad. De bogen zijn kleiner en eenvoudiger dan Jordi's wolkkrullen.
- **Poten**: ronde pluimen met 1 px omtrek; de klauwtjes zijn klein (2–3 px) en lezen op 1× als stipjes. Pluim C mist de warme schaduw onderaan die het model heeft.
- Close-ups alleen in `vel.png` en één uitsnede bekeken (gebruikslimiet).

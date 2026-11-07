# Lama fase 3: kleur ronde 5A2 (5 nov)

**Jordi (letterlijk):**
- "a is het beste"
- "waarom zijn de vlechten opeens bruin? Het oog kijkt meer boos dan nonchalant" ("bruin" = boos, volgens Claude)

Gemaakt vanaf `ronde5A/ronde5A.txt`. Alleen vlechten en oog zijn veranderd, met de hand in `bron/wijzigingen.txt`.
- **32 px gewijzigd** (oog 10, vlecht 22), **elders 0** (`controle.txt`).
- Alpha-diff met `silhouet_A`: +0 / −0. 0 open randen, 15 kleuren, palet ongewijzigd.

## Vlechten
- Terug naar de modelkleur (`kop_kleur_64_A`: bijna zwart): alle vlechtcellen `k`.
- Per knot (y14, 16, 18, 20, 22, 24) één klein koel lichtje `D` (donker blauwgrijs), linksboven in de knot, zoals zwart haar in Gen 3. Geen warm bruin meer.
- Scheiding met het oog alleen via 1 px kopkleur `S` (x26 y14–17, ongewijzigd uit 5A).

## Oog (lui, unimpressed)
- **Bovenlid licht:** de lidmassa in `C` (x22–25 y14) in plaats van `S`. Er staat geen donkere pixel boven het lid.
- **Lidlijn dalend naar buiten:** `kkk` op x22–24 y15, buitenhoek `k` op x25 y16. De binnenhoek ligt hoger dan de buitenhoek.
- **Oogwit 3 px:** x23–24 y16 en x23 y17.
- **Pupil 1 px**, laag en in het midden (x24 y17), met een bruine onderrand (x25 y17).
- **Kring zacht:** `SSS` op y18.
- Alles binnen x22–25 y14–18, ±1–2 px van de oogcellen van de bron.

## Eerlijk
- De lichtjes `D` zijn op 8× zichtbaar blauwgrijs. Op 1× lezen ze als glans op zwart haar; Jordi kan ze te blauw vinden.
- Het oog blijft klein (een oogwit van 3 px). De luie blik komt van het dalende lid, niet van de grootte.

## Bestanden
- `ronde5A2.txt`, `lama3.png`, `normal.pal`, `controle.txt`.
- `vel_ronde5A2.png`: 4× licht/donker, 1× (5A2 en 5A), kop 8× (5A | 5A2 | render), oog 12× naast Slakoth/Slaking.
- `bron/wijzigingen.txt`, `bron/bouw.py`, `bron/vel.py`.

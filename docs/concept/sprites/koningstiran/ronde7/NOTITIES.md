# Sapa Inca – ronde 7 (kleine bewerking op ronde 6b)

Basis: `ronde6b/sapa_inca.txt`; de wijzigingen staan onderaan in het blok "ronde 7". Bestanden: `sapa_inca.png/.txt` (stafkop A), `variant_top_zon.png/.txt` (stafkop B, verder identiek), `bouw.py`, `controle7.py` (diff per zone + buikbreedte per rij), `overlay.py` → `overlay.png`, `vel.py` → `vel.png` (lijf op 6× naast ronde 6b, overlay, stafkop op 10× naast ronde 6b en variant B, 1×), `kijk.py`, `uitlijning.npy`.

Jordi: "nu is het lichaam links weer net wat teveel weggesneden. en dat maakt gelijk de staf wat gekker, nu kan ik wel zien dat die op de juiste plek naar het lichaam gaat, dus zo slecht is dat niet. Het gele vlak in het midden heeft wel nog steeds een rare vorm, die mag nog wat ronder, aan de rechterkant is het beter, maar mag die nog een klein beetje dunner, we komen dichtbij nu. Poten ook netter afgewerkt." Daarna: "En de bovenkant van de staf moet nog mooier, dat is nu best lelijk afgewerkt, misschien dat we daar een soort van uiteinde van de staart idee van kunnen maken, dat het echt hybride staart en staf is".

## Wat er veranderde
1. **Lijf links voller:** de omtrek linksonder loopt nu als bolle boog (16,48) → (16,49) → (17,50) → (19,51) → (21,52) → (23,53) naar de dij. In ronde 6b was dat (16,48) → (17,49) → (19,50) → (21,51) → (23,52). Waar de staf het lijf in gaat, (20,48), is ongewijzigd.
2. **Gele buik als egaal ovaal:** de breedte neemt per rij geleidelijk toe en af (tabel hieronder). De top is smaller en ronder, en onderaan is de druppelpunt weg. Rechts is hij 1 px dunner (rechterrand x29–31 in plaats van x31–32), zodat er meer donkere flank overblijft. De zachte overgang a → l → m naar de flank schuift mee. Een vaste volgorde per rij: a-rand links, lichte top linksboven (y), g, a-kernschaduw rechts en onder.
3. **Stafkop (A, hoofdresultaat):** de zonneschijf met losse lavendel stralen (en de losse straal op (20,27)) is vervangen door het **uiteinde van een staartveer als scepterkop**: een spits toelopende veerpunt (x13–17, rij 24–29), symmetrisch rond de schacht x15, met een gouden schacht (y) door het midden, roestbruine vaan (t) en een gouden rand en punt (a). Eén gouden dwarsrij (rij 28) markeert de veerstructuur. Hij raakt de kroon niet: het kwastje links blijft 1 px vrij.
   **Variant B** (`variant_top_zon.png`): een gouden zonneschijf (5×4) die uit de veerpunt groeit, met de roestbruine vaan eromheen in plaats van losse stralen.
4. **Poten:** ongewijzigd. Alleen (23,53) is lijf geworden waar de vollere omtrek op de linkerdij aansluit.

## Breedte van de gele buik (a/g/y) per rij, ronde 6b → ronde 7
| rij | 6b | 7 |
|---|---|---|
| 34 | 25–29 (5) | 25–27 (3) |
| 35 | 22–31 (10) | 23–29 (7) |
| 36 | 21–32 (12) | 22–29 (8) |
| 37 | 20–32 (13) | 21–30 (10) |
| 38 | 20–32 (13) | 21–30 (10) |
| 39 | 20–32 (13) | 21–31 (11) |
| 40–42 | 20–31 (12) | 20–31 (12) |
| 43 | 20–30 (11) | 20–30 (11) |
| 44–45 | 21–30 (10) | 21–30 (10) |
| 46 | 21–29 (9) | 21–30 (10) |
| 47–48 | 22–30 (9) | 21–29 (9) |
| 49 | 23–28 (6) | 22–29 (8) |
| 50 | 24–29 (6) | 22–29 (8) |
| 51 | 25–28 (4) | 24–28 (5) |
| 52 | 26–28 (3) | 26–27 (2) |
Verloop ronde 7: 3, 7, 8, 10, 10, 11, 12, 12, 12, 11, 10, 10, 10, 9, 9, 8, 8, 5, 2: overal geleidelijk. De sprong 6b 9 → 6 (de druppel) is weg.

## Diff t.o.v. ronde 6b (`controle7.py`)
| Zone | Gewijzigd |
|---|---|
| kroon | **0 px** |
| gezicht en ogen | **0 px** |
| opgeheven rechtervleugel | **0 px** |
| staf boven de hand (rij 30–36) | **0 px** |
| poten | **0 px** |
| stafkop (rij 23–29) | 26 px |
| linkervleugel | 3 px: grensrandje (20,37–39), waar de buik nu 1 px later begint (a → m) |
| buik + lijf | 98 px (incl. (23,53), de aansluiting op de dij) |
| rest | 0 |
- Silhouet: +12 / −7 (1622 → 1627): +8 voor de vollere lijfomtrek linksonder ((16,49) t/m (23,53)), +4 en −7 bij de nieuwe stafkop (de oude stralen en de rechterrand van de schijf weg).
- 0 open randen; 15 kleuren + transparant; aandeel zwart 0,13.

## Zelf gekeken (1× en 6× naast ronde 6b, stafkop op 10×)
- De buik oogt ronder en egaler, en er is meer donkere flank rechts. Linksonder is het lijf niet meer weggesneden, en de staf verdwijnt nu beter achter de bolle rand.
- Stafkop A leest op 1× als een spitse gouden-bruine veerpunt, rustiger dan de schijf met losse stralen. B leest als een gouden knop op een veer.

## Eerlijk: wat nog niet klopt
- **Stafkop A** is smal (5 px) omdat het kwastje van de kroon links ernaast hangt. Op 1× leest hij als speerpunt of veer, minder als "koninklijke" scepterkop; de waaier van 3–5 veren paste er niet in zonder de kroon te raken.
- **Variant B** is een kleine schijf van 5×4 en lijkt sterk op A met een gouden knop.
- **Buik:** de top (rij 34–36) is nu smaller dan in ronde 6b, waardoor de bovenkant van de borst iets meer donker toont. De onderkant (rij 51–52) is een smalle ronding van 5 → 2 px vlak boven de dijen.

## Lessen
- Een buikvorm controleren via de breedte per rij (a/g/y): de "druppel" was een sprong 9 → 6 → 4 in drie rijen; een ovaal heeft stappen van hooguit 1–2 behalve bij de top en de bodem.
- Bij het wissen met '_' altijd de buren nalopen: een te breed wisblok haalde 2 px van het kroonkwastje weg (meteen hersteld).

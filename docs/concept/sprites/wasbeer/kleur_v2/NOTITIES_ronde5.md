# Kleur ronde 5 (maker-agent, 2 nov)

Basis `ronde4.txt` + de 8 reparaties uit `KEURING_ronde4.md`, alleen kleur. `rijen_ronde5.py` legt elke pixel vast als (oud → nieuw) en controleert de oude waarde. Uitvoer `ronde5.txt`, `ronde5.png`, `ronde5.pal`, vel `vel_ronde5.png` (ronde 5 naast ronde 4 op 4x licht/donker; 2x/1x naast olinguito, Coathief, zangoose, sneasel, linoone, ursaring, furret, sentret). Alpha-diff 0, geen open randen. 66 px + palet 8.

| # | reparatie | px |
|---|---|---|
| 1 | nabije hand: handrug a → 9 met één glans (24,26); slagschaduw 8 onder de klauwpunten (21–26, 34–35), (27,35) → 7 | 18 |
| 2 | nabije onderarm: bovenkant (28–31,29), (28–29,30) en elleboog (33,29) 2 → 4 | 7 |
| 3 | bovenarm hooglicht 3: waar nu 7 staat ((31,21–22), (32,23–24); de keurder noemde x 31 op y 21–24, maar op y 23–24 is x 31 de 4-voorrand) | 4 |
| 4 | staarthaak: lichte ring over de bocht (51–55,20), (51–54,21); schacht naast de binnenlijn (52,23–27) 4 → 5 | 14 |
| 5 | zakmond (36–37,20) d → 2 | 2 |
| 6 | verre dij lichtrand 6; (19,43) is een randpixel (selout 4 houden), daarom (20,43) | 9 |
| 7 | romp hooglicht 7 als boog verder het lijf in (19–21, 23–27, alleen waar 6) | 12 |
| 8 | palet 8 → oker (184,146,96) | palet |

Niet uitgevoerd (vragen aan Jordi): neus apart, wenkbrauwbalk, buideltint. Onderste staartring rechter (keuring §7) niet aangeraakt: valt buiten de 8 reparaties.

## Eigen zwakke punten (eerlijk)
- **Staarthaak:** de lichte ring maakt de bocht zichtbaar, maar op 1x leest de haakpunt nog niet als terugkrullende punt (geen opening in het silhouet).
- **Bovenarm:** het hooglicht 3 is 4 px; op 1x net een lichtstreep, nog geen arm.
- **Zakmond:** op 1x nog klein.
- **Oker 8:** maakt de schaduwen van de crème handen en buik warmer/geler; naast het warme wit kan het op 2x als vlek lezen (slagschaduw onder de hand).
- **Onderste staartring:** de grenzen zijn nog recht.

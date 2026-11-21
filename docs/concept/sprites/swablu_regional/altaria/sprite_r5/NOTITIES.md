# Onweerswolk-Altaria frontsprite, ronde 5 (vanaf r4, alleen de vleugels)

Opdracht (Claude): static, kuif, kop, hals en romp goed (diff 0); alleen de vleugels: per modelbol een eigen kap van ≥ 3×2 (hooglicht/licht linksboven, midden als tussenstap, donkere onderboog = naad naar de volgende bol), rand per bol volgens het model (inham bij een dip, ronde bult op de bol), vleugels mogen donker blijven.

Bestanden: `altaria_r5.png` (13 kleuren incl. transparant), `altaria_r5_8x.png`, `vel.png` (r5 | r4 | model op schaal | game-Altaria 8× / rechtervleugel 16× naast het natieve model / linkervleugel 16× naast het model / 1× op licht en donker), `bouw.py` (stap 11 `VL5`/`VR5`), `basis.py`, `controle.py`, `vel4.py`. Bouwen vanuit `altaria/`: `python3 sprite_r5/bouw.py && python3 sprite_r5/vel4.py`.

**Diff r5 ↔ r4: 89 px, links 47, rechts 42, elders 0.** Alpha-diff: linkervleugel 2 px ((8,16) erbij, (10,18) weg), rechtervleugel 0.

## Bollen, gemeten op het model (blokhelderheid per spritepixel, ×3 = L)
Linkervleugel (bovenrij licht, onderrij donker zoals het model):
- L1 kap X7–9, Y17–18 (L 180–190) → sprite (6–8,17) H H L, (6–8,18) L L M; onderboog (8–9,19) en (7–9,20).
- L2 kap X11–14, Y19–21 (L 160–186) → (11–13,19) H H L, (11–13,20) L L M; onderboog (10–13,21).
- L3 kap X15–18, Y20–22 (L 155–190) → (15–16,21) H H, (15–17,22) L; onderboog (14–17,23).
- L4 kap X16–18, Y23–25 (L 125–170) → (16–18,24) L L M, (16–18,25) L M M; onderboog (15–18,26).
- L5 (onderrij links, model L ±100) → (7–9,22) H H L, (7–9,23) L L M; onderboog = de bestaande selout-lijn Y25 X8–11.
- L6 (onderrij midden) → (11–12,23) L L, (11,24) L, (12,24) M; onderboog (12–13,25).
Rechtervleugel:
- R1 punt, kap X56–58, Y17–18 (L 150–190) → (57–58,17) H H, (59,17) L, (56–58,18) L; onderboog (56–59,19).
- Ra kap X47–51, Y20–21 (L 150–186; bovenrij valt onder de kuifstreng) → (47–48,21) H H, (49–50,21) L, (47–49,22) L; onderboog (48–50,23), (51,22).
- Rb kap X44–47, Y22–23 (L 140–177) → (46,22) H, (44–45,23) L, (46,23) H; onderboog (44–47,24).
- Rc kap X40–42, Y24–26 (L 130–177) → (41–42,25) H H, (40–42,26) L; onderboog (40–41,27), (43–44,26).
- Rd kap X43–44, Y26–27 (L 150–160) → (42–43,27) L L, (42,28) L; onderboog (42–45,29).
- Re (X52–55, Y17–20) ligt onder de kuifpunt en de static: niet aangeraakt (diff 0 daar).

## Rand
- Links: bult L1 (top Y16, X6–8; (8,16) erbij: modeldekking 5/9), inham tussen L1 en L2 ((10,18) weg; modelhelderheid daar L87 = de naad), bult L2 (top Y18, X11–13), L3 (Y20–21). Linkerrand: bult L1 X5 Y17–19, inham Y20–22 (X6).
- Rechts: niet veranderd; de modeldips liggen daar dieper dan 1/3 px niet (dekking aan beide kanten van de naad 8–9/9), de bestaande trap volgt Rc/Rb/Ra en de punt R1 (top Y16 X57–59, schouders Y17).

## Controle
13 kleuren incl. transparant; zwart alleen in de pupillen; geen lichte kleur op de buitenrand; pixels zonder 8-buur van dezelfde tint: dezelfde 12 als r4 (kuif-takpunten, oog/wang, vonk, halsrand, static-hoekjes), geen nieuwe in de vleugels.

## Eerlijke twijfels
- De rechtervleugel leest op 1× minder als bollen dan de linker: de kappen zijn kleiner, de lange static-lijn erover (bevroren) trekt meer aandacht, en Re zit onder kuif en static.
- De kappen zijn per bol op modelplek gezet (pixels niet uit de kale reductie, zie lijst hierboven); de vorm per kap is 3×2 met licht linksboven, geen modelvorm op 1/3-schaal.
- Randbulten zijn klein (2 px alpha); dieper golven zou meer pixels kosten dan het model op 1/3 rechtvaardigt.

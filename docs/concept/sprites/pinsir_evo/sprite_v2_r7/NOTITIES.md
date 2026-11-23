# Pinsir-evolutie v2, frontsprite r7 (23 nov)

r7 = r6 + de 4 reparaties uit `sprite_v2_r6/KEURING.md` (BIJNA). Elke reparatie staat in het script met een assert op de oude index.
- Bouwen vanuit `docs/concept/sprites/pinsir_evo/`: `python3 sprite_v2_r7/bouw.py && python3 sprite_v2_r7/vellen.py`.
- Diff tegen r6: 89 px. Het script controleert dat elke gewijzigde pixel bij een reparatie hoort.
- Lijnpixels (1/2) zijn alleen veranderd waar de keurder dat vroeg: (39,45) en (40,45) worden 3, (37,62) wordt 1.
- Palet = r6 (`sprite_v2_r6/palet.py`), 15 kleuren, index 0 transparant.

## 1. Korrel (60 px)
- **Telling.** De bruine vlakjes kleiner dan 3 px heb ik op dezelfde manier geteld als de keurder (4-buren, index 3/4/5): r6 had er 61, net als in de keuring.
- **Werkwijze.** Elk vlakje neemt de meest voorkomende bruine buurtint (3/4/5/14) die anders is dan het eigen vlakje. Wordt dat 14, dan wordt het 5, zodat hooglichten niet groeien. Dit herhaal ik tot er niets meer verandert.
- **Beschermd:**
  - het gezicht (x11–22, y20–33);
  - de klauwen (room);
  - de stekelflanken: bruin binnen 2 px van transparant, boven y31;
  - de hooglichten 14;
  - de lichte randstreep van het schild;
  - alle pixels van de reparaties 2–4.
- **Uitzondering op de stekelbescherming.** Vrijgegeven omdat de keurder ze noemt: (30–31,20), (35,18), (34,19) en (34–35,23).
- **Randstreep doorlopend.** (29,20) en (31,19) gingen van 4 naar 5. De streep loopt nu ononderbroken: (34,18), (31–33,19), (26–29,20).
- **Keurderlijst.** Alle genoemde pixels zijn veranderd, behalve (52,41). Dat pixel hoort nu bij een groter vlak 3, omdat (52,39–40) eerst 3 werden. Het is dus geen los vlakje meer.
- **Buiten de lijst.** (25,50) was een los bruin pixel 5 midden in de buik en werd room 6, de buurtint.
- **Na de opschoning: 20 vlakjes over.** 17 daarvan zijn beschermd (gezicht, stekelflanken). Drie staan buiten die uitzonderingen en ik heb ze laten staan, want ze hebben geen bruine buren:
  - (18–19,40): onder de kaak, tussen rood en lijn;
  - (11,42): pols van de verre arm, tussen lijn en rood.

## 2. Nabije arm lichter dan het lijf (17 px)
- Bovenarm: (33–35,37–39) en (33–34,40–41) gaan van 4 naar 5.
- Sikkel: (35,39) en (36,38–39) gaan van 3 naar 4.
- (32,37–38) blijft 5 als lichtrand. De slagschaduw op het lijf blijft 3.
- Onder de hand: (39,45) en (40,45) gaan van 1 naar 3, als slagschaduw op de dij. Rij 44 blijft de buitenlijn, en (36,45) en (37,45) blijven 1.

## 3. Knie als gesloten ring (9 px)
- In 3: boven (37–39,50), linksboven (36,51), links (35,52–53) en (35,54). Rechts en onder blijft de ring 2, zoals in r6.
- Hooglicht: (36,52) wordt 5 en (38,52) wordt 14. (37,52) blijft 14, zodat het hooglicht nu op (37–38,52) binnen de ring ligt.

## 4. Buitenrand
- (37,62) gaat van room 6 naar 1.

## Zelf gezien (1×/2×, `vel.png`)
- De nabije arm valt nu op als lichtere vorm vóór het lijf.
- De knie leest als een ronde schijf.
- Het lijf is rustiger dan in r6.
- Er is geen nieuwe keurder gebruikt: de herkeuring (telling + 1×/2×) moet nog.

## Bestanden
- `pinsir_evo_v2_r7.png`: de sprite.
- `bouw.py`: de opbouw.
- `vellen.py`: maakt de vellen.
- `vel.png`: r7 | r6 | model op 6×, plus 1× en 2× naast Tyranitar, Aggron en Pinsir, op wit en op donker.
- `onderdelen.png`: rug, hoofd, armen en benen op 12×, telkens r7 | r6 | model.

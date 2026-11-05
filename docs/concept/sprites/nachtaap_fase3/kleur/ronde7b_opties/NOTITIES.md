# Nachtaap fase 3, ronde 7b: massa's in de romp (vanaf ronde 7 optie B)

Claude-check op ronde 7:
- Het verschil met ronde 6 is op 1× klein.
- Het midden van de romp is nog één groot vlak basistint (±x26–42, r32–44).

Jordi: "een lichaam is niet bepaald 1 vlak namelijk en een staart groeit nooit volledig egaal ergens uit".

## Bestanden
- `opties.py`: een pixeltabel bovenop `../ronde7_opties/optie_B.png`, met de hand gezet.
- `check.py`: alpha-diff, bevroren vakken en open randen.
- `vlakken.py`: de grootste egale rechthoek in de romp.
- `vel.py` maakt `vel_opties.png`, met ronde 6, ronde 7 B, matig en sterk. Per versie staan daarop 3× licht en donker, 1× licht en donker en een close-up op 8×. Ernaast staan foto 6 en 7, Vigoroth, Zangoose, Aipom en de Machamp-rug.

## Opbouw: drie massa's met kern + gebogen schaduwband
Per massa: de kern ligt linksboven, eronder loopt een schaduwband (3) van ±2 px. Zo werken de buik van Primeape en de rug van Machamp in de back sprite, vertaald naar 4 vachttinten.

- **Borstkas** (onder de schouder, achter de healerarm):
  - De kern (5) zit bij x27–29 r31–37.
  - De schaduwband loopt schuin van x27 r39–40 op naar x31–32 r37–38.
- **Buik:** de bovenkant blijft 4, de onderkant krijgt de bestaande schaduw (3) van r41–44.
- **Bekken/heup:**
  - De kern is het hooglicht van het been uit optie B, iets ronder (x33–36 r31–36).
  - De schaduwband loopt linksonder van x33 r37 naar x36 r41 en gaat over in de liesplooi.
  - De schaduwkant rechts is breder en gebogen (x39–41 r36–40).
- **Taille:** de banden van borstkas en heup komen samen in een zachte Y bij x31–33 r37. Elke band loopt verderop dood: de borstband raakt de armplooi niet en de heupband raakt de rechterschaduw niet. Er zijn dus geen gesloten lijnen en het blijft één lijf.
- **Been en staart:** gelijk aan optie B (plooi uit de inham, licht van het been loopt in de heup, staart met eigen lichtkant, plooi in 2 en schaduwkraag).

**Matig (84 px t.o.v. ronde 6):** de opbouw hierboven met banden van 1–2 px.

**Sterk (97 px):**
- De kernen van borstkas en heup zijn groter (5).
- De heupband is overal 2 px.
- De onderkant van de buik is donkerder.
- De heup rechtsonder is donkerder.
- Het diepste punt van de liesplooi is 2.
- Er staan geen losse 2-stippen in de romp. Een eerdere poging met 2 in de taille las op 3× als scheurtjes en is weggehaald. Ook een buikkern in 5 las als vlek en is weggehaald.

## Bewijs
- `check.py`: beide versies hebben **alpha-diff 0**. Er zijn alleen tinten 1–5 gebruikt, binnen de zone x27–46 r29–45. Het palet is identiek.
- In de bevroren vakken is **0 px** veranderd:
  - kop/gezicht/maan
  - vuistarm
  - healerhand + gloed
  - staartspiraal x≥48
  - beide voeten
- **Open randen:** 0 nieuw. De 27 treffers zijn de turkooise gloedrand (index 12), gelijk aan ronde 6.
- `vlakken.py` meet de grootste egale rechthoek in de romp:

| versie | grootste egale rechthoek |
|---|---|
| ronde 6 | 49 px (7×7, tint 4) |
| ronde 7 B | 60 px (12×5, tint 4) |
| 7b matig | 21 px (3×7, tint 4, de middenkolom van dij en heup) |
| 7b sterk | 21 px (3×7, tint 3, de schaduwkant van de heup langs de omtrek) |

In geen van beide 7b-versies ligt nog een groot egaal vlak midden in de romp.

## Eigen check (1× en 3×, licht en donker, naast ronde 6 en B)
- **Ronde 6:** drie platte schijven, en de lichte driehoek van been en rug.
- **Matig:** op 1× lees ik een borstkas, een heup waar het been uit groeit, en de Y bij de taille. Het blijft rustig.
- **Sterk:** op 1× is het duidelijkst. Ik lees drie bollen die in elkaar overgaan: borstkas, buik en heup. Het been komt uit de heup en de staart heeft een eigen aanzet.
- Beide versies vind ik op 1× duidelijk beter dan ronde 6. Mijn voorkeur is **sterk**. Matig is het alternatief als Jordi het rustiger wil.

## Lessen
- Een massa lees je aan een **schaduwband van 2 px onder de kern**, niet aan een lijn van 1 px. Banden van 1 px in 3 lezen op 3× als krassen.
- Een losse 2 midden in de romp leest als een scheurtje. Gebruik 2 alleen in het diepste punt van een plooi die al aan de omtrek begint.
- Meet egale vlakken met een rechthoek-zoeker (`vlakken.py`), niet met samenhang. Doodlopende plooien laten het grondvlak per definitie samenhangen.

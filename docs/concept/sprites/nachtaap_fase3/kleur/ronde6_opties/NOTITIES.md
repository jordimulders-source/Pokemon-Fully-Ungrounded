# Nachtaap fase 3, ronde 6 opties: aanzet van het opgeheven been (heup/rug)

Basis: `../ronde6/nachtaap_fase3.png` + `normal.pal` (palet ongewijzigd). Script: `opties.py` (rijtabel per optie: linker omlijning, lichtrand, middentoon, schaduw, zwarte omlijning), bewijs: `check.py`, vel: `vel.py` → `vel_opties.png`.

Jordi (letterlijk): "maar ik vind nu wel met deze shading dat het bovenste been weer half uit het lichaam lijkt te steken." + foto 6 en foto 7.

## Diagnose van ronde 6
1. **Taille vlak boven de wortel:** de rechter omtrek springt op r24–25 van x38 naar x37 en weer terug (de schaduwband wordt daar 1 px). Het been knijpt in vlak voordat het het lijf in gaat: een buis met een hals.
2. **Harde hoek rechts (r27→28):** recht naar beneden en dan meteen 45° naar de staartwortel. Links springt de omtrek in één rij 3 px naar de rug (r29→30).
3. **Licht plateau onder het been:** de middentoon (4) van het been stopt op r29 en daaronder ligt een vlak in kleur 5 (r28–33, x29–37). Het been staat dus als een losse buis óp een licht vlak. Op foto 7 is de rug één vlak; het licht is een rand die van de rug over de heup het been in loopt.

## Opties (alle drie: lichtrand van 2 px (5) langs de linker omlijning die onderaan overloopt in het lichte schoudervlak; middentoon (4) van de dij loopt door in de heup; schaduw (3) van 2 px langs de rechterkant, die in de lies bij de staartwortel uitkomt, waar het bestaande donkere vlak al ligt)
- **A, toon + 6 px afronding** (33 px, waarvan 6 aan de omtrek): de taille op r24–25 is dicht (x38). Beide hoeken aan de wortel zijn 1 px afgerond (rechts r26–27 x39, r28 x40; links r27 x30). Het lichte plateau onder het been is middentoon geworden. Het been blijft smal: dit is de kleinste ingreep.
- **B, dij breed aan de wortel** (76 px, waarvan 23 aan de omtrek): vanaf r23 wordt de dij breder. Links loopt een holle curve naar de rug (x31→30→29→28→27, r23–30). Rechts loopt één doorlopende lijn naar de staartwortel (x39 r23–24, 40 r25–26, 41 r27–28, 42 r29–31, 43 r32–33). Op r29 is de wortel 15 px breed (x28–42). Tussen de heup en de staart blijft minstens 1 kolom lucht (x44).
- **C, de hele dij taps** (116 px, waarvan 43 aan de omtrek; mijn voorkeur): zoals op foto 6 en 7 is de dij dik bij de heup en wordt hij geleidelijk dunner naar de knie. Ik begin daarom al op r18 en niet pas onderaan. Rechts: x39 r18–20, 40 r21–23, 41 r24–26, 42 r27–31, 43 r32–33. Links: x32 r18–19, 31 r20–23, 30 r24–26, 29 r27–28, 28 r29, 27 r30. Breedte: r17 7 px, r22 10 px, r29 15 px. Zo is er geen trechter die pas aan het eind uitwaaiert. De dij leest als een been dat uit de heup groeit, en de rug en de heup blijven één vlak.

## Bewijs (`python3 check.py`)
- Gewijzigde zone: A x30–40 r23–33, B x28–43 r23–33, C x28–43 r18–33.
- Bevroren vakken, 0 px diff bij elke optie: kop/gezicht/maan (x0–19 r14–43), vuistarm (x0–25 r14–31), healerhand + gloed (x1–23 r44–63), staart (x≥44 r0–41) en het onderbeen en de dij (r≥34). Het palet is identiek.
- Open randen: 0 in de werkzone. Er staat nergens een vachtkleur naast transparant. De 27 treffers in de hele sprite zijn de turkooise gloedrand van de healerhand, en die is gelijk aan ronde 6.

## Eigen check (1×/3× licht en donker, 8× close-up, naast ronde 6, foto 6 en foto 7)
- Ronde 6: op 3× en 1× zie ik de buis met de hals en het plateau.
- A: op 3× loopt de dij in toon door in het lijf, en het plateau en de hals zijn weg. Het been is wel even smal als in ronde 6.
- B: op 1× komt het been duidelijk uit een brede heup, en de rechter lijn loopt als één boog naar de staartwortel.
- C: dit is het meest natuurlijk, vooral op 1×: een dikke dij die naar boven taps toeloopt, zoals het been op foto 6. De dij is aan de wortel dikker dan de bovenarm, zoals bij echte apen; de verhouding met de vuistarm blijft natuurlijk.
- Mijn volgorde is C > B > A.

## Lessen
- "Been steekt uit het lijf" komt zelden alleen door de shading. Kijk ook naar de omtrek vlak boven de wortel (een taille van 1 px), naar een harde hoek in de omtrek en naar een licht vlak waarop de middentoon van het been eindigt.
- Een dij is een kegel over de hele lengte: laat de verbreding hoog beginnen, anders oogt de wortel als een trechter.

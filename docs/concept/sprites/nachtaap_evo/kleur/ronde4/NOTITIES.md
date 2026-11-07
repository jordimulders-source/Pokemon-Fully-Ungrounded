# Nachtaap fase 2: kleursprite ronde 4

In deze ronde is alleen de maan veranderd: die is overgenomen uit variant **D2**, de keuze van Jordi (`../maanvarianten/variant_D2.png`). De zone is x 4–24, y 36–48. Al het andere is ronde 3 en bevroren.

## Bewijs
- **Diff buiten de zone t.o.v. ronde 3:** 0, met hetzelfde palet.
- **Alpha-diff:** 0 (1459 px, zowel tegen de `.txt` als tegen de `.npy`).
- **Open randen:** 0.
- **Afwijking t.o.v. D2:** 11 px in totaal.
  - **Vorm (wit + zilverlila):** 3 px anders dan D2.
    - (16,44) is de glans van het nabije oog. D2 had die per ongeluk op vacht gezet; ik heb hem teruggezet, want de ogen zijn bevroren sinds ronde 2.
    - (6,50) en (20,50): D2 heeft daar twee losse maanpixels. Ze liggen buiten de zone en hangen niet aan de punten (op y 49 staat vacht), dus ze zijn niet overgenomen.
    - Binnen de zone is de vorm van D2 dus gelijk.
  - **Tint:** 1 px wit ↔ zilverlila omgewisseld. Op (20,43) is zilverlila wit geworden, zodat de rechterpunt bovenaan als wit leest; de linkerpunt is ook wit.
  - **Vacht rond de maan:** 7 px.

## Opschoning in de zone
- **Vacht rond de maan:** het script had de vacht plat naar `b` gezet. Ik heb het kopvolume teruggegeven:
  - kruin rechts van de sikkel licht (`l`, y 37–39);
  - daarna `b`, en `s` naar de rechterrand (die stond er al).
- **Holte onder de sikkel:** de linkerrand (x 11, y 42–43) is `l`, omdat licht linksboven daar valt.
- **Sikkel:**
  - licht linksboven: de linkerhelft en de linkerpunt wit;
  - zilverlila langs de buitenrand rechts, langs de binnenrand van de rechterhelft en in de rechterpunt.
- **Losse pixels:** nieuw is alleen (16,37) `n`, een afrondingspixel aan de bovenkant van de sikkel. De andere zijn bewust en stonden er al.

## Vel
- De kop op 8×: ronde 3 | D2 | ronde 4 | onderlaag.
- De sprite op 4×, 3× en 1×, op licht en op donker.

## Lessen
- **Een variant uit een script altijd vergelijken met de laatst bevroren versie, ook buiten de zone.** D2 had een overschreven oogglans en twee zwevende pixels onder de punten.
- **Een sikkel leest als maan als hij dik is in het midden, tapse punten heeft en een ronde holte.** Het wit zit aan de lichtkant en zilverlila aan de schaduwkant en de binnenrand. De vacht in de holte krijgt licht aan de kant waar het licht vandaan komt.

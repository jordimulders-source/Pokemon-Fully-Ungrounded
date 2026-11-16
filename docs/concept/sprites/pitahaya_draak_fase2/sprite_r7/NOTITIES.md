# Pitahaya-draak fase 2, sprite r7 (maker): wig donkerder

Jordi (letterlijk): "ja kijk, en dan moet wat boven dat grijs zit dezelfde tint krijgen of nog zelfs een tint donkerder, binnenkant bovenkant mond"

Gelezen als: de wig boven de donkergrijze plooi krijgt de plooitint (A) of een tint donkerder (B). In het beeld zit boven de plooi alleen de wig, en daarboven de zwarte kaaklijn. Er is dus geen andere lezing die past.

Op `pitahaya2_r6.png`, script `maak_r7.py`, vel `vel7.py` → `vel.png`. Het vel toont de bek op 12× (model | r6 | r7A | r7B), de hele sprite op 8× (A | B), en 1× en 2× op licht en donker.

## Wijzigingen (5 px per versie; afwijkingenlijsten `pitahaya2_r7A_afwijkingen.txt` en `pitahaya2_r7B_afwijkingen.txt`)
- **Wig, 4 px:** (10,44), (12,44), (13,44) en (11,45) gaan van w (191) naar:
  - **A:** de plooitint v (155,154,159);
  - **B:** een nieuwe tint "donkerst" (120,119,125). Dat is een stap van 35 helderheid onder v, in dezelfde koele toon (blauw 5–6 hoger dan rood).
- De pit (11,44) blijft.
- **Keuring_r6:** (14,45) gaat in beide versies van w naar v. Daarmee loopt de plooi door tot de kaaklijn, zoals in de r5-meting (nx 44, ny 95,5). Het grijs achter de tong raakt de wig niet meer.

**Bewijs (asserts):** alleen deze 5 px zijn veranderd, de diff daarbuiten is 0, het silhouet is gelijk en er is geen dambord in de bek.
**Palet:** A 14 kleuren, B 15 kleuren (incl. transparant). De grijsgroep heeft in B 4 tinten: W, w, v en donkerst.

## Zelf getoetst
- **A:** wig en plooi zijn één donkergrijs vlak boven de witte tong. Op 2× leest dat als de schaduw van de bovenkant van de bek. De pit is goed zichtbaar (helderheid 155 tegen 43).
- **B:** de wig is donkerder dan de plooi. Op 12× zie je de trap donkerst → donkergrijs → wit, op 2× nauwelijks verschil met A. De pit is zichtbaar (contrast 77).
- **Probleem B:** de pit deelt de wig in stukken. (10,44) en (11,45) worden daardoor **losse pixels** van de donkerste tint: geen 4-buur in dezelfde tint, alleen pit, lijn en plooi eromheen. Dat botst met "geen losse pixels". Oplossen kan alleen door de pit te verplaatsen of weg te halen. Dat heb ik niet gedaan, omdat de pit moet blijven.

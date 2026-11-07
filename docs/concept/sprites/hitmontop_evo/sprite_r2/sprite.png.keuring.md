# Keuring sprite_r2/sprite.png (Hitmontop-evolutie, capoeira)

Bron: `docs/concept/sprites/hitmontop_evo/sprite_r2/sprite.png` (8×, 8× met raster per 8 px, 1× en 2×, plus pixeldump van de indexen), `docs/lessen/SPRITE_KERN.md`, `docs/concept/sprites/hitmontop_evo/SPEC.md`, `referenties/pose_eenhandsstand.webp`, `graphics/pokemon/hitmontop/anim_front.png` (bovenste 64×64), ter vergelijking `graphics/pokemon/hitmonlee`, `medicham`, `machop` (anim_front.png, bovenste 64×64). NOTITIES.md van de maker en eerdere keuringen niet gelezen.

## Blinde indruk (vóór de context)
Een tanige, bruinhuidige vechter in een eenarmige handstand: één dunne steunarm recht omlaag op een ronde bal-hand, het lijf schuin, twee lange blauwe benen in een V omhoog, rode koordjes die van de heup omlaag hangen. Het silhouet (omgekeerde Y) leest op 1× meteen als handstand. Wat raar is:
- De kop is groot, plat en breed, staat helemaal rechtop naast het lijf en heeft een **egale bruine pet/baret** als haar. Ik las het eerst als een muts, niet als haar; dreads zie ik niet.
- Het **bultje op het lijf** (rond x 37–48, y 17–31) leest als een knobbel of tweede bal, niet als een arm. Pas op 8× zie je dat het de vrije arm is met de hand direct aan de elleboog.
- De benen eindigen in **punten zonder voet**: de broek loopt tot het eind door, de "klauwen" zijn grijze stipjes van 1 px.
- Benen, steunarm en de lichte rand van het lijf hebben **evenwijdige strepen** (buis-shading).
- Het linkeroog plakt tegen de buitenlijn van de kop; de mond is een frons.
- Geen hoorn gezien.

## Per onderdeel
**(a) Hoofdvraag: pose en verhoudingen.**
Lijkt op: de foto (gespiegeld). Een verticale steunarm, het lijf schuin met de heup als hoogste punt van de romp, de kop laag naast het lijf, de V-split met de voeten als twee hoogste punten, het cordão dat met de zwaartekracht hangt. Op 1× leest het als handstand, en de lengte van lijf en benen klopt met een vechter van het formaat Hitmonlee.
Wijkt af in: de kop is ±25×20 px, net zo breed als het hele lijf, en staat stijf rechtop. Daardoor lijkt hij er naast geplakt (in de foto kantelt de kop met de kruin naar buiten). Dat is te verdedigen, want de SPEC vraagt "kop = Hitmontops kop rechtop als skelet". Herkenning als **Hitmontop**-evolutie op 1×: het leest als Hitmon-familie (bruin, blauw, ronde handen), maar niet specifiek als Hitmontop. De hoorn is onzichtbaar en de kop leest als een pet-kop.

**(b) Kop en haar.**
Lijkt op: Hitmontops brede, platte kop. Het haar zit alleen op de schedel (y 24–31); er staat niets op keel of kin, en de nek zit correct onder/achter de kaak (verbinding alleen op y 38–43, met een open gat erboven op x 29–34).
Wijkt af in: het haar is een gladde, ovale kap (bowlcut/baret) met ruis van losse donkere pixels. Het is geen Eddy Gordo-achtig haar met dreads of opgebonden lokken. Achter het rode haarelastiekje (x 27–28, y 26–30) zit een gestreept plukje (x 29–33, y 28–32) in huidtinten: dat leest als een oor of een pleister, niet als dreads. Het haar gebruikt dezelfde tinten als de huid (index 4/5 plus 14), dus op 1× is het alleen "donkerder huid". Hoorn: een lichtbeige noppie van 2×2 (x 17–18, y 24–25) dat als glans in het haar leest.

**(c) Anatomie.**
Lijkt op: het aantal klopt (kop, 2 benen, steunarm, vrije arm, 2 handen). De steunarm zit onder aan het lijf (de schouder) en de koordjes zitten aan de heup.
Wijkt af in: de vrije arm (x 36–48, y 17–31) heeft geen onderarm. De ronde hand (x 43–48, y 21–28) zit direct onder de elleboog (y 17–20), en arm en lijf hebben geen binnenlijn ertussen, dus op 1× een bult. De voeten hebben geen eigen vorm of enkel (vooral de linker, x 26–33, y 1–6). De steunarm is 4–5 px breed op een kop van 25 px: Hitmontop-dun, acceptabel.

**(d) SPEC-punten.**
- Kleine hoorn: aanwezig maar onleesbaar. **Fout.**
- Lange aansluitende blauwe broek: ja.
- Langer lijf: ja (±30 px van heup tot schouder).
- Langere benen: ja. Kleinere blauwe klauwvoeten: de voeten zijn niet te onderscheiden en de klauwen zijn stipjes van 1 px. **Fout.**
- Koordjes aan de broek (x 51–56, y 26–39) en om beide bovenarmen (vrije arm x 35–39, y 29–30; steunarm x 33–38, y 47–49): ja.
- Ronde handen: ja.
- Afro-Braziliaans/Eddy Gordo-haar: nee. **Fout.**
- Kijkt de kijker aan: ongeveer (3/4 naar links), maar het gezicht zit in de linkerhelft van de kop.

**(e) Netheid (SPRITE_KERN).**
- Palet van 16 kleuren, ≤ 3 tinten per groep: ok.
- Licht linksboven: ok.
- Selout op de lichte kant bij lijf en armen, maar de kop is rondom zwart omlijnd (inconsequent).
- **Banding:** beide benen zijn over de hele lengte strepen van 2 px (donker, midden, licht, navy) evenwijdig aan de rand (y 1–27). De steunarm is elke rij identiek "rand-licht-midden-schaduw" (x 33–37, y 45–52). Het lijf heeft een doorlopende lichte baan langs de linkerrand (x 35–38, y 17–45).
- Losse donkere pixels in het haar (x 11–26, y 28–31).
- Pure witte glans van ±7 px op de onderste hand (x 32–36, y 56–59) en op de vrije hand: te wit en te groot voor huid.
- De voeten raken bijna de bovenrand (y = 1).

8× bekeken: ja (met raster). 1× bekeken: ja (ook 2×).

## NODIG
1. **Haar (x 9–34, y 24–33):** vervangen door Eddy Gordo-achtig afro-Braziliaans haar: duidelijke dreads/lokken, opgebonden en vallend met de zwaartekracht, met een eigen donkerbruine haartint die op 1× van de huid te onderscheiden is. Alleen op de schedel, niets op keel, kin of schouder. Geen ruispixels. Het plukje in huidtinten op x 29–33, y 28–32 weg, of omzetten naar echte dreads in de haartint.
2. **Hoorn (x 16–20, y 22–26):** klein maar leesbaar (≥ 3 px hoog), van Hitmontops hoorn afgeleid (vorm en kleur) en in of tussen het haar. Nu leest hij als glans.
3. **Vrije arm (x 35–49, y 16–32):** moet op 1× als gebogen arm over buik/heup lezen: bovenarm, elleboog, een zichtbare onderarm en de ronde hand op de heup, met een binnenlijn tegen het lijf. Nu zit de hand aan de elleboog vast en leest het geheel als een bult.
4. **Voeten (links x 25–34, y 0–6; rechts x 56–63, y 0–7):** eigen voetvorm met enkelovergang (blauw, kleiner dan bij Hitmontop) en leesbare klauwen (licht/wit, ≥ 2 px, zoals bij Hitmontop). Nu lopen de broekspijpen in een punt door. Laat 1–2 px marge tot de bovenrand.
5. **Banding weg:** benen (y 1–27), steunarm (x 33–37, y 45–52) en de lichte baan langs de lijfrand (x 35–38, y 17–45). Schaduw als sikkel die de vorm volgt, met variatie in breedte bij knie, dij en pols, geen gelijke strepen over de hele lengte.
6. **Ogen (x 9–23, y 32–37):** het linkeroog los van de buitenlijn (nu versmolten op x 9–10, y 35), en de grootteverhouding logisch maken (het verre oog nu groter dan het nabije). Liefst pixel voor pixel van een echte sprite overnemen (Hitmontop of Hitmonlee).

## POLIJSTEN
1. Kop-omlijning: selout aan de lichte kant (linksboven), net als lijf en armen. Nu rondom zwart.
2. Witte glans op beide handen kleiner maken en geen puur wit, maar de lichtste huidtint met hoogstens 1–2 px wit.
3. Uitdrukking: de frons (x 15–22, y 37–39) leest als pijn of chagrijn. Het gezicht staat in de SPEC nog open, dus aan Jordi voorleggen.
4. De grijs-witte polsband op de steunarm (x 33–37, y 53–54) staat niet in de SPEC; schrappen of bewust maken.
5. Overweeg de kop een paar graden met de kruin naar buiten te kantelen (zoals op de foto), zodat hij minder los naast het lijf lijkt. Alleen als Jordi's "rechtop" dat toelaat.

## Reparatie of opnieuw?
**Met reparaties op te lossen.** Het silhouet (omgekeerde Y, V-split, steunarm, cordão) en de verhoudingen van lijf en benen kloppen en zijn bruikbaar. Opnieuw doen hoeft alleen voor de zones haar, hoorn, vrije arm en voeten, plus een shadingronde op benen, arm en lijf. Pixeldiff 0 buiten die zones.

Oordeel: FAIL

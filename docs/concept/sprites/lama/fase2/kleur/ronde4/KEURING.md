# Keuring kleurronde 4 lama fase 2 (verse keurder, 3 nov)

Vel: `keuring_vel.png` (lama op 1× en 3×, naast Mareep, Flaaffy, Girafarig, Ponyta, Numel, Slakoth, Stantler, Houndour, Camerupt en Rapidash, op licht en op donker; onderaan oog A/B/C op 3× en 1×). Eigen oordeel gevormd vóór het lezen van NOTITIES.md.

## Oordeel: **NEE**
Kop, hals, pose, halsband, handschoenen en kwasten staan goed en leveren een lama op. Jordi's belangrijkste vraag wordt niet ingelost: "het lichaam plus de nek moet fluffy zijn". Op 1× is het lijf een vlakke karamelkleurige plank met spikkels, geen wolmassa. De maker noemt zelf vier zwakke punten (fluffy "aan de grens", verre achterpoot, handschoenen, oog), en elk daarvan telt als fail. Geen nieuw silhouet nodig: alles hieronder past in de kleur plus ±1 px.

## Toetsing op 1×
1. **Wol (lijf en hals): fail.** Naast Mareep en Flaaffy is het vlak en korrelig. Het lijf is bijna helemaal middentint `l` met losse `b`/`h`-spikkels (y32–39). De "wolbogen" op y37–39 lezen als een gestreepte band en de lichtste tint `h` komt maar op 32 px voor (Mareep: 28 % lichtste tint). Er is geen licht koepelvlak linksboven en geen ronde schaduwsikkel, dus het lijf heeft geen volume. De hals laat een kolom stippels zien (`h` om de rij op x16–17), geen wol. Rechte omtrek: rug y26 x37–49 (13 px), achterwerk x50 y27–39 (13 px), borst x14 y29–37 (9 px), buik y40–41. Dat maakt de doos.
2. **Staart: fail.** Een knobbel van 4×3 (x47–50 y23–25) bovenop de hoek van het achterwerk. Op 1× leest het als een bultje of een oortje, niet als een pluim. Jordi: "zolang de staart maar definieerbaar blijft".
3. **Oog: half.** Oog B leest op 1× als een donker streepje, een dicht oog of een wenkbrauw, niet als een droge, open blik. A en B verschillen 5 px en zijn op 1× niet te onderscheiden. C (grijsbruine iris, 12 px anders) is het enige dat op 1× als oog leest. Op 1× werkt C het best, maar met het lid van B.
4. **Omlijning en accessoires.** Omlijning per kleurgroep klopt grotendeels (bruin rondom de wol, zwart aan de schaduwkant). De pseudo-omlijning op het oor en de nagels is acceptabel. Halsband, pompons, kwasten en handschoenen kloppen met het model. **De doek is een fail:** op 1× leest hij als een blok of koffer (bovenrand y25 9 px recht, zijkanten x28 en x38 recht op y26–33), terwijl het model een ronde trommel/zadeltas laat zien. Dat staat al in AFGEKEURD ("aguayo als rechthoekige koffer"). Kleurgebruik naast Mareep: te veel middentint en te weinig contrast tussen licht en schaduw, daardoor dof.
5. **Zelfgenoemde punten van de maker:**
   - *Rechthoekig lijf:* grotendeels op te lossen. Rond de hoeken af met ±1 px en zet licht en schaduw als een cilinder (zie R1–R2).
   - *Verre achterpoot leest als rand:* op te lossen met kleur. Geef hem een eigen tint en een eigen hoef (R5).
   - *Handschoenen lopen samen:* op te lossen met kleur. Maak de verre handschoen donkerder en zet er een harde scheiding tussen (R6).

## Reparaties (coördinaten x,y; budget = maximaal aantal gewijzigde pixels)
1. **Wol lijf, volume** (x15–50, y27–41, buiten de doek): leg een groot licht koepelvlak (`h`) linksboven over borst en schouder en een tweede lichtvlak op de bovenkant van het achterwerk (x40–48, y27–31), en breng `h` naar ±12–15 % van het lijf. Zet een doorlopende ronde schaduwsikkel (`b` naar `s`) langs het achterwerk en de buik. Zet de grens tussen licht en midden als 4–5 grote C-bogen (Mareep: bolletjes van 3–4 px breed die naar beneden openen), niet als losse spikkels. Haal alle losse spikkels van 1 px weg (y32–39). Budget ±120 px.
2. **Wolomtrek, alleen ±1 px:** zet in de rechte stukken 1-px-insnoeringen om de 3–4 px, zodat de omtrek uit bogen bestaat: rug x37–49 y26 (2–3 bogen), achterwerk x50 y28–39 (2–3), borst x14 y30–37 (2), buik y40–41 (2–3). Rond de hoeken (14,29), (50,27) en (49,40) met 1–2 px af. Budget ±25 px. *Let op:* SPEC staat ±1 px toe voor "glad" en de staart. Claude moet bevestigen dat wolbogen daar ook onder vallen; ze blijven binnen ±1 px van het model, dat zelf bollen in de wol heeft.
3. **Hals fluffy** (x16–25, y19–28): vervang de stippelkolom door 3 wolbogen (lichte C-vormen van 3 px boven elkaar) aan de lichtkant en een gladde schaduwband rechts. De hals zelf blijft recht. Budget ±25 px.
4. **Staart** (x46–51, y22–26): maak er een pluim van 5×4 met ±1 px, die schuin omhoog naar achteren staat. Geef de lichte kruin een `h`-punt, zet een donkere voet met `d`-scheiding tegen het achterwerk en houd 1 px lucht aan de rugzijde. Budget ±10 px.
5. **Verre achterpoot** (x48–50, y42–60): geef hem één egale donkere tint (`s`/`d`) met een zwarte scheidingslijn (`k`) naar de nabije poot. Zet onderaan een eigen hoef (`n`, 2 rijen), 1 px lager en verder naar rechts dan de nabije hoef (±1 px). Budget ±12 px.
6. **Handschoenen** (x14–30, y55–61): maak de verre handschoen een tint donkerder (`r`/`m`, geen `o`-licht) en geef de nabije een duidelijk `o`-licht linksboven. Zet een doorlopende `k`-lijn ertussen op x22–23, y57–60. Budget ±10 px.
7. **Doek** (x28–39, y25–33): rond de bovenhoeken af (±1 px), laat de bovenrand licht bollen en buig de onderzoom zichtbaar. Zet licht op de linkerbovenhoek en schaduw rechtsonder zodat hij als trommel/zadeltas leest zoals het model. Budget ±12 px.
8. **Oog** (x19–23, y11–15): gebruik de iris van C (`n`, lichtpixel laag vóór) onder het zakkende lid van B (de 4e mengvorm uit SPEC). Doel op 1×: een open, half geloken oog, geen streepje. Budget ≤ 6 px.
9. **Open randen** (klein): `b` op 3 randpixels en `v` op 3 randpixels. Alleen laten staan als de nagels en het oor op 1× zonder omlijning lezen; anders omlijnen. Budget ≤ 6 px.

Totaal ±225 px, kop/oren/halsband/pompons 0 px. Lever op met een diff tegen ronde 6 en tegen deze ronde 4 en een vel op 1× naast Mareep/Flaaffy.

## Voor Jordi (alleen smaak)
- Oogkeuze (na R8): de mengvorm B-lid + C-iris, of puur A/B/C. Het verschil moet eerst op 1× zichtbaar zijn.
- Vachttint: de karamel van de goedgekeurde ramp is lichter dan het bruine model. Moet de wol lichter/crèmer (meer `h`, richting Mareep), of mag hij karamel blijven?

## Samenvatting
- Oordeel **NEE**: het lijf en de hals zijn niet fluffy (vlakke plank met spikkels, nauwelijks lichtste tint, rechte omtrek).
- Kop, hals, pose, halsband, kwasten en handschoenen zijn goed en blijven staan.
- De staart leest op 1× als een bultje, niet als een pluim (R4).
- De doek leest als een koffer, wat al afgekeurd is (R7).
- Oog B leest als een streepje; A/B zijn op 1× niet te onderscheiden. Beste richting: het lid van B met de iris van C (R8).
- De verre achterpoot en de handschoenen zijn met kleur op te lossen (R5, R6).
- Het rechthoekige lijf wordt minder met licht en schaduw als cilinder plus ±1 px-wolbogen (R1, R2); Claude moet bevestigen dat ±1 px voor wolbogen mag.
- Budget ±225 px, geen nieuw silhouet nodig.

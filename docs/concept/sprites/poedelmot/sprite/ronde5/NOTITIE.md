# Poedelmot sprite ronde 5 (6 nov): alleen de poten, vanuit ronde 4

Jordi (letterlijk): "dit is niet netjes afgewerrkt. De poten zijn nu te geometrisch, het zijn geen driehoeken, kijk echt goed naar de fotos, want ie heb je niet nagemaakt. Ik heb met lijnen aangegeven dat de aansluiting van de poot nu niet meer klopt, plus de achterpoten zweven nu"

## Waar Jordi's lijnen liggen (schets over ronde 4 gelegd)
De schets is ronde 4 op ±3,82× (verschuiving 9,8 px; gevonden door de schets op ronde 4 te passen). Er staan twee zwarte lijnen, allebei op de **rechtervoorpoot** (de nabije kant); op de linkervoorpoot en de achterpoten staat niets.
- **Linkerlijn:** van x28-29 op y42 bijna recht omlaag, licht naar rechts, tot x30-31 op y49. Hij valt samen met de binnenrand van de poot in ronde 4 (de grens met de donkere buik).
- **Rechterlijn:** begint hoger, op x31-32 bij y41, en loopt schuin rechtsomlaag tot x35-37 bij y48. Hij loopt dwars door het lichte bovenbeen van ronde 4.
- De lijnen staan bovenaan ±4 px uit elkaar (y42) en onderaan ±5-6 px (y48).
- **Mijn lezing (vraag aan Jordi of dit klopt):** de twee lijnen zijn de randen van het bovenbeen: de poot komt smal uit de borst en loopt schuin naar buiten-onder. Wat in ronde 4 rechts van de rechterlijn zat (x33-38, y41-48), is dan geen poot maar de flank erachter. In ronde 4 zat de poot met de volle schouderbreedte vast, als een blok.
- `paneel_schets.png`: zijn lijnen (rood) op ronde 4, dezelfde lijnen op ronde 5, en ronde 5 zonder lijnen.

## Wat ik op de foto's zie (vóór het tekenen; `paneel_poten.png`)
- **vilt_poten_LEIDRAAD:**
  - De voorpoten komen direct onder het gezicht uit de borst. Het zijn wollige worsten van ongeveer een derde van de kopbreedte.
  - Ze lopen eerst naar buiten-onder en buigen dan naar binnen naar de vinger.
  - De rand is pluizig, nergens een rechte lijn. De punt is een smal pluizig eindje.
- **foto_tak_katoen_2:**
  - De poten zijn dikke wolkokers, opgebouwd uit plukken: elke pluk hangt naar onder en is onderaan breder.
  - De voet is een kwast van uitwaaierende haren, breder dan de enkel, met een rafelige onderrand. Daaruit steekt een dun puntje met een klauwtje.
  - De andere poten steken zijdelings achter de voorpoten uit en staan op de tak.
- **vilt_hand:**
  - Een dikke dij loopt van de zijkant schuin naar onder.
  - Het onderbeen is smaller en loopt naar binnen. Het voetje is klein en wollig, met twee piepkleine zwarte klauwtjes.
- **zijdemot_blad_frontaal:**
  - Het bovenbeen loopt schuin naar buiten. Bij het gewricht hangt een pluk lange haren naar buiten-onder, als een vlag.
  - Het voetpluk loopt asymmetrisch toe: de buitenkant heeft lange haren, de binnenkant is rechter. Op de punt zit een klein donker klauwtje.
- **Gemeen:**
  - Het is geen driehoek. De voet is een pluk die aan de buitenkant verder uitwaaiert en dan naar een smalle punt toeloopt.
  - De pootranden zijn bol en onregelmatig. De poten staan in plukken.
- **Gen 3** (`studie_gen3_poten.png`: Arcanine, Mightyena, Absol, Mareep, frame 1 op 12×):
  - Vacht aan poten heeft een rafelige rand met plukken van 1-2 px die naar onder wijzen (Arcanine).
  - Klauwtjes zijn tikjes van 1 px onder de voet (Absol, Mightyena).
  - Achterpoten staan op dezelfde grond als de voorpoten, de verre net iets hoger (Mightyena).

## Wat er gedaan is
- **Aansluiting rechtervoorpoot (y41-50):**
  - Tussen Jordi's twee lijnen zit nu het lichte bovenbeen (tint 5/6), dat smal uit de borst komt en schuin rechtsomlaag loopt.
  - Rechts van zijn rechterlijn zit de flank in schaduw (tint 3/4).
  - De binnenrand volgt zijn linkerlijn (binnenlijn tint 3).
  - Onder y49 gaat het bovenbeen over in de lijfrand.
- **Onderpoten en voeten (y51-59):**
  - De driehoeken zijn weg. Elke voorvoet is een pluk die bij de enkel smal is (y53).
  - Aan de **buitenkant** waaiert de pluk verder uit (links naar x13, rechts naar x39), daarna loopt hij naar een smalle punt.
  - Onder de punt zitten twee klauwtjes van 1 px in donkerbruin (b) in plaats van zwarte blokjes.
  - Er hangen een paar haarpuntjes van 1 px aan de onderrand (x13 en x31, y57).
  - De binnenrand van de rechteronderpoot schuift naar rechts op (x30 → x33), in het verlengde van Jordi's linkerlijn. De linkeronderpoot schuift naar links op. Zo is er geen rechte verticale rand.
- **Achterpoten staan op de grond:**
  - P (links) komt onder de flank vandaan en staat op y58, met een klauwtje, op dezelfde grond als de linkervoorpoot.
  - S (rechts) komt achter de rechtervoorpoot vandaan en staat op y59, op dezelfde grond als de rechtervoorpoot.
  - Q en R1 zie je alleen als een donker puntje achter P en S: Q met een klauwtje op x12, y58; R1 op x43, y57-58.
  - P en S zijn bovenaan smaller dan onderaan. Ze zijn half weggestopt achter de flank en de voorpoten.
- **Buiten de zone:** niets veranderd. De zone is rijen 45-63 plus het vak x26-38, y41-44, waar Jordi's lijnen liggen.
- **Pixeldiff tegen ronde 4:** 207 px, waarvan **0 buiten de zone** (`controle.txt`). Er zijn 0 lichte pixels op de buitenrand en 13 kleuren.

## Bestanden
- `poten.py` → `raster.txt`;
- `teken.py` → `anim_front.png`, `normal.pal`, `sprite_8x.png`;
- `controle.py` → `controle.txt`;
- `paneel.py` → `paneel_poten.png` en `paneel_schets.png`;
- `keurvel.png`: het keurvel.py-vel met ronde 4, LEIDRAAD, tak-foto, Mightyena en een close-up op 16×, met beide panelen eronder. De keuring staat in `keurvel.png.keuring.md`.

## Zwakke punten (eerlijk)
1. **Wol:**
   - Op de foto's zijn de poten veel ruiger dan in de sprite: daar hangen overal plukken haar.
   - Ik heb de plukvorm aan de voeten gezet en een paar haarpuntjes, maar de randen van de onderbenen zijn nog vrij glad.
   - Meer rafels maakt het op 1× snel onrustig. Of het wollig genoeg is, moet Jordi zeggen.
2. **Achterpoten:**
   - P en S staan nu op de grond. Daardoor zie je ze vrij duidelijk, en de sprite kan lezen als vier poten naast elkaar.
   - "Weggestopt, half zichtbaar mag" en "niet zweven" trekken hier tegen elkaar in. Vraag aan Jordi: is dit goed, of mogen ze nog verder achter de voorpoten?
3. **Q en R1** zijn alleen een donker puntje. Van de zes poten lezen er vier duidelijk.
4. **Linkervoorpoot:** Jordi tekende alleen op de rechtervoorpoot. De aanzet van de linkervoorpoot (y41-44) heb ik niet veranderd. Vraag: moet die aanzet ook zo smal uit de borst komen?
5. Een onafhankelijke keurder is nog niet geweest.

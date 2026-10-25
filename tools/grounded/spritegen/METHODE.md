# Spritegenerator: de methode (Dragonfly Cave-gids, stap voor stap)

Bron: `docs/lessen/bronnen/dragonflycave_spriting_guide.txt` (helemaal gelezen, 25 okt). Elke stap hieronder is een stap
in de motor en een paneel in de editor. Niets samengevat weggelaten; waar de motor iets nog niet doet, staat dat erbij.

## A. Basisregels (gelden altijd)
1. Nooit JPEG, nooit de sprite zelf schalen (alleen inzoomen), geen stijlen mengen, canvas strak om de sprite.
2. Alleen potlood van 1 px, gum, emmer en selectie zonder anti-aliasing.
3. Licht komt van linksboven bij een sprite die naar links kijkt (rechtsboven als hij naar rechts kijkt).

## B. Kleuren (uit 'Recolors' en 'Revamps')
1. Per kleurgroep: hooglicht, basis, schaduw, omlijningsbasis; de omlijningsschaduw is altijd (bijna) zwart.
2. De relatieve helderheid van de tinten blijft gelijk; geen twee tinten samenvoegen; hooglicht nooit donkerder dan basis.
3. Alle tinten van een groep in dezelfde tint (hue); schaduwen eventueel iets richting blauw.
4. De omlijning heeft ook kleur (omlijningsbasis) en moet donker genoeg zijn. Bij lichte kleuren: aparte
   omlijnings-hooglicht donkerder dan de schaduw, of overal omlijningsbasis behalve op de allerlichtste plekken.
5. Neem kleuren bij voorkeur over van een bestaande sprite met ongeveer die kleur (editor: paletten uit echte sprites).
   Anders: basis kiezen, hue/helderheid voor alle tinten met dezelfde stap verschuiven.
6. R/S-stijl gebruikt veel hooglicht (een sprite met weinig hooglicht oogt donkerder dan R/S).

## C. Pixel-over (de hoofdroute)
1. Kies een tekening (eigen modeltekening of officiële art). Verklein: breedte + hoogte samen ±140–160 px is de maat van de
   gids; voor Gen 3 maximaal 64×64. Verkleinen 'jagged' (naaste buur), zodat de lijnen te volgen zijn. Niet groter dan nodig
   voor de details.
2. Trek de omlijning over met een donkere kleur die niet in de sprite voorkomt, op een eigen laag. Volg de tekening niet
   slaafs: een gladde omlijning (sectie D) gaat vóór elke pixel van het origineel.
3. Pseudo-omlijning: delen van 1–2 px breed krijgen geen echte omlijning maar alleen een afwijkende kleur.
4. Wis de tekening (houd een kopie als naslag voor de schaduw); maak de omlijning zwart.
5. Vul alles met de schaduwkleur (emmer).
6. Eerste schaduwlaag: de basiskleur, volgens sectie E.
7. Hooglicht erbovenop in kleinere ronde vormen; daarna glans: kleine, (bijna) witte vlekjes.
8. Omlijning inkleuren (sectie F); eventueel binnen-anti-aliasing; transparant maken.

## D. Omlijnen (in-depth)
1. Gouden regel: geen vormgereedschap; met de hand, want het brein wil gladheid, geen wiskundige cirkel.
2. Rechte lijnen: segmenten die telkens 1 px verspringen; ongelijke lengtes alleen in een regelmatig patroon (1-2-1-2);
   te weinig afwijkende segmenten geven een 'bobbel': kies dan een eenvoudiger helling.
3. Hoeken: 'corner' (schuin, 4 richtingen) en 'point' (recht, 4 richtingen); alleen voor echte scherpe punten (klauwen).
4. Curven:
   - tussen een horizontaal en een verticaal segment langer dan 1 minstens één neutraal segment van 1 px
     (behalve bij hele kleine rondjes < 6 px);
   - nooit een corner in een curve; geen points in een curve (tenzij heel klein of heel steil);
   - geen besluiteloosheid: segmentlengtes lopen geleidelijk op of af, niet heen en weer (3-1-2-2-1 = fout);
   - een lange rechte lijn mag niet abrupt in een andere overgaan: helling geleidelijk laten veranderen.
5. Eén deel tegelijk: grof tekenen, dan pixel voor pixel gladstrijken; details pas als de grote vormen staan;
   riskante delen op een eigen laag.
6. Omlijning altijd 1 px breed, geen klonten zwart.

## E. Schaduw (in-depth)
1. Vorm-schaduw (glijdend) en slagschaduw (door een ander deel): slagschaduw is altijd volledig de schaduwkleur.
2. Vlakken: één tint per vlak, naar de hoek met het licht.
3. Ronde vormen: hooglicht rond en klein waar het licht loodrecht valt; de schaduw begint vrij abrupt op de evenaar
   (grens tussen naar het licht en van het licht af) en wordt daarna niet donkerder. Basis tussen hooglicht en evenaar.
4. Extra donkere tint alleen waar direct én teruggekaatst licht ontbreekt.
5. Delen achter het lijf (staart) krijgen veel schaduw, behalve aan de bovenkant. Waar een deel over een ander valt,
   komt de schaduwkleur op het achterste deel (de vleugels van Scyther).
6. Glans: alleen op glanzende delen; klein en rond; ogen (kraaloog) altijd een witte glansvlek én een gekleurde reflectie
   aan de tegenoverliggende kant. Bij heel glanzende delen een beetje teruggekaatst licht in de schaduw (gedithered).
7. Texturen: vacht = grens basis/schaduw gekarteld als de vacht zelf, eventueel wat dithering en korte streepjes in de
   haarrichting, niet overdrijven. Schubben: weglaten of groot met omlijning. Rots/staal: vlakken, elke lijn scheidt twee tinten.

## F. Omlijning inkleuren
1. Grofweg: zwart rond de schaduwkleur, omlijningsbasis rond de basiskleur, schaduwkleur rond het hooglicht.
2. Per segment van de omtrek een geleidelijke overgang: helemaal zwart → zwart met 1 px omlijningsbasis aan de binnenkant
   → omlijningsbasis → omlijningsbasis met 1 px omlijnings-hooglicht aan de binnenkant → een segment of twee omlijnings-hooglicht.
3. Anti-aliasing alleen aan de binnenkant van de omlijning, nooit aan de buitenkant.
4. Pikachu-voorbeeld: schaduwkleur als extreem hooglicht op de allerlichtste randen; omlijnings-hooglicht soms als
   extreme schaduw (voet).

## G. Splicen/revamps (voor later, in de editor als 'onderdeel uit een andere sprite')
Geen deel twee keer gebruiken of spiegelen voor de andere kant; daarna één kleurschema en de schaduw laten kloppen.

## Hoe de editor dit volgt
Elke stap C1–C8 is een zichtbare laag (je kunt per stap kijken, zoals de screenshots in de gids); de schuifknoppen
sturen alleen keuzes die de gids aan de spriter laat (maat, lijngevoeligheid, aandeel hooglicht, evenaar, ronde vlakken,
vacht-kartel, glans, omlijningsovergangen). De controles uit D en F worden op het canvas aangewezen (rood = curve-fout).

## Kalibratie tegen de gids (25 okt)
- **Vulpix is geen eerlijke test:** DC tekende zijn pixel-over naar de oude Gen 1-art (staart van ronde bollen, krul op
  de kop); de gids toont nu de nieuwere art (golvende staart met krullen). Pose en silhouet kloppen, de binnenlijnen niet.
- **Hitmonchan wel:** zelfde tekening als DC's pixel-over. DC-labels per pixel uit de PDF terug (raster 6,26 px, R/S-palet
  `graphics/pokemon/hitmonchan/normal.pal`; tint 164,156,164 = extra donkere tuniekschaduw).
- Wat DC doet en de motor nu ook (gemeten op beide):
  - lijnen = skelet van de tekenlijnen op het raster: 97–99% binnen 1 px;
  - kleine donkere details (pupil) altijd 1 px;
  - buitenrand zwart van het licht af en omlijningsbasis naar het licht toe (DC: 90% zwart aan de schaduwkant, 21% aan
    de lichtkant);
  - binnenlijnen zwart alleen waar ze aan schaduw grenzen (gids F1).
- **Toon** (licht/basis/schaduw) blijft 55–66% gelijk. Een classifier op vormkenmerken haalt over twee sprites heen
  ±45%: DC's schaduw is een artistieke keuze (verre ledematen donker, tuniek grotendeels schaduw), niet af te lezen uit
  de tekening. Daarvoor zijn de schuifknoppen en het pixelpaneel.
- Opnieuw meten: `node search_dc.js <map> iteraties` (zie `calibrate_dc.js` voor de bestanden).

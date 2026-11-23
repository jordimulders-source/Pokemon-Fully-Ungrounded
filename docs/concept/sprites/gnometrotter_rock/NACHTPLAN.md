# Gnometrotter: nachtplan 5 eindsprites (23 nov)

Jordi (letterlijk): "nee ik wil toch kijken of het lukt om een hybride vorm te maken. Dus je doet het volgende, je maakt eerst rock, dan doe je ijs en grass met dezelfde pose. Daarna ga je kijken of het lukt om alleen de onderdelen die in de hybride versies anders moeten te verplaatsen, zo netjes mogelijk. Ik ga nu slapen en wil morgen 5 eindsprites zien"

## De 5 sprites
| # | Naam | Model (bevroren) | Map |
|---|---|---|---|
| 1 | Rock | `gnometrotter_rock/r8/gemini_r8.png` | `gnometrotter_rock/sprite/` |
| 2 | Ice (zelfde pose) | `gnometrotter_ice/r3/gemini_r3_lijf.png` | `gnometrotter_ice/sprite/` |
| 3 | Grass (zelfde pose) | `gnometrotter_grass/r4/gemini_r4_lijf.png` | `gnometrotter_grass/sprite/` |
| 4 | Ice hybride | `gnometrotter_ice/hybride/model_hybride.png` | `gnometrotter_ice/sprite_hybride/` |
| 5 | Grass hybride | `gnometrotter_grass/hybride/model_hybride.png` | `gnometrotter_grass/sprite_hybride/` |

## Hybride (Claude's uitwerking van Jordi's opdracht)
- Wat anders moet (Jordi over de zelfde-pose-versies: "het enige wat nu wel zo is, is dat het roze/blauwe lichaam nu minder ijsblokken, houtvormen zijn"; daarvóór "nog niet wat we eerst hadden"): het roze/blauwe lichaam (romp, armen, handen, benen, voeten) moet het materiaal krijgen zoals in de eerste versies: Ice `gnometrotter_ice/r1/gemini_r1.png` ("ice perfect"), Grass `gnometrotter_grass/r1/gemini_r1_handen_gewisseld.png` ("echt heel vet de grass").
- Werkwijze: knippen en plakken (Jordi: "moet met knippen en plakken lukken"). De omtrek, pose en maat van de zelfde-pose-versie blijven heilig; per onderdeel wordt het overeenkomstige stuk uit de eerste versie geknipt, op de maat van het onderdeel gebracht en binnen het masker van dat onderdeel geplakt. Muts, baard, haar, riem, rugkam, zolen en stok blijven van de zelfde-pose-versie, tenzij een onderdeel uit de eerste versie past zonder de omtrek te veranderen.
- Grass: Jordi gaf toestemming "om ietsje van het model af te werken, omdat het knip en plak werk niet super netjes is".

## Gemeenschappelijk voor alle 5 (Wormadam: "hooguit paar pixels afwijking")
- Alle modellen hebben dezelfde omtrek in het 1024×559-beeld (figuur x 274–749, y 41–522). Alle 5 sprites gebruiken **dezelfde reductie** (zelfde raster/schaal/verschuiving), zodat ze even groot zijn en op dezelfde voetlijn staan. De Rock-maker legt die vast in `gnometrotter_rock/sprite/GEDEELD.md` (+ script); de andere makers nemen die over.
- Zelfde palet voor gedeelde delen (zwart, roze neus/lijf, blauw), zelfde indexen.
- Oogstrook: de donkere strook onder de muts die als ogen leest wordt in de sprite dichtgemaakt met mutskleur (Jordi bij Rock: "1 akkoord").
- Werkwijze: `docs/lessen/SPRITE_KERN.md` + `SPRITE_WERKWIJZE.md` → "Gemini-model namaken"; model overnemen, niet hertekenen; Dragonfly Cave-omlijning in de eindkeuring; voorbeeld en scripts: `gnomad/sprite_r1/` t/m `sprite_r11/`.
- Jordi (23 nov, nacht): "en je gaat niks of zo weinig mogelijk opnieuw tekenen"
- Jordi (23 nov, over de 5 eindsprites): "Ze zijn eigenlijk allemaal nog niet mooi he"
- Jordi (23 nov): "ik vind ze alle 5 heel slordig. de gesp is nergens goed gelukt, rock heeft willekeurige pixels in de hoed, het lijnenwerk is slordig, nergens is het kleurgebruik/schaduwgebruik met tinten perfect gelukt. ijs heeft 2 keer een afgekapte rechterschouder, desondanks vind ik de rechtse versie nog net wat beter, maar ook halfbakken, de vraag is of het lichaam echt goed een ijsvorm kan krijgen, bij grass zijn beide lichamen ontzettend slordig en mislukt"
- Jordi (23 nov, op Claude's analyse "te druk/te groot"): "ze zijn niet te druk, niet met teveel details, niet te groot, jij hebt gewoon slordig werk geleverd"

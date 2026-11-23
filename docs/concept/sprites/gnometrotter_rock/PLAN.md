# Gnometrotter: 5 eindsprites (23 nov)

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
- Jordi (23 nov): "het silhouet is prima" → silhouetten van alle 5 bevroren; alleen binnenwerk netjes maken.
- Jordi (23 nov): "ijs mag je rond maken zoals bij rock, zoals we volgens mij afgesproken hadden. Akkoord met slechts een paar materiaal vormen bij ijs en grass"
- Jordi (23 nov): "kijk vooral ook naar andere pokemon, ijs pokemon voor ijs en nuzleaf en shiftry en andere houten pokemon als die er zijn voor grass"
  - Referenties (eerste frame van `graphics/pokemon/<soort>/anim_front.png`): Ice: regice, glalie, snorunt, avalugg, bergmite, cryogonal, vanillish. Grass/hout: nuzleaf, shiftry, seedot, trevenant, phantump (Jordi: "sudowoodo en bonsly zijn niet van hout"). Rock: regirock, graveler, golem.
- Jordi (23 nov): "en kijk vooral hoe je de vorm kan creëren zonder de kleur te veranderen van het roze en blauw" (materiaal op het lijf via vorm, niet via andere kleuren; roze en blauw blijven de Gnomad-kleuren)
- Jordi (23 nov): "je mag de gesp trouwens bij rock en ijs weglaten"
- Jordi (23 nov, gesp): "is bij grass ook en ziet er prima uit" (Grass heeft geen gesp; zo laten)
- Jordi (23 nov): "je hebt dingen opnieuw getekend, of niet?" · "ja dat had je meteen moeten stoppen" → Rock r6 vanaf de kale verkleining van r8, alleen technisch opschonen.
- Jordi (23 nov, over r5): "hij is niet slecht hoor, maar het wijkt veel meer af van het model dan nodig is. Ga niet dingen opnieuw bouwen die niet nodig zijn, gebruik al wat je hebt, maar het moet beter. Het kleurgebruik is grotendeels wat beter al, maar je hebt vaak wel minimaal 3 kleurtinten nodig voor perspectief" → r6 = r5 als basis, alleen afwijkende vormen terug naar het model, ≥3 tinten per vorm.
- Jordi (23 nov, over r6): "linkerhand arm is nog niet de goede vorm, arm is een rechte lijn, rechterschouder mag ietsje ronder, punt van de muts en rots lijken een beetje 1 te zijn, het model weet verschil te creëren doordat de rots schuin is waar ze hier allebei recht zijn, haar links en tussen muts mag een lijn, verder is die qua silhouet goed, maar het kleurgebruik qua tinten moet nog een stuk beter"
- Jordi (23 nov, over r7b): "beter al, maar je bent er nog niet. Rots op de rug is ook prima, het gaat nu echt om belijning, kleuren en schaduwen" → vormen r7b bevroren; ronde r8 alleen belijning/kleur/schaduw.
- Jordi (23 nov): "de vorm laat je intact vanaf nu"
- Jordi (23 nov): "kijk ook naar geslaagde sprites die wij al gemaakt hebben" → o.a. steenjaguar + welp (`steenmozaiek/af/`, steen), Lunatone- en Solrock-evolutie (`lunatone_evo/af/`, `solrock_evo/af/`, steen), Gnomad/Gnomini; overzicht `showcase/frontsprites_af.png`.
- Jordi (23 nov, over r8): "weer wat beter, maar de zwarte lijnen lijken wat willekeurig te zijn, dat is niet hoe dat in andere goede sprites gelukt is"
- Jordi (23 nov): "het lijf is uiteraard drukker dan gnomad, dat is het design" (geen punt; niet als zwak punt melden)
- Jordi (23 nov): "alleen de lijnen van de stenen wijken af van het model ook, kijk daar goed naar, daarom lijkt het slordiger, er zijn teveel kleine vormen"
- Jordi (23 nov): "ja en als het echt niet mooi is, dan is dat ook een les en dan houden we het lichaam neutraal"
- Jordi (23 nov, over r9): "ja r9 is weer wat beter, het kan wel dus. Sterker nog, ik denk dat die naar de eindkeuring kan, goed naar kleurtinten, schaduw vooral en lijnen kijken" → eindkeuring r9.
- Jordi (23 nov, over r10): "de schaduw mag wat meer uberhaupt op het lichaam vallen, de neus is niet meer rond nu, de schaduw is gewoon vrij inconsitent nog of niet?"
- Jordi (23 nov, over r11): "ik zie in het roze lichaam een paar gekke horizontale lijnen, als je dat nog kan fixen en de neus rond kan maken dan zijn we er denk ik"
- Jordi (23 nov, over r12): "ja maar nu zijn er weer 2 onnodige horizontale lijntjes op de arm terug, en de onderkant van de arm is ook te recht horziontaal" → r13.
- Jordi (23 nov): "hij is te hoekig"
- Jordi (23 nov): "en je moet geen zwarte lijnen onnodig doen"
- Jordi (23 nov, over r13-schouder): "nee weer fout"
- Jordi (23 nov): krabbel op r13: gele cirkel om de schouder (sprite ±x 41–52, y 22–30) en een gele boog van onder het haar rechts (±38,19) naar de arm (±55,29): de schouderbal hoort daar groter en hoger, met de bovenrand langs die boog (zoals het model: bal vóór de rugrots).
- Jordi (23 nov, bij de krabbel): "dit zijn schetsen" · "dus niet volledig nadoen" · "je past telkens het verkeerde aan" · "de bovenarm moet gewoon iets ovaler" · "en de ruglijn is een diagonale rechte lijn"
- Jordi (23 nov, over r14): "neee"
- Jordi (23 nov, krabbel op r12 12×): "geel moet weg, zwart moet nog een binnenlijn (niet in het zwart) voor 1 aansluiting en rood is de lijn die iets ronder moet"
- Jordi (23 nov): "verder verander je niks"
- Jordi (23 nov, over r15): "AAAAAAH" · "ik teken de fucking pixels" · "en je doet het gewoon nog niet"
- Jordi (23 nov): "gele puntjes betekenen ALLEEn die pixel, niet de hele lijn"
- Jordi (23 nov): "juist 15 is goed" → af: `af/gnometrotter_rock.png` (= sprite_r15).
- Jordi (23 nov): "dan mag die naar een definitieve eindkeuirng" → definitieve eindkeuring r15.
- Definitieve eindkeuring r15: PASS, geen reparaties (`keuring_r15/KEURING.md`). Rock definitief af.
- Jordi (23 nov): "klopt de zwarte lijn bij de neus wel, erg dik" → r16 voorstel: (18,21) en (19,22) zwart → 7, boog 1 px.
- Jordi (23 nov, over r16/r15 heel): "nee die is nog niet af" · "dat is nog niet mooi" → Rock NIET af; r16 = laatste stand.
- Jordi (23 nov): "moet dat niet gewoon een zeer donkere roze tint zijn" (neusboog) → r17.
- Jordi (23 nov): "links is af nu" → r17 af (`af/gnometrotter_rock.png`).

## Ice en Grass (nieuwe sessie, 23 nov)
- Jordi: "ijs en gras zouden gebouwd worden vanuit het basis lichaam van rock, en niet rock af, eerdere rock" · "het LICHAAM he niet de rest" (= de nachtsprites, gebouwd op het lichaam van de eerdere Rock).
- Jordi (over het vel Rock af | Ice r3 | Ice hybride r2 | Grass r3 | Grass hybride r2): "ijs links, maar moet geen gesp hebben, de rechtershouder is nog niet goed, voor de rest mag je het lichaam meer ijsvormen geven, de rest behouden. Grass heeft geen goede neus en geen goede rechterschouder, de linkerhand wijkt ook af van rock, maar dat doet ijs ook. Dan mag die het lichaam verbeteren, bij grass is het lichaam nog het slechtste"
- Jordi: "ik bedoel dus dat we niet de rock versies pakken"
- Jordi: "want alle rock versies vertalen niet goed" · "en ik wil geen knip en plak werk" (geen hybride, niets uit Rock of r1 plakken)
  → Ice: basis `gnometrotter_ice/sprite_r3/gnometrotter_ice.png` (niet de Rock-sprite); gesp weg; rechterschouder goed; lijf meer ijsvormen; de rest behouden. Jordi: "nee ijs moet de linkerhand ook als rock" → linkerhand (vuist + arm) zoals Rock af.
  → Grass: neus en rechterschouder niet goed, lijf verbeteren (slechtste deel).
- Jordi: "de rechter hybride grass, maar ze zijn allebei nog niet goed" · "ja de linkerhand moet gelijk worden aan rock" · "bij allebei"
  → Grass: basis `gnometrotter_grass/sprite_hybride_r2/gnometrotter_grass_hybride.png`; neus, rechterschouder, linkerhand zoals Rock af, lijf verbeteren.
- Jordi (over Grass r5): "grass gaat de goede kant op, alleen de rechte lijnen mogen wat minder recht, onthoud het perspectief" → r6: plank-/nerflijnen buigen mee met de ronde ton in driekwart.

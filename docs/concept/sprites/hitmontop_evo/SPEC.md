# Hitmontop-evolutie (capoeira): SPEC

## Besloten (Jordi, 5 nov)
- Geen regional form: "zijn japanse naam is zelfs capoeira gebaseerd, dus we gaan hem alleen evolven".
- Eerst alleen ontwerp: "ik wil puur naar design kijken, de rest komt daarna".
- **Pose:** "dit is wel de perfecte pose he" bij `referenties/pose_eenhandsstand.webp`.

## De pose (beschrijving van de foto)
- Handstand op **één arm**: de steunarm staat recht en verticaal omlaag, de hand plat op de grond, de vingers naar voren.
- Het lijf hangt schuin (±45°), de heup is het hoogste punt van de romp; de kop zit laag, naast de steunarm, en **kijkt de kijker aan**.
- De **benen in een brede V-split** omhoog: één been schuin naar linksboven, het andere schuin naar rechtsboven, met de voeten gestrekt of geflexed aan de uiteinden. Dat zijn de twee hoogste punten van het silhouet.
- De vrije arm ligt **gebogen over de buik/heup**.
- Het **cordão** (koord) hangt van de heup omlaag door de zwaartekracht.
- Silhouet: een omgekeerde driehoek of Y. Wijd bovenin, smal punt onderin (de hand). Herkenbaar op 1×.

## Ontwerp (Jordi, 5 nov, letterlijk)
Bij `referenties/fanart_mestrimba.png` (fanart van iemand anders, "Mestrimba"; alleen ter inspiratie, niet overnemen): "er dacht iemand hetzelfde over."
- "De hoorn blijft maar wordt een veel kleiner onderdeel, niet meer functioneel, want de evolutie is zo goed geworden met handen en voeten dat het niet meer nodig is."
- "Het blijft duidelijk een hitmon familie lid, dus met bruine huid en duidelijke kenmerken, maar de broek die blauw blijft wordt nu langer en aansluitend."
- "Zijn haren blijven bruin maar worden een veel meer afro braziliaanse haarstijl, beetje eddy gordo achtig"
- "de benen worden langer en de voeten passen goed erbij, maar blijven blauw met klauwen en minder groot in verhouding tov de benen als voorheen."
- "het tenue wordt nu meer een broek en het lichaam van hitmontop wat langer."
- "Die touwtjes die aan de broek hangen doen we ook, maar die hangen ook aan zijn armen, beetje zoals bij muay thai vechters." (zoals de *prajiad*-armbanden)
- "De handen blijven rondjes"

## Kenmerken op een rij (afgeleid van Hitmontop, `graphics/pokemon/hitmontop/anim_front.png`)
- Bruine huid (kop, armen, benen), ronde lichte handen.
- Blauw onderlijf wordt een lange, aansluitende blauwe broek; het lijf langer dan bij Hitmontop.
- Kleine, niet-functionele hoorn op de kop, tussen of in het haar.
- Bruin haar in een afro-Braziliaanse stijl (richting Eddy Gordo: dreads/opgebonden).
- Blauwe voeten met klauwen, kleiner ten opzichte van de (langere) benen.
- Koordjes: aan de broek (cordão) en om de bovenarmen.
- Pose: zie hierboven (eenarmige handstand, V-split).
- Anders dan de fanart: geen witte broek of berimbau-benen; blauw blijft.

## Type (Jordi, 5 nov)
- **Fighting/Ground** (twijfel was Fire/Water/Ground; "dark vind ik niet passen. Ik denk ground het beste omdat die telkens aan de grond zit"). Niet eerder in de dex (Great Tusk staat uit). Verdedigend: zwak voor Flying, Water, Grass, Psychic, Ice, Fairy; Rock ×¼, Poison/Bug/Dark ×½, immuun voor Electric.

## Werkwijze (Jordi, 5 nov)
- "nee doe maar niet met blender, dat gaat vaker fout dan goed"; "nee je maakt een model zelf, daarna pas evt silhouet"; "en gebruik de hitmontop sprite, want het wordt een evolutie"; "nee de lama, niet de nachtaap".
- Dus: eigen 3D-poppetje zoals lama fase 3 (`lama/ontwerp/pop3d_lama.py` op `olinguito_v2/silhouet_kolibriemethode/pop3d.py`), met de Hitmontop-sprite als basis; pas daarna het silhouet.
- Poppetje ronde 2 afgekeurd (Jordi: "what the fuck heb je met dat hoofd gedaan", "wat een mormel"): kop als bol met rokje, ondersteboven, dreads als octopuspoten. **Nieuw (Jordi): "we doen het anders / ga met sprite art werken / je hebt hitmontops sprite al"**: direct in pixels vanaf de Hitmontop-sprite, kop = Hitmontops kop rechtop als skelet.
- Jordi: "ga maar sprite assets gebruiken die je al hebt en daarmee bouwen": onderdelen van bestaande sprites (Hitmontop-kop/handen/voeten, Hitmonlee-benen, enz.) als bouwstenen, naden met de hand weg, één palet. Geldt hier boven de algemene collageregel.
- Sprite r1–r3 afgekeurd (Jordi, 6 nov): "de hele sprite is echt verschrikkelijk, de hitmontop haren moet je anders doen, niet nieuwe haren bedenken". Dus: het bestaande Hitmontop-haar (de bruine puntige 'top' met strepen) als vertrekpunt en dat restylen richting afro-Braziliaans/Eddy Gordo; geen nieuw kapsel verzinnen. "Ga met agents hier aan werken en kom pas terug als een andere agent het echt goed vindt."

## Werkwijze vanaf 6 nov (Jordi)
- "Als je nu gewoon een stick man variant of een basis silhouet van die pose maakt. Dan gaan we daar steeds meer assets op plakken. [...] handen en voeten, dat is simpel. [...] Zodat het skelet uitgebouwd wordt." Stap voor stap, telkens meerdere opties. Stappen: 1 skelet → 2 handen/voeten/kop → 3 ledematen → 4 romp/koordjes → 5 één geheel.
- Stap 2 (Jordi): "juist, dit is wat ik bedoel". Stap 3 (Jordi): "Voor het hoofd kan je nu hitmontop zijn hoofd ophangen. Voor de armen kan je hitmonchans armen gebruiken en voor de benen kan je hitmonlees benen gebruiken. Als lichaam etc kan je ook assets van hitmonchan en misschien tyrogue gebruiken, als we dan de pose hebben kunnen we alles aanpassen"; "dan is het eerst een knip en plak werk maar dan snap je waar ik heen wil". Skelet: optie D14.
- Stap 3b (Jordi, 6 nov): "ok dit is de vorm", "vanaf hier gaan we alles stap voor stap aanpassen". Bevroren als basis: `stap3b/` (welke optie A–D: navragen).
- Basis = stap 3b optie C (Jordi: "maakt niet uit welke van de 4"). Stap 4 (Jordi, 6 nov, letterlijk): "we gaan er eerst een goed hoofd op zetten. Gebaseerd op Hitmontop, die maken we zodat die goed past in de hoek en de pose die we van plan zijn. De stekel bovenop het hoofd van Hitmontop wordt iets minder aanwezig en de 'haren' kammen we naar achteren in een klein staartje of knotje, maar het lijkt me niet dat die te zien is in de pose, of juist net wel, voor de rest gaan we nog nergens aan zitten". Aanvulling: "ogen, wenkbrauwen, mond blijven hetzelfde, maar we kunnen een beetje met de uitdrukking spelen". En: "pixel voor pixel is misschien niet mogelijk, vanwege pose en hoek" (zelfde vorm en karakter, met de hand aan de hoek aangepast). Geen ongevraagde stappen (Jordi: "ik heb je helemaal geen instructies gegeven").
- Hoofd ronde 1 (Jordi): "ja de mond is weg, de stekel is alleen dunner, maar die moet gewoon kleiner in zijn geheel, plus het mag iets duidelijker zijn dat het haar naar achter is gekamd, een knot moet wel duidelijk zijn".
- Jordi: "de puntige haarrand kammen we naar achteren, dus die is weg" (glad naar achteren gekamd haar met knot, geen punten).
- Jordi: "maar het hoofd mag wel iets groter, hitmontop heeft een erg groot hoofd voor zijn lichaam, bij deze evolutie wordt het naar verhouding minder, maar het wordt geen mens".
- Jordi: "en de mond mag wat meer vreugde uitstralen dan bij hitmontop".

## Hoofd: Jordi over ronde 3b (6 nov, letterlijk; leidend)
Referenties: `referenties/hitmontop_anime.webp` (Hitmontop in de anime) en `referenties/krabbel_hoofd_jordi.png` (zijn lijnen over ronde 3b).
"dus de mond zit aan de bovenkant, onder de haar kant? Dus hij is kaal en heeft een baard? Dit is door een agent goedgekeurd? Desalniettemin niet zo'n ramp. De kleinere hoorn moet nog steeds door de haren heen zichtbaar blijven. Het enige wat deze nieuwe vorm heeft is de haren die hij al had wat langer laten groeien en opgeknot, om een kleinere punt heen. Plus de hoofdvorm is anders. Daarnaast mag het hele hoofd sowieso counterclockwise draaien, zodat het perspectief klopt. Hitmontops haren en hoorn zijn altijd hetzelfde materiaal/kleur. Dat veranderen we nu niet, plus het is dezelfde kleur als zijn hoofd. De ogen blijven rond, wenkbrauwen heeft die niet, dat is de lijn van zijn haren, maar dat gaan we slim doen. De ogen blijven zwarte rondjes met een wit puntje erin, dat verandert in welke emotie dan ook niet. De mond is gewoon een streepje, dus het is veel makkelijker dan je nu doet. Ik heb met wat lijnen getekend wat er moet gebeuren. Het design mag dus ook echt simpel zijn, want dat past in de lijn. Alle hitmons zijn relatief simpel getekend"
Samengevat: haar, hoorn en huid één materiaal en één kleur (Hitmontops bruin); haar = zijn eigen haar, langer gegroeid en opgeknot rond een kleinere punt die zichtbaar blijft; de 'fronslijn' is de haarlijn (geen wenkbrauwen); ogen = zwarte rondjes met een wit puntje (nooit anders); mond = één streepje, lager; hele hoofd tegen de klok in draaien; simpel tekenen zoals alle Hitmons.
Daarna (Jordi): "andere kleur is niet erg, daar hadden we het niet over gehad, maar het hoofd onderste boven is wel erg gek. Volg mijn instructies en we komen er wel" (hoofdpunt: het hoofd moet rechtop lezen; haarkleur is bijzaak).
Op ronde 4 (Jordi): "je luistert niet, het haar is niet anders dan het hoofd, het is hetzelfde materiaal en dezelfde kleur, er zit dus geen streep tussen"; "kijk aub een keer goed naar hitmontop en stop met dingen verzinnen". (Claude had zelf "haar onderscheiden met lijnen" verzonnen.) Hitmontops kop = één glad geheel: punt bovenop loopt uit de kop door, flappen opzij, alleen dunne plooitjes in de flappen en twee plooilijnen boven de ogen; ogen zwarte rondjes met wit puntje; mond een streepje.
Daarna (Jordi): "rare kippenpoot heeft die ook in zijn haar"; "de enige streep is wat nu boven zijn ogen zit, maar gezien die haren nu dus naar achter gaan, komt die streep veel hoger te staan, een beetje als een fade, maar dat kan je wel berekenen hoop ik" (dus één streep: de haarlijn, hoog op het hoofd, zacht; geen plooitjes).
Jordi: "en design eerst maar puur het hoofd zonder de rest", "dan keuren we dat" (hoofd los ontwerpen, pas na goedkeuring op de vorm).
Op ronde 5b (Jordi): "ja dit is echt nog niet goed. Je bent from scratch aan het tekenen, ik heb liever dat je hitmontops hoofd pakt en daarmee gaat spelen." "want dit is echt nog heel ver ervan af, geen enkele van mn punten zie ik er in". Ronde 6: Hitmontops kop-pixels als basis en bewerken, niet tekenen.
Op ronde 6 (Jordi): "ik vind het compleet prutswerk, de laatste is niet eens een hoofd meer, lijkt eerder op vanillite. In nergens is er haar af te lezen, in nergens zit de bovenkant goed. Kan je dit uberhaupt wel?"; voorstel om voorbeeldfoto's te zoeken: "nee want dan ga je weer ander haar bouwen"; daarna: "nee laat maar". **Hoofd gepauzeerd** (6 nov). Bruikbaar: pose/skelet (stap 2), vorm (stap 3b). Het hoofd ontbreekt nog.

## Hoofd: Jordi's recept (6 nov, letterlijk; leidend)
Bij `referenties/hitmontop_3d.webp`: "kijk naar deze afbeelding. De V-vorm tussen zijn ogen, die lijn gaan we naar achter trekken, die haren komen samen in een soort knot, dat mag gewoon een rondje zijn met een witte band, bijna zoals zijn handen. en de stekel bovenop mag kleiner, makkelijker kan ik het echt neit maken".
Dus: (1) de V tussen de ogen (de voorrand van de flappen) naar achteren trekken; (2) de flappen komen achter samen in een knot = een rondje met een witte band, zoals zijn handen met polsband; (3) de stekel kleiner. Verder niets.
Op ronde 8 (Jordi): "dit kan toch niet"; "je volgt niet eens het allersimpelste wat ik kan vragen"; "namelijk de v vorm in het hitmontop hoofd, want die sluit neit aan in een punt". Daarna: "stop maar", "ik ben er ff klaar mee". **Gepauzeerd.** Volgende keer eerst: de V van Hitmontop (twee lijnen die tussen de ogen in één scherpe punt samenkomen) naar achteren getrokken, nog steeds als V met punt.

## Hoofd: concept goedgekeurd (6 nov)
- Jordi's Gemini-bewerking van het 3D-plaatje: `referenties/hoofd_gemini_concept.webp`. Jordi: "je hebt nog gelijk ook. Dit is het idee wat ik voor het hoofd had min of meer". Dit is de bron voor de pixels (ronde 9: `stap4_hoofd/ronde9/`, silhouet uit de bron, details met de hand).

## Model (Jordi, 6 nov)
- `referenties/model_gemini_pose.png`: volledig model in de pose (Gemini, Jordi). Jordi: "ik heb nu een model. Als we hiervan een sprite maken en het iets beter inkleuren dan zijn we er". Dit is de bron voor de sprite (zoals de render bij Picapau), bevroren. Jordi: "en het moet minder een mens worden". Versie 2 met ronde steunhand: `referenties/model_gemini_pose_v2.png`. **Versie 3 = de bron** (`referenties/model_gemini_pose_v3.png`, gladde buisarm; Gemini weigert verdere bewerkingen). Nog menselijk, op te lossen in de sprite: borst/schouderblad-anatomie glad maken, lijf iets gedrongener. Open: broek wit (model) of blauw (SPEC).

## Gemini-ontwerp (Jordi, 7 nov)
- Nieuwe poging via een Gemini-prompt met hoofd + pose als bijlagen: `gemini/PROMPT.md`. Jordi: "ik wil dat die geen shirt heeft, en dat de broek gele en groene strepen hebben als patroon. er zit zon typisch capoeira touwtje aan de broek en ik wil dat zijn armen een soort van muay thai banden hebben, maar dan meer capoeira mode".
- Jordi: "belangrijk is dat die echt hitmon blijft en dus niet mens, dus verhoudingen van hoofd, handen en voeten zijn groter dan de benen en armen".
- Jordi (na Gemini ronde 2): "de broek mag ook echt minder een broek zijn en gewoon meer de benen met kleur".

## Nog open
- Kleur van de koordjes, gezicht/uitdrukking, de vorm van de kleine hoorn.

## Sprite uit model v3 (6 nov)
- Silhouet: D gekozen (Jordi: "is niet erg, het is een silhouet, ga maar een sprite bouwen dan kijken we verder"; D = gedrongen romp, kop iets groter, benen net wat korter, voeten en handen iets groter).
- Sprite ronde 1 (`sprite_model/`, kleur per script uit de verkleinde render): Jordi: **"lachwekkend slecht"**. Afgekeurd. Oorzaak (Claude): kleur per script gekwantiseerd uit de render, in strijd met de vaste regel "kleurt nooit per script"; het resultaat leest als een verkleinde 3D-render, niet als een getekende Hitmon-sprite.
- **Focus volgende keer (Jordi, 6 nov): "dat hij zo ACCURAAT mogelijk is tov het model".** Elke vorm, kleurvlak en detail van `model_gemini_pose_v3.png` volgen, met de hand getekend; niets toevoegen of vereenvoudigen wat niet in het model staat.

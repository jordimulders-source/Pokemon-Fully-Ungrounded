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

## Nog open
- Kleur van de koordjes, gezicht/uitdrukking, de vorm van de kleine hoorn.

# Spriting: regels uit de Dragonfly Cave-gidsen

Bronnen (van Jordi, 23 okt): `docs/lessen/bronnen/dragonflycave_spriting_guide.pdf` (*Spriting Guide*, The Cave of Dragonflies) en `make_fakemon_guide.pdf` (*Making Fake Pokémon*). Lees dit samen met `FAKEMON_DESIGN.md` **vóór elke spriteronde**. Hieronder de regels, en per regel wat wij fout deden.

## 1. Gereedschap: alles met de hand, nooit met vormfuncties
- **Gouden regel van omlijnen: gebruik geen vormgereedschap** (cirkel/ellips-tool). De computer tekent de wiskundig dichtste benadering van een cirkel, maar die is niet de mooiste: een met de hand getekende 'cirkel' is gladder voor het oog.
- Alleen een 1-pixel-potlood, emmer zonder anti-aliasing, geen verkleinen/vergroten van de sprite zelf.
- **Wat wij deden:** vormen met PIL-ellipsen en -polygonen, schaduw en omlijning met scripts. Dat is precies de 'wiskundige cirkel'. Daarom oogden onze sprites als plastic speelgoed.

## 2. Werkwijze: grof tekenen, dan per onderdeel gladstrijken
- Teken de grote lichaamsdelen eerst **grof met de hand** (als een krabbel), en strijk elk deel daarna **pixel voor pixel** glad tot een nette 1-pixel-omlijning. **Eén lichaamsdeel tegelijk**, nooit de hele sprite in één keer.
- Kleine details (klauwen, vingers) pas als de grote vormen staan; dunne ledematen pixel voor pixel.
- Riskante delen op een aparte laag of kopie.
- **Pixel-over** is een erkende methode: verklein een tekening (Sugimori-art of een eigen modeltekening) tot spriteformaat en trek hem met de hand over, met de regels van het omlijnen. **Dit is de logische stap na onze modeltekeningen**: de goedgekeurde tekening verkleinen tot ±64 px en met de hand overtrekken, in plaats van een bestaande sprite als skelet te nemen.
- Hoe groter de sprite, hoe exponentieel moeilijker: blijf bij het Gen 3-formaat (max. 64×64, de figuur meestal kleiner).

## 3. Lijnen, hoeken en curven
- Een schuine lijn = segmenten die telkens 1 pixel verspringen; een regelmatig patroon (bijv. 1-2-1-2) leest als recht. Liever een eenvoudiger helling dan een 'bobbel'.
- **Hoeken** (corner) wijzen schuin, **punten** (point) recht; samen 8 richtingen. Gebruik ze alleen voor echte scherpe punten (klauwen).
- **Curven:**
  - tussen een horizontaal en een verticaal segment langer dan 1 moet minstens één 'neutraal' segment van 1 pixel zitten;
  - **nooit een hoek of punt in een curve** (geeft een zichtbaar 'spijkertje');
  - geen 'besluiteloosheid': de segmentlengtes moeten geleidelijk oplopen of aflopen (bijv. 1-1-2-3), niet heen en weer (3-1-2-2-1 leest als wiebelig);
  - een lange rechte lijn die abrupt in een andere overgaat, breekt de curve; laat de helling geleidelijk veranderen.
- **Symmetrie en identieke delen verraden een nep-sprite**: nooit een lichaamsdeel kopiëren en spiegelen voor de andere kant. *(Onze nachtaap: frontaal en symmetrisch.)*

## 4. Kleuren en palet
- Per kleur **3 tinten** (hooglicht, basis, schaduw) plus een donkere omlijningstint; de relatieve helderheid tussen de tinten blijft altijd gelijk.
- Alle tinten van een kleurgroep in dezelfde tint; schaduwen eventueel een beetje richting blauw.
- **'Overshaden'** (meer tinten, verlopen) ziet er nep uit. Werken met een beperkt palet is juist de kunst.
- Neem kleuren liefst over van een bestaande sprite met ongeveer die kleur (geen te felle eigen kleuren).

## 5. Licht en schaduw
- **Licht komt van linksboven** bij een sprite die naar links kijkt (rechtsboven als hij naar rechts kijkt). Denk aan een spuitbus vanuit die hoek: wat de verf raakt is licht, de rest schaduw.
- De grens basis/schaduw ligt op de **'evenaar'**: de grens tussen de delen die naar het licht en van het licht af gekeerd zijn. Volg de ronding van het lijf; delen achter het lijf (staart) krijgen veel schaduw.
- Hooglicht klein en precies waar het licht loodrecht valt; **slagschaduw** van een ander lichaamsdeel altijd volledig in de schaduwkleur; de extra donkere tint alleen waar zowel direct als teruggekaatst licht ontbreekt.
- **R/S-stijl gebruikt veel van de hooglichtkleur** (de Yellow-Scyther met witte glimlichtjes oogde donkerder dan de R/S-Scyther met veel lichte groentint). Te weinig hooglicht maakt een sprite te donker.

## 6. Glans en ogen
- Glans (*shine*) = een klein rond, bijna wit vlekje waar het licht naar de kijker weerkaatst; niet op elk hooglicht, alleen waar het oppervlak glanst.
- **Ogen:** kraalogen (zoals Pikachu en Eevee) hebben **altijd een witte glansvlek én een gekleurde reflectie aan de tegenoverliggende kant** (teruggekaatst licht). Dat geeft diepte. *(Onze ogen: grote ronde 'brillenglazen', egaal gloeiend of poppenogen met te veel glans: Jordi: "de ogen zijn vaak niet echt Pokémon-achtig".)* Bij zeer glanzende delen een beetje teruggekaatst licht in de schaduw, eventueel gedithered (Voltorb).

## 7. Texturen
- **Vacht:** maak de grens tussen basis en schaduw **gekarteld, zoals de vacht zelf**, eventueel met wat dithering en korte streepjes in de haarrichting. Niet overdrijven. Ook voor veren. *(Alpaca: 'klonterige wolschaduw'.)*
- **Schubben:** meestal weglaten, of groot genoeg om met omlijning te tekenen (Magikarp).
- **Rots/staal:** opdelen in vlakke vlakken, die elk één tint krijgen; elke lijn moet echt twee vlakken scheiden.
- De meeste Pokémon: gewoon zoals de bol hierboven; het zijn tekenfilmwezens.

## 8. Omlijning (de grootste les)
- **Volledig zwarte omlijning oogt 2D en tekenfilmachtig** (de guide laat het zien bij de Scyther-revamp). *(Precies wat Jordi bij de nachtaap zei: "heel cartoony"; onze meting: donkere rand 0,93 tegen 0,35–0,6 bij Gen 3.)*
- Omlijning per kleurgroep:
  - **zwart** (of bijna-zwart) rond de schaduwkant;
  - de **omlijningsbasis** (een donkere tint van die kleur) rond de basiskleur;
  - de **schaduwkleur als omlijnings-hooglicht** op de meest belichte randen;
  - eventueel (Pikachu) de schaduwkleur als extreem hooglicht op de lichtste randen.
  - Overgang langs de omtrek: helemaal zwart → zwart met een pixel omlijningsbasis aan de binnenkant → omlijningsbasis → omlijningsbasis met een pixel hooglicht aan de binnenkant → een paar segmenten hooglichtkleur.
- Omlijning altijd **1 pixel breed**, geen klonten zwart.
- **Anti-aliasing alleen aan de binnenkant** van de omlijning (lichtere pixels naar binnen), **nooit aan de buitenkant**: dat geeft lelijke gekleurde puntjes op een andere achtergrond.
- **Pseudo-omlijning:** dunne delen van 1–2 pixels (bijv. een rand van Scythers sikkels) niet omlijnen, maar alleen met kleur scheiden.

## 9. Overige sprites (voor later)
- Gen 3: voorkant 64×64, 2 frames (Emerald); achterkant 64×64, vergroot en links/onder afgesneden; party-icoon 32×32 in 2 frames (bovenkant bijna-zwarte omlijning, onderkant grijze omlijning om diepte te geven; slechts 3 icoonpaletten); overworld 32×32 (kleine 16 breed), grote 64×64; voetafdruk 16×16 als silhouet.
- Shiny = alleen een ander palet; binnen een lijn meestal dezelfde shinykleuren.

## 10. Uit de fakemon-guide (aanvullend op FAKEMON_DESIGN.md)
- Drie soorten fakemon: origineel, tegenhanger van een bestaande, en (pre-)evolutie. Lijkt een idee te veel op een bestaande Pokémon, overweeg het dan in die lijn op te nemen of maak het juist duidelijk anders.
- Grootte en stadia volgen de game: vroeg = klein eerste stadium (3 stadia als de eindvorm groot is), midden = groter begin, laat = grote losse soort. **Pre-evoluties zijn bijna altijd kleiner, schattiger en eenvoudiger.**
- Type: liever een nieuwe combinatie, of een type dat soortgelijke Pokémon nog niet hebben. Geen idee? Normal.
- Stats: begin bij een vergelijkbare Pokémon en schuif; HP = dik/groot, Defense = pantser, Sp. Def = vacht/vet (isolatie), snel = klein en slank. Krachtige gimmick = lage stats.
- Evolutie: max. 3 stadia per lijn; geen level-evolutie na een steen-, ruil- of vriendschapsevolutie (behalve baby's); steen-evoluties leren daarna nauwelijks nog moves.
- Level-up-moves: 1–2 startmoves (zwak, meestal Normal, ≤ 40–50 kracht), een vast ritme van levels (bijv. om en om 2 en 4), na evolutie ruimer; nooit meer dan 3 statusmoves op rij.
- Sekseverschillen alleen als de soort daar reden voor geeft; bij dieren is het mannetje meestal het opvallendste, geen menselijke stereotypen.
- Naam: meestal een samentrekking van een woord voor het type en een woord voor het basisdier/-voorwerp; niet te obscuur.

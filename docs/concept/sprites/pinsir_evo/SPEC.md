# Pinsir-evolutie (Bug/Ground)

## Jordi, letterlijk
- 9 nov: "een enorme tor/kaiju-hybride; welke tor nog bepalen, kunnen ook meerdere combineren."
- 22 nov: "tijd voor een pinsir evolutie".
- 22 nov: "sabeltandboktor, kaiju op twee poten, Bug/Ground blijft"
- 22 nov: "hij moet echt wel een evolutie van Pinsir ogen ook, dus wat meer stekels en typische dingen die kaiju hebben"

## Besloten
- Tor: **sabeltandboktor** (*Macrodontia cervicornis*, Amazone).
- **Kaiju op twee poten.**
- Type **Bug/Ground** (zoals Pinsir).
- Moet duidelijk een Pinsir-evolutie zijn; **meer stekels** en typische kaiju-dingen.

## Open
- Naam, evolutiemethode/level, kleuren (geen wens van Jordi).
- Golofa: nu waarschijnlijk regional Heracross (niet besloten).

## Voorstel Claude (niet van Jordi)
- Pinsir-herkenning: bruin lijf, het gezicht met de getande bek, de twee grote stekelscharen op de kop, korte stevige armen. Sabeltandboktor: die scharen worden de lange gebogen sabelkaken, schorspatroon op dekschilden/rug, lange gesegmenteerde antennes.
- Kaiju-dingen in de prompt: rechtop op twee zware poten, dikke staart, rij stekels/platen over de rug, zware gebogen houding.

## Rondes
- Prompt r1: `gemini/PROMPT.md` (nieuw gesprek, geen bijlage).
- r1 (`gemini/r1.png`), Jordi: "de dubbele mond ben ik geen fan van, die gekke voelsprieten passen ook niet, kleur beetje te monotoon, verder conceptueel wel prima, maar zou dit vertalen naar een sprite?"
  Claude: kale reductie naar 64 px (`plak/r1_64_8x.png`): de kaken nemen ±40 % van de hoogte, waardoor kop en lijf klein worden; gezicht wordt ±10 px (brij), de zaagtandjes en stekels worden losse pixels, de schorstekening valt weg. Conceptueel vertaalt het, in deze verhouding niet goed. Prompt r2 (nieuw gesprek, geen bijlage): `gemini/PROMPT_r2.md` (Jordi daarna: "ik heb liever de reguliere pinsir mond wat groter", "en stekeliger"; één bek, geen antennes, meer kleurcontrast; als voorstel van Claude: grotere kop en lijf, kaken iets korter, stekels groot genoeg voor 64 px).
- r2 (`gemini/r2.png`), Jordi: "dit is teveel pinsir". Prompt r3 (nieuw gesprek, geen bijlage): `gemini/PROMPT_r3.md` = basis r1 + Jordi's punten; van Pinsir alleen mond en scharen (Claude), kleuren van de echte sabeltandboktor in plaats van Pinsir-bruin (Claude), kopschild met stekelranden (Claude, van de echte kever); kaaklimiet van r2 geschrapt.
- Jordi bij r2: "dan was de vorige beter", "ik zie die tor ook niet erin die je bedoelde". Prompt r3 daarom op r1 gebouwd, met meer van de echte kever: kaken naar voren gericht en naar elkaar toe gebogen zoals de echte sabeltandboktor (Claude), kopschild, schorspatroon, keverkleuren.
- r3 (`gemini/r3.png`), Jordi: "lijkt dit op die tor?" Claude: deels; kaken en dekschilden wel, kopschild leest als hoed, dekschilden bij de echte kever lichter (crème/okergeel met zwarte vlekken).
- Jordi bij r3: "de kaken lijken nu vooral een beetje opgeplakt, anders dan bij de echte sabeltandboktor". Prompt r4 (`gemini/PROMPT_r4.md`) = r3 + kaken dik aan de basis, vergroeid met de kophoeken naast de mond.
- r4 (`gemini/r4.webp`), Jordi: "ik vind hem wel tof, alleen die kaken wijken een beetje af omdat ze een totaal andere kleur hebben", "en de vleugels zitten gek", "of heeft hij 4 vleugels en zien we er maar 2/". Claude: kaken omgekleurd zonder Gemini (`kaakkleur/`: A kopbruin, B donker roodbruin; `vergelijk.png`). Vleugels: echte kevers hebben 2 harde dekschilden + 2 vliezige vleugels eronder; dicht zie je alleen de dekschilden, plat op de rug met een naad in het midden. In r4 is maar één dekschild te zien, als schild op de zij. Bijstuurprompt r5 (bijlage = r4 met gekozen kaakkleur, alleen vleugels): `gemini/PROMPT_r5_bijsturen.md`.
- Jordi over de vleugels: "nee maar dan is het goed, want dan heeft die 2 extra vleugels maar buiten beeld". Vleugels blijven zoals in r4; bijstuurprompt r5 vervalt.

## Model gekozen (22 nov)
- **r4 met kaakkleur B gekozen**, Jordi: "en rechts is de beste kleur", "ga maar bouwen daarmee". Bevroren model: `referenties/gemini_gekozen_r4B.png` (r4 van Gemini, kaken door Claude omgekleurd naar donker roodbruin; vleugels zoals r4).
- Frontsprite r1: maker gestart.
- r1 (`sprite_r1/`): mond en kaken goed; Claude: poten vlekkerig, schorspatroon weg, te veel zwart, ruis op stekels. Jordi bij r1: "ogen zijn ook gewoon een rij witte pixels".
- r2 (`sprite_r2/`): ogen met pupil en wenkbrauw, schildtinten naar het model, stekels netter, zwart 29 %. Claude: poten nog vlekkerig (losse lichte plekken in plaats van ronde platen); verse maker alleen voor poten/onderlijf (r3).
- r3 (`sprite_r3/`, verse maker, alleen onderlijf): platen met schaduw en glans, lichter dan het model; Claude: beter, maar nog druk. Naar Jordi: `sprite_r3/naast_model.png`.
- Jordi bij r3: "ogen niet goed en beetje zelfde probleem als pitahaya fase 3 had" (daar: geen belijning tussen delen/blur, schaduw en kleur niet optimaal, te weinig contrast). r4: verse maker, kleurronde over de hele sprite (contrast, licht/schaduw per vorm, lijnen tussen delen) + 3 oogvarianten.
- r4 (`sprite_r4/`, verse maker): kleurronde (lijf 61/95/131/175, kaak 57/91/135, schild 56/106/157), 3 oogvarianten A/B/C; zelf: onderlijf midden nog druk. Naar Jordi: `sprite_r4/ABC_8x.png`.
- Jordi bij r4: "oog a is goed, hij is nog steeds super blurry, het ligt aan het feit dat er niet genoeg kleurtinten gebruikt worden en de lijnen te zacht zijn", "en nee dat betekent niet meteen zwarte lijnen doen nu". r5: oog A bevroren, volle palet (16), hardere lijnen via gekleurde donkere tinten per onderdeel, geen extra zwart.

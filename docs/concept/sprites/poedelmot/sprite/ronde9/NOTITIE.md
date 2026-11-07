# Poedelmot sprite ronde 9 (6 nov): de onderkant volgens Jordi's rode vormen, vanuit ronde 8

Jordi op ronde 8 (letterlijk): "je luistert weer niet, waarom is er nu weer aan de linkerkant een uitstulpsel. Al 2 keer gevraagd om dat niet te doen, en de rechterpoten zitten weer niet vast en hangen er weer onnatuurlijk bij. Ga eens kijken of je de ruimte binnen mijn rode vormen kan implementeren, dat zijn schetsen, geen harde lijnen"

Schets: `referenties/jordi_schets_ronde8_vormen.png`.

## De schets over ronde 8 gelegd (`overlay.py`)
- **Passing:** de schets is ronde 8 (versie 8b) op **10×** (niet 9,4×), verschoven met (-9, -51) px. Sprite-x is dus (px+9)/10 en sprite-y is (py+51)/10. Bij die passing valt 92,5 % van de niet-rode spritepixels op dezelfde kleur. Ik heb die passing gezocht over schaal en verschuiving, ook tegen ronde 8 vóór 8b; 8b past net iets beter.
- **Rode vormen in spritecoördinaten (wat ik zie):**
  1. **Kruis links:** x10-15, y45-51, precies op de bult van de flanklob van 8b. Dat is het uitstulpsel dat weg moet.
  2. **Midden, twee lussen:**
     - de eerste is een U van de achterkant van de linkervoorpoot (x22, y55) omlaag tot y58 (x25) en weer omhoog tot x28-29, y51;
     - de tweede lus loopt van x29-30, y50 rechtsom via x31, y54 terug naar x27, y57.
     - Samen beslaan ze de ruimte tussen de voorpoten onder de buik (x22-31, y50-58). De tweede lus ligt ook over de linkerrand van de rechtervoorpoot (x29-31).
  3. **Rechts, een lange lus:** twee verticale streken van x38-41, y42 (onder de vleugel, in de inham tussen arm en vleugel) tot y56. Een onderstreep loopt van x35, y56 (de achterkant van de rechtervoorpoot) tot x41.
     - Daarbinnen liggen: de inham, het stuk achterlijf links van R1, S, en het gat tussen rechtervoorpoot en S onderaan.
     - R1 (x42-44) en het rechterdeel van het achterlijf vallen **buiten** de lus.

## Wat er gedaan is
- **Links (kruis):** de bult is weg. De linkerrand loopt nu glad en gesloten door: x16 → x15 → x14 (y41-43), recht omlaag langs x14 (y43-50) en dan via x15 (y51) naar de linkervoorpoot (x16, y52). Er is geen bult of punt meer. Het kruis valt nu volledig naast het lijf (controle: 0 rode cellen op het lijf links van x16).
- **Midden (U):** de ruimte tussen linkervoorpoot, buik en rechtervoorpoot is gevuld met wol in schaduwtint, zonder naad met de buik (x22-29, y52-57). Onderaan zitten een punt en 2 klauwtjes op y58, de grond van de linkervoorpoot.
- **Rechts (lus):**
  - de inham tussen arm en vleugel (x39-43, y41-45) is gevuld;
  - S is nu een kolom die uit het lijf onder de vleugel doorloopt tot de grond (x35-41, y42-57). Hij sluit onderaan aan op de rechtervoorpoot (onderstreep), met een punt en 2 klauwtjes op y58.
  - Hij hangt niet meer: hij is net zo breed als het lijf erboven.
- **Voorpoten:** ongewijzigd ten opzichte van ronde 6 (controle: 0). Er liggen wel rode lijnstukken over de voorpoten: (22,55) aan de linkervoorpoot, en (30-31, y52-56) en (34-35, y55-56) aan de rechtervoorpoot. Daar staan de voorpoten vóór de gevulde ruimte. Ik heb ze niet veranderd, want de vorm zit erachter.
- **Niet aangeraakt, buiten de vormen:** R1 en het rechterdeel van het achterlijf (x42-45).

## Toets (`paneel.png`: schets over ronde 8, schets over ronde 9, ronde 9 los, alle drie op 8×, plus de onderkant op 16×)
- De vulling valt binnen zijn vormen, in het midden en rechts.
- Links is geen uitstulpsel meer, ook niet op 1×.

## Controle (`controle.txt`, `diff.png`)
- 81 px gewijzigd tegen ronde 8, 0 buiten de drie zones.
- Voorpoten: 0 gewijzigd tegen ronde 6.
- 0 lichte pixels op de buitenrand, 0 ingesloten gaten, 13 kleuren.

## Zwakke punten (eerlijk)
1. **Linkerrand:** die is nu een recht stuk van 8 px (x14, y43-50). Hij is glad en zonder bult, maar recht.
2. **Midden:** de gevulde ruimte tussen de voorpoten is één donkere wolmassa met één punt en 2 klauwtjes. Op 1× leest hij eerder als schaduw onder de buik dan als een poot. Ik heb zijn vorm gevuld en niets bijverzonnen.
3. **R1:** het kleine pootje rechts buiten de lus is onveranderd. Of dat ook "hangt", moet Jordi zeggen.
4. Een onafhankelijke keurder is nog niet geweest.

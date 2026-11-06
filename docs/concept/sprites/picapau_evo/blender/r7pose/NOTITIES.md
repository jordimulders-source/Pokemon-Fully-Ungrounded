# Evo van Picapau: pose-proef r7pose (vanuit P3, naar Pidgeot)

## Jordi letterlijk
- Over de poseproef r6pose: **"ik kies p3, en hij mag nog iets meer naar rechts draaien, net als gen 1 raichu beide ogen in beeld, of gaat het niet passen om ook de linkervleugel in de sprite te krijgen lichtjes? Zijn er vogel sprites die dat hebben?"**
- Aanvulling: **"ja pidgeot toont hoe het moet"**

## Pidgeot bestudeerd (`graphics/pokemon/pidgeot/anim_front.png`, eerste frame, op 8×)
- **Lijf en kop:**
  - Het lijf staat ±45–55° naar links-voor. Borst en buik zie je schuin van voren, met de lichte buik links.
  - Het lijf loopt van de kop linksboven schuin naar de staartwaaier rechtsonder.
  - De kop draait verder naar links dan het lijf en staat bijna in profiel, met de kuif als lange band naar achteren (naar rechts).
- **Vleugels:**
  - De verre vleugel (links in beeld) steekt achter de kop hoog uit, schuin omhoog naar de linkerbovenhoek. Hij is smal (±8–10 px) omdat hij schuin wegdraait, maar je ziet de veren als waaier.
  - De nabije vleugel (rechts) staat groot en wijd open naar rechtsboven, met de handpennen in een waaier tot de rand van het beeld.
- **Snavel en ogen:**
  - De snavel wijst naar links en iets omlaag en steekt links buiten de kop uit.
  - Je ziet maar één oog (het nabije), vlak achter de snavelbasis. Het verre oog is niet te zien.
  - Beide ogen staan dus niet bij Pidgeot. Die zie je wel bij Raichu Gen 1 en Ho-Oh.
- **Poten:** beide poten staan naar voren gestoken met gespreide klauwen. De verre poot staat links en hoger, de nabije lager in het midden. Pidgeot zit in een vliegpose met de klauwen vooruit.

## Varianten (vanuit P3: lijf 55, kop +5, achterover 30; beide ogen aan)
- **Eerste proef Q1–Q3** (`eerste_proef/`): meer lijf- en kopdraai (60–72, kop +12–14) met de snavel schuin omlaag.
  - Resultaat: de kop staat recht van voren en de snavel wordt korter. Het leest als een uil, niet als Pidgeot.
  - Ik heb ze laten staan, maar ze zijn vervangen door R1–R3.
- **R1–R3:** het lijf blijft 3/4 zoals P3, de kop draait iets meer dan het lijf (+5 tot +12) en de snavel wijst naar links (schuin −6° tot +2°).
  - De verre vleugel is opgetild, naar buiten gezet en om de schouder naar buiten geklapt (`VERRE_OPEN`), zodat hij zoals bij Pidgeot links achter kop en borst omhoog uitsteekt.
  - De nabije vleugel staat groot open rechts, zoals in r5.
  - Het verre oog staat aan en zit dicht bij de snavelbasis (oog_az 40–42).

| variant | lijf | kop extra | snavel | verre vleugel opgetild / opengeklapt |
|---|---|---|---|---|
| R1 | 55 | +5 | +2 | 11 / 25° |
| R2 | 58 | +9 | −2 | 12 / 32° |
| **R3 (gekozen)** | 62 | +12 | −6 | 13 / 38° |

- Bestanden:
  - `vel_pose.png`: Pidgeot eerst, dan R1–R3, P3, Ho-Oh, Fletchinder en Raichu Gen 1, op 1×, 4× en als render.
  - `maak_pose.py` (`STAP=0.5`).
  - `picapau_evo_r7pose.py` (kopie van r6pose, met `TWEE_OGEN`, `SNAVEL_HOEK`, `VERRE_VLEUGEL` en `VERRE_OPEN`).

## Keuze: R3
- **Verre vleugel zoals Pidgeot.** Hij steekt het duidelijkst uit: links achter kop en borst omhoog, als smalle waaier.
- **Nabije vleugel.** Groot open rechts.
- **"Iets meer naar rechts" gedraaid.** Lijf 62°, kop +12°, en de kop draait meer dan het lijf.
- **Beide ogen in beeld.** Het verre oog is net zichtbaar achter de kopwelving links van het nabije, zoals Raichu Gen 1.
- **Snavel.** Hij wijst naar links en iets omlaag, en de open beitelsnavel leest nog als boven- en ondersnavel.
- **Basis van P3.** Achterover en de bolle buik naar voren blijven.

## Past het in 64×64? (eerlijk)
- **Ja, het past.** Alle varianten passen op dezelfde schaal (0,80) in 61 px, zonder te krimpen tegen P3.
- **De verre vleugel is wel smal.** Op 1× is hij een strook van ±5–7 px breed en ±15 px hoog links van de kop. Pidgeot krijgt hem groter doordat hij in vliegpose het hele frame vult en geen bliksem en staartlus naast zich heeft. In de sprite kan de waaier met de hand 1–2 px breder en duidelijker.
- **Het verre oog is op 1× klein:** 1–2 px. In de sprite neem ik het verre oog smaller over (half oog achter de kopwelving), zoals bij Raichu Gen 1.
- **Krappe linkerkant.** De bliksem staat links tegen de buik en de verre vleugel links boven. In de sprite is daar weinig ruimte: de bliksem moet iets lager en naar links, zodat vleugel, buik en bliksem elk een eigen plek hebben.

Er is niets gecommit.

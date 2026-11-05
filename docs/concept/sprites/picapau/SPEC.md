# Picapau (Electric/Flying, middelste/hoofdvorm): SPEC

Bron: *Celeus flavus* (cream-colored woodpecker), Amazone. Concept: `docs/concept/IDEEEN.md` (Roomkleurige specht). Convergente soort van Pikachu via kleur en tekening (niet via vorm).

## Jordi letterlijk
- "Dit is net Pikachu, hier moet ik iets mee." (5 nov)
- "Wordt electric/flying uiteraard en in ons ontwerp wordt het nog net wat meer pikachu dan irl" (5 nov)
- "Picapau is echt geniaal" (naam, 5 nov)
- "begin met picapau" (5 nov)
- Bij foto 3–6: "Je kan als inspiratie ook pikipek gebruiken, zorg wel dat het geen pikipek kopie wordt. Maar de pose kan vergelijkbaar zijn ... Dus vleugels dicht, snavel wat meer omhoog, en maak het nog iets meer pikachu dan de echte vogel, misschien dat we nog iets van de staart of de oren van pikachu erin kunenn verwerken, bijv dat de top van de kuif zwart wordt zoals pikachu's oren"
- Silhouet geknipt uit foto: "nee maak ook een model", "want nu ga je slordig knipwerk doen" → afgekeurd.
- Model v2: "geweldig idee qua design! nu nog iets meer een pose zoals op een van de fotos"
- Model v4: "nu nog de goede angle pakken, kan je er een paar klaarzetten op ong driekwart"
- Hoeken: "b1 is het beste, zorg wel dat de poten vast aan het lichaam zitten"

## Referenties
- `referenties/jordi_foto1_zijaanzicht_tak.png`: zijaanzicht op een tak; bron voor de massa (lijf, kuif, staart als steun, houding).
- `referenties/jordi_foto2_stam_verticaal.png`: klimhouding tegen een stam (staart als steun, tenen).
- `referenties/jordi_foto3..6_*.png`: kop close-up, rechtop met snavel omhoog (foto 4 = houding), rug tegen stam, kop schuin.
- `referenties/vergelijking_vogels_pikachu.png`: Pikachu, Pikipek, Trumbeak, Toucannon, Taillow, Starly, Chatot, Emolga op 4× + foto 1 gespiegeld.

## Onderdelen
| onderdeel | bron | Jordi | status |
|---|---|---|---|
| model | `blender/picapau.py` (één huid, SDF), stand B1 = lijf 30°, kantel 8° (`blender/b1.py`) | "geweldig idee qua design"; "b1 is het beste" | gekozen |
| pose | schuin lijf (linksboven → rechtsonder), kop en snavel omhoog (40°), vleugels dicht | "vleugels dicht, snavel wat meer omhoog" | gekozen |
| poten | dijen in de huid, poten groeien uit het lijf | "zorg wel dat de poten vast aan het lichaam zitten" | gedaan, wacht op Jordi |
| silhouet | `silhouet/silhouet_b1_1x.png` uit de B1-render | – | wacht op Jordi |
| kuif (= Pikachu-oren) | twee punten + rafelige achterkuif | "de top van de kuif zwart ... zoals pikachu's oren" | in model |
| wangvlek (= wangzak) | foto 1 | – | open |
| vleugels (= rugstrepen) | foto 1: donkerbruin met roomkleurige schubben | – | open |
| staart (= bliksemstaart) | foto 1/2: stijve roodbruine steunstaart | – | open |
| kop, oog, snavel | Pikachu-kop, beitelsnavel | "net wat meer pikachu" | open |

## Afgekeurd (niet herhalen)
- Silhouet geknipt en vervormd uit foto 4 (`silhouet/silhouet_v1*`): "slordig knipwerk".
- Pikipek-kopie: alleen de houding mag vergelijkbaar zijn.
- Stippen op de vleugel in het model zijn een plaatshouder: in de sprite geschubde veren (foto 1, 5).

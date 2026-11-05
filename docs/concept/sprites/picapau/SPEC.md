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
- Silhouet B1: "goed silhouet" (5 nov) → **bevroren**.

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
| poten | dijen in de huid, poten groeien uit het lijf | "zorg wel dat de poten vast aan het lichaam zitten" | gedaan (in het bevroren silhouet) |
| silhouet | `silhouet/silhouet_b1_1x.png` uit de B1-render; toonkaart `blender/B1/toonkaart_1x.png` | "goed silhouet" | **bevroren**; alleen dunne delen (snavelpunt, kuiftoppen, achterkuif, tenen) ±1 px, gemeld |
| kuif (= Pikachu-oren) | twee punten + rafelige achterkuif | "de top van de kuif zwart ... zoals pikachu's oren" | in model |
| wangvlek (= wangzak) | foto 1 | – | open |
| vleugels (= rugstrepen) | model: donkerbruin met ronde lichte stippen | "ik vond die stippen ipv die pidgey vleugels leuker" | besloten: stippen |
| staart (= bliksemstaart) | foto 1/2: stijve roodbruine steunstaart | – | open |
| kop, oog, snavel | Pikachu-kop, beitelsnavel | "net wat meer pikachu" | open |

## Afgekeurd (niet herhalen)
- Silhouet geknipt en vervormd uit foto 4 (`silhouet/silhouet_v1*`): "slordig knipwerk".
- Pikipek-kopie: alleen de houding mag vergelijkbaar zijn.
- Geschubde (Pidgey-)vleugels: Jordi vindt de stippen van het model leuker.

## Stand (5 nov)
- Kleur r1–r5 door één maker-agent; verse keuring na r3 (`kleur_r3/KEURING.md`: B gekozen, reparaties gedaan in r4/r5). Versie B wijkt 23 px af van het bevroren silhouet (dikkere snavelbasis, poten los met tenen, ronde buik; lijst in `kleur_r3/controle_B.txt` + `kleur_r5/controle_uitvoer.txt`). `kleur_r5/picapau.png` + `voor_jordi.png`: **Jordi: "ja ik vind dit weer tenenkrommend hoor"** (afgekeurd; eerst vragen wat hij ziet).
- Open (uit het silhouet, ter info): voorrand vrij recht, kuiftoppen op 1x klein, 831 px is klein voor een middelste vorm.

## Afgekeurd r5 (Jordi, 5 nov), letterlijk
"ja ik vind dit weer tenenkrommend hoor" · "alsof we elke keer weer opnieuw moeten beginnen" · "hij lijkt volledig 2d, het is geen drie kwart, het perspectief klopt niet, de klauwen zijn weer afgeknapt, de shading is weer niet goed, de snavel is weer weg" · "waarom moet ik dit allemaal voorkauwen" · "ga eens goed kijken wat een sprite goed maakt, welke lessen we geleerd hebben, dragonflycave etc etc" · "wat er in de eerdere sessies wel goed ging"
**Oorzaak (Claude):** (1) model zonder aparte kopdraai: de kop draaide mee met het lijf = profielkop (les kolibrie pre-evo: "een profiel draaien geeft geen 3/4"); (2) model niet op 64 px gecontroleerd (les nachtaap): snavel en tenen vielen weg bij het verkleinen en werden niet in het silhouet hersteld (les wasbeer); (3) Claude liet het zelf door. De lessen van na 25 okt stonden op andere branches.
**Model v5 afgekeurd** (Jordi: "je moet het model niet aanpassen" · "de SPRITE" · "en nu is het model veel lelijker ook" · "het model was helemaal perfect" · "'model is geweldig', claude gaat weer aan het model werken, ipv aan de sprite waar het juist fout gaat"). `blender/picapau.py` is terug naar het goedgekeurde B1-model (render opnieuw: 0 px verschil met `B1/b1.png`). **Model en B1 zijn bevroren; al het werk zit in de sprite.**

- Jordi (5 nov) bij de B1-render: **"aan dit model gaan we niks veranderen, deze is subliem"**.

## Sprite v2 (5 nov): overtrekken van de B1-render
Bron: `sprite_v2/bron/` (`bron.py`: kleur per spritepixel uit `blender/B1/b1.png`, onderdelen uit `blender/B1/labels.png` (`blender/labels.py`), `overtrekvel.png` met raster). Methode van lama fase 3 (kop/onderdelen cel voor cel van het model, niet hertekenen).

- **Jordi over sprite v2 r2 (5 nov), krabbel `referenties/jordi_krabbel_r2_model_genegeerd.png`:** "ik heb hier een aantal lijnen neergezet om aan te geven waarin het model genegeerd wordt". Lezing Claude: (1) twee lijnen in de kuif: de twee kuifpunten zijn in het model eigen kegels die van de kop loskomen (vorm over vorm), in de sprite smelten ze in één gele massa; (2) lange boog van onder de wang langs de borst naar de onderkant van de buik: de bolle borst/buik van het model (ronde voorkant die onderaan naar rechts omkrult), in de sprite een rechte voorkant; (3) korte boog bij de vleugelvoorrand: de ronde schouder/voorrand van de vleugel over het lijf.
- Jordi (5 nov): "maar dat is niet alles" (krabbel = voorbeelden; Claude maakte zelf de volledige lijst render vs r2: kop, kuif, oog, wang, snavel, borst/buik, vleugel, poten, staart, licht) · **"het lichaam moet echt bol, dat is juist een kenmerk van pikachu"** · **"en ik vond die stippen ipv die pidgey vleugels leuker"** → vleugel met de ronde stippen van het model, geen schubben.
- Jordi over sprite v2 r4 (5 nov): **"het lichaam is beter maar het hoofd rechts negeert weer compleet mijn instructies"** (= de twee kuif/kop-lijnen uit zijn krabbel; rechterkant van de kop in r4 een rechte rand) → r5: krabbellijnen teruggerekend in de sprite, ronde achterkant van de kop, bewijs `krabbel_over_r5.png`.
- Jordi (5 nov): **"daar zijn opeens ook allemaal rare onnodige aanpassingen gemaakt"** (kop rechts in r4) · **"die nergens op lijken, niet kloppen met het model, niet kloppen met mijn instructies, gewoon dom hallucineerwerk"** → kop rechts terug naar r2 (waarop hij tekende) + alleen zijn twee lijnen en de ronde achterkant.
- Jordi (5 nov): **"hij moet niet alleen mijn lijnen toevoegen, hij moet oa aanpassingen doen nav die lijnen"** → op de aangewezen plekken de sprite naar het model aanpassen.
- Jordi (5 nov): **"en als er aanpassingen gebeuren moet dat allemaal uit te leggen zijn waarom het nu dichter in de buurt komt van het model"**.

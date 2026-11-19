# Gemini-prompt: Picapau in driekwart (19 nov)

Jordi: "die moet gewoon driekwart staan en voor de rest precies hetzelfde." Design = bevroren (SPEC.md; B1-model "subliem").

## Bijlagen
1. `bijlage1_huidige_sprite_8x.png`: huidige sprite (kleuren, kenmerken).
2. `bijlage2_model_b1.png`: het goedgekeurde 3D-model (vorm, bolle buik, kuif).

## Prompt v1
```
Redraw this Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), now in a proper 3/4 view.

ATTACHMENTS
- Attachment 1 is the current sprite, attachment 2 is the approved 3D model. The DESIGN is final and must stay exactly the same: same creature, same proportions, same colors, same features. Do not add, remove or reinterpret anything.
- The only problem: the current sprite looks flat and 2D, almost a side view, and the perspective is wrong. Redraw it in a real 3/4 view facing left, with volume, like an official Game Freak sprite.

THE CREATURE (keep all of this)
- Electric/Flying woodpecker, based on the cream-colored woodpecker (Celeus flavus), with Pikachu colors and markings.
- Bright yellow round body; the belly is clearly round and full (like Pikachu).
- Head: yellow, a short sturdy grey chisel beak pointing up and to the left, a round black eye, a round red cheek patch.
- Crest: two pointed crest spikes on top with BLACK tips (like Pikachu's ears), plus a ragged spiky crest running down the back of the head.
- Wings closed against the body: dark brown with round cream spots.
- Tail: a stiff reddish-brown woodpecker tail pointing down and back, used as a prop.
- Short grey legs attached to the body, grey toes.
- Pose: upright and leaning slightly back, head and beak raised.

3/4 VIEW
- Body turned about 30-45 degrees towards the viewer: we see the round chest and belly from the front-left and the closed wing on the side.
- The head is turned towards the viewer too, not a profile: the far eye may just be visible or hidden behind the beak, the near eye and cheek patch clearly visible.
- Both feet visible.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No branch, ground, rock, shadow or base. No electricity, sparkles or effects. One single creature.

AVOID
- Not Pikipek, Pikachu, Woody Woodpecker or Chatot. No plush toy, chibi or mascot look, no oversized sparkly eyes.
```

## Ronde 1 (prompt v1) → `r1_prompt_v1.png`
Jordi (19 nov): "ziet er goed uit, behalve dat de vleugelkleur veranderd is, maar dat is geen issue, ik twijfel wel of hij weer niet hetzelfde eruit gaat zien, want het oog links zal wegvallen, hoe dan andere sprites dat? Moeten we misschien voor een leukere pose gaan?"
Studie `studie_vogels_gen3.png`: profielkop met één oog is gewoon in Gen 3 (Taillow, Swellow, Spearow, Chatot, Pikipek); de diepte zit dan in het lijf. Kop naar de kijker met twee ogen: Pidgey, Starly, Torchic, Hoothoot.
Jordi (19 nov): "nee prima, laten we hem nog een beetje naar de kijker draaien, kan met een korte verbeterprompt wel toch? Praat tegen Gemini in graden"

### Verbeterprompt r2 (in hetzelfde gesprek)
```
Good, keep everything exactly as it is (design, colors, crest, wings closed, tail, legs, style). Change only the angle:

- Right now the bird is almost in side view: about 10-15 degrees from a pure profile. Rotate the whole bird about 30 degrees more towards the viewer, so the body is at about 45 degrees (a true 3/4 view, facing front-left). We see more of the round yellow chest and belly from the front.
- Turn the head a bit further than the body, to about 60 degrees, so it looks more at the viewer: both eyes and both red cheeks are visible, the far ones partly. The beak points front-left, slightly up.
- The far wing and the tail may peek out behind the body.

Same 64x64 Gen 3 sprite style, white background, nothing else changed.
```

## Ronde 2 (verbeterprompt r2) → `r2_verbeter.png`
Jordi (19 nov): "wat vind je hiervan, ik heb het gevoel dat het perspectief van het hoofd niet meer klopt" · "en hoort de snavel zo hoog?"
Claude: lijf niet gedraaid (vleugel nog volledig opzij), alleen een verre wang erbij geplakt; nabije oog op de profielplek, snavel aan de rand van de kop op ooghoogte; derde kuifpunt links erbij. Ter vergelijking het B1-model gedraaid: `hoek3d/vel.png` (B1 = 30°, 45°, 60°; render met `python3.11` + pip `bpy`, `scikit-image`, apt `libegl1`).

Jordi (19 nov): "de render lijkt me genoeg, hoort het vogeltje waarop we picapau gebaseerd hebben zo'n hoge snavel te hebben? Als we de render gebruiken moeten we wel GEmini vertellen dat het boller en minder statisch mag, omdat dit heel erg met rondjes en rechte symbolen gemaakt is als je snapt wat ik bedoel"
Snavel echte vogel (foto 3): bovenrand snavel op ooghoogte, rode vlek eronder/erachter; het model heeft hem iets lager.

## Prompt v2 (nieuw gesprek, enige bijlage: `bijlage_render45.png` of `bijlage_render60.png`)
```
Draw this Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

ATTACHMENT
- The attachment is a rough 3D blockout of the Pokémon, built from simple spheres, cones and straight shapes. Use it for the DESIGN and the VIEWING ANGLE: keep exactly this 3/4 angle and all the features (two crest spikes with black tips, the ragged crest at the back of the head, round eye, red cheek, grey chisel beak, closed spotted wings, stiff tail, short grey legs). Do not add or remove anything (no extra crest spikes).
- Do NOT copy its stiff geometric look. Draw it like a real Game Freak artist: rounder, softer and more organic, with smooth flowing shapes, a plump round body and a lively, natural posture (like a bird that is alert and proud, chest out), not a static statue. Same angle, same features, just alive.
- The colors in the render are wrong because of the lighting. Use these colors: bright Pikachu yellow body and head, dark brown wings with round cream spots, reddish-brown tail, grey beak and legs, black crest tips, red cheek.

THE CREATURE
- Electric/Flying woodpecker, based on the cream-colored woodpecker (Celeus flavus), with Pikachu colors and markings. The belly is clearly round and full, like Pikachu.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No branch, ground, rock, shadow or base. No electricity, sparkles or effects. One single creature.

AVOID
- Not Pikipek, Pikachu, Woody Woodpecker or Chatot. No plush toy, chibi or mascot look, no oversized sparkly eyes.
```

## Ronde 3 (prompt v2) → `r3_prompt_v2.png`
Jordi (19 nov): "prima, alleen nog steeds zou ik hem iets meer naar rechts willen draaien"

### Verbeterprompt r4 (in hetzelfde gesprek)
```
Good, keep everything exactly as it is (design, shapes, colors, style). Change only the angle: rotate the whole bird about 20 degrees further to the right, around its vertical axis, so it turns more towards the viewer. We see more of the yellow chest and belly from the front, the beak points more towards the viewer and to the left, the near eye and cheek move a bit towards the middle of the face, and the far side of the head and the far wing start to show on the left. Do not add anything. Same 64x64 Gen 3 sprite, white background.
```

Jordi (19 nov): "ik heb niet gezegd dat de kleur van de vleugels anders moest, maar prima. Als je de sprite gaat bouwen wil ik dat je de kleuren van pikachu daarvoor gebruikt"
→ **Sprite bouwen met de kleuren van Pikachu** (`graphics/pokemon/pikachu/normal.pal`: geel 255 246 164 / 246 230 82 / 246 189 32 / 222 148 0, bruin 156 82 0 / 98 49 8, rood 230 148 131 / 230 90 65 / 197 32 24 / 123 41 8, grijs 123 123 139 / 64 64 72 / 41 41 41, zwart, wit). Gemini-kleuren niet overnemen.

## Ronde 4 (verbeterprompt r4) → `r4_verbeter.png`
Jordi (19 nov): "nee geen issue betekent dat je dat kan aanpassen. Anyways de hoek en pose vind ik prima. In de sprite betekent dat dat er 1 of 2 pixels max aan zwart oog boven de snavel uit komt. Ik heb het gevoel dat de staart nu wel veranderd is, past dit bij de vogel waarop die geinspireerd is?"
- Hoek en pose: goed. Sprite-eis: verre oog max. 1–2 px zwart boven de snavel.
- Staart (Claude, foto 1): echte specht = stijve, puntige, donkere steunstaart schuin omlaag in het verlengde van het lijf; de roodbruine kleur zit in de lange slagpennen. r4 = korte, horizontale waaier van losse veren (zangvogelstaart); r1–r3 en het model = stijve punt omlaag, past beter.
Jordi (19 nov): "laten we 1 keer gemini proberen nog"

### Verbeterprompt r5 (in hetzelfde gesprek)
```
Good, the angle and pose are perfect now, keep them exactly. Change only the tail: it became a short, horizontal fan of separate feathers, like a songbird. Put back the tail of the earlier versions: one stiff, pointed woodpecker tail that points diagonally DOWN and back, continuing the line of the body, like the tail a woodpecker leans on against a tree trunk. Same length and color as before. Nothing else changes. Same 64x64 Gen 3 sprite, white background.
```

## Ronde 5 (verbeterprompt r5) → `r5_verbeter.png`
Jordi (19 nov): "beter?" Vergelijking: `staart_r3_r4_r5_foto.png`.

## Gekozen: r5 (19 nov) → sprite
Jordi: "ja alleen de vleugels/staart moeten pikachu kleuren krijgen, de rest mag je volledig hetzelfde palet aanhouden als picapau, dat was al een erg goed design" · "dus de vleugels moeten juist niet terug naar het origineel" · keuze: **vleugel bruin, staart roodbruin** (vleugels in Pikachu's bruin 156 82 0 / 98 49 8; staart roodbruin met Pikachu's 123 41 8 als schaduw; stippen crème van Picapau).
- Palet: alles verder = `../af/normal.pal` (Picapau). Vervangt de regel hierboven "sprite met de kleuren van Pikachu".
- Verre oog: max. 1–2 px zwart boven de snavel.

## Sprite v3 (19 nov)
- r5 oog: Jordi "A, maar alleen de rechtse pixel behouden" → r6.
- r6, Jordi: "ok paar puntjes, we zijn er bijna: de kleur van het lichaam moet hetzelfde zijn als de originele picapau, niet als het model · Het hoofd mag iets ronder aan de linkerkant. Er zit ook 1 bruine pixel die er niet hoort naast de onderkant van de snavel, net boven de wang. · De gele stekel net onder het rechteroor, mag iets diagonaler gelijnd worden naar onderen, naar de bovenkant. 1 pixel is voldoende denk ik. · Het oog is nu een beetje een ei vorm, mag volledig rond. · De afwerking van de snavel is een beetje gek, met een paar pixels naar links, kan dat uiteinde iets scherper? · De rest is allemaal goed en mag je precies zo behouden (op dalijk een kleur en schaduwronde na)" → r7.
- Jordi (19 nov): "ja dus echt niks opnieuw tekenen, hooguit wat pixels aanpassen op de punten die ik aan gaf"
- r7, Jordi: "de stek is nog niet helemaal opgelost, zie mijn puntjes op de 2 pixels" · "je hebt de onderkant beter gemaakt, maar de bovenkant zit nog te dicht op het oor" · "lijkt net alsof die vast zitten aan het oor, terwijl in het origineel ze iets meer ertussen leken te zitten" → r8b: stekel 1 rij lager met geel inhammetje tussen oor en stekel (12 px t.o.v. r7, door Claude).
- r8b, Jordi: "maak eens een versie waar je de stekels weglaat en het hoofd ronder is" · "aan beide kanten" · "kijk in dit 3d model zitten de stekels echt tussen de oren in, dus of we halen ze weg, of we maken ze slechts lichtjes zichtbaar, zodat het duidelijk is dat ze tussen de oren in zitten" → r9: A_rond (stekels weg, achterhoofd rond, 14 px), B_lichtjes (A + klein puntje achter het rechteroor, 19 px), door Claude.
- r9, Jordi: "allemaal slecht. Je snapt niet wat ik bedoel. Kijk eens goed naar het model. Het zit hem in kleurgebruik en schaduw, zodat duidelijk te zien is dat de stekels niet vast aan de zijkant van het hoofd zitten maar tussen de oren in zitten" → r10 door de maker (vorm r8b, kuif via kleur/schaduw achter de kop).
- Jordi over r9 A/B: "A en B allebei waardeloos slecht bedoel ik dus" · "stop daar maar mee" → r9 vervalt; r10 alleen kleur/schaduw op vorm r8b.
- r10, Jordi: "A is goed, goed idee, alleen de bovenste stekel moet nu weer terug naar de eerdere vorm. Kijk naar het model, hij staat eerder naar boven dan naar beneden gericht. Dan moet het hoofd aan de linkerkant nog steeds ronder, dan is de vorm klaar" → r11 (maker).
- r11, Jordi: "het hoofd links moet ronder" → r12: 3 varianten A/B/C (maker).
- Jordi: "hoe vaak moet ik dat zeggen" · "hij is nu nog platter" (r11 linkerrand werd een verticale wand x16). r12-opdracht gecorrigeerd: bolle boog boven én onder de snavel, geen rechte stukken > 2 rijen.
- Jordi: "is 1 rechte lijn" · "die moet meer uitbollen naar links" → r12 varianten: uitbollen 1/2/3 px naar links, snavel schuift mee.
- Jordi: "GAST" · "maak er gewoon een cirkel van" · "zoals het model" · "kijk naar de vorm van het model en neem die over" → r13 (Claude): linkeromtrek van de kop = kale modelreductie (r1/kaal_11.npy) rij 22–26 (22,19,18,17,17) + verre wang rij 32–33 op x15; 11 px t.o.v. r11. C/D vervallen.
- r13, Jordi: "vanaf de snavel is die nog steeds te recht, maak dat stuk ook net wat ronder" · "naar onderen vanaf de snavel" → r14 (Claude): kin onder de snavel bolt uit, omtrek rij 33–38 = 15,14,14,15,16,17 (12 px).
- r14, Jordi: "NEEEEE" → r14 vervalt; terug naar r13, Jordi tekent zelf op raster_kop.png.
- Jordi: "dat is toch geen cirkel meer" → r15 (Claude, vanaf r13): onder de snavel buigt de kop als cirkel terug naar de hals (omtrek rij 32–37 = 16,17,18,18,19,19); verre wang (rood) valt daardoor weg; 15 px.
- Jordi: "neeeee" (r15) · "jezus man hoe moeilijk kan didt zijn" → r16 (Claude, vanaf r13): linkerhelft van de kop op een echte cirkel (middelpunt oog 26,29, straal 10): bovenlinks een koepel tot aan het linkeroor, onder de snavel terug naar de hals; ±34 px.
- Jordi tekende de rand op r13/raster_kop.png (`r13/jordi_rand.png`): "als dit de nieuwe rand is ben je er vgm" → r17 = r13 + (15,31) en (15,34) donkerrood: rand x15 van rij 31 t/m 34 (2 px). r14–r16 vervallen.
- Jordi: "lieg niet" · "je hebt 2 pixels toegevoegd ipv 4" → ook (15,30) en (15,35); r17 = r13 + 4 px (15,30/31/34/35).
- Jordi: "dit kan toch niet allemaal wangkleur zijn" · "nee ook niet allemaal zwart" · "kijk naar het fucking model" → r17 rand x15 rij 30–35 zoals het model: boven bruine selout met geel ernaast, onder donkerrood met rood ernaast (verre wang), 13 px t.o.v. r13.
- Jordi: "waarom heb je nu de snavel aangepast?" → Claude had (17,30),(17,31) ongevraagd donkergrijs gemaakt; teruggezet.
- Jordi: "HUH" → ook (16,30–32) was de zwarte snavelrand en was geel geworden; terug. r17 = r13 + 7 px: (15,30),(15,31) bruine selout, (15,34),(15,35) donkerrood, (16,33–35) rood. Snavel = r13.

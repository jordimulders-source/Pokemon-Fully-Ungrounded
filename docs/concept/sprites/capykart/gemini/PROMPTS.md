# Capykart: Gemini-prompts
Basis = de r3-prompt van Capybarrel (die werkte), alleen met Jordi's woorden voor fase 2. Nieuw gesprek, zonder bijlage (GEMINI.md). Pre-evolutie niet bij naam in het gezicht/ontwerp noemen.

## r1 (24 nov)
```
Design an original Pokemon called CAPYKART. Type: Normal. Second and final stage of a two-stage line of early-route rodent Pokemon.

Concept: a capybara Pokemon whose body has become a small wooden toy wagon (a kart shape), with parts of its body sticking out of it. The capybara and the wagon are one creature, not an animal riding in a vehicle.

- The capybara's head sticks out of the front of the wooden toy wagon. The head looks a bit more grown-up than a first-stage baby Pokemon, but is still stylized and Pokemon-like.
- On the back of the wagon, three or four wooden toy blocks are stacked on top of each other.
- The wagon is made of warm brown wood with darker grain lines, like a classic wooden children's toy.

Make it look like a real Pokemon, at the same level of stylization as the rodent Pokemon of the main games, but do not copy any of them: simple, clean shapes with few details, no realistic fur texture. It must still read as a capybara: blunt square muzzle, big flat nose, small rounded ears, heavy calm build. Fur: warm reddish-brown.

Style: official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, dark outline, facing 3/4 to the left, compact composition. White background, no ground, no shadow, no effects, no motion lines.

AVOID: realistic animal look, plush toy / Neopets look, beaver look, a real car or go-kart with an engine, a driver sitting in a car, a cartoon vehicle with a face, letters or numbers on the blocks, water.
```
Eigen toevoegingen (Claude, schrappen als Jordi ze niet wil): "no motion lines", "letters or numbers on the blocks" in AVOID, "classic wooden children's toy", "a real car or go-kart with an engine".

## Ronde 1 (24 nov)
- `r1/capykart_r1.png`: capibara zit in een houten mijnkar met voorpoten op de rand, blokken los naast elkaar. Jordi: "dit is een mijnkaart, het moeten een houten speelgoedautotje zijn, mijn fout was om niet te vertellen dat de toy blocks opgestapeld moeten zijn. De capybara is de auto trouwens he. Zijn hoofd steekt er alleen uit, het autotje is zijn lichaam".

## r2 (nieuw gesprek, zonder bijlage)
```
Design an original Pokemon called CAPYKART. Type: Normal. Second and final stage of a two-stage line of early-route rodent Pokemon.

Concept: a capybara Pokemon whose body IS a small wooden toy car. Only its head sticks out of the toy car; the toy car is its body. It is one creature, not an animal sitting or riding in a vehicle.

- The body is a small wooden toy car, like a classic wooden children's toy car: smooth rounded wooden shapes, warm brown wood with darker grain lines, round wooden wheels. It is NOT a mine cart, wagon, crate, tub or open box.
- Only the capybara's head sticks out of the front of the toy car. No paws, arms or legs stick out; the wheels are its legs.
- The head looks a bit more grown-up than a first-stage baby Pokemon, but is still stylized and Pokemon-like.
- On the back of the toy car, three or four wooden toy blocks are stacked on top of each other in one tower.

Make it look like a real Pokemon, at the same level of stylization as the rodent Pokemon of the main games, but do not copy any of them: simple, clean shapes with few details, no realistic fur texture. It must still read as a capybara: blunt square muzzle, big flat nose, small rounded ears, heavy calm build. Fur: warm reddish-brown.

Style: official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, dark outline, facing 3/4 to the left, compact composition. White background, no ground, no shadow, no effects, no motion lines.

AVOID: mine cart, wagon, open box or tub the capybara sits in, paws resting on the edge, a real car or go-kart with an engine, a driver sitting in a car, a cartoon vehicle with a face, blocks placed side by side, letters or numbers on the blocks, realistic animal look, plush toy / Neopets look, beaver look, water.
```

## Ronde 2 (24 nov)
- `r2/capykart_r2.png`: houten speelgoedauto als lijf, hoofd steekt vooraan uit, blokken in twee stapels naast elkaar. Jordi: "beter, alleen de toyblocks moeten opgestapeld, misschien leuk om de vorm iets meer een derby car te maken, of een van de andere foto's, dat het net wat natuurlijker is dat het hoofd zo eruit komt". Foto's: `referenties/` (derby car, open geel autootje, houten autootjes met pinnetjespoppetjes).

## r3 (nieuw gesprek, zonder bijlage; prompt r2 als basis, alleen blokken + autovorm veranderd). A = derby car, B = open autootje

### r3A
```
Design an original Pokemon called CAPYKART. Type: Normal. Second and final stage of a two-stage line of early-route rodent Pokemon.

Concept: a capybara Pokemon whose body IS a small wooden toy car. Only its head sticks out of the toy car; the toy car is its body. It is one creature, not an animal sitting or riding in a vehicle.

- The body is a small wooden derby car (a hand-made wooden pinewood-derby style toy car): a long, low, smooth wooden body with rounded edges, warm brown wood with darker grain lines, four round wooden wheels. It is NOT a mine cart, wagon, crate, tub or open box.
- Only the capybara's head sticks up out of a round cockpit opening in the top of the car, the way the round wooden peg head sits in the cockpit of a toy derby car. No paws, arms or legs stick out; the wheels are its legs.
- The head looks a bit more grown-up than a first-stage baby Pokemon, but is still stylized and Pokemon-like.
- On the back of the toy car, three or four wooden toy blocks are stacked on top of each other in ONE single vertical tower: each block sits directly on top of the block below it. No blocks next to each other.

Make it look like a real Pokemon, at the same level of stylization as the rodent Pokemon of the main games, but do not copy any of them: simple, clean shapes with few details, no realistic fur texture. It must still read as a capybara: blunt square muzzle, big flat nose, small rounded ears, heavy calm build. Fur: warm reddish-brown.

Style: official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, dark outline, facing 3/4 to the left, compact composition. White background, no ground, no shadow, no effects, no motion lines.

AVOID: mine cart, wagon, open box or tub the capybara sits in, paws resting on the edge, a real car or go-kart with an engine, a driver sitting in a car, a cartoon vehicle with a face, blocks placed side by side, letters or numbers on the blocks, realistic animal look, plush toy / Neopets look, beaver look, water.
```

### r3B
```
Design an original Pokemon called CAPYKART. Type: Normal. Second and final stage of a two-stage line of early-route rodent Pokemon.

Concept: a capybara Pokemon whose body IS a small wooden toy car. Only its head sticks out of the toy car; the toy car is its body. It is one creature, not an animal sitting or riding in a vehicle.

- The body is a small open wooden toy car (a classic wooden children's convertible): smooth rounded wooden shapes with a low open seat, warm brown wood with darker grain lines, four round wooden wheels. It is NOT a mine cart, wagon, crate, tub or open box.
- Only the capybara's head sticks up out of the open seat of the car, the way the round wooden peg figure sits in a wooden toy car. No paws, arms or legs stick out; the wheels are its legs.
- The head looks a bit more grown-up than a first-stage baby Pokemon, but is still stylized and Pokemon-like.
- On the back of the toy car, three or four wooden toy blocks are stacked on top of each other in ONE single vertical tower: each block sits directly on top of the block below it. No blocks next to each other.

Make it look like a real Pokemon, at the same level of stylization as the rodent Pokemon of the main games, but do not copy any of them: simple, clean shapes with few details, no realistic fur texture. It must still read as a capybara: blunt square muzzle, big flat nose, small rounded ears, heavy calm build. Fur: warm reddish-brown.

Style: official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, dark outline, facing 3/4 to the left, compact composition. White background, no ground, no shadow, no effects, no motion lines.

AVOID: mine cart, wagon, open box or tub the capybara sits in, paws resting on the edge, a real car or go-kart with an engine, a driver sitting in a car, a cartoon vehicle with a face, blocks placed side by side, letters or numbers on the blocks, realistic animal look, plush toy / Neopets look, beaver look, water.
```

## Ronde 3 (24 nov)
- `r3/capykart_r3.png`: één toren van 3 blokken (blauw, rood, geel), hoofd uit een open zitplaats. Jordi: "ja het enige wat ik nog mis is een driehoekig toyblock op de bovenste"; "en de blauwe mag dezelfde vorm zijn als de andere twee"; "een groene driehoek erbovenop".

## r4 (bijsturen in hetzelfde gesprek; "keep everything, change ONLY" werkte bij Alphyena)
```
Keep everything exactly the same: the capybara head, the eye, the wooden toy car, the wheels, the pose, the colors, the outline, the three stacked blocks.

Change ONLY these two things:
1. The bottom blue block gets exactly the same cube shape and size as the red and yellow blocks above it.
2. Add one green triangular wooden toy block (a triangular prism, like a roof piece from a wooden block set) on top of the yellow top block, so the tower has four blocks.

Style: official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, dark outline, white background.
```

## Ronde 4 (24 nov)
- `r4/capykart_r4.png`: groene driehoek bovenop, blauw blok gelijk. Jordi: "prima, leest die genoeg als een pokemon en niet alleen als een capybara in een houten auto? en genoeg als een evo van capybarrel". Claude's beoordeling + voorstellen (open): zie het antwoord van 24 nov; kern: hoofd los in een zitopening, hout en vacht dezelfde tint, gezicht en hout/hoepels van Capybarrel ontbreken.
- Jordi (24 nov) op de voorstellen: "we kunnen de kleuren veranderen he"; "1 en 2 akkoord, 3 idd netjes laten overgaan, 4 is niet nodig imo". Dus: (1) gezicht (neus, tanden, blije oog) en palet van Capybarrel in de spritefase; (2) hoepels van de ton terug; (3) geen zitopening, hoofd gaat netjes over in de auto; (4) niets van het lijf achterin.
- Jordi (24 nov), nog aan het denken: "Ik denk dat hij ook nog iets volgroeider moet lijken dan capybarrel, maar ik ben nog aan het nadenken hoe dat kan zonder de capybara niet meer herkenbaar te maken, misschien maken we de capybara zelf een wat lichtere tint, meer richting beige en doen we de vorm van het hoofd net wat ronder, zodat die meer lijkt op een ventje in een toy car".

## r5 (bijsturen in hetzelfde gesprek als r4; max 2 wijzigingen: hoepels + overgang; kop/kleur in de spritefase)
Keuze Claude: hoepels als banden om de auto (dichtst bij de ton); alternatief was velgen om de wielen.
```
Keep everything exactly the same: the capybara head, the eye, the wooden toy car shape, the wheels, the pose, the colors, the outline, the tower of four blocks.

Change ONLY these two things:
1. Remove the seat opening and its rim around the neck: the capybara's neck flows smoothly and naturally into the wooden car body, as if the fur gradually becomes the wood. One creature, not an animal sitting in a car.
2. Add two dark grey iron hoop bands around the wooden car body, like the iron hoops of a wooden barrel.

Style: official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, dark outline, white background.
```

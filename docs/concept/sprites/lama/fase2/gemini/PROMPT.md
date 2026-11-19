# Gemini-prompt: Llamauler opknappen (19 nov)

Opknapronde: `../../../OPKNAPRONDE_GEMINI.md`. Regels: `docs/lessen/GEMINI.md`. Ontwerp: `../../SPEC.md`.

## Jordi (19 nov, letterlijk)
- "llamauler is idd erg plat, niet helemaal goed in verhouding, niet goed aangekleed, handschoenen kunnen beter en de kop is net niet llama genoeg"
- Op Claudes punten (plat profiel, lijf één blok, stokpoten, romp hoog, minst gestileerd van de lijn; kleed/halsband losse kleurvlakken die niet om het lijf vallen, minder aangekleed dan na de alpaca te verwachten; oren recht i.p.v. banaanvormig, oog paard/hert): "Voor de rest ben ik het eens met je"
- Handschoenen: "ja de handschoenen behouden, hij wisselt juist van vechtstijl en dat vind ik prima. Het maakt niet uit dat je maar deel van die mma handschoenen ziet, bij fighting types is het vaak wel gebruikelijk om iets van accessoires te tonen, als enige type misschien."

## Bijlagen
1. `bijlage1_oude_sprite_8x.png`: huidige sprite (alleen kleuren en kledingstukken; niet overtrekken).
2. `bijlage2_lama_pose.png`: echte lama in de pose die Jordi koos (SPEC: foto 1).
3. `bijlage3_mma_handschoenen.png`: de MMA-handschoenen (SPEC: foto 5).
Fase 1 en 3 alleen in woorden (een eerdere sprite als bijlage wordt gekopieerd).

## Prompt v1 (nieuw gesprek; bijlagen 1–3)
```
Draw a Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), facing left in 3/4 view.

ATTACHMENTS
- Attachment 1 is the old, failed sprite of this Pokémon. Use it ONLY for the colors and for which clothing pieces it wears. Do NOT trace its pose, body shape, head or proportions: those are what must improve.
- Attachment 2 is a real llama. Use it for the anatomy, the llama head and the pose: standing on four legs, body turned 3/4 towards front-left, head turned towards the viewer, tail up.
- Attachment 3 shows the gloves: red MMA gloves (short, open fingers, black wrist strap). Ignore the logos and text.

THE CREATURE
- A Fighting-type llama Pokémon, the middle stage of a starter line (like Charmeleon, Monferno or Marshtomp): clearly an evolution of a small fluffy alpaca, but not yet fully grown. Its final evolution is a big adult llama dressed as a cholita wrestler with a bowler hat, so this stage wears less than that.
- It stands on all four legs. It is an animal, not a humanoid.
- Caramel llama fur (colors as in attachment 1).

WHAT MUST CHANGE
- Not flat: a real 3/4 view with volume. We see the chest from the front-left and the side of the body; the body is a rounded, woolly shape, not a rectangular block.
- Proportions: stylized like an official Pokémon, not a realistic tall thin llama. The legs are not thin sticks and the body does not hang high above long legs. Compact, filling a square frame. The head is about one third of the total height.
- Head: clearly a LLAMA head, as in attachment 2: long face with a clear muzzle and split lip, and long BANANA-SHAPED ears that curve inwards at the tips. Not straight upright ears, not a horse or deer head. Dark, almost black eyes; no heavy sleepy eyelid.
- Clothing: the same pieces as in attachment 1 (red wool tassels in the ears, a woven multicolored Andean aguayo band around the neck, a woven aguayo cloth on the back), but drawn as real woven fabric that wraps around and follows the body, with folds and thickness. Not flat stickers of color. It is a bit more dressed than its small alpaca pre-evolution, and clearly less than its final evolution.
- Gloves: red MMA gloves with a black wrist strap on the FRONT feet, as in attachment 3. It is fine if only part of the glove is visible.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No ground, rock, shadow or base. No effects. One single creature.

AVOID
- Not a horse, deer, sheep or camel. Not standing on two legs. No plush toy, chibi or mascot look, no oversized sparkly eyes. No bodybuilder muscles.
```

## Ronde 1 (prompt v1) → `r1/r1_prompt_v1.png`
Jordi (19 nov): "dit is niet bepaald een vooruitgang. Hij is wel heel erg buff, minder llama dan voorheen, de kleding is niet mooi en hij heeft nu echt vingers in de handschoenen, dat is ook niet de bedoeling" · "en totaal niet fluffy"
Fout van Claude: prompt v1 was geschreven zonder de hele SPEC te lezen en ging tegen eerdere besluiten van Jordi in: lijf fluffy à la Mareep/Flaaffy en jonger, fase 3 = de buffe (2 nov); zwaar droog ooglid (Numel/Slakoth, "dat ooglid is ook een mooie toevoeging", 3 nov; v1 verbood het); pose F (lijf bijna zijaanzicht, kop driekwart, foto 8; v1 vroeg lijf 3/4 naar foto 1); kaarsrechte hals; halsband met pompons. "Open fingers" + "not thin sticks/compact" gaven vingers en spierbundels.

## Jordi (19 nov, na r1, letterlijk)
"het ging me puur om hoe gemini het tekende. De pose is prima, ik vond niet dat het volume en de schaduw ontbraken, daar heb ik niks over gezegd" → pose F en de kledingstukken van het bevroren ontwerp blijven; geen instructie over volume/schaduw.

## Prompt v2 (nieuw gesprek; bijlagen: `bijlage1_oude_sprite_8x.png`, `bijlage2_v2_lama_foto8.png`, `bijlage3_mma_handschoenen.png`)
Bevroren besluiten uit `../../SPEC.md` erin: fluffy/jonger à la Mareep/Flaaffy (2 nov), kaarsrechte hals, droog zwaar ooglid Numel/Slakoth (3 nov), pose F (foto 8), halsband 3 strepen + 5 pompons, aguayo-lap op de rug, MMA met de twee teennagels.
```
Draw a Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), facing left.

ATTACHMENTS
- Attachment 1 is the old sprite of this Pokémon. KEEP its pose (body almost in side view facing left, head turned 3/4 towards the viewer, all four legs on the ground in a walking step, tail up), its colors and its clothing pieces. Redraw everything else better; do not trace its drawing.
- Attachment 2 is a real llama in the same pose. Use it for the llama anatomy and the llama head. Ignore its brown and white colors.
- Attachment 3 shows the gloves: red MMA gloves with a black wrist strap. Ignore the logos and text.

THE CREATURE
- A young Fighting-type llama Pokémon, the middle stage of a starter line (like Charmeleon or Monferno): the evolution of a small fluffy alpaca, not yet fully grown. Its final evolution is the big muscular one; this one is young and FLUFFY, not muscular.
- It stands on all four legs. It is an animal, not a humanoid.
- Fur: caramel, very fluffy and woolly, like Mareep and Flaaffy: the body and the neck are soft rounded masses of wool, with a few big smooth wool bumps in the outline. Not smooth short fur, not muscles.
- Neck: long and dead straight, upright, also woolly.
- Head: clearly a LLAMA head as in attachment 2: long face, rounded muzzle with a split lip, small nostrils, long BANANA-SHAPED ears that curve inwards at the tips.
- Eye: one dark brown eye high on the side of the head with a heavy, flat, half-closed upper eyelid pressing on it: a dry, unimpressed, "watching the world go by" look, like Numel or Slakoth. No smile, no big round cute eyes, no sparkles.

CLOTHING (draw these well, as real woven Andean fabric)
- Red wool tassels in both ears.
- A narrow woven aguayo band around the base of the neck (three colored stripes) with five small wool pompoms hanging from it.
- A woven aguayo cloth lying on the back, with a fold and a hem, hanging down a bit on the side.
- Red MMA gloves with a black wrist strap on the FRONT feet only. The glove covers the hoof like a mitten; only the two small toenails of the llama hoof peek out at the front. NO fingers, no hand, no toes like a hand. The back feet are normal hooves.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No ground, rock, shadow or base. No effects. One single creature.

AVOID
- Not a horse, deer, sheep, camel or alpaca. Not muscular, no bodybuilder look. Not standing on two legs. No plush toy, chibi or mascot look.
```

Jordi (19 nov, letterlijk): "gemini heeft echt een prima referentie kader dus die andere fotos zijn niet nodig, noteer dat ook vanaf nu in de documenten, ik ga deze prompt gebruiken" → vastgelegd in `docs/lessen/GEMINI.md` (bovenaan).

## Ronde 2 (prompt v2) → `r2/r2_prompt_v2.png`
Jordi (19 nov): "de handschoenen zijn prima, ga je in een sprite toch amper zien. Halsband is even de vraag of het anders naar een sprite te vertalen is. Verhouding, oren en mondlijn akkoord" + "A, maak maar een nieuwe prompt" (A = akkoord met Claudes kritiek: lijf grote wolk op dunne gladde stokpoten met vrij kleine kop (schaapkant), oren recht i.p.v. banaan, glimlachje). Halsband: kleuren zijn die van de goedgekeurde sprite; vertalen in de spritefase.

## Prompt v3 (nieuw gesprek; alleen `bijlage1_oude_sprite_8x.png`, geen andere foto's)
```
Draw a Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), facing left.

ATTACHMENT
- The attachment is the old sprite of this Pokémon. KEEP its pose (body almost in side view facing left, head turned 3/4 towards the viewer, all four legs on the ground in a walking step, tail up), its colors and its clothing pieces. Redraw everything else better; do not trace its drawing.

THE CREATURE
- A young Fighting-type llama Pokémon, the middle stage of a starter line (like Charmeleon or Monferno): the evolution of a small fluffy alpaca, not yet fully grown. Its final evolution is the big muscular one; this one is young and FLUFFY, not muscular.
- It stands on all four legs. It is an animal, not a humanoid. It must read as a LLAMA, not a sheep.
- Fur: caramel, fluffy and woolly, like Mareep and Flaaffy: the body and the neck are soft rounded masses of wool, with a few big smooth wool bumps in the outline. Not smooth short fur, not muscles.
- Proportions: the body is NOT a huge wool cloud sitting on thin bare stick legs. The wool follows the llama body shape, and the wool continues a little down onto the upper legs. The head is bigger than you would expect: about one third of the total height.
- Neck: long and dead straight, upright, also woolly.
- Head: a real llama head: long face, rounded muzzle with a split lip, small nostrils.
- Ears: long BANANA-SHAPED ears: they curve outwards from the head and then the tips curve inwards towards each other, like a pair of bananas. Not straight upright ears.
- Mouth: closed and neutral, a straight line. No smile, no smirk.
- Eye: one dark brown eye high on the side of the head with a heavy, flat, half-closed upper eyelid pressing on it: a dry, unimpressed, "watching the world go by" look, like Numel or Slakoth. No big round cute eyes, no sparkles.

CLOTHING (draw these well, as real woven Andean fabric)
- Red wool tassels in both ears.
- A narrow woven aguayo band around the base of the neck (three colored stripes) with five small wool pompoms hanging from it.
- A woven aguayo cloth lying on the back, with a fold and a hem, hanging down a bit on the side.
- Red MMA gloves with a black wrist strap on the FRONT feet only. The glove covers the hoof like a mitten; only the two small toenails of the llama hoof peek out at the front. NO fingers, no hand. The back feet are normal hooves.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No ground, rock, shadow or base. No effects. One single creature.

AVOID
- Not a horse, deer, sheep, camel or alpaca. Not muscular, no bodybuilder look. Not standing on two legs. No plush toy, chibi or mascot look.
```

## Ronde 3 (prompt v3) → `r3/r3_prompt_v3.png`, vergelijking `r2_vs_r3.png`
Jordi (19 nov): "de nek is wel heel recht nu" · "als in, 2 lijnen" · "probeer nog maar 1 prompt met dingen waar je nog niet teevreden mee bent"
Claude (r3 t.o.v. r2): kop, pompons, lijf/poten beter in r3; hals (buis van 2 rechte lijnen, kaal), kleed (kaal, patroon weg) beter in r2; oren in beide recht; mond hangt nu iets omlaag. Fout Claude: "dead straight" voor Jordi's "relatief kaarsrecht" (3 nov).

## Prompt v4 (nieuw gesprek; alleen `bijlage1_oude_sprite_8x.png`)
```
Draw a Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), facing left.

ATTACHMENT
- The attachment is the old sprite of this Pokémon. KEEP its pose (body almost in side view facing left, head turned 3/4 towards the viewer, all four legs on the ground in a walking step, tail up), its colors and its clothing pieces. Redraw everything else better; do not trace its drawing.

THE CREATURE
- A young Fighting-type llama Pokémon, the middle stage of a starter line (like Charmeleon or Monferno): the evolution of a small fluffy alpaca, not yet fully grown. Its final evolution is the big muscular one; this one is young and FLUFFY, not muscular.
- It stands on all four legs. It is an animal, not a humanoid. It must read as a LLAMA, not a sheep.
- Fur: caramel, fluffy and woolly, like Mareep and Flaaffy: the body and the neck are soft rounded masses of wool, with a few big smooth wool bumps in the outline. Not smooth short fur, not muscles.
- Proportions: the body is NOT a huge wool cloud sitting on thin bare stick legs. The wool follows the llama body shape, and the wool continues a little down onto the upper legs. The head is bigger than you would expect: about one third of the total height.
- Neck: long and upright, but WOOLLY: its front and back outline have soft wool bumps, like the body. It must NOT be a smooth tube drawn with two straight parallel lines.
- Head: a real llama head: long face, rounded muzzle with a split lip, small nostrils.
- Ears: long BANANA-SHAPED ears, clearly curved, not straight. Each ear bends like a banana: the base leans outwards and the tip curves back inwards, so the two ear tips point towards each other. Straight upright ears are wrong.
- Mouth: closed and relaxed, a short almost flat line. Not smiling and not frowning, the corners do not go up or down.
- Eye: one dark brown eye high on the side of the head with a heavy, flat, half-closed upper eyelid pressing on it: a dry, unimpressed, "watching the world go by" look, like Numel or Slakoth. No big round cute eyes, no sparkles.

CLOTHING (draw these well, as real woven Andean fabric)
- Red wool tassels in both ears.
- A narrow woven aguayo band around the base of the neck (three colored stripes) with five small colored wool pompoms hanging from it.
- A woven aguayo cloth lying on the back: RED with a clearly visible colorful woven pattern of stripes and small geometric motifs, with a fold, a hem and small tassels on the lower edge, hanging down a bit on the side. Not a plain single-colored cloth.
- Red MMA gloves with a black wrist strap on the FRONT feet only. The glove covers the hoof like a mitten; only the two small toenails of the llama hoof peek out at the front. NO fingers, no hand. The back feet are normal hooves.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No ground, rock, shadow or base. No effects. One single creature.

AVOID
- Not a horse, deer, sheep, camel or alpaca. Not muscular, no bodybuilder look. Not standing on two legs. No plush toy, chibi or mascot look.
```

## Ronde 4 (prompt v4) → `r4/r4_prompt_v4.png`
Jordi (19 nov): "op de achterste handschoen na vind ik dit het beste ontwerp" (verre voorhandschoen: open voorkant waar de hoef als een duim uitsteekt).

### Verbeterprompt r5 (in hetzelfde gesprek als r4)
Jordi (19 nov): "die handschoen is omgekeerd"
```
This is very good. Keep EVERYTHING exactly as it is: pose, head, ears, eye, wool, neck, clothing, colors, style.
Change only ONE thing: the far front glove (the one further back, behind the near front leg). It is drawn the wrong way around, reversed. Turn it around so it faces forward to the left, exactly like the near front glove: same shape and direction, red, black wrist strap, only two small toenails peeking out at the bottom front. Nothing else changes.
```

## Ronde 5 (verbeterprompt r5) → `r5/r5_verbeter.png`
Jordi (19 nov): "hetzelfde issue" (handschoen nog omgekeerd). Claude begon het gat zelf op te vullen; Jordi: "niet doen" · "copy paste egwoon van een van de andere ontwerpen" · "en dan doen we nog 1 gemini ronde".
Plakwerk: `handschoen/r4_met_handschoen_r3.png` = r4 met de achterste handschoen van r3 (dx −7, dy +10, onder de wolrand van r4).

## Prompt r6 (nieuw gesprek; bijlage `handschoen/r4_met_handschoen_r3.png`)
```
This is a finished Pokémon design, drawn as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art). Keep EVERYTHING exactly as it is: pose, head, ears, eye, mouth, wool, neck, collar, pompoms, back cloth, near front glove, back legs, colors, style.

Only one spot needs cleaning: the far front glove (the red glove on the right, behind the near front leg) was pasted in from another drawing, so it is blockier and its edges don't match. Redraw ONLY that glove in the same clean style as the near front glove: a closed red MMA glove with a black wrist strap, pointing forward to the left, the same direction as the near glove, slightly darker because it is further away, with two small toenails peeking out at the bottom front. No open palm, no thumb, no fingers. Nothing else changes.
```

## Ronde 6 → `r6/r6_plak_opgeschoond.png`
Jordi (19 nov): "hij verandert niks" (bekende les: Gemini wijzigt een eigen bijlage amper).

## Plakwerk 2 (Jordi: "komt ook door jouw matige knip en plak werk" · "doe de hele poten" · "r3 is de enige met goede handschoenen" · "beide voorpoten" · "en dan kunnen we een gemini ronde doen" · "dit lukte net bij palpaca ook")
`handschoen/r4_voorpoten_r3.png`: r4, beide voorpoten vanaf de bovenkant van de polsband vervangen door die van r3 (per poot verticaal uitgelijnd op de polsband). Werkwijze zoals Palpaca r10 → r11 (ruw plakken, Gemini maakt de naad glad).

## Prompt r7 (nieuw gesprek; bijlage `handschoen/r4_voorpoten_r3.png`)
```
This is a finished Pokémon design, drawn as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art). The two front feet with their red gloves were roughly pasted in from another drawing, so they are blockier than the rest and the seams don't match.

Redraw the picture as one clean, consistent sprite: smooth the seams where the woolly front legs meet the gloves, and draw both gloves in the same clean style, outline and shading as the rest of the body.
KEEP the gloves exactly as they are in shape, size, position and direction: both are closed red MMA gloves with a black wrist strap, pointing forward to the left, with small toenails at the bottom front; the far glove is slightly darker. Do not turn, open or move them.
Keep EVERYTHING else exactly as it is: pose, head, ears, eye, mouth, wool, neck, collar, pompoms, back cloth, back legs, colors.
```

## Ronde 7 (prompt r7, naad) → `r7/r7_naad.png`, vergelijking `r7/plak_vs_r7.png`
Jordi (19 nov): "vgm is dit hetzelfde? Staan de poten zoals ze horen te staan bij een lama?"
Claude: bijna identiek aan het plakwerk (alleen polsband voor rood, hoekje glad). Gang: nabije voor vóór + nabije achter achter, verre voor achter + verre achter vóór = diagonaal (draf), geen telgang (lama/alpaca, SPEC 24 okt). Opties aan Jordi: zo laten en in de spritefase repareren / nog één Gemini-poging met poten in woorden / foto als bij Palpaca.

## Prompt v5: telgang met foto (nieuw gesprek; enige bijlage: foto van een lopende lama in telgang, door Jordi)
Jordi (19 nov): "bij palpaca lukte het ook, dus we gaan het proberen, prompt aub" (uitzondering op de regel zonder extra foto's, door Jordi zelf gekozen; zoals Palpaca prompt v7 → r10). Tekst = v4 + gang en handschoenrichting; de beste delen worden daarna in r4 geplakt (zoals Palpaca r10 → r11).
```
Draw a Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), facing left.

ATTACHMENT
- The attachment is a photo of a real llama walking. Use it ONLY for the walking gait: llamas PACE, the two legs on the same side move together. Ignore its colors, wool and background.

POSE AND LEGS
- Body almost in side view facing left, head turned 3/4 towards the viewer, tail up, all four feet on the ground, walking.
- PACING GAIT: the near front leg and the near hind leg (the two legs on the side facing us, drawn lighter) both step FORWARD together. The far front leg and the far hind leg (the two legs on the other side, drawn darker, partly behind the body) are both BACK together.
- Not a trot: the near front leg and the far hind leg must NOT be forward together.

THE CREATURE
- A young Fighting-type llama Pokémon, the middle stage of a starter line (like Charmeleon or Monferno): the evolution of a small fluffy alpaca, not yet fully grown. Its final evolution is the big muscular one; this one is young and FLUFFY, not muscular.
- It stands on all four legs. It is an animal, not a humanoid. It must read as a LLAMA, not a sheep.
- Fur: caramel, fluffy and woolly, like Mareep and Flaaffy: the body and the neck are soft rounded masses of wool, with a few big smooth wool bumps in the outline. Not smooth short fur, not muscles.
- Proportions: the body is NOT a huge wool cloud sitting on thin bare stick legs. The wool follows the llama body shape, and the wool continues a little down onto the upper legs. The head is bigger than you would expect: about one third of the total height.
- Neck: long and upright, but WOOLLY: its front and back outline have soft wool bumps, like the body. It must NOT be a smooth tube drawn with two straight parallel lines.
- Head: a real llama head: long face, rounded muzzle with a split lip, small nostrils.
- Ears: long BANANA-SHAPED ears, clearly curved, not straight. Each ear bends like a banana: the base leans outwards and the tip curves back inwards, so the two ear tips point towards each other.
- Mouth: closed and relaxed, a short almost flat line. Not smiling and not frowning.
- Eye: one dark brown eye high on the side of the head with a heavy, flat, half-closed upper eyelid pressing on it: a dry, unimpressed, "watching the world go by" look, like Numel or Slakoth. No big round cute eyes, no sparkles.

CLOTHING (draw these well, as real woven Andean fabric)
- Red wool tassels in both ears.
- A narrow woven aguayo band around the base of the neck (three colored stripes: red, yellow, green) with five small colored wool pompoms hanging from it.
- A woven aguayo cloth lying on the back: RED with a clearly visible colorful woven pattern of stripes and small geometric motifs, with a fold, a hem and small tassels on the lower edge, hanging down a bit on the side.
- Red MMA gloves with a black wrist strap on BOTH front feet. BOTH gloves are closed and point forward to the LEFT, in the walking direction; the far glove is slightly darker. The glove covers the hoof like a mitten; only two small toenails peek out at the front. NO fingers, no thumb, no open palm. The back feet are normal hooves.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No ground, rock, shadow or base. No effects. One single creature.

AVOID
- Not a horse, deer, sheep, camel or alpaca. Not muscular, no bodybuilder look. Not standing on two legs. No plush toy, chibi or mascot look.
```

## Ronde 8 → `r8/r8.png`
Bijna gelijk aan r7 (kleed, halsband identiek); oren nu gekruld, achterste handschoen weer open, gang ongewijzigd. Jordi: "hoe deden we dit net bij alpaca?" → uitleg: Palpaca r10 kwam uit een NIEUW gesprek met alleen de foto (geen eerdere ronde), ontwerp volledig in woorden.


## Ronde 9 (prompt v5, nieuw gesprek, alleen foto) → `r9/r9_foto.png`
Jordi (19 nov): "leg meer nadruk op de positie van de achterpoten". Claude: in r9 staat de donkere verre achterpoot nog vóór onder de buik en de lichte nabije achteraan (= diagonaal).

## Prompt v6 (nieuw gesprek; alleen de lamafoto) = v5 met nieuw blok POSE AND LEGS
```
Draw a Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), facing left.

ATTACHMENT
- The attachment is a photo of a real llama walking. Use it ONLY for the walking gait: llamas PACE, the two legs on the same side move together. Ignore its colors, wool and background.

POSE AND LEGS (most important part of this picture)
- Body almost in side view facing left, head turned 3/4 towards the viewer, tail up, all four feet on the ground, walking.
- Llamas walk with a PACING GAIT: the two legs on the SAME side move together. Read the legs from left to right in the picture, it must be exactly this order:
  1. leftmost: the NEAR front leg (light, with a red glove), stepping forward.
  2. second: the FAR front leg (darker, with a darker red glove), placed a bit back, partly hidden behind the near front leg.
  3. third: the NEAR hind leg (light caramel, a bare hoof), stepping FORWARD under the belly.
  4. rightmost: the FAR hind leg (darker, a bare hoof), placed BACK under the tail, at the very rear of the body.
- The darker far hind leg must be the rearmost leg in the picture. It must NOT stand forward under the belly. The light near hind leg must NOT be at the back.
- Not a trot: the near front leg and the far hind leg must NOT be forward together.

THE CREATURE
- A young Fighting-type llama Pokémon, the middle stage of a starter line (like Charmeleon or Monferno): the evolution of a small fluffy alpaca, not yet fully grown. Its final evolution is the big muscular one; this one is young and FLUFFY, not muscular.
- It stands on all four legs. It is an animal, not a humanoid. It must read as a LLAMA, not a sheep.
- Fur: caramel, fluffy and woolly, like Mareep and Flaaffy: the body and the neck are soft rounded masses of wool, with a few big smooth wool bumps in the outline. Not smooth short fur, not muscles.
- Proportions: the body is NOT a huge wool cloud sitting on thin bare stick legs. The wool follows the llama body shape, and the wool continues a little down onto the upper legs. The head is bigger than you would expect: about one third of the total height.
- Neck: long and upright, but WOOLLY: its front and back outline have soft wool bumps, like the body. It must NOT be a smooth tube drawn with two straight parallel lines.
- Head: a real llama head: long face, rounded muzzle with a split lip, small nostrils.
- Ears: long BANANA-SHAPED ears, clearly curved, not straight. Each ear bends like a banana: the base leans outwards and the tip curves back inwards, so the two ear tips point towards each other.
- Mouth: closed and relaxed, a short almost flat line. Not smiling and not frowning.
- Eye: one dark brown eye high on the side of the head with a heavy, flat, half-closed upper eyelid pressing on it: a dry, unimpressed, "watching the world go by" look, like Numel or Slakoth. No big round cute eyes, no sparkles.

CLOTHING (draw these well, as real woven Andean fabric)
- Red wool tassels in both ears.
- A narrow woven aguayo band around the base of the neck (three colored stripes: red, yellow, green) with five small colored wool pompoms hanging from it.
- A woven aguayo cloth lying on the back: RED with a clearly visible colorful woven pattern of stripes and small geometric motifs, with a fold, a hem and small tassels on the lower edge, hanging down a bit on the side.
- Red MMA gloves with a black wrist strap on BOTH front feet. BOTH gloves are closed and point forward to the LEFT, in the walking direction; the far glove is slightly darker. The glove covers the hoof like a mitten; only two small toenails peek out at the front. NO fingers, no thumb, no open palm. The back feet are normal hooves.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No ground, rock, shadow or base. No effects. One single creature.

AVOID
- Not a horse, deer, sheep, camel or alpaca. Not muscular, no bodybuilder look. Not standing on two legs. No plush toy, chibi or mascot look.
```

## Ronde 10 (prompt v6) → `r10/r10_v6.png`
Jordi (19 nov): "lukt weer niet, ander idee, deze lama heeft de juiste pose toch, maar dan gespiegeld? We vragen gewoon aan gemini om daar een pokemon sprite van te maken, in exact dezelfde pose. Moet jij alleen even de foto spiegelen. Dan knippen/plakken en nog een laatste ronde"
Foto: `foto/lama_loop_origineel.png` (Jordi), gespiegeld `foto/lama_loop_gespiegeld.png`; bijlage = `foto/lama_loop_gespiegeld_uitsnede.png` (zonder watermerkregel onderaan).

## Prompt v7 (nieuw gesprek; enige bijlage `foto/lama_loop_gespiegeld_uitsnede.png`)
```
Turn the llama in this photo into a Pokémon, drawn as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

POSE: copy the pose of the photo EXACTLY: facing left, walking, every leg in exactly the same position and angle as in the photo (which leg is forward, which is back, which is near and which is far). Do not change, straighten or re-arrange the legs. Ignore the background, water, reflection and the colors of the photo.

THE CREATURE
- A young Fighting-type llama Pokémon, the middle stage of a starter line: young and FLUFFY, not muscular. An animal on four legs, a LLAMA, not a sheep.
- Fur: caramel, fluffy and woolly like Mareep and Flaaffy: soft rounded wool masses on the body and the neck, a few big smooth wool bumps in the outline; the wool continues a little down onto the upper legs.
- Head about one third of the total height; long upright woolly neck.
- Llama head: long face, rounded muzzle with a split lip, long banana-shaped ears, one dark brown eye with a heavy, flat, half-closed upper eyelid (a dry, unimpressed look). Mouth closed, a flat line.

CLOTHING
- Red wool tassels in both ears.
- A narrow woven aguayo band around the base of the neck (red, yellow, green stripes) with five small colored wool pompoms.
- A red woven aguayo cloth with a colorful pattern lying on the back, with small tassels on the lower edge.
- Red MMA gloves with a black wrist strap on BOTH front feet: closed, pointing forward to the left, the far one slightly darker, only two small toenails peeking out. No fingers, no thumb. The back feet are normal hooves.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No ground, water, reflection, shadow or base. No effects. One single creature.

AVOID
- Not a horse, deer, sheep, camel or alpaca. Not muscular. No plush toy, chibi or mascot look.
```

## Ronde 11 (prompt v7) → `r11/r11_v7.png`
Jordi (19 nov): "je prompt is niet goed, hij moet de llama nabouwen, niet ons design"

## Prompt v8 (nieuw gesprek; enige bijlage `foto/lama_loop_gespiegeld_uitsnede.png`)
```
Redraw the llama in this photo as pixel art in the style of an official Gen 3 Pokémon front sprite (Ruby/Sapphire/Emerald).

Copy THIS llama exactly: the same animal, the same pose, the same colors and the same wool. Most important: every leg in exactly the same position and angle as in the photo (which leg is forward, which is back, which is near and which is far). Do not change, straighten or re-arrange the legs. Do not add anything.

64x64 pixels, max 16 colors, 1 px dark outline, clean Gen 3 shading. Plain white background: no water, reflection, mountains, shadow or ground. One single llama.
```

## Ronde 12 (prompt v8, alleen de foto) → `r12/r12_lama_foto.png`
Jordi (19 nov): "dan gaat die focussen op de poten" · "eindelijk"
Plakwerk v1 (`poten/plak.py`), Jordi: "je moet het even wat beter plakken hoor" · "dat het tenminste aansluit" → v2 `poten/r4_poten_r12.png` (`poten/plak2.py`: per poot uitgeknipt zonder buikhaar, per poot aangesloten onder de wol, nabij licht/ver donker, nabije achterpoot ×1,38 gerekt, gaatjes gedicht). Eerder: r4 met de vier poten van r12 (×0,93, verschoven (12, 250), omgekleurd naar karamel op luminantie); r4-handschoenen en achterpoten weggehaald (voor vanaf y 865, achter vanaf y 812).

## Prompt r13 (nieuw gesprek; bijlage `poten/r4_poten_r12.png`)
```
This is a Pokémon design, drawn as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art). The four legs were roughly pasted in from another drawing, so the seams don't match and the legs look rough.

KEEP the position, angle and order of all four legs EXACTLY as they are in this picture. Do not move, straighten or re-arrange any leg. This walking pose is correct.

Clean it up into one consistent sprite:
- Connect the legs smoothly to the woolly body, in the same caramel colors, outline and shading as the rest of the body. Remove the loose hairs between the legs.
- The two legs on the far side are slightly darker than the two near legs.
- Put red MMA gloves with a black wrist strap on BOTH front feet (the two left-most legs): closed, pointing forward to the left in the walking direction, only two small toenails peeking out. No fingers, no thumb, no open palm. The back feet are normal hooves.

Keep EVERYTHING else exactly as it is: head, ears, eye, mouth, wool, neck, collar, pompoms, back cloth, tail, colors, style. Plain white background.
```

## Model met handschoenen (19 nov)
Jordi: "pardon waarom gebruik je niet het model met handschoenen?" · "ik vroeg nog of je die er eerst op kon plakken" · "ja van r3" · "maar die zie ik helemaal niet terug". Fout Claude: stap "eerst de handschoenen op het model plakken" overgeslagen (maker plakte ze op spriteformaat); maker r1/r2 gestopt.
`poten/model_handschoenen_r3.png` (`poten/handschoen_r3.py`): plakwerk v2 + beide handschoenen van r3 (1:1, polsband tegen de wol). Naar Jordi; daarna = bron voor de sprite.

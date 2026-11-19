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

# Gemini-prompts: Octillery-evolutie (10 nov)

Regels: `docs/lessen/GEMINI.md`. Lijn: `docs/concept/POKEMON.md` (Octillery-evolutie).

## Besloten (Jordi, 10 nov)
- Geen oorlogsschip: "het gaat er bij remoraid en octillery om dat ze dingen afschieten"; "ik ben bang dat bij een warship de kanonnen niet pronounced genoeg zijn".
- **Water/Steel**, "maar het moet wel pokemon blijven, dus niet te overdesigned en het moet overduidelijk een evolutie van octillery zijn".
- "hij moet wel sterker worden, dus ook een sterkere look, meer kraken". **Duidelijk groter en zwaarder.**
- **Metaal organisch.** "meer dan 3 kanonnen wordt teveel, of 1 gatling gun en 2 kanonnen".
- Pose driekwart (sprites). De beta-tank (Spaceworld #210) laten we los.
- Twee prompts naast elkaar: **A** = richting 1+2 (gatlingsnuit + twee tentakelkanonnen), **B** = richting 3 (kanonnen op de mantel).
- Keuze Claude in B (Jordi kan bijsturen): de buissnuit van Octillery blijft en telt als kanon, plus 2 op de mantel = 3.

## Bijlagen (beide prompts, in deze volgorde)
1. `bijlage_octillery_8x.png` (Octillery, Gen 3-sprite)
2. `bijlage_remoraid_8x.png` (Remoraid, Gen 3-sprite)

Elke prompt in een **eigen nieuw gesprek**.

## Prompt A: gatlingsnuit + twee tentakelkanonnen

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

ATTACHMENTS
- Attachment 1 is Octillery (Gen 3 sprite). The new Pokémon is its EVOLUTION and must be instantly recognisable as an evolved Octillery.
- Attachment 2 is Remoraid, the first stage. The line is about shooting things: Remoraid is a pistol, Octillery a cannon, this stage is heavy artillery.

THE CREATURE
- Third stage of the line, Water/Steel. A kraken: clearly BIGGER, HEAVIER and STRONGER than Octillery. Broader, taller mantle, thick powerful tentacles that spread out wide and heavy over the ground.
- Keep from Octillery: the round red head/mantle, the heavy-lidded grumpy eyes, the round yellow warts on the head and on the tentacle tips, the red-orange body colour.
- The Steel is ORGANIC: parts of the mantle are covered by smooth gunmetal-grey armour that has grown out of the body like a shell or a thick hide. No bolts, screws, rivets, seams, wires or machine parts. It looks grown, not built.

THE WEAPONS (exactly three, nothing more)
- 1: Octillery's tube snout has grown into a rotary gatling: a short cluster of several barrels grown together around the mouth, made of the same organic gunmetal. It points forward-left. This is the most important feature.
- 2 and 3: the two front tentacles end in one thick cannon barrel each, grown from the tentacle like a shell, with the opening at the tip. They are raised and aimed forward.
- All other tentacles are normal octopus tentacles with the yellow warts at the tips.
- The weapons must be big and clearly readable in the silhouette, but the creature must still look like an animal, not a machine.

POSE AND VIEW
- Body in 3/4 view facing left, sitting heavily on its spread tentacles, gatling and both tentacle cannons aimed forward-left.
- Both eyes visible. Calm and menacing; heavy and unshakable, not angry and not screaming.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO water, splash, ground, rock, shadow or base.
- No muzzle flash, smoke, bullets, ink, glow, sparkles, motion lines, text or effects. One single creature, no extra views.

AVOID
- Not Blastoise, Clawitzer, Tentacruel, Grapploct, Cloyster or a recoloured Octillery.
- Not a robot, mech, tank, ship or submarine: no hull, deck, treads, turrets, chimneys or flags.
- Not over-designed: no spikes, chains, armour everywhere or tiny details. No plush toy, chibi, Neopets or mascot look.
```

## Prompt B: kanonnen op de mantel

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

ATTACHMENTS
- Attachment 1 is Octillery (Gen 3 sprite). The new Pokémon is its EVOLUTION and must be instantly recognisable as an evolved Octillery.
- Attachment 2 is Remoraid, the first stage. The line is about shooting things: Remoraid is a pistol, Octillery a cannon, this stage is heavy artillery.

THE CREATURE
- Third stage of the line, Water/Steel. A kraken: clearly BIGGER, HEAVIER and STRONGER than Octillery. Broader, taller mantle, thick powerful tentacles that spread out wide and heavy over the ground.
- Keep from Octillery: the round red head/mantle, the heavy-lidded grumpy eyes, the round yellow warts on the head and on the tentacle tips, the red-orange body colour.
- The Steel is ORGANIC: parts of the mantle are covered by smooth gunmetal-grey armour that has grown out of the body like a shell or a thick hide. No bolts, screws, rivets, seams, wires or machine parts. It looks grown, not built.

THE WEAPONS (exactly three, nothing more)
- 1: Octillery's tube snout stays, bigger and thicker, with a gunmetal rim grown around the opening, pointing forward-left.
- 2 and 3: two thick cannon barrels grow out of the top of the mantle, one on each side, like horns made of the same organic gunmetal, both aimed forward. They grow from the body, they are not mounted turrets.
- All tentacles are normal octopus tentacles with the yellow warts at the tips; no weapons on the tentacles.
- The weapons must be big and clearly readable in the silhouette, but the creature must still look like an animal, not a machine.

POSE AND VIEW
- Body in 3/4 view facing left, sitting heavily on its spread tentacles, snout and both mantle cannons aimed forward-left.
- Both eyes visible. Calm and menacing; heavy and unshakable, not angry and not screaming.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO water, splash, ground, rock, shadow or base.
- No muzzle flash, smoke, bullets, ink, glow, sparkles, motion lines, text or effects. One single creature, no extra views.

AVOID
- Not Blastoise, Clawitzer, Tentacruel, Grapploct, Cloyster or a recoloured Octillery.
- Not a robot, mech, tank, ship or submarine: no hull, deck, treads, turrets, chimneys or flags.
- Not over-designed: no spikes, chains, armour everywhere or tiny details. No plush toy, chibi, Neopets or mascot look.
```

## Rondes
- **r1 (10 nov):** `r1_A_gatling.png`, `r1_B_mantel.png`. Jordi: "Beide echt slecht, is gewoon octillery met wat kanonnen". Jordi stuurde géén bijlagen mee ("dat is het ironische"); de tekst "keep from Octillery" + de opsomming van Octillery-kenmerken was genoeg om Octillery na te tekenen met wapens en een helm erop. Jordi: "Ik wil dat die meer kraken wordt. Maar ook echt een oorlogswapen. Het steel gedeelte moet natuurlijk zijn, hier lijkt het erop geplakt. Dat is bij een Empoleon bijv ook niet". Verder met richting A.

- **r2 (10 nov):** `r2_A2.png` (prompt A2). Jordi: "nog steeds lelijk, nu is die wat meer een kraken vorm, maar het lijkt echt heel goedkoop, wat metaal erop geplakt en voor de rest echt precies octillery". Twee rondes mis → stoppen, eerst overleggen.

## Prompt A2 (na r1; richting A, meer kraken, oorlogswapen, steel als anatomie zoals Empoleon)
Keuzes Claude (Jordi kan schrappen): mantel langgerekt als bij een inktvis met twee stalen vinnen bovenaan (leest als granaat/torpedo); de snuit = de sifon (waarmee inktvissen echt water spuiten) die een gatling is.

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE IDEA
- The final evolution of the Remoraid line, Water/Steel. Remoraid is a pistol, Octillery a cannon; this stage is a living weapon of war: a KRAKEN, the giant sea monster that drags warships down, grown into heavy artillery.
- This is NOT Octillery with weapons added. The whole body has changed into a new, much bigger and more dangerous animal. Only the red colour, the heavy-lidded half-closed eyes and a few round yellow warts tell you it evolved from Octillery.

ANATOMY (a giant squid / kraken)
- A long, tall, torpedo-shaped mantle that rises up and back behind the head, like a giant squid, ending in two broad fins at the top.
- Long, thick, muscular tentacles, much longer than the body is tall. Several of them rise up and curl in the air around the body like a sea monster rising from the deep; the others brace heavily on the ground.
- Big, heavy and powerful. Menacing and calm, not screaming, not angry.

THE STEEL IS PART OF THE BODY (like Empoleon's steel beak and wing edges)
- No armour, helmet, plates or casing laid over the body. Only these body parts ARE steel, dark gunmetal with a blue sheen, and they keep the natural shape of that body part, flowing smoothly into the red flesh:
  - the siphon/snout in front of the face (the tube squids use to jet water) has grown into a rotary gatling of several barrels, pointing forward-left. The most important feature;
  - the two fins at the top of the mantle, shaped like the tail fins of a torpedo or artillery shell;
  - the ends of the two front tentacles, which have hardened into one thick cannon barrel each, the opening at the tip, raised and aimed forward. The tentacle itself becomes the barrel; nothing is attached to it.
- Exactly three weapons: the gatling and the two tentacle cannons. No other guns.

POSE AND VIEW
- 3/4 view facing left, towering up, weapons aimed forward-left. Both eyes visible.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO water, splash, ground, rock, shadow or base.
- No muzzle flash, smoke, bullets, ink, glow, sparkles, motion lines, text or effects. One single creature, no extra views.

AVOID
- Not Octillery with a helmet or guns stuck on. Not Blastoise, Clawitzer, Tentacruel, Grapploct, Malamar or Cloyster.
- Not a robot, mech, tank, ship or submarine: no hull, deck, treads, turrets, bolts, rivets, seams or flags.
- Not over-designed: no spikes, chains or tiny details. No plush toy, chibi, Neopets or mascot look.
```

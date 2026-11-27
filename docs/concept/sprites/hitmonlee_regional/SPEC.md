# Regionale Hitmonlee (glas, voetbal) – SPEC

## Besluiten (Jordi, 27 nov; letterlijk)
- "ja een voetballende hitmonlee lijkt me goed, doe maar een omhaal pose, maar we maken hem van glas gloeiend en geblazen"
- "ook soort knipoog naar 'de man van glas' wat vaak met voetballers gezegd wordt"
- Type: puur Fire. Geen bal. Helemaal gloeiend. Voetbal alleen in de pose.
- Tyrogue blijft hetzelfde. Hitmonchan regional = Ice, ijssculptuur met handschoenen als kubussen (apart; type nog open).

## Gemini-prompt r1 (Engels, zonder bijlage)
```
Design a regional form of the Pokémon HITMONLEE, as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64 pixels, max 16 colors, clean dark outline, white background.

What it is: Hitmonlee made entirely of hand-blown glass that is still glowing hot, like glass just taken out of the furnace: the whole body glows molten orange-yellow, translucent, with the smooth rounded swellings of blown glass. It looks fragile, a nod to the football saying "the man of glass" for a player who is always injured. Type: Fire.

Anatomy: keep Hitmonlee's body plan exactly: an egg-shaped torso with the eyes directly on it (no separate head, no neck), thin arms with big hands, very long thin legs with big flat feet. Same number of limbs as Hitmonlee: two arms, two legs.

Pose: a football bicycle kick (overhead kick): body leaning back in mid-air, one leg kicking high up over the torso, the other leg folded below, arms out for balance. Facing 3/4 to the left. Keep the composition compact so it fits a square sprite; limbs stay close to the body.

No ball. No football clothes, no shirt, no shoes, no patterns: the football is only in the pose.
No flames, no sparks, no glow halo, no heat haze, no effects, no ground, no shadow.
AVOID: a human in a glass costume, a glass statue on a pedestal, a plush/Neopets look.
```

## r1 (`gemini/r1.png`)
- Jordi: "pose klopt niet en hij is nog niet echt glas achtig".
- Claude: staande hoge trap i.p.v. omhaal (lijf rechtop); materiaal leest als ondoorzichtig oranje plastic/klei; beenringen beige (lezen als verband, niet als glas).

## Gemini-prompt r2 (nieuw gesprek, zonder bijlage)
```
Design a regional form of the Pokémon HITMONLEE, as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64 pixels, max 16 colors, clean dark outline, white background.

What it is: Hitmonlee made entirely of hand-blown glass that is still glowing hot, fresh out of the glassblower's furnace. It must clearly read as GLASS, not plastic or clay:
- translucent: the far arm and far leg are faintly visible through the torso;
- the glow comes from inside: a bright yellow-white hot core, turning orange and then deep red toward the edges and the thin ends;
- sharp, small white glossy highlights like on a glass bottle, and a thin bright rim of light along the edges;
- smooth rounded swellings and pinched thin necks at the joints, like blown glass.
The ribbed coils on the legs are ribbed glass in the same glowing colors (no beige, no bandages). Everything is the same glowing glass, no other materials.
It looks fragile, a nod to the football saying "the man of glass" for a player who is always injured. Type: Fire.

Anatomy: keep Hitmonlee's body plan exactly: an egg-shaped torso with the eyes directly on it (no separate head, no neck), thin arms with big hands, very long thin ribbed legs with big flat feet. Two arms, two legs.

Pose: a football BICYCLE KICK (overhead scissor kick), NOT a standing high kick. The body is airborne and almost horizontal, lying back in the air with its back toward the ground, the top of the torso pointing down-left. Both legs are up in the air in a scissor motion: the kicking leg swings up and over above the torso with the foot at the top of the sprite, the other leg drops down behind it. Both arms are spread out toward the ground to break the fall. Nothing touches the ground. Facing 3/4 to the left. Compact composition that fits a square sprite.

No ball. No football clothes, no shirt, no shoes, no patterns: the football is only in the pose.
No flames, no sparks, no glow halo around the body, no heat haze, no effects, no ground, no shadow.
AVOID: orange plastic or clay look, opaque body, a human in a glass costume, a glass statue on a pedestal, a plush/Neopets look.
```

## r2 (`gemini/r2.png`) = MODEL
- Jordi (27 nov): "dit is hem, vertaalt die naar een sprite?"
- Test (Claude): eigen raster 10,24 px (100×100), figuur 68×74 cellen → licht verkleinen naar 64 (rijen schrappen); kale reductie in `test/`. Aandacht: gloed in de romp wordt vlekkerig, omlijning ontbreekt grotendeels, doorschijnend been in de romp en het oog klein.
- Jordi: "kijk ook of gemini dingen heeft gedaan die niet overeenkomen met hitmonlee" / "op het eerste gezicht lijkt het van niet".
- Vergelijking met Gen 3-Hitmonlee (Claude, `test/vergelijk.png`): (1) handen dunne spinvingers i.p.v. dikke stompe wanthanden; (2) polsring op de nabije arm (Hitmonlee heeft alleen beenringen); (3) voeten zonder scherpe witte klauwen (trapvoet laars, andere voet ronde teentjes; kussentje wel als witte stip); (4) oog ovaal met oranje iris i.p.v. hoekig boos wit oog met zwarte pupil. Voorstel: die delen uit Gen 3-Hitmonlee overnemen en naar glas omkleuren; rest 1-op-1 model. Wacht op Jordi.
- Jordi (27 nov): "nagels iets minder scherp zie ik maar vind ik geen ramp" / "ga maar bouwen" / op het voorstel Hitmonlee-delen: "nee hoeft niet, het is een regional form, dus mogen het iets anders doen". → Sprite 1-op-1 naar het model (r2), geen Hitmonlee-delen.

## Sprite (27 nov)
- Maker r13 → `sprite/kandidaat.png`; eindkeuring ek1 (PASS beide eisen, 23 px: belijning + doorschijnend kickbeen in de romp terug naar modeltint) → `eindkeuring/ek1.png`. Ter beoordeling bij Jordi.
- Jordi: "top eindkeuring nog" → tweede (DC-)eindkeuring ek2: PASS beide eisen, 1 px (hiel trapvoet zwart → donkerrood). Open: linkerwand romp ±10 px recht (model rondere koepel; komt van rijen/kolommen schrappen).
- Jordi (27 nov): "ok nog even een rechte lijnen check doen, de benen hebben slordige rechte lijnen ipv de vorm die hitmonlee hoort te hebben, is opnieuw getekend? arm ook, kijk naar de oorspronkelijke hitmonlee hiervoor. Bovenop hoofd ook een lange rechte lijn"
- Claude: niet hertekend, maar (a) rijen/kolommen schrappen maakte rondingen recht (koepel, linkerwand) en (b) de maker zette de ringen met de hand als rechte banden (zijn eigen twijfelpunt 3). → reparatieronde r14.
- Jordi (27 nov): "het ziet er iig niet uit, dat moet nog gefixed worden, verder is de sprite goed" → r14 repareert alleen de rechte lijnen (koepel, linkerwand, benen/ringen, arm); rest blijft ek2.
- r15 (benen per ring als Gen 3-Hitmonlee, koepel rond, arm taps; 138 px t.o.v. ek2, rest gelijk) → eindkeuring ek3 PASS, 0 px (`eindkeuring/ek3.png`). Ter beoordeling bij Jordi.

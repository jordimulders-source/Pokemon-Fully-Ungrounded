# Gemini-prompt: viscacha, overworldsprite (18 nov)

Jordi: "dan moeten we alleen nog naar de overworld sprite kijken, laten we dat ook nog met Gemini proberen eerst". Eisen: `../../rug_icoon_studie/STUDIE.md` §1 en §3 (Overworld): HGSS-stijl zoals alle bestaande overworldsprites in de game; 32×32 per frame; drie aanzichten (naar beneden = recht van voren, naar boven = recht van achteren, naar links = profiel), elk stilstaan + lopen; figuur ±20 px hoog (front 49 → ±0,43×), onderkant y 29; eigen palet (≤15 kleuren + transparant).
Nieuw gesprek, alleen bijlage `../af/viscacha_8x.png` (geen voorbeeld: bij rug en icoon werkten voorbeelden tegen). Eerst alleen de drie stilstaande aanzichten; loopframes daarna.

## Prompt r1
> This is a Pokémon battle sprite of my creature. Draw its overworld walking sprite, in the style of the Pokémon that follow the player in Pokémon HeartGold/SoulSilver: a small chibi figure that walks around on the map.
>
> Draw three views of the SAME creature side by side, each in its own 32×32 pixel square, all standing on the same baseline:
> 1. facing down, toward the viewer: a straight front view (not three-quarter), the face looking at us;
> 2. facing up, away from the viewer: a straight back view, we see the back of the head, the ears, the back and the tail;
> 3. facing left: a side profile.
>
> Keep my creature exactly as it is: same face, same colors and color pattern, the two long upright ears, the yellow cheek tufts, the whiskers, the light belly patch and the tail with the spiky jagged yellow tuft at the end. Do not add anything new and do not redesign it. Chibi proportions: big head, compact body, each view about 20 pixels tall. Black outline, flat colors with one shade, no dithering.
>
> Show it enlarged so every pixel is clearly visible as a square. Plain white background, no ground, no shadow, no effects, no text.

## Toetsen (les van het icoon)
Eerst: is het ontwerp het onze (gezicht, oren, wangpluk, kleurverdeling) en staat elk aanzicht recht (voor/achter/opzij)? Pas daarna maat en techniek.

## Ronde 1 (18 nov): afgekeurd
(beeld kwam niet als bestand binnen) Drie aanzichten, maar rechtop op twee poten met ronde buik; Jordi: "lijkt meer op een raichu" · "of pachirisu". Gemini glijdt naar bekende soorten (zie GEMINI.md, viscacha werd eerder ook Raichu).

## Ronde 2 (19 nov)
Jordi: "doe toch een prompt voor de zekerheid met een afbeelding, het kost niks om het te proberen". Claude bouwt intussen de eigen route (onderdelen uit front/icoon/rug); Gemini is de vergelijking.
Verschil met r1: bijlage toont front én rug van ons ontwerp (`bijlage_r2_ontwerp.png`), de bouw staat in woorden (viervoeter, gehurkt, lang lijf), en wat niet mag lijken staat erbij (r1 werd een rechtopstaande Raichu/Pachirisu).

**Variant A** (nieuw gesprek, alleen `bijlage_r2_ontwerp.png`):
> The image shows the battle sprites (front and back) of my own Pokémon, a mountain viscacha (a South American rodent related to chinchillas). Draw its overworld sprite in the style of Pokémon HeartGold/SoulSilver walking Pokémon: three views of the SAME creature, each in its own 32×32 pixel square, side by side on one baseline:
> 1. facing down toward the viewer: straight front view, both eyes visible, symmetrical;
> 2. facing up away from the viewer: straight back view, we see the back of the head, both ears, the back and the tail;
> 3. facing left: side view.
>
> Body plan (keep it): a FOUR-LEGGED rodent, crouched low with a long body and a round arched back, standing on all fours, NOT upright on two legs. Long tail that curls upward with a jagged yellow tuft at the tip. Two rounded upright ears close together. Heavy-lidded, half-closed sleepy dark eye. A yellow lightning-shaped tuft on each cheek, thin whiskers, sandy ochre fur, cream chest. Copy the colors from the image.
>
> AVOID: Raichu, Pikachu, Pachirisu, Dedenne, rabbits, standing on two legs, a round belly facing the viewer, round red cheeks, big shiny anime eyes, any electricity or effects.
>
> Chibi proportions like HGSS walking sprites: head a bit larger, body compact, each view about 21 pixels tall. Black outline, flat colors with one shade. Show it enlarged so every pixel is a clear square. Plain white background, no ground, no shadow, no text.

**Variant B** (alleen als A het aanzicht/de maat niet snapt; nieuw gesprek, bijlagen `bijlage_r2_ontwerp.png` + `bijlage_r2_layoutvoorbeeld_eevee.png`): zelfde prompt, met na de eerste alinea:
> The second image is only an example of the format (three views, size, outline style) using a different Pokémon, Eevee. Do NOT copy Eevee's shape, face, ears, colors or fur; only copy how the three views are laid out and how simple and small they are.

Toetsen: eerst eis 0 (lijkt het op onze front: viervoeter, bolle rug, oren, slaperig oog, wangpluk, staart), dan of elk aanzicht recht is, dan maat en techniek.

### Ronde 2 resultaat (variant A): `gemini_r2_A.png`
Jordi: "stiekem best prima, op de ogen na" · "en geen snorharen, maar dat is niet erg".
Claude: opzij lijkt het meest op onze front (bolle rug, krullende staart met pluim, oren, wangpluk). Voor: goed (viervoeter, oren, wangplukken, crème borst, staartpluim boven de kop). Achter: middenlijn splitst de rug in twee billen en de staart hangt recht omlaag, terwijl hij voor en opzij omhoog krult. Ogen: dichte streepjes met een wenkbrauw, niet ons oog (donkere amandel met glanspixel en zwaar bovenlid). Maat: Gemini-pixel ±5 px, figuren ±39 px hoog, dus ±1,9× te groot (doel ±21 px): verkleinen hoort bij de werkwijze.

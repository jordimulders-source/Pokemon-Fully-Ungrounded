# Gemini-prompt: vuurwerklijn fase 3, v12 (16 nov): alleen de barsten (bijlage v11)

Bijlage 1: `r9/gemini_v11.webp`. Optioneel bijlage 2: een foto of pixelart van een echte vuurwerkbarst (pioen/treurwilg) die Jordi mooi vindt.

## Jordi over v11 (letterlijk, 16 nov)
"het vuurwerk is wederom geen vuurwerk"

## Analyse Claude
- v10: dichte sterren = stripboek-POW. v11: spaken met een felle kern = glinster/lensflits. Beide hebben het licht in het midden.
- Echt vuurwerk: het midden is leeg of dof, het licht zit in de uiteinden (de "sterren"), met sporen die naar het midden vervagen en onder de zwaartekracht naar beneden buigen (pioen, treurwilg). Een bol van vallende lichtsporen.

## Prompt

```
Image 1 is a Pokémon sprite: KEEP EVERYTHING EXACTLY (shape, coils, face, colors, rocket). Change ONLY the two burst shapes on its body.

They still look like sparkles or glints, not like fireworks, because the bright light is in the middle. Redraw them as REAL AERIAL FIREWORK SHELLS bursting:
- The CENTER IS EMPTY or dim.
- The light is at the ENDS: a ring of bright glowing dots (the firework stars) around the empty center.
- Behind each dot a trail that fades toward the center.
- The trails CURVE DOWNWARD under gravity, drooping like a willow or a peony firework, so the burst looks like a sphere of falling light.
- Pink, magenta and gold, about as big as the head.
[If image 2 is attached: draw the bursts like the firework in image 2.]

Official Gen 3 front sprite style, 64x64, max 16 colors, plain white background.
```

## v12b (16 nov): met Jordi's vuurwerkreferentie als bijlage 2
Jordi: "dit is vuurwerk imo" (`../referentie_vuurwerk_pixelart.png`, pixelart-vel met negen barsten op een donkere lucht).
Wat het vuurwerk maakt (Claude): losse, onderbroken stralen van ongelijke lengte met gaten ertussen, verspreide felle pixels langs en aan het eind van de stralen, onregelmatig (niet perfect symmetrisch), geen omlijning, klein of geen fel midden. Risico op wit: het vel leunt op een donkere lucht; de roze barsten (linksonder, midden onder) hebben genoeg donkere pixels om op wit te blijven staan.

```
Image 1 is a Pokémon sprite: KEEP EVERYTHING EXACTLY (shape, coils, face, colors, rocket). Change ONLY the two burst shapes on its body.

Image 2 shows what real fireworks look like in pixel art. Redraw the two bursts in exactly that style, like the PINK bursts at the bottom left and bottom middle of image 2: separate broken rays of uneven length with gaps between them, scattered bright pixels along and at the ends of the rays, slightly irregular, no outline, no big bright center. Keep them about as large as the head, in pink, magenta and gold, with enough dark magenta pixels to stay visible on a white background.

Do NOT copy the dark background of image 2. Official Gen 3 front sprite style, 64x64, max 16 colors, plain white background.
```

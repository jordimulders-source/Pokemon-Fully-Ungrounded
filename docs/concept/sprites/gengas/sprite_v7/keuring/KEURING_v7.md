# Keuring Gengas v7 (verse eindkeurder, 15 nov)

**Hoofdvraag: BIJNA.** Blind op 1×/2× leest hij meteen als een Gengar-achtige bol met losse manen, en het gezicht zit er goed op (vel `blind_1x2x.png`). Model-trouw buiten het gezicht is hoog (`diff_model_8x.png`: verschil zit bijna alleen in de afgesproken gezichtszone en in de krul). Ogen en grijns zijn gemeten Gengars pixels 1-op-1 op (x−6, y+5): 98/98 gezichtspixels kloppen, de paletmapping is consequent. Jordi's oude klachten (manen, linkeroor, vlak onder het rechteroor, pupillen, linkeroog) zijn weg: dat volgt nu het model of Gengar. Er blijven twee zichtbare punten op 8×.

## MOET
1. **Krul** (x36–46, y31–40; `krul_12x.png`, `krul_vs_poliwhirl.png`): de binnenlus is een hoekige "G" met haakse hoeken en rechte stukken van 3–4 px. Het model heeft een zachte, onregelmatige spiraal. Poliwhirls Gen 3-spiraal loopt rond, met trapjes van 1–2 px. Zelfde plek en grootte, alleen de hoeken van de lijn (tint 3) afronden. Dit is Jordi's klacht "krul niet mooi" en die is nog niet opgelost.
2. **Gezichtsband onderbroken** (y25–29; `punten_10x.png`, geel): links staat een grijzige rest (x6–10, tint 8, maar 13 px in de hele sprite), in het midden is de band weg (x11–24, gewone lijftint 5/6) en rechts loopt hij vol donker (tint 3) tot vlak boven het rechteroog (x25–37). Het model heeft één doorlopende band. Afgesproken was "lichter", niet "weg". Nu oogt het als een gat in de band achter het gezicht. Oplossing: één lichtere bandtint die van x6 tot x37 doorloopt, aan beide kanten even licht.

## MAG
- **Tandlijnen** (x14–29, y40–44; groen kader): tint c (136,135,132) is neutraalgrijs en ±30 lichter dan Gengars tandschaduw (106,98,123). Daardoor lezen de tanden iets vlekkerig. Dit is al genoemd in NOTITIES punt 3. Slot 8 (13 px) is een kandidaat om vrij te maken als punt 2 die tint toch overbodig maakt.
- **Losse pixels rond de krul**, bijvoorbeeld (38,28), (36,29), (36,37), (40,37), (37,38), (43–44,38): clusters van 1–2 px in tint 3/5/6. Opruimen zodra punt 1 klaar is.
- **De donkere tinten 2 (81,37,60) en 3 (96,54,74)** liggen maar ±15 helderheid uit elkaar (Gen 3: 30–40). Dat ziet je weinig, maar het is het enige tintpaar onder de norm.
- **De gaspluimen van het linkeroor** (x13–22, y5–8) en de punt bij (57–58,16) zijn lichtroze zonder omlijning. Dat is model-trouw (gas) en dus acceptabel.

Beeldmateriaal: `vgl_8x.png` (sprite | model | Gengar), `gezicht_12x.png`, `linkeroor_12x.png`, `rechteroor_12x.png` (beide trouw aan het model), `sprite_10x_raster.png`.

# Keuring Gnomini sprite r1 (variant A) – verse keurder, 22 nov

Gekeurd: `../sprite_r1/gnomini_A.png` tegen het bevroren model `../r2/gemini_r2.png`.
Hulpbeelden: `A_8x.png` (blind), `naast_8x.png` (sprite | kale reductie | model op schaal), `1x_3x.png` (1× op wit/groen/donker, 3× vergroot), `clusters.py` (tintvlakjes < 3 px).

## Oordeel: FAIL (kleine reparatieronde; geen vorm- of mutswerk)

### Blind (1× en 8×)
Leest op 1× meteen als een rond kaboutertje met grote muts en neus; formaat 34×41 (x15–48, y18–58) past bij een kleine eerste fase. Omlijning 1 px, gesloten, zwart aan de schaduwkant, gekleurde selout aan de lichtkant (mutstop, armpje L, voet L). Geen dithering of ruis. Zwakste punt: het roze lijf oogt vlak (middentint + een lichte vlek in het midden), terwijl muts en broek wel bol lezen.

### Eis 1: trouw aan het model – voldoet
Silhouet = kale reductie (0 px verschil volgens het makerrapport, visueel bevestigd naast het model). Muts (vorm, krul, vouwstreep, selout boven), neus, armpjes als rondjes, broekgrens, beide voetjes: alles aanwezig, niets toegevoegd. Broek rechts omhoog langs de arm komt uit het model. De rechte roze/blauw-grens komt uit het model (ter info, geen oordeel).

### Eis 2: Gen 3 – bijna
Tinten (helderheid): muts 104/130/174/194 (104 = vouw/selout), roze 105(lijn)/139/183/206, blauw 96(selout)/133/173/205 → ≤ 3 tinten + lijn per kleur. Stappen ±40 behalve hooglichten (muts 174→194 = 20, roze 183→206 = 23; zacht maar acceptabel).
Volume per vlak (hoofdvraag):
- Muts: licht linksboven, schaduwvlak rechts. Rechter paneel (x36–45, y25–38, ±100 px) is één effen tint; muts is bevroren ("uitstekend"), dus alleen ter info.
- Broek: goed – hooglicht linksboven, sikkel rechts die naar onder breder wordt.
- Roze lijf: **onvoldoende** – hooglichtlens (x29–33, y41–43) staat precies in het horizontale midden van het lijf (x21–42) en de schaduw rechts is maar een 1 px diagonaal (41,42)(40,43)(39,44). Leest als "effen vlak met een vlek" (Coathief-les), niet als bol.

## Reparaties (prioriteit)
1. **Hoog – roze schaduwsikkel rechts verbreden naar 2–3 px**, de bol volgend: zet q (213,102,136) op (39,41)(40,41), (38,42)(39,42)(40,42), (37,43)(38,43)(39,43), (37,44)(38,44), (36,45)(37,45). Bestaande q/blauw rechts ervan blijft.
2. **Hoog – roze hooglichtlens 2 px naar links** (meer linksboven op de bol): s (251,184,202) van (30–32,41),(29–33,42),(30–32,43) naar (28–30,41),(27–31,42),(28–30,43); vrijgekomen pixels → r. Rij 41 x28–29 grenst aan de neusrand: blijft er geen r-rand tussen lens en neuslijn, dan de lens een rij lager (y42–44).
3. **Midden – binnenlijn armpje L/lijf is open op (20,41)**: r → p (172,72,102), zoals de kale reductie.
4. **Laag – losse donkere pixel in de muts (26,33)**: b → c (184,163,211), zoals de kale reductie (geen vouwlijn in het model op die plek; 1-px vlekje).
5. **Laag – dunne beenstrook voet R (41,52)**: 1 px vulling tussen twee lijnpixels; mag blijven; optioneel (41,52) v → de kale-reductietint (56,109,142) zodat het als schaduw onder het lijf leest.

Ter info (geen reparatie): voet R is boven donker en onder licht (uit het model, teen naar de kijker); muts-rechterpaneel effen (muts bevroren).

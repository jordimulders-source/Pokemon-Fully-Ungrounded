# Gnomini (Fairy), fase 1 van de gnome-lijn (Gnomini → Gnomad → Gnometrotter)

## Jordi (letterlijk, 22 nov)
- "Ik denk aan een Gnome fairy lijn. Het woord gnome laat ook veel woordgrappen toe"
- "Iig een grote ronde neus en een muts die de ogen blokkeert"
- "Soort tuinkabouter achtig."
- "Fase 1 is gnomini, een hele kleine grappige ronde gnome."
- "laten we eerst beginnen met Gnomini ontwerpen"
- Antwoorden op vragen (22 nov): lichaam: "geen baard"; kleuren: "Eigen kleuren"; pose: "Waggelend lopen".
- "het moet een pokemon worden he niet een tekening van een tuinkabouter"
- "dat de muts veel bedekt lijkt me geinig ja" (na voorstellen: mol als basis / muts als lichaamsdeel à la Hatenna / paddenstoelhoed; keuze nog niet gemaakt)
- "nee gewoon een gnome, maar dan cartoony, niet een ventej in kleding"
- "het mutsje wordt lavendel, huid roze, de armpjes worden idd gewoon rondjes"
- Lijn en vormen: `docs/concept/IDEEEN.md` → "Gnome-lijn".

- r1 (`r1/gemini_r1.png`, prompt v1): "hij is toch wat aan de kale kant zo"
- "misschien wel een soort 'broek' wat gewoon een 2e kleur op het lichaam is"
- Broekkleur: "hemelsblauw" → prompt `gemini/PROMPT_v2.md`.
- r2 (`r2/gemini_r2.png`, prompt v2): "lijkt nu een beetje op een verrassingsei haha"
- Jordi over r2: "de muts is uitstekend, ik vind het wel een prima ontwerp en ik denk dat jij de schaduw en volume wel kan verbeteren, misschien is het lijf te eivormig en mag dat ronder nog"
- **Bevroren model: `r2/gemini_r2.png`.** Toegestane afwijkingen in de sprite: schaduw en volume verbeteren; lijf ronder (minder eivormig). Muts: "uitstekend" (bevroren).
- Sprite r1 (`sprite_r1/`, A = lijf als model, B = 3 px breder): Jordi "A". Over B: "B is compleet mislukt", "dat is niet rond".
- r2 (`sprite_r2/`): vraag "grens roze/blauw met de bol mee laten buigen?" → Jordi: "ja en misschien dat we een soort streep ertussen moeten doen, doe dat als A/B test".
- "en zijn linkerhand is niet rond" (= armpje links in beeld, met het duimachtige bultje; eerder: "de armpjes worden idd gewoon rondjes").
- r3 (`sprite_r3/`, A gebogen grens / B + donkerblauwe streep): Jordi "B is goed, maar het lichaam moet nog iets smoother rond qua vorm".
- r4 (`sprite_r4/`, A licht smoother / B onderflanken uitgebold): Jordi "A".
- Eindkeuring r4-A: PASS; 5 pixelreparaties door Claude → **af: `af/gnomini.png`** (+ `_8x`), op het overzichtsvel (New).

## Open (overleggen vóór de Gemini-prompt)
- Type: puur Fairy?
- Neuskleur (prompt: roze als de huid).
- Na af (22 nov): "Gnomini mag trouwens ook nog wel een dragonflycave keuring ja" (zelfde ronde als Gnomad r10–r11).
- Dragonfly Cave-ronde r6 (A egaal donkerroze rond de neus, B + 2 zwarte px): Jordi "de hele lijn om de neus dezelfde kleurtint?" · "maar daar worden toch meerdere tints gebruikt?" · "ja waarom doe je dat dan niet" → variant C (lijnen lopen mee met het licht).
- Variant C (verloop + 2 zwarte px rechtsonder de neus): "het klopt gewoon weer niet, 2 zwarte pixels rechtsonderin de neus, is echt bij elke cirkel de gehele lijn om de cirkel heen dezelfde kleurtint? dat hebben we toch eerder nog nooit zo gedaan?" → gecontroleerd op Gen 3 (Azurill, Jigglypuff, Whismur) en Gnomad af: binnenlijn rond een vorm = één egale eigen tint, zonder zwart → A klopt.
- "nu ben je echt aan het gaslighten" · "je zegt iets en daar geef je voorbeelden die je eigen ongelijk bewijen" (vergelijkingsvel `sprite_r7/binnenlijnen_vergelijk.png`). Onverifieerde les uit SPRITE_KERN gehaald.
- "maar zoek nou eens naar ronde vormen zoals de neus van gnomini" · "dezelfde grootte" · (over "die was al goed") "ja vond ik maar nu niet meer omdat ik er ook wel eens naast zit". Vergelijking: `sprite_r7/neus_gen3.png` (Grumpig-snuit, Mr. Mime-cirkels).
- "fix de neus van gnomini gewoon" → **af = r6-A** (neuslijn donkerroze, zwart alleen aan de buitenrand, zoals de Grumpig-snuit).

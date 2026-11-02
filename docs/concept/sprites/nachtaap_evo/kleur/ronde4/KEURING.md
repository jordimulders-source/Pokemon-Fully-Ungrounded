# Keuring nachtaap fase 2: ronde 3 en ronde 4 (onafhankelijke keurder, 2 nov)

**Wat gekeurd is:**
- **Maan en voorhoofd** (zone x4–24, y36–48): op `ronde4/nachtaap.png`. Dat is Jordi's keuze D2. De vorm ligt vast; ik keur alleen of het leest en hoe het getekend is.
- **De rest:** op `ronde3/nachtaap.png`. Buiten de zone is ronde 4 daar pixel voor pixel gelijk aan (gemeten: 44 px verschil, allemaal in x5–23, y37–48; zelfde palet; alpha-diff 0).
- Vergelijkingsvel: `../ronde3/keuring_vgl.png`. Scripts en uitsneden: `../ronde3/keuring/`.

**Oordeel: TERUG.**
- **Wat goed is:** de techniek. Het silhouet heeft 0 diff, er zijn 0 open randen, hij gebruikt 15 kleuren en het zwart-aandeel van de rand is 0,46.
- **Wat beter is:** de maan van ronde 4 leest een stuk beter dan die van ronde 3. In ronde 3 las hij als wit masker of schedel.
- **Wat niet goed is:**
  - De handen lezen op 1× als **beige plankjes**.
  - De kené leest als **krassen of bliksemlijntjes**.
  - De kop heeft een **doosvorm** (rechte binnenlijnen).
  - Het **verre oog is een exacte kopie** van het nabije.
  - Klein: de **rechterpunt van de maan** valt op 1× weg.

Ik heb eerst zelf geoordeeld, met de maan van ronde 3. Daarna heb ik de maan opnieuw gekeurd op ronde 4 en pas als laatste de NOTITIES gelezen (onderaan).

## Harde eisen (SPRITE_NORM 1–10)

| # | Eis | Oordeel | Waarom |
|---|---|---|---|
| 1 | Leest op 1× als echte Pokémon | **FAIL** | Lijf, staart en spiraal staan goed naast Lairon, Sableye, Aipom en Slakoth. De handen lezen als beige plankjes (F4) en de kop als doos (F2). Daardoor oogt hij eerder als buidelrat dan als aap. |
| 2 | 3/4 links-voor, kop meer naar de kijker | PASS | Lijf 40° schuin, kop bijna frontaal (Jordi's A2). Twee ogen met de neus ertussen. |
| 3 | Alle ledematen tellen op 1× | **FAIL** | De verre hand (x3–14, y56–60) is een vlek van E en F door elkaar, zonder vingers. De verre achtervoet (x23–27, y56–58) leest als de duim van de nabije hand. → F4 |
| 4 | Geen Escher | PASS | De verre voorhand ligt links, hoger en in schaduwtint. Dat klopt voor een dier dat naar links kijkt: je ziet dan zijn linkerflank. |
| 5 | Geleidelijke curven, geen doos-kop | **FAIL** | De kop is binnen het silhouet een afgeronde doos (→ F2): <br>• kruin y36 x12–19: 8 px recht (idx 2) <br>• kin y54 x8–21: 14 px recht zwart <br>• rechterzijde x25 y42–49: 8 px recht zwart <br>Daarnaast zijn de ogen een kopie (F3). |
| 6 | Kop | PASS | Kopvak ±435 van 1459 px (±30%). Het lijf is naar verhouding groter dan in fase 1, zoals gevraagd. |
| 7 | Ogen geïntegreerd | **FAIL** | Bovenlid zwart, iris donker boven en licht onder, glans: in orde. Maar de binnenkant van het verre oog (x16–19, y43–47) is pixel voor pixel gelijk aan die van het nabije (x7–10), ook in ronde 4. → F3 |
| 8 | Kenmerken op 1× leesbaar | **FAIL** | • Spiraal: goed. <br>• Maan (r4): leest als ∩-sikkel; alleen de rechterpunt valt weg (F1). <br>• Kené: leest als krassen of bliksem, niet als patroon (F5). <br>• Handen: geen vingers (F4). |
| 9 | Omlijning, licht linksboven, geen open randen | PASS | 0 open randen. De rand bestaat uit zwart (112), violet (107) en crème-omlijning (25). Licht van linksboven, ook op de maan. |
| 10 | Geen Chernobyl of beige vlakken | **FAIL** | • Verre hand: vuil-beige vlak met een dambordje van E/F (x4–12, y57–59). <br>• Nabije hand en achtervoet: crème blokken met een rechte bovenkant (y57 x31–38, 8 px). <br>→ F4 |

## §0-checklist SPRITING.md
| # | Punt | Oordeel |
|---|---|---|
| 1 | Lijf én blik diagonaal | PASS |
| 2 | Ledematen geteld en verbonden | **FAIL** (F4) |
| 3 | Geen rechte lijnen | **FAIL** (F2) |
| 4 | Ogen geïntegreerd, verre oog geen kopie | **FAIL** (F3) |
| 5 | Silhouet leest als de soort | **FAIL**: op 1× eerder buidelrat dan aap. Het silhouet is bevroren, dus de reparatie zit in de kleur: handen met vingers (F4). |
| 6 | Formaat | PASS (1459 px = 1,54× fase 1) |
| 7 | Pose niet stijf | PASS |

## Leest het op 1×? (per onderdeel)
- **Kop als eigen bol:** het is wel een eigen vorm, maar geen bol (doos, F2).
- **Maan, ronde 3:** las als wit masker, skibril of schedel om de ogen. Dat zat dicht bij de afgekeurde "bleke gezichtsschijf". Dit is vervangen.
- **Maan, ronde 4:** ja, grotendeels. De sikkel is dik bovenaan, wit aan de lichtkant, de holte boven de ogen is violet en de punten lopen omlaag. Je ziet een maan over de ogen, geen masker meer.
  - De rechterpunt (x20–21, y43–48) staat in zilverlila (idx 7) op idx 4. Op 1× zie je daardoor alleen de witte linkerpunt, en lijkt het op licht een scheve kap. → F1
  - Op 4× is de maan in orde.
- **Ogen:** starend en rood, ja; nu minder brilachtig dan in ronde 3. Het verre oog is wel een kopie (F3).
- **Snoet en mond:** de lichte snoet (x11–15, y48–53) met neus en neutrale mond leest. PASS.
- **Oortjes:** rechts in orde. Links is het een crème schuin streepje (x4–6, y37–41) dat op 1× als hoorntje leest. Klein punt, zie "Voor Jordi".
- **Handen en achtervoet:** nee (F4).
- **Spiraal:** ja.
- **Kené:** nee (F5).
- **Volume van het lijf:** in orde.
- **Selout:** in orde.

## FAILs: zone, wat te doen, pixelbudget
Het silhouet blijft bevroren; alleen indexen binnen de figuur veranderen. De maanvorm van D2 blijft staan.

- **F1 Rechterpunt maan** (x20–21, y43–46, ≤ 4 px):
  - **Wat:** laat de bovenste 3–4 px van de rechterpunt wit lezen, net als de linker.
  - **Hoe:** idx 7 → 8 op x21 y44–46. Zilverlila houd je alleen aan de onderste 2 px en langs de buitenrand.
  - **Waarom:** de vorm verandert niet, het gaat alleen om de tint.
- **F2 Doos-kop** (±12 px, buiten de maan):
  - **Kin** y54 x8–21: beide uiteinden 1 rij omhoog (x8–9 en x20–21 naar y53), zodat de onderkant een boog wordt.
  - **Rechterzijde** x25 y42–49: de onderste 2 px 1 kolom naar binnen buigen.
  - **Kruin** y36 x12–19 (8 px recht idx 2, raakt de maanzone): het midden 1 px hoger (y35 x14–17), maar alleen als dat de D2-vorm niet raakt. Anders laten staan en aan Jordi melden.
- **F3 Verre oog geen kopie** (x15–20, y43–47, ≤ 3 px):
  - **Wat:** geef het verre oog een eigen schaduw.
  - **Hoe:** de buitenkant van de iris (x19, y45–46) van A naar 9.
  - Grootte en positie blijven gelijk; het gezicht verandert niet.
- **F4 Handen en voeten** (x3–27, y55–62 en x31–41, y56–60, ±35 px):
  - **Verre hand:** haal het E/F-dambord weg; maak 3 vingers van 2 px, gescheiden door E-lijntjes in één richting.
  - **Nabije hand:**
    - 3–4 vingers met scheidingen;
    - de bovenste rij (handrug) violet in plaats van crème, zodat er crème vingerkussens overblijven (zoals fase 1) in plaats van een plank.
  - **Verre achtervoet:** een violette enkel en 2 px tenen in schaduwcrème.
  - **Nabije achtervoet:** breek de rechte bovenkant met 2 teenscheidingen.
- **F5 Kené** (x16–47, y26–36, ±45 px):
  - **Wat nu misgaat:** de diagonale trapjeslijnen van 1 px lezen als krassen of bliksem. Het gaat om idx 6/7 en om de idx-5-diagonaal bij de staartaanzet (x44–47, y30–33).
  - **Wat ervoor in de plaats komt:** een herhaald, rechthoekig getrapt meandermotief van horizontale en verticale stukken, 2–3 keer herhaald langs de ruggengraat.
  - **Kleur:** idx 6 op de basis en idx 5 op de schaduwkant.
  - **Doel:** op 1× leesbaar als patroon. De toon blijft rustig (lichter dan de vacht, niet wit).

## Voor Jordi (smaakkeuzes, geen FAIL)
- **Psychic?** De rode ogen met zwarte pupil, de donkere violette vacht en het wit zetten hem naast Sableye en Misdreavus: hij leest eerder als Ghost/Dark dan als Psychic. Dat volgt uit je keuzes (rodere ogen, donkerder vacht). Wil je meer Psychic, dan helpt een roze of magenta glans in de iris, zoals in fase 1.
- **Volgende fase van fase 1?** De violette vacht en de spiraal komen terug. Kop en ogen zijn bewust anders (jouw wens), en daardoor voelt hij nu eerder als een verwante Pokémon dan als de volgende fase.
- **Rat of aap?** Het bevroren silhouet (laag gehurkt, dunne lange staart, kop vooraan) leest snel als rat of opossum. Handen met lange vingers (F4) helpen al; de rest is een vormkeuze.
- **Crème oortjes:** dat is een licht vlak op de kop naast de maan, terwijl je zei: "het enige witte op het hoofd moet de halve maan zijn". Mogen de oortjes violet worden, met alleen crème aan de binnenkant?
- **Kené-richting:** het poppetje heeft zelf zigzagbanden die op bliksem lijken. Bedoelde je die vorm, dan gaat F5 alleen over leesbaarheid. Wil je echte Shipibo-geometrie, dan moet het motief rechthoekiger.

## Wat ik mat
Alle scripts en uitsneden staan in `../ronde3/keuring/`.

**`meet.py`** (argument `ronde3` of `ronde4`):
- 1459 px, 15 kleuren plus transparant.
- Alpha-diff tegen `silhouet_bevroren.npy` en `.txt`: 0 in r3 en in r4.
- Rand:
  - zwart 112, violet 107, crème-omlijning 25;
  - aandeel zwart 0,46;
  - open randen 0.
- Zwart in totaal: 12,3%.
- Losse stippen (geen 8-buur met dezelfde index): r3 21, r4 19. Dat is vooral de oogrand en de E-stippen in de handen; in r4 komen daar (16,37) en (16,44) bij.
- Rechte binnenlijnen van 5 px of meer:
  - y54 x8–21;
  - y36 x12–19;
  - x25 y42–49.
- Binnenkant van de ogen: in r3 én r4 identiek.
- Wit: 84 px (r3), 66 px (r4). Crème: 138. Kené (idx 6/7): 70–75.
- r3 tegenover r4: 44 px verschil, alleen in x5–23 en y37–48.

**`zoom.py`:** uitsneden op 8, 12 en 14× (kop van r3 en r4, rug) en op 4× op donker.

**`vel.py`:** maakt `../ronde3/keuring_vgl.png`, met:
- r3, r4 en fase 1;
- daarnaast 15 echte sprites: Lairon, Sableye, Misdreavus, Mismagius, Aipom, Ambipom, Grumpig, Zigzagoon, Spinda, Kecleon, Natu, Abra, Mightyena, Slakoth en Espeon;
- elk op 3× en 1×, op lichte en op donkere achtergrond.

## Na het lezen van de NOTITIES (ronde 1–4)
Dit verandert mijn oordeel niet. Wel drie verschillen met wat de maker schreef:
- **Ogen:** ronde 1 noemde het verre oog "1 px smaller, geen kopie". Sinds ronde 2 zijn de binnenkanten weer identiek; ronde 4 schrijft dat de ogen "bevroren sinds ronde 2" zijn. De kopie zit er dus al twee rondes in, onopgemerkt.
- **Verre hand:** ronde 2 schreef dat die "op 1× als lichte hand met vingertoppen, niet als plankje" leest. Ik zie op 1× wel een plankje: de vingerscheidingen lezen als een dambordje.
- **Kené:** ronde 1 rekende het als leesbaar ("als lichte lijnen"). Lichte lijnen zijn precies wat er nu staat, maar dat is geen patroon.

Wat de maker over de maan van ronde 4 schrijft (dik midden, tapse punten, zilverlila aan de schaduwkant) klopt. Alleen kost de zilverlila rechterpunt op 1× zijn leesbaarheid (F1).

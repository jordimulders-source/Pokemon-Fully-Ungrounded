# Eindkeuring nachtaap fase 2, kleur ronde 14 (onafhankelijke keurder, 3 nov)

**Oordeel: TERUG.** Er zijn twee kleine FAILs, allebei in de crème tenen en samen 8 px:
- **F1:** aan de onderkant (schaduwkant) staan nog 6 bruine (E) randpixels naast transparant. Daar hoort zwart.
- **F2:** de achtervoet heeft een hark van 1 px op y59 (E C E C E C). De tenen op y58 en y59 lopen niet in dezelfde kolommen, dus je ziet een dambordje.

Alles daarbuiten is af. Na deze 8 px is hij volgens mij GOED: de proef is gedaan, met alpha-diff 0 en 0 harken (`eindkeuring/proef_fix.png`, `proef_poten12.png`). De sprite zelf is niet gewijzigd.

Gekeurd: `nachtaap.png` + `normal.pal`. Vel: `eindkeuring_vgl.png`. Het toont de nachtaap naast fase 1, Growlithe, Slakoth, Vigoroth, Lairon, Sableye, Misdreavus, Espurr, Aipom, Grumpig, Natu, Abra en Monferno, op 3× en 1×, licht en donker. Uitsneden staan in `eindkeuring/`: `kop16`, `poten16`, `staart16`, `rug14`, `zoom8_licht`/`_donker`.

## 1. SPRITE_NORM, harde eisen
| # | Eis | Oordeel | Bewijs |
|---|---|---|---|
| 1 | Leest op 1× als een echte Pokémon | PASS | Naast Lairon, Slakoth en Sableye leest hij als een gehurkt Pokémon met een maankop en een krulstaart. Hij valt niet uit de toon. |
| 2 | 3/4 links-voor, kop meer naar de kijker | PASS | Lijf 40°, kop 80° (bevroren). De snoet zit tussen de twee ogen. |
| 3 | Ledematen tellen, met lucht ertussen | PASS | Verre hand x3–9, nabije hand x10–21, verre achtervoet x23–26, achtervoet x31–38 en de staart zijn allemaal verbonden. Er zit een luchtgat tussen de armen (15–16,56). |
| 4 | Geen Escher | PASS | De kop ligt voor het lijf. Er is een kruinlijn (14–17,35)–(20–21,37), met de violette kruin 5 tussen de maan en de lijn. |
| 5 | Curven, geen doos | PASS (zie "Voor Jordi") | De kin uit ronde 11 is gerepareerd: nu 3-9-4 (y53/54/53), met de flank ingesprongen op x24 vanaf y46. De resterende rechte stukken liggen in het bevroren silhouet. |
| 6 | Kop | PASS | Bevroren. |
| 7 | Ogen geïntegreerd | PASS (bevroren r10) | Het bovenlid is vlak donker (y43). De iris is A boven en B onder, met glans 8 links boven en een 2×2-pupil. Het verre oog is wel een kopie, zie "Voor Jordi". |
| 8 | Kenmerken op 1× leesbaar, geen harken | **FAIL (F2)** | Maan, ogen, spiraal, wiggen en vingers lezen op 1×. De hark zit op de achtervoet: y59 x31–37 = E C E C E C D. |
| 9 | Omlijning per groep, zwart aan de schaduwkant, geen open randen | **FAIL (F1)** | Violet is in orde: bovenop/links 111× 2, rechts/onder 117× 1, zwart-aandeel van de rand 0,48. De crème groep heeft onderaan nog 6× E naast transparant (zie de tabel). |
| 10 | Geen Chernobyl | PASS | Het gezicht is rustig, de mond neutraal, er zijn geen vlakken uit het niets. |
| P | Patroonregels | PASS | F (168,196,236) is een eigen toon. De wiggen zijn vlak en 3–8 px breed, zonder bevel, en buigen om de rug. In de schaduwplooi y30–34 en bij de staartwortel worden ze 6; dat volgt de lijfschaduw (4 wordt daar 3), dus het is consequent. Wig 3 volgt Jordi's krabbel. |

## 2. §0-checklist (SPRITING.md)
| # | Punt | Oordeel |
|---|---|---|
| 1 | Lijf én blik diagonaal | PASS |
| 2 | Ledematen, oren en ogen geteld en verbonden | PASS |
| 3 | Geen rechte lijnen | PASS. Wat overblijft staat in het bevroren silhouet en is door Jordi geaccepteerd. |
| 4 | Ogen geïntegreerd, verre oog geen kopie | PASS op integratie. De kopie staat onder "Voor Jordi", omdat de ogen bevroren zijn. |
| 5 | Silhouet leest als de soort | PASS (lori-gelijkenis: Jordi akkoord) |
| 6 | Formaat | PASS: 1459 px (1,54× fase 1) |
| 7 | Pose niet stijf | PASS |

## 3. Per onderdeel (op 1× en 3×)
| Onderdeel | Oordeel | Opmerking |
|---|---|---|
| Kop | PASS | Lichtkant links (5 op x5–6 y49–50), schaduw 3 rechts. De kinlijn is gerepareerd. |
| Maan | PASS | Wit, met schaduw in 7 aan de rechter- en onderbinnenrand ((14–15,41), (16–19,42), x20–21). Er zit kruinviolet tussen de maan en de kopcontour. |
| Ogen | PASS | Bevroren en sterk. De glans staat in beide ogen links boven, dus consequent. |
| Snoet en mond | PASS | Neus (12–13,50), mond (12–14,52). Hooglicht in 5/6. |
| Oortjes | PASS | Bevroren. Het verre oortje is een knopje (x3–7, y37–41) met 6 aan de lichtkant. |
| Armen en handen | PASS op de vorm, **FAIL F1** op 2 randpixels | De vingerlijnen van de nabije hand lopen door (x13, x16). De diagonale vingerlijn (8,58)–(7,59) van de verre hand is bewust (ronde 13). |
| Achtervoet | **FAIL F1 + F2** | Een hark op y59 en een bruine hoek (31,59) onderaan. |
| Verre achtervoet (x23–26, y57–58) | **FAIL F1** | De onderrij y58 is helemaal E, terwijl daaronder transparant is. |
| Spiraal en staart | PASS | De buitenring is 2 px, de binnenkrul is pseudo-omlijnd (2/1), wat bij een staartpunt kan. Het hooglicht 5 loopt als strook aan de lichtkant van de steel. Er zijn geen gaten. |
| Wiggen | PASS | Zie P hierboven. |
| Volume | PASS | Licht linksboven: rugtop 5 (x16–25, y28–34), schaduw 3 rechtsonder, de staart achter het lijf grotendeels in 4/3. |
| Selout | PASS | Violet in orde. De maan grenst links aan 2 (Vigoroth-niveau), zie "Voor Jordi". |

## 4. Dragonfly Cave (`dragonflycave_spriting_guide.txt`)
| Regel uit de gids | Oordeel | Bewijs |
|---|---|---|
| "Outline shadows" zijn (bijna) zwart | PASS | Index 1 = (28,20,36). |
| Omlijning per kleurgroep (outline base, outline-hooglicht aan de lichtkant) | PASS | Violet: 2 aan de lichtkant, 1 aan de schaduwkant. Crème: E als outline base. Wit (de maan): 2. GF gebruikt naast wit vaak een middengrijs (Zangoose 139,148,148, Absol 98,98,131) en Vigoroth een donker (72,64,64); onze 2 (50,34,78) ligt dicht bij Vigoroth. |
| Zwart rond de schaduwkant | **FAIL (F1)** | Onderaan nog E naast transparant: (9,59), (10,61), (23–25,58), (31,59). |
| Omlijning 1 px, geen zwarte klonten | PASS (met opmerking) | Het enige 2×2-blok zwart is de kinlijn plus de bovenrand van het luchtgat (15–16,54–55). Dat is een diepe plooi zonder licht, en de gids zegt dat daar de donkerste tint hoort. |
| Geen anti-aliasing aan de buitenkant | PASS | Alle randpixels zijn 1, 2 of E. Er staan geen lichte puntjes buiten de lijn, ook niet op een donkere achtergrond (`zoom8_donker`). |
| Licht linksboven, consequent | PASS | Lijf, kop, staart, maan (7 rechts) en oogglans (links boven) volgen allemaal dezelfde lichtrichting. |
| Grens basis/schaduw op de "evenaar"; slagschaduw volledig in schaduwkleur | PASS | Onder de kin en tussen de armen staat 3. De plooi bij de staartwortel is 3, en het patroon wordt daar 6. |
| 3 tinten per kleur, relatieve helderheid gelijk, één tint per groep | PASS | Violet 3/4/5 (+6/7 als extra licht), rood 9/A/B, crème D/C + E. De helderheid loopt in elke groep op. |
| Niet overshaden | PASS | Er zijn geen verlopen. 6 en 7 komen alleen op kleine plekken voor (snoet, oortjes, maanschaduw, patroonschaduw). |
| Genoeg hooglicht (R/S-stijl) | PASS | 5 = 124 px (8,5 %), plus de lichte wiggen. Op 1× is hij niet te donker naast Sableye of Misdreavus. |
| Glans: klein en alleen waar het glanst; kraalogen met glans én reflectie | PASS | Eén pixel 8 per oog, links boven, en B als gekleurde reflectie onderaan. Verder staat er geen glans op de vacht. |
| Curven: geen punten of hoeken in een curve, geen besluiteloze segmenten | PASS | De kin loopt nu 3-9-4. Wat overblijft (rugtop y25 10 px, kopflank x4, staartsteel) is bevroren silhouet. |
| Geen symmetrie of gekopieerde delen | Voor Jordi | Het verre oog (x6–11) is gelijk aan het nabije (x15–20), op 2 pixels na ((6,45), (6,46) = 9 in plaats van B). De ogen zijn bevroren. |
| Vachttextuur: gekartelde grens, niet overdreven | PASS | De vacht is glad, met tekenfilmschaduw zoals de meeste GF-sprites. De gids staat dat expliciet toe ("de meeste Pokémon: gewoon zoals de bol"). |
| Dithering spaarzaam, geen ruis | **FAIL (F2)** | De lijfvlakken bevatten 0 dithering. Op de achtervoet staat een hark van 1 px (y59). Het dambordscript vindt verder alleen trapjes langs de omlijning, net zo veel als bij Growlithe, Slakoth en Vigoroth (12–15). |
| Pseudo-omlijning bij dunne delen | PASS | De binnenkrul van de spiraal is 2 px, alleen donker 2/1, zonder extra omlijning. |
| Banding / pillow shading | PASS | De gids noemt die termen niet letterlijk. Ik heb ze getoetst via de bolregel (schaduw aan één kant, niet naar alle randen). Er is geen pillow shading: de schaduw zit rechts en onder, de lichtkant is licht tot aan de lijn. Er is ook geen banding: de enige evenwijdige strook (staartsteel 2-5-4-3-1) is buisschaduw, zoals bij de staart van Aipom. |

## 5. FAILs: pixeltabel (8 px; alpha-diff 0; buiten deze pixels geen wijziging)
| # | Pixel (x,y) | Nu | Wordt | Waarom |
|---|---|---|---|---|
| F1 | (9,59) | 14 (E) | 1 | Rechtsonder aan de verre hand. Hierdoor verdwijnt ook de hark E-D-E-D-E op y59 x5–9. |
| F1 | (10,61) | 14 | 1 | Linksonder aan de nabije hand. |
| F1 | (23,58) | 14 | 1 | Onderrand van de verre achtervoet. |
| F1 | (24,58) | 14 | 1 | Idem. |
| F1 | (25,58) | 14 | 1 | Idem; sluit aan op de bestaande 1 op (26,58). |
| F1 | (31,59) | 14 | 1 | Linksonder aan de achtervoet. |
| F2 | (35,59) | 14 | 12 (C) | Tenen uitlijnen met y58. De scheidingen komen op x33 en x36. |
| F2 | (36,59) | 12 | 14 | Idem. Achtervoet y59 wordt E C E C C E D: drie tenen (x32, x34–35, x37), net als bij Sableye. |

De E aan de linker- en bovenranden blijft staan, want dat is de lichtkant. De diagonale vingerlijn van de verre hand uit ronde 13 blijft ook. Controle met `eindkeuring/proef.py`: 8 px, alpha-diff 0, 0 harken. Daarna staat er aan de schaduwkant nog 1× E, op (3,58); dat is een linkerrand, dus in orde.

## 6. Voor Jordi (bevroren of smaak, geen FAIL)
- **Het verre oog is een kopie van het nabije** (28/30 px gelijk). §0.4 en de gids zeggen "geen kopie", maar de ogen zijn bevroren ("zeer sterk"). Een eventuele kleine stap: het verre oog 1 kolom smaller of donkerder maken aan de buitenkant. Alleen doen als Jordi dat wil.
- **Rechte stukken in het bevroren silhouet:** rugtop y25 x23–32 (10 px), kopflank x4 y42–49, staartsteel x48/x51 y13–20 en de voetzolen y60. Jordi vond ze niet storend.
- **De maan naast 2:** GF zet naast wit vaak een lichtere outline base. Er is geen vrije paletplek. Als Jordi de maan op 1× zachter wil, kan dat met 2→3 op de lichtkant van de maan: x4 y42–48, (8,38) en (9–11,37), ±11 px. Smaak; niet nodig.
- **Kleur 6** is zowel vachthooglicht (snoet, oortjes) als schaduwtint van het patroon (wig 2 en 3). Op 1× stoort het niet, omdat het patroon het alleen in de schaduw gebruikt.
- **Wiggen in F** lezen als ijsblauw, niet als zilver (dat zei ronde 11 ook). Smaak.

## 7. Wat ik mat (scripts en uitvoer in `eindkeuring/`)
- **`meet.py` → `meet_uitvoer.txt`** (basis: ronde 11):
  - Modus P, transparency 0, PNG-palet gelijk aan `.pal`. 15 kleuren plus transparant.
  - 1459 px. Alpha-diff 0 tegen `silhouet_bevroren.npy` en `.txt`.
  - Zwart 11,2 %, 1+2 23,2 %. Rand 244 px, zwart-aandeel 0,48.
  - 13 "open" randpixels: alleen E.
- **`rand.py` → `rand_uitvoer.txt`:** de omlijningskleur per kant. Schaduwkant: 117× 1, 19× 2 (bovenrechts op de rug, dus lichtkant), 7× E. Die laatste zijn F1 plus (3,58).
- **`ruis.py` → `ruis_uitvoer.txt`:**
  - 15 dambordjes van 2×2. Bijna allemaal omlijningstrapjes, vergelijkbaar met Growlithe (12), Slakoth (12), Vigoroth (14) en Sableye (12).
  - 3 harken van 5 px, alle op y59 in de tenen. Ter vergelijking: Sableye heeft er ook één in de klauwen, maar daar lopen de klauwen over 2 rijen uitgelijnd.
- **`proef.py`:** past de 8 px toe op een kopie (`proef_fix.png`) en maakt `proef_poten12.png` en `proef_voor_na.png`. Resultaat: 0 harken, alpha-diff 0.
- **`crop.py` en `vel.py`:** de uitsneden en het vergelijkingsvel.

## 8. Na het oordeel gelezen: `ronde11/EINDKEURING.md`
- **De F1 en F2 van ronde 11 zijn opgelost.** Wig 3 is vlak lila volgens Jordi's krabbel. De kin is van 12 naar 9 px gegaan, de uiteinden staan op y53 en de flank springt in op x24. Dat bevestigt mijn PASS op kop en patroon.
- **Ronde 11 zette de E-randen bij de vingers onder "Voor Jordi"** (bevroren handen). In ronde 13 heeft de coördinator de onderrand van de verre hand al zwart gemaakt, als afwerking ("de onderrand aan de schaduwkant is zwart"). Mijn F1 maakt dat af voor de laatste 6 pixels. Het is kleurafwerking, geen vormwijziging, en valt daarmee onder Jordi's "voorpoten gek qua afwerking in kleur".
- **De hark op de achtervoet** werd in ronde 11 niet genoemd. Het is een nieuwe bevinding van mij, gemeten met het script.
- **Mijn oordeel verandert niet: TERUG op F1 (6 px) en F2 (2 px), daarna GOED.**

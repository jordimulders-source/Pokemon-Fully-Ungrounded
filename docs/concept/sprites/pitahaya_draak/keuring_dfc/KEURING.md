# Eindkeuring Dragonfly Cave, pitahaya-draak fase 1, r8 (16 nov)

Gekeurd: `af/pitahaya_draak.png` (= `sprite_r8/pitahaya_r8.png` = de r7-simulatie, diff 0). Vergeleken met het model (`model/model.png`, natief raster `sprite_r7/natief.png`, spritepixel (X,Y) = natief blok (3X+4..3X+6, 3Y+6..3Y+8)) en met Treecko, Cacnea, Bagon, Oddish en Larvitar (bovenste 64×64, op 8×). Eerst zelf geoordeeld, daarna pas `keuring_r7/KEURING.md` gelezen.

- **Vel:** `vel.png`. Bovenaan r8, de simulatie en het natieve model op 8×. Rood = MOET, blauw = KAN, oranje = ter info. Rechts staan r8 en de simulatie op 2× en 1×, op licht en donker. Onderaan de Gen 3-refs op 8×.
- **Scripts:**
  - `meet_dfc.py` meet tinten, zwakke tintgrenzen, zwart, 2×2-zwartklonten, dambord, vulvlakjes, losse zwarte pixels en lijnkanten. Hij gebruikt `keuring_r7/meet.py`. Met `--ref` meet hij de Gen 3-refs.
  - `sim.py` past de MOET-lijst toe, met een assert op de oude index, en schrijft `sim_moet_sprite.png`.
  - `vel.py` maakt het vel.

## Oordeel: **FAIL, 3 px** (na de MOET-lijst PASS; simulatie gemeten)

### Hoofdvraag (1× en 2×)
- **Wat werkt.** De sprite leest meteen als een draakje met een pitahayakop op een cactuslijf. Dat geldt op licht en op donker.
- **Model.** De sprite is trouw aan het model. De ogen, de grijns met tandje, de groene schubpunten (bovenop, links en rechts), de rib-areolen en de losse rechterarm met gat zijn allemaal herkenbaar.
- **Naast Gen 3.** Het lijf is drukker dan dat van Treecko, Bagon en Larvitar, met veel ribbenlijnen. Dat komt uit het model: het model heeft ribben en vlekschaduw. Cacnea is even druk.

### Per onderdeel
| onderdeel | licht / schaduw | lijnen | oordeel |
|---|---|---|---|
| kop | Licht linksboven met lichte schubbulten (5). De schaduwsikkel rechts en onder is 2 px breed (3) en loopt langs de vorm. Geen pillow shading: links is de rand licht tot aan de selout. | Selout links/boven in 2 of 8 (68 px), schaduwkant zwart (75 px, 0 selout). Om-en-om 0, lichte tint op de rand 0. De schubnaden rechts zijn 1 px in donkerroze 2, uit het modelskelet (min-lum 11–42). | goed |
| schubpunten | De groene punten hebben lichte tinten (10/11) aan de lichtkant, met 8 als selout. De punten rechts (y 17–19 en 27–28) zijn kleiner dan in het model, omdat het modelblok daar < 5/9 dekt. Het silhouet volgt het model (≥ 5/9-regel: 0 afwijkingen buiten het armgat). | De vork van de naad op (39–41, 20–21) is een dambord. Die vork staat zo in het model. | goed |
| gezicht (technisch) | Bevroren, alleen gemeten. Muilkleur 6 tegen roze 4 heeft een lum-verschil van 0,4. Dat zijn de enige echte zwakke grenzen in dezelfde kleurfamilie (4 paren). Ze lezen wel, omdat de kleurtoon verschilt (357° tegen 341°). | De pupil is een 2×2-zwartklont (32,23). Dat hoort bij een oog. | ter info |
| romp | Donkerder onder de kop, lichter links (a), zoals in het model. Geen banding. | Bij de nek hangen drie zwarte tikjes onder de kopbodem: (26,37), (29,37) en (32,37). Ze vormen een regelmatig stippelpatroon en maken de lijn plaatselijk 2 px dik. Het model heeft daar geen dikke zwarte lijn. Zie MOET. | **MOET** |
| armen | Rechterarm: licht aan de buitenkant, met een doorlopende armlijn en een gat (r7-fix werkt). Linkerarm: licht a/b met 8 als selout. | De klauwen van de linkerhand lezen als een zwarte balk (16–18, 45–46). Het model heeft daar 3 lichte klauwtjes. | KAN |
| poten | De dijen zijn licht (b), de voeten donker. Lichte tenen rechts uit het model (r7-fix). | De tenen zijn 1 rij licht boven een zwarte tip, zoals de klauwen van Bagon. | goed |

### Metingen (r8 → simulatie)
| meting | r8 | sim | Gen 3 Treecko / Cacnea / Bagon / Oddish / Larvitar |
|---|---|---|---|
| tinten (incl. lijn) | 13 | 13 | 15 / 14 / 12 / 10 / 9 |
| zwakke tintgrenzen (< 20 lum) | 3,1 % | 3,2 % | 2,4 / 4,6 / 1,6 / 1,8 / 1,1 (norm 0–9 %) |
| zwart van de figuur / binnen | 12,8 / 4,0 % | 12,6 / 3,7 % | 21,7/7,4 · 22,4/10,7 · 14,3/4,1 · 14,3/4,5 · 15,4/6,4 |
| 2×2-zwartklonten | 4 (oog 1, onder de kin 3) | 4 | 0 / 16 / 0 / 0 / 5 |
| dambord 2×2 | 9 | 10 (+(28,37), de ribbenlijn die nu op de kop aansluit) | 21 / 9 / 5 / 16 / 12 |
| losse zwarte pixels binnen de figuur | 3 | 2 (beide in de bevroren mond) | |
| buitenlijn licht (sel/zwart) · schaduw (zwart/sel) | 68/4 · 75/0 | idem | |
| om-en-om / lichte tint op de rand | 0 / 0 | 0 / 0 | |

- **Contrast per tintstap** (lum van de vlaktinten):
  - roze 2→3→4→5: 62 → 95 → 133 → 168, stappen 33 / 38 / 35;
  - groen 8→9→10→11: 67 → 99 → 132 → 169, stappen 32 / 33 / 37;
  - muil 6→7: 28;
  - oog 12→13: 51.
  - Binnen ±30–40, alleen de muilstap is iets onder 30 (bevroren).
- **Wat de zwakke-grenzenmeting telt.** Roze en groen hebben bijna dezelfde lum: 3 tegen 9, 5 tegen 11 en 2 tegen 8. Ze verschillen wel in kleurtoon, dus dat is geen zwakke tintgrens. Een RGB-meting < 60 telt 19 %, maar dat komt alleen door deze complementaire paren.
- **Hue-shift.** Groen schuift van licht naar donker van 94° naar 128°, naar blauwgroen. Goed. Roze schuift niet: 344° naar 342°. Het model ook niet (mediaan 345° naar 340°). Dus trouw, zie ter info.
- **Vulvlakjes < 3 px buiten het gezicht (21).** Dat zijn allemaal 1-px groene of lichte schubpunten, de teenlichtjes, klauwpunt (20,45) en de schaduwpuntjes 3 en 9 in de naden rechts op de kop, en ze staan alle in het model. Geen ruis.

## MOET (3 px; overnemen uit het model)
1. **De zwarte nektikjes worden de bovenkant van de ribbenlijnen.** Ze worden donkergroen 8. Per pixel de natieve modelmeting:
   - **(26,37): 1 → 8.** Blokgemiddelde (65,92,73), dichtste tinten 9/8. Er liggen maar 2/9 donkere natieve pixels (15, 22), een dunne lijn. Volgens de r7-regel is dat niet zwart, dus de donkerste vlaktint.
   - **(29,37): 1 → 8.** Gemiddelde (43,49,46), dichtste tint 8. Het was de "losse zwarte pixel" uit r7. Hij sluit nu diagonaal aan op de ribbenlijn (28,38)–(28,39).
   - **(32,37): 1 → 8.** Gemiddelde (37,56,47), dichtste tint 8. Er ligt maar één natieve rij donker (12/15/17). Hij sluit aan op de ribbenlijn (32,38).

**Simulatie** (`sim_moet_sprite.png`, zelfde palet, index 0 transparant):
- 3 px gewijzigd;
- silhouet- en gezichtsdiff 0;
- zwart binnen de figuur gaat van 4,0 naar 3,7 %, losse zwarte pixels van 3 naar 2;
- om-en-om blijft 0;
- er komt één dambord bij, de diagonale aansluiting (29,37)–(28,38). Dat is een modellijn, net als de andere 1-px diagonalen.

Op 2× en 1× is de nek rustiger: de kopbodem is één strakke lijn en de ribben beginnen eronder, zoals in het model. Nergens is het slechter.

## KAN
- **(17,45): 8 → 9.** Het modelgemiddelde (96,113,84) ligt het dichtst bij 9; natief 3 donker en 5 licht (lum 172–176). Dit is een klauwtje van de linkerhand, dat nu één zwarte balk is. Het wordt een vulvlakje van 1 px (een klauwlichtje, zoals (20,45)).
- **(44,47): 8 → 9.** Dit is de klauwpunt van de rechterhand (KAN uit r7). Het modelgemiddelde (99,120,88) ligt het dichtst bij 10/9.
- Beide samen in een proef: geen nieuw dambord of om-en-om, zwart buiten de figuur iets lager.

## Ter info voor Jordi (geen MOET)
- **Zwarte klont onder de rechterkin**, (35–40, 33–36), 3 klonten van 2×2. Het model heeft daar twee dunne lijnen die samenkomen, met donkerroze ertussen. De maker heeft de kopbodem bewust zwart gemaakt, als vorm over vorm aan de schaduwkant. Gen 3 doet dat ook (Cacnea 16 klonten, Larvitar 5). Ik heb (37,34) 1→2 en (36,35) 1→2 geprobeerd (modelgemiddelde lum 56/63): de klonten verdwijnen, maar er komt een dambord bij op (36,34). Daarom geen goede wissel.
- **Het roze schuift niet in kleurtoon** (schaduw even koel of warm als het licht), net als in het model. Gen 3 schuift roze schaduw vaak iets naar paars. Dat zou een paletronde zijn (0 px), maar het verandert de kleur van het model. Dat is dus aan Jordi.
- **Drukte van het lijf.** De ribben en vlekschaduw komen uit het model. Een rustiger lijf zou een ontwerpwijziging zijn.

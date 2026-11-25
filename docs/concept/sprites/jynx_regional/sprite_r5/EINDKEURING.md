# Eindkeuring regionale Jynx (sirene): r4 B → r5

Verse eindkeuring op schaduw, kleurtinten en lijnen (25 nov). Jordi vroeg erom ("eindkeuring qua schaduw/kleurtinten en lijnen").
- **Basis is r4 variant B** (zonder rokvouwlijn). Jordi koos B: "rechts beter".
- **Werkwijze:** eerst een blinde blik, pas daarna de keuringen van r1 en r3 gelezen.
- **Vergeleken met:**
  - het model `gemini/r5.png`, op schaal en per pixel gemeten (modelhelderheid L);
  - de maatstaf-sprites Skinguin, Dundragoon, Zapacha en Princadee;
  - de Gen 3 `anim_front_gba.png` + `normal_gba.pal` van Jynx (haar en rok), Gardevoir (stof) en Pidgeot (vleugels).

Bouwen: `cd docs/concept/sprites/jynx_regional && python3 sprite_r5/bouw.py`. Dat maakt ook `_8x.png` en `vel.png`.

## Eindoordeel: **PASS, 0 px gewijzigd**
Ik vond geen pixel die binnen "alleen uitvoering" aantoonbaar beter wordt. r5 is dus gelijk aan r4 B. `bouw.py` bewijst dat:
- 0 px anders dan r4 B, silhouet-diff 0;
- 16 kleuren inclusief transparant, mode P, transparency 0.

Jordi vond r3/r4 al netjes, en elke wijziging die ik overwoog was óf tegen het model in, óf een met de hand verzonnen band (zie onder). Dat is precies het vaste foutpatroon uit SPRITE_KERN, dus die wijzigingen heb ik niet gedaan.

## Per punt

### Lijnen: PASS
- **Outline base per onderdeel** volgens DC (gids r. 340–470):
  - veren en rok: veerlijn (120,48,24);
  - haar: haar donker (84,50,28);
  - lippen: lipdonker (96,28,48);
  - gezicht: de haarlijn als binnenlijn tegen het haar.
- **Zwart alleen aan de schaduwkant.** Gemeten met de randnormaal van het afgevlakte silhouet; het licht valt van linksboven.
  - 0 selout-pixels aan de schaduwkant.
  - 3 zwarte pixels aan de lichtkant: (21,56) (19,57) (20,57). Dat zijn de bovenkanten van de linkerpoot onder de overhangende rok. r3 heeft ze bewust zwart gelaten, als slagschaduw. Ik laat ze zo.
  - Nergens wisselen zwart en selout om en om.
- **Binnenlijnen niet zwart:** buiten het gezicht staat geen zwart binnenin.
  - De enige losse zwarte pixel is (25,16), de binnenooghoek van het rechteroog. Die staat ook zo in het model (los zwart blokje links van het oog).
- **1 px:** de lijnen zijn overal 1 px. Waar ze 2 px zijn, zijn het knooppunten van twee lijnen (zie r3).
- **Outline highlights** staan binnen de lijn (vleugels, linker rokpaneel, kruin). Er staat geen lichte kleur op de buitenrand (`controle.py`: leeg).
- **Zwart:** 7,3 % van de figuur. Gen 3-Jynx: 7,4 %.

### Schaduw: PASS (één punt ter info)
- **Gemeten per tint:** de gemiddelde modelhelderheid onder de spritepixels.

  | groep | tinten (sprite) | model L |
  |---|---|---|
  | veren | licht / midden / schaduw | 149 / 143 / 106 |
  | haar | licht / midden / schaduw / donker | 114 / 88 / 70 |

  De volgorde klopt overal, en de schaduw volgt de modelhelderheid.
- **Achterhaar rechts:** dit is het grote vlak in haar donker. Daaronder is het model 57–64, en het is daar zelf zo donker en vlak.
- **Rechter rokrand:** het lichte plekje (47–49,46–48) naast het haar staat in het model (142–160).
- **Rok:** licht links (kraag en linker paneel), midden in het midden, schaduw rechtsonder. Licht valt van linksboven, de grenzen zijn gebogen en er zijn geen banden.
- **Overwogen en niet gedaan:**
  - Pixels waar model en tint licht verschillen: vleugelpunt rechts (52,16) (56,16) (54,17) model 110–113, kraagrand links (19,27–30) model 100–113.
    - Dat is de anti-aliasing van modellijnen.
    - Omzetten gaf óf losse tintvlekjes van 1 px, óf een rechte verticale band van 4 px.
  - Het lichtere middenpaneel rechts (x39–47, y39–46, model 153–159 tegen 145 in de rest van de rok). Omzetten naar licht maakt een groot licht vlak aan de schaduwkant. Dat leest als licht van rechts.

### Kleurtinten: PASS
- **Helderheidsstappen**, alle binnen ±30–40 (Taillow/maatstaf):
  - veren: 172 / 141 / 106 / 67;
  - haar: 124 / 89 / 58 (+ haarlicht 160);
  - gezicht: 248 / 202.
- **Hue shift naar de schaduw:**
  - veren: 23° → 22° → 19° → 15°, roder in de schaduw, zoals Jynx' rok;
  - haar: 31° → 27° → 26° → 24°.
- Per groep ≤ 3 tinten + lijn.
- De kleine tintvlekjes < 3 px (`controle.py`) zijn diagonale lijnstukjes, strengschaduw naast een haarstreng (Gen 3-Jynx doet dat ook) en modeldetails (iris, tong, ooghoek).

## Wat veranderd is
| zone | px |
|---|---|
| gezicht | 0 |
| haar | 0 |
| vleugels | 0 |
| lijf + rok | 0 |
| poten + klauwen | 0 |

## Ter info voor Jordi (ontwerp/smaak, niet uitgevoerd)
1. **De rok is vlakker dan die van Gen 3-Jynx.**
   - Gemeten in de rok:

     | | licht | midden | schaduw | lijn |
     |---|---|---|---|---|
     | onze rok | 60 | 454 | 57 | 163 |
     | Gen 3-Jynx | 17 | 345 | 205 | 76 |

   - Jynx heeft dus ±35 % schaduw (rechterhelft en een band langs de zoom) en de helft minder lijnen. Onze rok is midden met veel vouwlijnen, zoals het model (rok vlak 145), en dat past bij de vaasstijl.
   - Meer schaduw zou van mij komen, niet uit het model. Als je de rok te effen vindt, zeg het, dan maak ik varianten. Uit het model komt dan niets: dat zijn ontwerpkeuzes.
2. **Het achterhaar rechts** is één donker vlak in de lijntint van het haar, zoals het model. Gen 3-Jynx kleurt het achterhaar in de schaduwtint, met strengen in de donkerste tint. Alleen veranderen als je het te zwaar vindt.
3. **Rest van de rokvouw in B:** in variant B blijft een stukje van de vouw over, (47,48) en (48,49), met een schaduwpixel (48,48) ernaast. Op 8× ziet dat rommelig uit. Je koos B om rechts, dus ik heb het laten staan.

## Bestanden
- `jynx_regional_r5.png` (= r4 B) en `jynx_regional_r5_8x.png`.
  - Een aparte `_B`-versie is er niet: B is de hoofdversie geworden, en de r4-variant met lijn vervalt.
- `bouw.py`: bewijs (0 px, silhouet-diff 0, 16 kleuren), plus 8× en vel.
- `vel.png`:
  - r5 | r4 (met lijn) | model, op 8×;
  - close-ups op 12× van gezicht + haar, rok en rechtervleugel, telkens naast het model;
  - op 1× en 2×, op licht en op donker, naast Skinguin, Dundragoon en Gen 3-Jynx.

# Vuurduivel fase 1, sprite r3 (alleen het gezicht)

**Sprite:** `vuurduivel_r3.png` (64×64, 4-bit palet, 14 kleuren incl. transparant; het mondbruin is niet meer nodig). 50 px hoog.
**Vel:** `vel.png` = r3 8× | r2 8× | model op dezelfde schaal; daaronder het gezicht van r3 op 16× naast het modelgezicht op dezelfde schaal (ook los als `gezicht_16x.png`); 1× op licht en donker.
**Script:** `wijzig_r3.py` (r2-raster + gezichtsblokken); elke pixel met reden in `wijzigingen_r3.txt`.
**Pixeldiff t.o.v. r2:** 28 px, allemaal in x17–28, y27–39 (kop). Daarbuiten 0 (gemeten).

## Voorbeeld: Haunter (Gen 3 `anim_front_gba.png`)
Techniek overgenomen:
- dik zwart lid (2 px waar nodig) dat schuin naar de neus zakt; samen vormen de twee leden de V
- het oogwit als halvemaan onder het lid
- de pupil groot in het wit aan de binnenkant
- geen zwarte onderrand onder het oog

Plek, maat en blik komen uit het model.

## Wat er veranderd is (r2 → r3)
- **Linkeroog (x15–19, y30–34):**
  - lid 2 dik: (15–18,31) en (18–19,32), zakt naar rechts
  - wit (16–17,32) en (16,33–34)
  - pupil 2×2 (17–18, 33–34) rechts in het wit, naar de neus, zoals het model (pupil kol 35–36)
  - wenkbrauwpixel (17,30) opgegaan in het dikke lid
- **Rechteroog (x23–29, y28–34):**
  - lid 2 dik: (27–28,29), (24–28,30) en (24–25,31), zakt naar links
  - wit (26–28,31) en (27–28,32–33)
  - pupil 2×2 (25–26, 32–33) aan de binnenkant (model kol 50–53)
  - de losse wenkbrauwpixels (26,28) en (25,29) zijn opgegaan in het dikke lid; (26,27) daarboven werd een losse zwarte pixel en is nu donkergrijs
- **Mond, op modelmaat en -plek gemeten in het natieve raster:**
  - mondhoeken omhoog (18,36) en (26,35), zwarte rand rondom, open van x18 tot x26
  - rood mondinterieur (21–23,37), (25,37) en (21,38)
  - roze tong (22–25,38) en (22–24,39)
  - witte hoektand rechtsboven (24,36–37), wit tandje linksboven (20,37)

## Niet uit het model
- **Mondinterieur:** rood (162,41,41) in plaats van het donkere mondbruin van het model, zodat de open mond leest tegen het donkere lijf. Kleur mag afwijken.
- **Leden 2 px dik en de wenkbrauw samengevoegd met het lid:** de Haunter-techniek; Gen 3 overdrijft het gezicht iets.
- **Hoektand 2 px** in plaats van 1.

## Zelf gezien
Op 1×–3× leest het gezicht nu als een grijns met schuine ogen in plaats van verbaasd. Het linkeroog valt niet weg.

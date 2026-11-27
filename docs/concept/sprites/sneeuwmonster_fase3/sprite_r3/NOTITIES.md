# Sauna-yeti – sprite ronde 3 (maker, reparaties van Claude op r2)

`sauna_yeti_r3.png` = r2 met 178 px gewijzigd + 2 paletkleuren; buiten de drie zones (en de handtint) diff 0. `bouw.py` (met argument `log` print elke pixel met reden), `vel.png` = r3 | r2 | model op 8×, close-ups 12×, 1× licht/donker naast fase 2.

## Palet (P1, 70 px)
- Handen/voeten: twee tinten → één, (112,151,164) = gemeten gemiddelde van de vlakke handcellen van het model; donker = de bestaande lijntint. Alle 70 handlicht-pixels → handtint (in het model verschillen de twee tinten weinig; dit viel op 1× het minst op).
- Plek 12 = **rood (216,72,32) terug** (fase 2) als buitenste gloedtint.

## 1. Gezicht (G, 52 px)
- Gezichtsvlak = de gemeten gezichtscellen van het model (g−r ≥ 20, L 190–235, gem. 197,222,233): per rij de spanwijdte van pixels met ≥ 35 % gezicht (rij 22–31), gaten dicht. Vlak = h (208,226,244); schaduw m alleen waar ≥ 40 % schaduwcellen (gem. 164,192,209) én rechts (X ≥ 32), zoals het model. Alle vacht-/wenkbrauw-/wanglijnen binnen het vlak weg.
- Daarop alleen ogen/leden/neus/mond op de gemeten plekken uit r1 (ongewijzigd): leden rij 23 (X26–28, X32–35), ooghoeken (26,24)(35,24), oogwit (27,24)(33,24), pupillen (28,24)(34,24), neus (30,25), glimlach rij 27 X27–32 + haak (33,26). Ogen niet vergroot: ze lezen nu op 1× tegen het egale vlak.
- Losse schaduwvlekjes < 3 px in het vlak → vlak.

## 2. Stenen (S, 69 px)
Per steen opnieuw opgebouwd uit dezelfde modelmeting (gloedaandeel per pixel), nu met dikte 1 px:
- rand (1 px buitenste ring): **rood** waar het model ≥ 40 % gloed heeft, anders zwart;
- naden **oranje**: diepe binnenpixels met ≥ 40 % gloed, plus een pixel direct naast de rand alleen als hij aan zo'n diepe naad raakt (de naad loopt door tot de rand). Gloeiende pixels naast de rand zonder naad worden steen → geen band meer;
- **geel** alleen in de heetste naadpixels (hoogste geelaandeel): 2 per schoudersteen, 1 per kleine steen;
- rest: steen, grijs facet waar de donkere steen L ≥ 50.
Gloed nu 71/256 steenpixels (28 %, model 28 %): rood 50, oranje 15, geel 6.

## 3. Vacht kop/schouders/manen (V, 35 px; zone X12–52, Y18–36, buiten gezichtsvlak, ogen ±1 px, stenen, emmer en buitenlijn)
- Lijnstukjes (lijntint/s, 8-samenhangend) < 4 px → vlaktint van de buren: alleen doorlopende strengen blijven.
- Vlakvlekjes < 3 px (m/h/w) → meest voorkomende buurtint (ook in het gezichtsvlak).
- Losse zwarte pixel (23,24) → w.

## Controle
bbox x1–62, y12–60 (62×49), 16 kleuren incl. transparant, geen lichte kleur op de buitenrand. Overgebleven vlekjes < 3 px: de oogwitjes (bedoeld) en 5 px buiten de vachtzone. Losse zwarte pixels: alleen pupillen, neus, mondhaak en 2 in stenen.

## Zelf nog zwak
- Linkerschoudersteen heeft maar 1 oranje naad + 2 geel (gemeten); het model toont meer brokken.
- Het gezicht leest nu, maar de bovenkant van het gezicht (rij 21–22) gaat zonder lijn over in de witte vacht; het model heeft daar een lichte vachtrand.

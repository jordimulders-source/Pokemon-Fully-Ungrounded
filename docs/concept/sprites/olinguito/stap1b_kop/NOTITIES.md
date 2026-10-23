# Olinguito stap 1b: gezicht van Galar-Linoone

Basis: `stap1_kop/anim_front.png` en het palet daarvan (byte voor byte gelijk). Leidraad: `referenties/galar_linoone_front.png`.
Bouw: `bron/bouw_stap1b.py` (met de hand per rij uitgeschreven, kolommen x11–36, rijen y26–32). Vergelijking en bewijs: `bron/vergelijk.py`.

## Hoe Galar-Linoone het doet (8×, coördinaten in zijn 64×64-sprite)
- **Oog:** x8–10, y36–37 (glans 7, roze 8/9). De neuspunt ligt op x1, y36–38. Het oog zit dus **8 px achter de neus en op dezelfde hoogte als de neus**, direct onder de voorrand van het voorste oor (oorbasis x9–13, y24–25; het oog zit 12 rijen lager). De achterkant van de kop (waar de kaaklijnen eindigen) ligt bij x≈15–16, dus het oog staat op ±0,5 van neus naar achterkop, midden op de kop. Hoogte: ±0,7 van oorbasis (y25) naar kin (y41). Het oog ligt op de snuitlijn, niet erboven.
- **Masker:** de donkere band (3) loopt van het oog **vrijwel horizontaal** naar voren, y31–35 over x4–12, en raakt de bovenrand van de snuit. Boven de neus zie je geen grijs/wit vlak maar de band zelf (de neusbrug is zwart).
- **Wenkbrauw:** de witte streep (5/6) ligt **direct op de bovenrand** van de zwarte band, zonder rij ertussen (y26–31, x7–14), en loopt mee met die rand.

## Metingen (horizontaal: neuspunt → achterkop; verticaal: oorbasis → kin)
| | neus → oogmidden | positie op kop | oog t.o.v. voorste oor | oog t.o.v. neushoogte | band oog → neus |
|---|---|---|---|---|---|
| Galar-Linoone | 8 px (x1 → x9) | ±0,5 | onder de voorrand van het oor | gelijk (y36,5 vs y37) | vlak, tot boven de neus |
| Stap 1 | 17 px (x9 → x26) | 0,59 | 5–9 px achter het oor (tussen de oren) | 1,5 rij hoger | schuin (y28 → y31), bruine brug erboven |
| **Stap 1b** | **12 px (x9 → x21)** | **0,41** | **direct achter het voorste oor** (oor x15–19, oog x19–23) | 1,5 rij hoger (ongewijzigd) | **vlak op y28**, tot boven de neus |

- Kopmaat bij ons: neus x9, achterkop x38, oorbasis y24, kin y38.
- Verder naar voren dan x19 kan niet: dan botst het oog met de knik in de snuitomtrek (x14, y28) en verdwijnt de band ervoor. Lager kan ook niet, want de grijns en kaak op y33–36 zijn bevroren. Ons oog zit al op neushoogte; die verhouding telt bij Linoone.

## Vertaling (101 px per frame gewijzigd t.o.v. stap 1)
1. **Oog + oogpatroon 5 px naar voren:** het lid (y29), het oog (y30–32), de wimperpunt (x24, y28), de lob achter het oog (y27 x26–28, y26 x29) en de maskerbreedte rond het oog (4 px erachter) verschuiven als één geheel van x24–34 naar x19–29. Waar de lob zat, komt bruine wang (x28–36). Het masker rond het oog is niet kleiner: dezelfde rand, lob en dikte. De onderlob (y33 tot x32, y34 x30–33) blijft staan en loopt nu als band onder de wang door naar achteren, zoals bij Linoone de donkere lijnen onder de wang.
2. **Masker over de neusbrug tot boven de neus:** de bruine neusbrug van stap 1 (y28–31, x11–18) is nu masker. De bovenrand ligt **vlak op y28** van het oog tot de snuitomtrek, en volgt vóór x15 de omtrek tot boven de neus (x11, y31). Langs de omtrek staat een rij glans (3: x15–16 y28, x14 y29, x13 y30, x11 y31) als licht van linksboven. Dat is geen nieuw bruin vlak.
3. **Wenkbrauw direct op de maskerrand:** 7-8-7-7-6 op y27, x19–23, recht boven het lid en direct op de maskerbovenrand (y28). Er zit geen bruine rij meer tussen. Het blijft 5 lichte pixels (net als in stap 1; de oude wenkbrauw op y26–27 x23–27 is nu vacht).

## Bevroren delen: pixeldiff-bewijs (`python3 bron/vergelijk.py`)
```
t.o.v. stap 1, frame 1: gewijzigd 101, buiten gezichtszone x11-34 y26-32: 0
t.o.v. stap 1, frame 2: gewijzigd 101, buiten gezichtszone x11-34 y25-31: 0
t.o.v. ronde 18, frame 1: gewijzigd 102, buiten gezichtszone x11-34 y26-32: 0
t.o.v. ronde 18, frame 2: gewijzigd 102, buiten gezichtszone x11-34 y25-31: 0
palet gelijk: True | transparency 0
silhouet gelijk: True | gewijzigde pixels naast transparant (open-randcheck): []
```
Oren (y19–25), neus, grijns en kaak (y33+), lijf, poten, klauwen en staart zijn identiek. Het silhouet van de kop is ongewijzigd en de omlijning is niet aangeraakt.

## Afvinken
- [x] Jordi 1: het oog en het oogpatroon zijn wat naar het midden en naar de snuit geschoven (5 px; neus→oog van 17 naar 12 px).
- [x] Jordi 2: boven de neus zie je het oogpatroon. Het masker loopt over de neusbrug, en er is geen bruine brug meer.
- [x] Jordi 3: de wenkbrauw zit direct boven het oog, op de maskerrand, en zweeft niet meer.
- [x] Kernpunt "oog te ver van de snuit": het oog zit direct achter het voorste oor, op 12 px van de neus.
- [x] Kernpunt "band horizontaler": de bovenrand ligt vlak op y28 van oog tot snuit in plaats van schuin y28 → y31.
- B1–B7 (FAKEMON_CHECKLIST): zoals in stap 1. B2: één oog, de neus is het meest linkse punt. B4: de oog-as en de band wijzen naar links, naar de neus. B7: oog, neus en grijns zijn er.
- Geen nieuw beige of crème (het aantal lichte pixels blijft 5), geen schaling, palet gelijk, geen open randen, PNG met transparency=0.

## Zelfcheck (compare.png: ronde 18, stap 1, stap 1b en Galar-Linoone op 1×, 3× en kop 8×)
- Op 1× en 3× leest het als dezelfde Pokémon, nu met een echt wasbeer- of Linoone-gezicht: één oog vlak achter de snuit, een donkere band tot de neus en een lichte streep erboven. Het is niet vreemder of minder schattig dan stap 1. Het oog staat dichter bij het "gezicht" en de kop oogt minder als een frontaal gezicht dat opzij is geplakt.
- Zwakke punten: (a) de wang achter het oog is nu een vrij groot effen bruin vlak (x28–36). Een rij schaduw (3) onderaan kan later, maar alleen als Jordi dat vraagt. (b) De band van oog tot neus is één donker vlak; de glansrij langs de omtrek is op 1× nauwelijks te zien. Bij Linoone is dat precies zo.

## Lessen
- **"Oog naar het midden" = meten, niet schatten:** meet bij de leidraad neus→oog, oog t.o.v. het voorste oor en oog t.o.v. neushoogte, en reken dat om naar onze kopmaat. Het voorste oor bleek de beste ijkpunt (Linoone: oog onder de voorrand van het oor).
- **Verschuif het oogpatroon als één blok** (lid, oog, wimper, lob en maskerbreedte) met een vaste dx. Dan blijft het masker rond het oog even groot, en wordt alleen het gat erachter vacht.
- Een onderlob van het masker die naar achteren doorloopt (y34 x30–33) niet "opruimen": zonder de band op y33 erboven wordt het een losse donkere streep.

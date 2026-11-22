# Vuurduivel fase 1, sprite r6 (kleurronde)

Opdracht: Jordi, letterlijk: "de oogvorm is goed, het kleur/schaduwwerk kan beter, over de gehele sprite". Uitgevoerd volgens `keuring_r5/KEURING.md`, MOET 1–10.

- **Sprite:** `vuurduivel_r6.png` (64×64, 4-bit, 16 kleuren incl. transparant).
- **Vel:** `vel.png` met r6 8× | r5 8× | model, plus 1× en 2× op licht en donker.
- **Scripts:** `wijzig_r6.py` (r5-raster + benoemde tinten) → `raster_r6.txt` → `bouw.py`. Elke pixel staat met reden in `wijzigingen_r6.txt`.

## Scriptcontrole (`controle.py`)
- alpha-diff t.o.v. r5: **0**.
- ogen (x15–19 y30–34 en x23–28 y28–34; lid, oogwit, pupil, witte pixels): indexdiff **0**.
- Lijnpixels: geen enkele bij. Weg zijn alleen de 9 die MOET 9 noemt: staartstam (36–41,50) en de bovenkant van de schuine stam (42,49), (43,48), (44,47), nu d.

## Palet (16 incl. transparant): samengevoegd
- Glans en vlam-middentint moesten erbij, dus er moesten twee kleuren uit.
- **Hoornlicht (233,100,94) + tong (198,98,92) + nieuwe vlam-middentint → één tint X (226,88,62)**, L≈127 zoals de keurder vroeg. Hoorns: R / H / X (L 46/88/127). Tong: X (iets oranjer roze dan r5). Vuur: R / r / X / O / Y.
- Index 15 is nu **glans (139,131,131)**.

## Per MOET-punt
1. **Lijfpalet:**
   - d → (41,38,38), m → (66,62,62), l → (98,92,92), lijn → (16,16,16). Stappen ±25–30, lijn→d 25. Alleen een paletwissel, dus de indexen in de ogen blijven gelijk.
   - Glans (139,131,131) op 6 px: 4 op de kop, 2 op de borst.
2. **Kop:**
   - Het l-vlak is breedst bovenaan en wordt naar onder smaller: (17,28), (22,28), (16–17,29), (21–22,29) zijn m.
   - Glans 2×2 op (20–21,25–26).
   - Wangbolling: (17,35) en (17,36) zijn l.
3. **Borst:**
   - Bolling: l op (22–26,43), (22,44), (25,44), (23–25,45). Glans op (23–24,44).
   - d-sikkel langs rechts (28–29,44), (29,45–47), (28–29,48) en onder (27–28,49). Het midden blijft m.
4. **Armen:**
   - Nabije arm: bovenrij l, (21,44) en (20,45). Hand linksboven l, (17,46). De rest m.
   - Verre hand: onderkant d, (37–38,45) en (37,46).
5. **Linkeroor:** lichte voorrand (13,31) l en (13,32) m. Binnenoor (14,31–34) blijft d.
6. **Broek, twee dijen:**
   - Linkerdij: t-bolling (19–25, 50–53).
   - Rechterdij: t linksboven (29–31, 51–53).
   - B in het kruis (25–28, 51–52) en op de taille rechts (rij 48–50 waren t).
   - b-sikkel langs de rechterrand (32–35, 47–56) en onder de rafels.
7. **Poten/hoeven:**
   - Poten: schaduwkant rechts b, (25,57), (24,58), (36,57), (37,58).
   - Rechterhoef is één t-vlak (35–36, 59–61) met B rechts; de streep in rij 60 is weg.
   - Linkerhoef: t-vlak van 3 px, (21–22,59) + (22,60).
8. **Vlammen:**
   - Middentint X op elke r/O-grens: O-pixels met r links of onder werden X, zodat elke tong R → r → X → O → Y loopt.
   - Rechts van de kop zijn de tongen in X gezet: (32–33,25), (35,25–27), (34,27), (37,26–27). Er staat r omheen.
9. **Staartstam:** de bovenrij en de bovenkant van het schuine stuk zijn d (zie scriptcontrole).
10. **Pijlpunt:** (45,38) is Y, zodat het geel 2 px breed is.
- **KAN, uitgevoerd:** de bovenste mondrij (21–23,37) is R (keelschaduw). De KAN over lichte selout op de vlammen is niet gedaan.

## Zelf gezien
- Het lijf leest nog zwart, maar heeft nu volume: kop met bolling en glans, borst met bolling en sikkel, verre arm donkerder.
- De broek leest als twee dijen. De hoeven zijn effen.
- De vlammen lopen vloeiender van rood naar geel.
- **Twijfel voor de keurder:** de tong is door de samenvoeging iets oranjer.

# Kudu sprite ronde 11: B6b netter (maker)
Jordi: "doe maar b6b, maar netter, minder rechte lijnen". Vorm en manier van B6b (r10) blijven. Oog K4.
Script: `sprite/r11.py` (bouwt op `r10.bouw(6,'b')`); vel en telling: `sprite/vel11.py`. Per gewijzigde pixel de reden staat in `telling.txt`.

## Wat er veranderd is
1. **Nekbovenlijn.**
   - Vorm: een boog van achter de oren (21,26) naar de schoft (33,31), steil bij de kop en vlak naar de rug. Stappen van 1, 2, 3, 3, 3 en 1 px in plaats van de trap van 2 px.
   - Lijnkleur: **K**, de donkerste eigen lijftint. Die zit ook in de kinlijn van de kop. K is sterker dan D, maar aan de lichtkant geen zwart.
   - Aansluiting: bij de schoft sluit hij aan op de ruglijn (D) van r6.
2. **Halsstrook.** Hij is 2 px M gebleven en buigt 1 px mee:
   - x13–14 (rij 28–30), x14–15 (31–33), x15–16 (34–36), x16–17 (37–38), x17–18 (39–40).
   - De rechterrand van de franje (0) en de linkerrand van de nekmanen (d) volgen hem.
   - Wat erdoor vrijkomt of opschuift, krijgt de vultint van de dichtstbijzijnde B6b-manenpixel of wordt lijf-M.
3. **Nekvolume.**
   - De losse L-vlek is weg.
   - Licht van boven als sikkel onder de nekboog: 1 px L over de hele boog, 2 px in het midden (x25–31). Dat is hetzelfde als de flank van r6, die L heeft onder de ruglijn. De rest is M.
   - Naast de rechterrand van de manen ligt 1 px D als slagschaduw.
   - Het model heeft hier haar (de kam). Zijn helderheid gaf licht ónder en donker bóven, dus die is niet gebruikt.
4. **Netheid.**
   - Omtrek van de manen: lichtkant d, schaduwkant 0.
   - De linkerrand van de nekmanen tegen de halsstrook is d.
   - Langs de kop geen extra lijn: de manen lopen achter de kop door.
   - Tintvlakjes kleiner dan 3 px (8-verbonden) in het gewijzigde deel zijn opgeruimd.

## Telling (`telling.txt`)
- **Rechte lijnstukken (d/0/K) > 3 px** in de manen, nek, franje en halsstrook: **geen**. In r10 B6b waren het er 4: x9 y30–33, x12 y30–34, x13 y35–38, x15 y28–35.
- **Pixeldiff:** buiten manen + nek + halsstrook 0 px; oogvlak 0 px.
- **Omvang:** 96 px anders dan r10 B6b. Palet ongewijzigd (15 kleuren).
- **0 naast d:** dat komt nog 4× voor, alleen op de overgang van licht naar schaduw (onderhoek franje, onderhoek manen) of tegen de kop. Nergens om en om.

## Zelf gekeken (8× en 1×)
- De nekboog leest nu als een gebogen, duidelijke nekrug. De manen hangen als franje plus nekhaar langs de hals naar de schouder.
- De halsstrook blijft zichtbaar als lichte strook tussen franje en nekmanen.
- **Zwak punt:** onder de punt van de franje is de borst vrij donker. Dat komt van de slagschaduw D plus de D uit r9/r10, rij 38–40. Een keurder moet zeggen of dat te zwaar is.
- **Zwak punt:** waar de K-boog op de schoft overgaat in de D-ruglijn van r6, is op 8× een kleurwissel te zien.

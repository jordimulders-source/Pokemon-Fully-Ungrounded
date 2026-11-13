# Keuring Krassault sprite 2, ronde 2 (`r2/octi.png`)

Onafhankelijke keurder, 13 nov. Geen makerrapport of eerdere keuring gelezen. Vergelijkingsvel: `keur_vel.png`
(boven: 2× tussen Octillery, Tentacruel, Gyarados | Krassault | Kingdra, Scizor, Crawdaunt, Seviper, licht en donker;
midden: 8× naast het model; onder: 1×/2×/4× licht en donker).

**Eindoordeel: NIET klaar voor Jordi.** Wel haalbaar met benoemde reparaties: de aanpak deugt, de opzet staat.

## 1. Hoofdvraag

**(a) Valt hij op tussen officiële Gen 3-sprites? Ja, hij valt op.** Twee redenen die je op 1× al ziet:
de onderkant is een platte, rechthoekige balk (twee keer hetzelfde blok naast elkaar) en de hele sprite is donkerder
en doffer dan alles eromheen. De bovenhelft (mantel, vin, rechteroog) kan er wél tussen staan.

**(b) Mooie natuurlijke sprite of knutselwerk?** Bovenhelft: echte sprite, met de hand getekend, leest goed.
Onderhelft en tentakels: knutselwerk. De rupsbanden zijn twee gekopieerde dozen met liniaalstrepen, drie tentakels zijn
kaarsrechte palen. Dat is precies wat Jordi "prutswerk" zou noemen, en de rupsbanden zijn het onderdeel dat hij expliciet noemde.

**(c) Leest elk onderdeel op 1× en 2×?**
| Onderdeel | 1× | 2× |
|---|---|---|
| Mantel + vin | ja | ja |
| Rechteroog (boos, geel) | ja | ja |
| Linkeroog | geel vlekje | nee: geel hokje met tralie |
| Kanonmond | grijsroze ring ("gasmasker/patrijspoort") | ring ja, loop met ribbels nauwelijks |
| Kanon links (tentakel) | ja | ja |
| Kanon rechts | ring tegen de kop, leest als oor/patrijspoort | redelijk |
| Tentakels | ja, als bos | ja, maar stijf |
| Rupsbanden als **opgerolde tentakels** | **nee**: slee / twee planken / pallet | **nee**: latjes, geen rol, geen spiraal |

**(d) Wat stoort een kritische eigenaar als eerste?**
1. De rupsbanden: plat, hoekig, identiek, geen rol. (Model: twee dikke rollen met ronde uiteinden en een duidelijke spiraal.)
2. De stijve verticale tentakels (palen in plaats van S-bochten).
3. Het linkeroog.
4. Zwaar en donker lijnwerk; dof framboosroze naast de felle echte sprites.

## 2. Metingen

| | px | bijna-zwart (L<50) | gem. helderheid | gem. verzadiging |
|---|---|---|---|---|
| **Krassault r2** | 2234 | **0,30** | **80** | 0,64 |
| Octillery | 1134 | 0,19 | 116 | 0,79 |
| Scizor | 1990 | 0,18 | 115 | 0,75 |
| Crawdaunt | 1792 | 0,19 | 110 | 0,77 |
| Tentacruel | 1785 | 0,14 | 125 | 0,53 |
| Gyarados | 2125 | 0,12 | 129 | 0,34 |
| Kingdra | 1596 | 0,08 | 143 | 0,46 |
| Seviper (donkere soort) | 1635 | 0,17 | 80 | 0,32 |

- Bijna-zwart 30% tegen 8–19% bij de echte (checklist E3: band 0,10–0,25). Oorzaak: twee lijntinten die allebei bijna zwart
  zijn, `(32,12,18)` L18 = 267 px en `(72,16,30)` L34 = 403 px. De tweede is bedoeld als gekleurde selout/binnenlijn, maar is
  op 1× gewoon zwart. Er is dus feitelijk geen gekleurde selout.
- Roodtrap: schaduw `(130,38,56)` L67 → basis `(176,58,76)` L95 → licht `(206,86,98)` L123 → glans `(234,136,136)` L165.
  Stappen 28/28/42: de stappen zelf zijn in orde. Het probleem is het niveau en de tint: de basis is even donker als de
  *schaduw*tint van Octillery/Scizor/Crawdaunt (L94–98), terwijl hun basis op L130–141 ligt. Het palet is **te donker en te dof**
  (roze-framboos, S 0,5–0,7; echte rode sprites S 0,8–1,0). Het model is zelf wijnrood, dus de tint mag donkerrood blijven,
  maar binnen Gen 3-helderheid.
- 12 kleuren gebruikt; er is ruimte voor 3 extra (o.a. een echte selouttint).
- 17 bruine pixels `(116,72,28)` liggen onomlijnd op de buitenrand (zuignappen): (21–22,23) (20,24) (23,24–25) (53,25) (52,26–27)
  (57,26) (58,27–28) (59,32) (60,33–34) (60,42) (6–7,44).
- Oppervlak 2234 px, box 62×56: past bij een eindvorm.

## 3. Per onderdeel

### GOED (bevriezen)
- **Silhouet en compositie**: mantel schuin naar rechtsboven, kop links-voor, breed en laag. Trouw aan het model.
- **Mantel en vin** (x29–55, y7–33): volume klopt, licht linksboven, roze selout op de linkerrand, banden lopen als
  doorlopende curven. Het sterkste deel.
- **Rechteroog** (x33–40, y34–40): leest op 1× als boos Pokémon-oog. Alleen de wenkbrauw is te dik (zie 7).
- **Kanon links** (x3–9, y25–32) en zijn tentakel: leest als loop, sluit aan.
- **Zuignappen 2×2 met glans** als idee: prima, Gen 3-waardig (behalve de randpixels, zie 8).
- Niets zweeft echt los; elke tentakel komt achter de kop of een andere tentakel vandaan.

### REPAREREN (op belang)

**1. Rupsbanden opnieuw tekenen (x7–62, y50–62). Belangrijkste punt, hele onderdeel.**
- Nu: twee rechthoeken van 26×11 px met rechte zijkanten (x=7, y54–59; x=62, y52–57), vlakke bovenkant, en als "spiraal"
  drie liniaalrechte lijnen van 13–17 px (y53, y55, y57; rechts idem y53/55/57). Leest als latten.
- De rechter is een kopie van de linker, 26 px opgeschoven. Het model heeft een nabije (rechts, groot, voor) en een verre
  (links, kleiner, deels achter de kanonmond).
- Opdracht: (a) beide uiteinden rond (hoeken 3–4 px afronden; een rol, geen doos); (b) de zijkant toont een echte spiraal:
  buitenwinding volgt de ronde omtrek, bij beide uiteinden een zichtbare bocht, eindigt in een krulletje in het midden; max 2
  windingen, lijnen in de schaduwtint, niet in bijna-zwart; (c) volume als cilinder: lichtband boven, donker onder, de
  voorkant (zuignappenvlak) een tint donkerder dan de zijkant zodat je twee vlakken ziet; (d) de verre (linker) band kleiner,
  in schaduwtint en gerust half achter kanonmond/nabije band verstopt, zoals Jordi zelf voorstelde; (e) de zuignapringen
  (`oYo/YdY/oYo`, x10–12 en x36–38) staan nu als drie identieke ruitjes strak onder elkaar: 2 ringen, licht verspringend met
  de kromming mee, of 3 kleinere open ringetjes.
- Onderrand y59–62: de dubbele zwarte trap ((9–20,60–61), (25–29,59), (35–46,61–62), (51–59,59–60)) wordt één vloeiende 1 px-curve.

**2. Tentakels zijn palen (checklist A6: evenwijdige randen > 6 px).**
- Achterste linker tentakel x19–23, y26–40: 15 rijen kaarsrecht (`KPdd#` / `Kdd#`).
- Kanontentakel links, rechterrand x=17, y31–42: 12 rijen recht.
- Rechter tentakel x53–58, y28–36: 9 rijen identiek `KPPR#`/`KPPd#`; daaronder nog 4.
- Opdracht: elk een S-bocht zoals in het model (dik aan de voet, taps naar de punt, de punt krult). Per rij 0–1 px verspringen
  in vloeiende reeksen (3-2-1-1-2-3), geen trapjes.

**3. Te veel bijna-zwart, geen echte selout.**
- Lijntint `(72,16,30)` vervangen door een echte donkerrode selout (richting L45–55, bv. rond `(110,24,36)`), zwart alleen
  aan de schaduwkant (rechts/onder).
- Binnenlijnen op verlichte vlakken (mantelbanden y14–25, vinvouw x=48, spiraal) in de schaduwtint `(130,38,56)`-achtig, niet in lijntint.
- De strook tussen de linker tentakels (x17–24, y26–42) is een tralie van 2 px brede donkere stroken (`#.K`, `##`, `K#`):
  terug naar 1 px, of de spleet openmaken tot achtergrond.
- Doel: aandeel L<50 van 0,30 naar ≤ 0,20.

**4. Palet te donker en dof.**
- Hele roodtrap ±25–30 helderheid omhoog en verzadigder/warmer (basis richting L120–130, S ≥ 0,75), schaduwtint mag wijnrood
  blijven zodat het karakter van het model overeind blijft. Glans `(234,136,136)` is nu pastelroze: warmer.
- Dit is een tintkeuze die het model raakt (model is donker wijnrood): leg twee paletproeven naast elkaar aan Jordi voor
  in plaats van zelf te kiezen.

**5. Linkeroog (x22–26, y35–39).**
- Nu: zwart kader met een zwarte verticale balk en losse gele pixels eromheen ((23,36) (23,37) (25,37) (23,38) (25,38)); leest
  als getralied raampje. Model: zelfde boze amandel als rechts, smaller en deels achter de tentakel.
- Opdracht: als smallere versie van het rechteroog tekenen (schuine bovenrand als wenkbrauw, geel vlak aaneengesloten ≥ 3 px,
  pupil als spleet aan de neuskant), of het grootste deel achter de tentakel laten verdwijnen. Geen losse gele pixels.

**6. Kanonmond (x19–33, y41–49).**
- Boring is een vierkant blok zwart (x23–26, y44–47, 4×4 met 1 hoekpixel eraf): rond maken (ovaal, 1 px binnenrand in donkerrood
  aan de lichtkant zoals het model).
- De loop met ribbels is teruggebracht tot losse verticale streepjes (x27/28, x31, x33, y41–48): 2–3 duidelijke ringen die met
  de ronding meebuigen.
- **Kleur wijkt af van het model**: ring en loop zijn grijsroze `(204,136,140)`/`(142,70,84)`; in het model zijn de kanonnen
  lijfrood met een lichtere rand. Geldt ook voor kanon links en rechts. Dit is iets verzonnen; terug naar rood, of expliciet als
  "voorstel" aan Jordi voorleggen (het helpt de Steel-lezing, maar het is niet zijn model).
- Onderrand van de ring valt samen met de bovenrand van de rupsband (x20–25, y50): bij het hertekenen van 1 overlap duidelijk
  maken (kanon vóór de band).

**7. Kleine lijnfouten.**
- Wenkbrauw rechteroog: zwart blok 2 px dik (x37–40, y34–35 en x35–37, y36): 1 px.
- Boring rechterkanon x45–49, y29–31: rechthoek; afronden.
- Vinvouw x=48, y9–19: 11 rijen loodrecht; in het model loopt hij schuin mee met de mantel.
- Zwarte inham bij de linker onderpunt (x4–5, y48–49 `##` binnen de tentakel): weg of dichtmaken.
- Rechter kanon zit als ring tegen de kop geplakt; 1–2 px loop naar achteren (zoals links) zodat het een kanon op een tentakel is.

**8. Zuignappen op de rand.**
- De 17 bruine randpixels hierboven krijgen een omlijning of schuiven 1 px naar binnen. Een paar noppen minder mag
  (rechts x52–60, y25–34 staan er vijf dicht op elkaar: ruis op 1×).

## 4. Trouw aan het model
- Aanwezig en op de juiste plek: mantel, vin, twee ogen, kanonmond, twee kanontentakels, tentakels, twee rupsbanden, gele noppen.
- Afwijkend: rupsbanden (plat/hoekig, geen spiraal, geen ver/nabij), tentakels recht in plaats van gebogen, kanonnen grijsroze
  in plaats van rood, ribbelloop van de mond vrijwel weg.
- Plaknaden uit het model zijn niet overgenomen: goed.

## 5. Conclusie
Nee, niet naar Jordi. De bovenhelft is op niveau; de onderhelft niet, en juist daar ligt zijn nadruk. Reparaties 1–3 zijn
de voorwaarde (rupsbanden, tentakelbochten, lijnwerk); 4 en 6 hebben een keuze van Jordi nodig (palet, kanonkleur);
5, 7 en 8 zijn afwerking. Mantel, vin, rechteroog en linkerkanon bevriezen (diff 0). Daarna opnieuw laten keuren door een
verse keurder, met dezelfde hoofdvraag.

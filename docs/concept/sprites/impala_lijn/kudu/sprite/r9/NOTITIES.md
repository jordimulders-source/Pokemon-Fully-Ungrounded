# Kudu sprite ronde 9: manen links kleiner (maker)
Jordi over r8 (letterlijk): "de vorm klopt niet, gezien het links veel meer eroverheen loopt dan rechts, daarom houd je ook bijna geen ruimte over. Links is het zelfs helemaal 1 geworden met de poot, wat een prutswerk weer".
Scripts: `sprite/r9lib.py` (snede, borsttinten, klasse `Vorm9`), `sprite/r9.py` (6 varianten), `sprite/vel9.py` (pngs, keuzevel, telling, bronnen). Basis = r8-methode (`r8/NOTITIES.md`). Oog K4.

## Keuzes voor Jordi (`vel.png`)
- **Vorm:** de onderrand van de manen aan de borstkant ligt **3, 6 of 9 px hoger** dan nu (de kolommen). De snede is een lijn door (12, 44−N) en (24, 42) in rastercoördinaten. Aan de schouderkant (rechts) blijven de manen zoals in r8; ze vallen dus vooral over de schouder.
- **Manier:** **A** = pluizige kraag met puntjes (Arcanine); **B** = lang hangend kapsel met gerafelde onderrand (de rijen).

## Wat er vrijkomt
- **Borst en hals:** de haarpixels onder de snede worden lijf. Het lijf krijgt de bestaande lijftinten. Het volume komt uit model A3: de helderheid per cel, over ±1 cel gemiddeld, want de haarstrengen in het model zijn geen lijfvolume. Het lichtste kwart wordt L, de rest M. L-vlakjes kleiner dan 3 px worden M.
- **Buitenrand:** waar de borst aan de achtergrond grenst, krijgt hij een zwarte buitenlijn (0), net als de rest van het lijf.
- **Los van het lijf:** direct onder de manenrand wordt de borst 1 px D, als slagschaduw. Dat doen Arcanine en Growlithe ook naast hun kraag; zo zitten de manen los.
- **Onderrand van de manen:** opnieuw gerafeld met de punt van de Arcanine-borstkraag (19,47)-(23,51). Die punt staat telkens op de nieuwe onderrand en steekt 1 px uit. Waar nog een recht stuk zat, is automatisch de kleine Arcanine-bult (54,17)-(58,20) geplaatst, op de plek die het rechte stuk het beste breekt.
- **Oude stukken:** stukken uit r8 die in de vrijgekomen borst zouden vallen, zijn weggelaten.
- **Per pixel:** de bron staat in `bronnen.txt`.

## Controle (`telling.txt`, alle 6)
- 0 px anders buiten de manen + vrijgekomen zone; oogvlak (K4) 0 px; halsstrook 0 px.
- Geen rechte manenlijnen > 3 px.
- De voorpoot raakt de manen nergens: de kleinste afstand is 4 px (N=3), 5 px (N=6) en 6 px (N=9). Daartussen ligt borst (32–91 px).
- Zelf gekeken op 8× en 1×:
  - **N=3:** de borst is maar een smalle strook en links blijft het nog zwaar.
  - **N=6:** borst en de bovenkant van de poot zijn duidelijk; links en rechts zijn het meest in balans.
  - **N=9:** de manen liggen bijna alleen nog over de hals en de schouder; onder de kaak blijft een klein stukje keelfranje over.

## Zwakke punten
- **Borst:** er zit geen borst in het model, want daar staat de manen. De lijfhelderheid komt dus van de haarlaag, gemiddeld. De borst is daardoor vrij vlak M, met een lichte voorrand.
- **Buitenrand borst:** bij N=9 loopt hij 4 px recht (x9, y37–40). Dat is de oude franjeomtrek; geen manenlijn, wel een recht stuk.
- **Voorpoot:** krijgt geen extra binnenlijn. Hij is los door de tint (D tegen M) en door zijn eigen buitenlijn.

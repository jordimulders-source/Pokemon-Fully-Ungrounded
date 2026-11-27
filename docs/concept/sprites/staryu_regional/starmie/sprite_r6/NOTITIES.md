# Regionale Starmie, frontsprite ronde 6 (voorpunten minder puntig)

Jordi na r5: "de punten van de voorkant moeten ook minder puntig van starmie". Aanvulling: "meet desnoods de hoek van de originele starmie sprite op deze twee" (uitsnede `../../referenties/jordi_starmie_punten.png`: de lichte punt naar rechts en de donkere punt naar rechtsonder van de Gen 3 Starmie).

Bestanden:
- `starmie_r6_licht.png`: basis r5_licht. De vijf voorpunten zijn afgesneden waar de punt 4 px breed is (zoals de achterpunten in r5).
- `starmie_r6_sterk.png`: basis r5_sterk. Snede bij 5 px.
- `starmie_r6_jordi.png`: basis r5 zonder afstompen. Alle tien punten (voor en achter) zijn afgestompt naar de twee Gen 3-punten van Jordi.
- `vel.png`:
  - 8×: r6 licht | r6 sterk | r6 jordi | r5 licht | model r4 | Gen 3.
  - 12×: Gen 3 rl | Gen 3 br | r6 jordi voorste ster rechts | r6 jordi achterpunt rechtsonder.
  - 1× op wit en donker, plus maatstaf-sprites.
  - 2×.
- `bouw.py`: `python3 sprite_r6/bouw.py licht|sterk|jordi` (vanuit `starmie/`), met logs `log_*.txt`.
- `gereedschap/g3punten.py`: meting van de Gen 3-punten (`log_g3punten.txt`).
- `gereedschap/vel6.py`.

## Regels (alle drie)
- **Alleen weghalen**, binnen het modelsilhouet. Er komt nergens een pixel bij.
- **Buitenlijn opnieuw zoals r5:** rand rechts/onder zwart, links/boven donkerbruine selout. Losse zwarte pixels worden donkerbruin.
- **Koekrand:** een glazuurpixel die direct achter een nieuwe buitenlijnpixel komt, krijgt de koektint van de dichtstbijzijnde modelrand.
- **Glazuur, zigzag, hagelslag en juweel:** 0 px veranderd. Script-bewijs: diff buiten de punten = 0.
- **Uitsteeksels:** een 1-px uitsteeksel na de snede (een pixel met hooguit 1 buur) gaat weg. Zo'n uitsteeksel ontstaat doordat de snede schuin over het raster loopt. Twee gevallen:
  - (31,4) bovenop de voorste bovenpunt;
  - (43,9): in r5 al een los uitsteeksel op de achterpunt rechtsboven. Daardoor verschillen licht en sterk 2 px van r5 in de achterpunten: (43,9) is weg en (43,10) is nu buitenlijn.

## licht / sterk: voorpunten

Snede loodrecht op de as juweelmidden → modeltip, op de eerste plek waar de punt W px breed is (`stomp.py` r5).

| voorpunt | licht weg | licht breedte 1/2 px van de tip | sterk weg | sterk breedte 1/2 px |
|---|---|---|---|---|
| boven | 6 + 1 uitsteeksel | 5,0 / 6,0 | 10 | 5,0 / 6,0 |
| links | 3 | 4,2 / 5,1 | 8 | 5,1 / 6,1 |
| rechts | 3 | 4,2 / 5,1 | 8 | 5,1 / 6,1 |
| linksonder | 6 | 4,6 / 6,0 | 9 | 6,0 / 6,0 |
| rechtsonder | 5 | 4,6 / 6,8 | 7 | 5,5 / 7,7 |

- Koekrand naar binnen: 0 px. Nergens kwam glazuur aan de nieuwe rand.
- Figuur: licht 53×51 (1727 px), sterk 51×50 (1690 px).

## Gen 3: de twee punten van Jordi (`g3punten.py`)

Breedte per schijf van 1 px loodrecht op de as kern → tip, inclusief de buitenlijn:

| punt | richting | lengte vanaf kern | schijf 0 | 1 | 2 | 3 | 4 | 5 | 6 | 8 | tiphoek (puntmaat r5) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rl, licht, naar rechts | −7° | 28,2 | 4,1 | 4,1 | 5,1 | 6,1 | 7,1 | 7,1 | 9,1 | 10,1 | ±28° |
| br, donker, naar rechtsonder | −37° | 28,9 | 3,8 | 5,2 | 4,6 | 6,6 | 7,4 | 6,0 | 8,0 | 8,2 | ±39° |

- **Tipvorm:** beide eindigen in een **plat eind van ±4 px loodrecht op de as**.
  - rl: verticaal vlak van 3 px plus een hoekpixel.
  - br: de hoek is afgeknot, met 3 px verticaal en 3 px horizontaal; dat is een schuine snede loodrecht op de −37°-as.
- **Verloop:** daarna wordt de punt ±1 px breder per px (4 → 5 → 6 → 7).
- **Voet:** de breedte op 8 px van de tip is 8–10. De lengte is ±2× de voetbreedte.

## jordi: alle tien punten naar die maten
1. Snede waar de punt 4 px breed is (het platte eind van ±4 px).
2. Tipvorm: per schijf langs de eigen hartlijn van de punt (midden op 6 px → midden van het platte eind) mag de punt hooguit het Gen 3-doel breed zijn: 4,5 / 5,1 / 5,4 / 6,9 op 0/1/2/3 px. Dat is het gemiddelde van rl en br (4,0/4,6/4,9/6,4) + 0,5. Wat breder is, gaat weg als randpixel, van buiten naar binnen.
3. Een weggehaalde pixel die een kerf of haak in de rand zou maken, komt terug als modelpixel.

| punt | weg (snede + tipvorm + uitsteeksel) | breedte na, 0/1/2/3 px |
|---|---|---|
| voor boven | 6+4+1 = 11 | 4,0 / 4,0 / 6,0 / 7,0 |
| voor links | 3+5 = 8 | 3,2 / 4,2 / 4,2 / 5,4 |
| voor rechts | 3+2 = 5 | 3,2 / 4,2 / 5,1 / 8,3 |
| voor linksonder | 6+9+2 = 17 | 2,4 / 3,8 / 4,6 / 6,8 |
| voor rechtsonder | 5+3 = 8 | 4,6 / 4,6 / 6,8 / 9,1 |
| achter linksboven | 6+8+1 = 15 | 2,4 / 3,8 / 4,6 / 7,4 |
| achter rechtsboven | 6+4 = 10 | 3,2 / 5,2 / 6,0 / 6,8 |
| achter linksonder | 6+1+1 = 8 | 3,2 / 5,5 / 6,8 / 8,6 |
| achter rechtsonder | 4+3+1 = 8 | 3,2 / 4,6 / 5,5 / 7,7 |
| achter onder | 4+5 = 9 | 4,1 / 4,1 / 5,1 / 7,1 |

- De breedtes zijn gemeten langs de straal uit de kern. Bij schuine punten (voor rechts, linksonder) wijkt dat af van de hartlijn, waardoor de waarden op 0 px kleiner lijken (2,4–3,2) dan het eind echt is.
- Koekrand naar binnen: 4 px, alle bij de voorste bovenpunt: (29,8), (30,8), (28,9), (29,9).
- Figuur 53×51 (1679 px). Diff t.o.v. r5: 162 px, waarvan 80 in de achterpunten.

## Controle
Alle drie:
- 64×64, mode P, index 0 transparant, 16 kleuren;
- geen lichte buitenrand, geen losse zwarte pixels;
- diff buiten de punten = 0.

## Twijfels
1. **De voorpunt rechts** heeft in het model een dunne, rafelige bovenrand (rij 21). Die staat in alle versies zoals in r5.
2. **jordi, onderste achterpunt:** die leest nog een tikje spits (de schijven 4,1/4,1 komen wel overeen met de Gen 3).
3. **jordi gaat bij een paar punten verder dan de Gen 3**, omdat het model daar smaller is: voor linksonder en achter linksboven zijn op 0–2 px smaller dan het doel. Er wordt niets bijgezet, dus de punten blijven daar smaller.

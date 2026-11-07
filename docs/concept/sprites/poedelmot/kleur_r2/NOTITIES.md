# Poedelmot: kleur r2 (maker)

Jordi (letterlijk, 6 nov): "Dit is precies het design in de pose die ik wil in de game, maak hier een sprite van, zo true to form als mogelijk" · "hij is bijna perfect, maar hij heeft teveel poten toegevoegd. Pak anders deze, met de voelsprieten van de andere".
Nieuw (via de coördinator): "ga je werk heel kritisch keuren voordat je het als af bestempelt, moet echt heel erg lijken op het model, anders is die niet goed". r1 is afgekeurd (te weinig gelijkend, blokkig); r1 staat ongewijzigd in `kleur_r1/`.

## Bestanden
- `raster.txt` (bron, 64×64, één teken per index: `.` 0, `1`–`9`, `A`–`C`), `palet.py` → `poedelmot.png` (geïndexeerd, index 0 transparant) + `normal.pal` (JASC, 16 kleuren, veelvouden van 8, 13–15 ongebruikt).
- `vel.py` → `vel.png`: r2 | r1 | bron op 8×, r2 op 1×/2× licht en donker, en close-ups (12×) van ogen/gezicht, sprieten, pootjes en vleugels, r2 naast de bron.
- `controle.py` → `controle_uitvoer.txt` (leest `spriet_zone.txt` en `klauw_rand.txt` naast het raster).
- `stappen/`: de bouwvolgorde (`bouw.sh`): onderlegger → kop/ogen → sprieten → opschonen → vleugels → onderkant → verre vleugel → opschonen → reparaties → buitenlijn. Alleen naslag.

## Werkwijze r2
- **Onderlegger**: per pixel de dichtstbijzijnde paletkleur bij `gids_gemiddeld.png` (`stappen/onderlegger.py`), zoals de coördinator vroeg. Dat is een script; daarna is vrijwel elk onderdeel met de hand op een close-up van de bron hertekend. Opschonen van clusters < 3 px gebeurde met een kleine stap (de pixel krijgt de meest voorkomende vlaktint van zijn buren; gezicht en randpixels uitgezonderd), daarna nagewerkt.
- **Palet** naar de echte bronkleuren (k-means op de gids): koeler en neutraler bruin dan r1; aparte koele grijsroze schaduw (`8`, `C`) voor vacht en pluimen, warm crème/tan (`7`, `6`, `5`) voor de vleugels.
- **Ogen** (fout 1): twee grote schuine amandelogen, met de hand op de bron getekend. Bijna zwart (`1`) met een zwartbruine rand (`2`), witte glans linksboven (4 px nabij, 3 px ver), zwakke grijze reflectie onderaan, een tan rand (`6`) en een donkere lijn (`4`) rond het nabije oog. Nabij: x25–33, y32–40. Ver: x14–20, y32–40, dus 7 px tegen 9. NB: in de bron zelf is het verre oog maar ±3,5 px breed. Ik heb de opdracht gevolgd ("hoogstens 1 px smaller"), het is nu 2 px smaller dan het nabije oog (rand meegeteld).
- **Masker** (fout 2): glad crème vlak (`9`/`A`) tussen en onder de ogen, tan snuit (`7`) en een donkere boog onder de snuit (`3`, taps in `4`). Daaronder de witte kraag.
- **Sprieten** (fout 3): vlak bijna zwart (`1`). De nerf is een doorlopende dunne curve van basis tot tip (`6`, met de hand als pixellijst). De baarden zijn fijne schuine streepjes van 1 px breed (`4`, onderaan `3`, vast patroon `(x − y//2) mod 4`). Boven de nerf staan subtiele kammetjes (`3`).
- **Pootjes** (fout 4): zes pluimen zoals in de bron (A, B, onderpluim B2, C, D, E achter), als ovalen op de bron gemeten. Lichte kern, koele schaduw `8`/`C` onderaan, donkerbruine spleten (`2`/`3`) tussen de pluimen. Achterlijfplaten in tan, kleine bruine klauwtjes (4 groepjes). Geen extra poten.
- **Vleugels** (fout 5): de voorvleugel heeft een witte voorrand met een donkere lijn naar de kop, een grote C-krul, golven, boogjes per lob en een witte geschulpte onderrand. Daaronder één doorlopende scheidingslijn, zonder inkeping. De achtervleugel heeft een tan basis, een ronde krul, een schubboog en schulpen. De verre vleugel links is crème met tan schubjes en een geschulpte rand.
- **Omlijning** (fout 6): buitenlijn donkerbruin (`2`) aan de schaduwkant, selout `4` aan de lichtkant. Zwart (`1`) alleen in ogen en sprieten. Binnenlijnen alleen tussen vormen, in `3`/`2`.
- **Vacht** (fout 7): een paar boogvormige plukjes (`7`) op de borst/kraag, geen ruis.

## Controle (`python3 controle.py`)
- **Alpha-diff met silhouet: 0** (1782 = 1782 px). Geen randpixel veranderd.
- Open randen: 0. Bewuste uitzondering: de klauwtjes/voetjes op (19,56), (25,57), (25,58) en (44,59) zijn bruin `4` op de buitenrand.
- Selout `4` op de buitenrand: 7 reeksen, geen afwisseling met donker binnen één rand. De drie korte reeksen zijn de klauwtjes.
- Losse pixels: 0. Tintclusters < 3 px: 0. Dat geldt voor de vlaktinten 5–9, A en C; 1–4 tellen als lijn- en detailkleuren (lijnen, contouren, klauwtjes, sprietbaarden). Sprietzone en oogglans zijn uitgezonderd.

## Eerlijke zwakke punten (wat ik nog anders zie dan de bron)
- **Verre oog**: breder dan in de bron (zie hierboven, bewust volgens de opdracht). Daardoor kijkt het gezicht frontaler dan Jordi's driekwart-kop.
- **Kopvorm**: de bron heeft een duidelijk ronde witte koepel met een donkere wangrand. Hier lopen kop, kraag en verre vleugel nog deels in elkaar over; de koepelrand bovenaan is alleen zichtbaar via de spriet-basis.
- **Pootjes**: rond en los, maar korter en ronder dan de hangende, ovale pluimen van de bron. Het silhouet laat de onderkant niet lager toe. Het achterlijf tussen B en D oogt iets zwaarder/bruiner dan in de bron.
- **Vleugelpatroon**: zachter dan r1, maar de krullen blijven grover dan Jordi's fijne schubtekening. De dither van de bron (vleugelbasis) is weggelaten.
- **Sprieten**: donker met nerf en baarden zoals de bron. De baarden staan om de 4 px; in de bron zijn ze fijner dan een pixel. De tips volgen het (bevroren) silhouet en zijn daardoor niet spitser te maken.
- **Werkwijze**: onderlegger, sprietbaarden, ovale pluimvormen en de opschoonstap zijn met scripts gezet (op mijn ontwerp of op de gids), daarna met de hand nagewerkt. Puur handwerk is het dus niet.

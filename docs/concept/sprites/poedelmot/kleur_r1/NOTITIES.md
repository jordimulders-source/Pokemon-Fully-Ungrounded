# Poedelmot: kleur r1 (maker)

Jordi (letterlijk, 6 nov): "Dit is precies het design in de pose die ik wil in de game, maak hier een sprite van, zo true to form als mogelijk" · "hij is bijna perfect, maar hij heeft teveel poten toegevoegd. Pak anders deze, met de voelsprieten van de andere".
Bron: `referenties/jordi_2_lijf.png` (lijf, vleugels, kop, ogen, pootjes) + sprieten van `jordi_1_voelsprieten.png`, vergeleken op `samengesteld.png`. Silhouet: `silhouet/silhouet.png` (bevroren).

## Bestanden
- `raster.txt`: 64×64 tekstraster, één teken per paletindex (`.` = 0 transparant, `1`–`9`, `A`). Dit is de bron.
- `palet.py`: palet + raster → `poedelmot.png` (geïndexeerd, index 0 transparant) en `normal.pal` (JASC, 16 kleuren, alle waarden veelvouden van 8; 11–15 ongebruikt/zwart).
- `vel.py` → `vel.png`: sprite 8× naast de samengestelde bron (zelfde uitsnede en schaal als `sil.py`), plus 1× en 2× op licht/donker/wit/groen.
- `controle.py` → `controle_uitvoer.txt`.
- `stappen/`: hoe het raster ontstond (handgeschreven rijsegmenten `rows.py`, pixelbewerkingen `edits.py`/`make.py`, daarna hertekenstappen `s_*.py` via `schoon.py`). Niet nodig om te bouwen; alleen naslag.

## Werkwijze
- Studie op 6×: Venomoth, Dustox, Masquerain, Beautifly (vleugels, dither, belijning), Swablu en Altaria (witte vacht: stappen van ±16–30 in helderheid, gekleurde selout), Venonat (pluizige vacht), Butterfree (twee grote ogen in 3/4).
- **Ogen**: het nabije oog is het rechteroog van Butterfree (`graphics/pokemon/butterfree/anim_front_gba.png`, x 23–30, y 27–36) pixel voor pixel overgenomen, gespiegeld (zodat het onder naar links helt zoals bij Jordi), rij 31 en 34 weggelaten (8 rijen hoog), omgekleurd naar zwart/donkerbruin; glans 3 px wit linksboven en een grijze reflectieboog rechtsonder zoals in de bron. Het verre oog volgt het smalle Butterfree-oog (4 breed), maar is meer met de hand aangepast.
- Kleur met de hand als tekstraster, gids alleen bekeken (niet gekwantiseerd). Eén uitzondering op "met de hand": de **sprietbaarden** zijn een vast ontworpen patroon (schuine traplijnen, helling 2, periode 7: `(2x − y) mod 7 ∈ {0,1,2}`, kleur 4 op 1) dat een script binnen de sprietvlakken op mijn eigen raster zette; korte stukjes aan rand/nerf zijn zwart gemaakt. Niet uit de gids afgeleid.
- Silhouet: **niets** aan de omtrek veranderd (ook geen dunne delen), alpha-diff 0.

## Palet (helderheid)
`1` zwartbruin 18 · `2` donkerbruin 52 (binnenkant oog) · `3` bruin 80 · `4` tanbruin 112 · `5` tan 151 · `6` crème-tan 192 · `7` crème 226 · `8` wit 247 · `9` grijs 113 (oogreflectie) · `A` selout 135.
Vacht: 8/7/6 (stappen 21 en 34, zoals Swablu/Altaria; Taillow's 30–40 geldt voor blauw). Licht linksboven; zwart aan de schaduwkant (rechts/onder), selout `A` aan de lichtkant.

## Controle (`python3 controle.py`)
- Pixels 1782 = silhouet 1782; **alpha-diff 0** (extra: geen, mist: geen).
- Open randen: 0. Bewuste uitzondering: het voetje onder pluim B, (25,58) en (25,59) in tanbruin `4` op de buitenrand (een voetje van 1 px breed kan geen eigen omlijning hebben).
- Selout op de buitenrand: 42 px in 4 aaneengesloten reeksen (kopplukje, verre vleugel boven, verre vleugel onder + borst links, voorvleugel boven); nergens A en zwart om en om. Tussen de twee A-reeksen links zit de donkere inkeping (10–12, 36) tussen verre vleugel en onderlob: dat is een vormgrens, geen afwisseling op één rand.
- Losse pixels: 0. Tintclusters < 3 px (4-samenhangend, tinten 3–8): 0, glans (28,35),(29,35),(28,36),(18,34) uitgezonderd.

## Eerlijke zwakke punten
- **Pootjes** zijn leesbaar als vier witte pluimen met voetjes plus de rechter pluim, maar blijven wat blokkig: platte onderkanten en rechte contourstukken (bovenkant C, onderkant B). Bij Jordi zijn het ronde, pluizige bollen met zwarte omtrek; ik gebruik bruin `3` als binnenlijn.
- **Vleugelpatroon**: de krullen moesten 4-samenhangend en ≥ 3 px zijn, dus ze zijn hoekiger ("C"/haakjes) dan Jordi's zachte schubkrullen; de fijne dither van de bron heb ik weggelaten.
- **Sprietbaarden** zijn grover (om de 3–4 px) dan de fijne veertjes van Jordi; de nerf van de linkerspriet ligt direct onder de bovenrand en leest daardoor ook als lichte bovenrand.
- **Vacht**: de borst heeft maar een paar plukstreken; de pluizige textuur van de bron is veel rijker. De kop is aan de linkerkant niet scherp van de verre vleugel gescheiden (alleen via tan schaduw), net als in de bron, maar op 8× vloeit het wit wat in elkaar over.
- **Schaduwtint** is overal warm crème-tan; bij Jordi hebben de pootpluimen een iets koelere, grijsroze schaduw.
- Het verre oog is klein (4 × 7) en meer handwerk dan overgenomen.

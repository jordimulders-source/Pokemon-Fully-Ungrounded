# Gaucho-Lombre r3: ogen naar de Lombre-artwork (maker, 25 nov)

Jordi: "ah excuses die sprite helpt niet, hier zie je hoe lombre er uit ziet" (referenties `../../referenties/lombre_artwork.png`, `lombre_anime.png`, `lombre_3d.png`); zijn eis blijft: "het linkeroog valt nu teveel weg en is het rechteroog nog net niet genoeg lombre maar dan bozer".

Wat de referenties tonen (zelf bekeken): een rond wit oog met een zwarte omtrek, waarvan de bovenkant is afgedekt door een rechte, dikke zwarte ooglidlijn. Daardoor is het zichtbare wit de onderhelft. Een kleine zwarte pupil zit direct onder het lid. Beide ogen zien er zo uit. Op de artwork loopt het lid licht schuin.

## Basis en bestanden
- Basis = `../r2/lombre_gaucho_r2_B.png`. Het hoofd (r2) en mond A5 blijven precies zo.
- `lombre_gaucho_r3_A/B/C.png`: 64×64, P, index 0 transparant, 14 kleuren incl. transparant.
- Verschil met r2 B: A 16 px, B 16 px, C 17 px, **allemaal in de oogvakken** (nabij x29–34, y25–28; ver x21–22, y24–26). Daarbuiten 0 px (gecontroleerd in `bouw.py`).
- `pixels.txt`: elke pixel oud → nieuw. `bouw.py`: de ogen als tekstraster.
- `vel.png`: kop 12× (r2 B | r3 A | B | C | model | artwork-kop gespiegeld); A/B/C geheel 8×; 1× (en 2×) op wit en donker.

## Ogen (getekend naar de artwork, niet uit het model of een sprite; alle pixels in de vakken zijn dus nieuw)
Legenda: K zwart, W wit, L rood lijn (onderrand van het oog als binnenlijn, niet zwart), F gezicht (rood midden).
- **Ver oog (gelijk in A/B/C), x21–22, y24–26:** rij 24 `K K` (lid), rij 25 `W K` (pupil rechts tegen het lid, naar de kijker), rij 26 `W W`. Er zit 3 px wit onder het lid. De kopomtrek ernaast (x20) blijft rood lijn, zodat het oog niet in zwart opgaat.
- **Nabij oog**, x29–34, y25–28. De zwarte rand op x35 (rijen 25–26, uit het model) sluit het lid achteraan af.
  - **A**, lid bijna vlak (1 trede omlaag naar de snuit), pupil midden onder het lid:
    `F F K K K K` / `L K W K W W` / `L W W W W L` / `F L W W L F`
  - **B**, lid duidelijk schuin (3 treden naar de snuit, bozer), pupil direct onder het lid:
    `F F F F K K` / `F L K K W W` / `L K W K W L` / `F L W W L F`
  - **C**, lid als A, maar de pupil vooraan tegen het lid (naar de snuit), zoals de linkerpupil op de artwork:
    `F F K K K K` / `L K K W W W` / `L W W W W L` / `F L W W L F`

## Zwakke punten (eerlijk)
1. Op 4 rijen is het oog klein. De ronde onderkant is 2 px wit met rood lijn ernaast, dus op 1× leest hij eerder als een halve maan dan als een rond oog.
2. In C smelt de pupil vooraan visueel samen met het lid tot een dikkere lidpunt.
3. Het verre oog is maar 2 px breed. Lid en pupil vormen samen een zwart haakje, en het wit (3 px) zit links ervan tegen de omtrek.
4. Er is nog geen keurder en geen DC-eindkeuring gedaan.

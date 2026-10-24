# Olinguito v2: schets (24 okt)

Nieuwe start na het schrappen van het oude ontwerp (zie `../olinguito/` en `docs/lessen/RETRO_OLINGUITO.md`). Eerst schetsen, geen pixels.

**Jordi (24 okt, letterlijk):** "we gaan er meer een olinguito van maken. [...] Het is best een sinister diertje, zie de ogen, de snuit die we ietsje langer maken, de staart is een belangrijk kenmerk. Het grootste verschil met de echte olinguito wordt een langere neus en 2 langere klauwen, zoals sandslash. De foto in de boom komt in de buurt van de pose die ik wil. Deze linoone sprite ook, eigenlijk zijn linoones klauwen bij nader inzien nog passender. We doen een donkerder masker om de ogen heen en een goede donkerbruine tint. [...] Ik twijfel wel nog of we de staart naar boven moeten doen of naar beneden. [...] ik vind de foto in de boom eigenlijk veel beter dan mijn schets."

Referenties in deze map: `referentie_foto_voor.png`, `referentie_foto_boom.webp` (pose), `referentie_halliday.webp`, `referentie_linoone.png` (pose + klauwen), `schets_jordi.png`.

Ronde 1 (`schetsen_v1.png`; script in de git-geschiedenis):
- Pose: kop omlaag naar links, rug als boog omhoog naar de romp (boomfoto + Linoone).
- Olinguito-kenmerken: ronde kop, kleine ronde oren, donkerbruine vacht, goudbruine keel/buik, lange dikke staart.
- Afwijkend: iets langere snuit, donker masker rond beide ogen, 2 lange lichte klauwen per voorpoot (Linoone).
- Sinister: roodbruine ogen in het masker onder een zware wenkbrauw.
- Jordi koos staart omhoog (A).

## Ronde 2 (`schetsen_v2_ronde2.png`)
**Jordi (24 okt, letterlijk):** "ja de staart moet wel dunner, zoals bij de olinguito. ER komt maar 1 oog in beeld in deze pose, net als bij linoone, en net als op de fotos moet 1 oor dominant zijn en de tweede nauwelijks zichtbaar. Het mag nog iets meer op een olinguito lijken zoals op de fotos en wat minder op een wasbeer. Misschien een optie om de neus toch in te korten en pas bij de coati evolutie te vergroten. De klauwen mogen ook iets minder, iets meer linoone. en de poten mogen iets dynamischer zoals op de foto van de olinguito die hangtn in de boom, met zijn achterpoten wat meer naar voren, indien dat fysiologisch een beetje klopt" + "het vlak op de buik hoeft ook niet, dat is een fout in mijn schets".
- Profiel: één oog, één dominant oor (het verre oor is een randje boven de schedel).
- Dunnere staart omhoog; kortere snuit (langere snuit pas bij de coati).
- Minder wasbeer: geen maskerband, alleen zacht donker rond het oog; grijzig bruine kop zoals op de foto's.
- Kortere, Linoone-achtige klauwen (2 per voorpoot).
- Achterpoten onder het lijf naar voren (knie naar voren, voet onder de buik: zoals een klimmer die zich verzamelt).
- Geen buikvlak meer; alleen de kin/keel goudbruin.

## Ronde 3 (`schetsen_v2_ronde3.png`)
**Jordi (24 okt, letterlijk):** "maak het hoofd nog wat ronder, de staart moet langer, zoals op de fotos en de poten moeten dynamischer, zoals op de foto, ze zijn te symmetrisch"
- Kop: schedel als bijna-cirkel.
- Staart: ±1,6× zo lang, omhoog en in een boog terug over de rug.
- Poten asymmetrisch (boomfoto): verre voorpoot ver gestrekt en grijpend, nabije voorpoot opgetild en gebogen; nabije achterpoot opgetrokken (knie hoog, voet onder de buik), verre achterpoot gestrekt naar achteren (zet zich af).

## Ronde 4 (`schetsen_v2_ronde4.png`)
**Jordi (24 okt, letterlijk):** "het oog moet ook veel kleiner, zie de fotos, plus in pokemon sprites kijken ze altijd diagonaal, dus dat moeten we ook nog iets meer creeren" + "het oor mag iets groter".
- Oog ±half zo groot (klein roodbruin kraaloog met glans en zware wenkbrauw, zacht donker vlak eromheen).
- Kop in 3/4 naar de kijker: de snuit komt uit het midden van het gezicht (verre wang zichtbaar links ervan), kop en snuit als één vorm met een korte lijn voor de snuitrug.
- Nabij oor ±25% groter; het verre oor blijft een randje.

## Ronde 5 (`schetsen_v2_ronde5.png`, afgekeurd)
**Jordi (24 okt, letterlijk):** "pak nog wat meer de vorm van dit hoofd" (foto: `referentie_kop.png`).
- Kop als druppel: brede ronde schedel achter-boven, loopt glad af naar een spitse snuit met lichtgrijze punt en roze neus.
- Kleur zoals de foto: warmbruine kruin, grijs gezicht, donkere streep van het voorhoofd langs het oog naar de snuitrug.
- Oor: donkere rand, lichtere binnenkant, hoog achter op de kop.
Jordi: "kijk goed naar de foto, dit is niet dezelfde vorm". Les: een kop niet 'in de geest van' een foto tekenen, maar de omtrek overtrekken (raster over de foto, punten aflezen).

## Ronde 6 (`schetsen_v2_ronde6.png`, los `schets_v2_ronde6.png`; script `scripts/schets.py`)
**Jordi (24 okt, letterlijk):** "kijk goed naar de foto, dit is niet dezelfde vorm" + (foto's van de poten, olinguito's in bomen) "en hier ter referentie de poten" "zitten wat verder naar voren voor mn gevoel met een iets kleiner lichaam".
- Kop overgetrokken van `referentie_kop.png` (`head_pts()` zet fotocoördinaten om naar het canvas, 12° gedraaid zodat de neus iets naar links wijst): neus recht omlaag, het oog laag bij de snuit, een hoog rond voorhoofd en het oor bovenop de kop, naar voren gericht. De warme kruin loopt door in de nek.
- Kleiner, gebold lijf; ronde dij als deel van de romp.
- Poten verder naar voren: achtervoeten onder de buik vlak achter de voorpoten (zoals op de boomfoto's), dikke schouder, roze voeten.
- De foto's van de poten en de olinguito's in de bomen kwamen alleen in de chat binnen, niet als bestand (niet in deze map).

# Salticonda – silhouet ronde 2 (vanaf variant A)

Jordi (letterlijk): "ik vind de slangenkop juist wel oke, gezien we de sandaconda neus een beetje na gaan doen. De pose van A vind ik wel vrij aardig, alleen ik vraag me af of die echt bulky en imposant genoeg is, echt als een zoutkegel"

Vel: `vel.png`. Varianten: `variant_D.png`, `variant_E.png` (+ `_raster.txt`). Scripts: `../scripts/silhouet2.py` (bouw), `../scripts/check2.py` (losse pixels, gaatjes, horizontale randstukken), `../scripts/kopbewijs2.py` (kop bevroren), `../scripts/vel_silhouet2.py` (vel).

## Kop bevroren (bewijs)
`python3 scripts/kopbewijs2.py`:
- de kopvorm uit ronde 1 (303 px, `HEAD` in `silhouet1.py`) zit volledig in A op (9,11) en in D en E op (9,6);
- het vrije deel van de kop boven de kegel is gelijk aan A, verschoven met (0,−5): **0 px verschil** voor D en E.

De kop is dus alleen 5 px omhoog geschoven, niet herschaald of hertekend.

## Opbouw (beide varianten)
- **Eén doorlopende kegel:** de halve breedte volgt een gladde curve (superellips, p = 1,45) van ±14 px onder de kop tot ±28 px aan de voet. De flanken lopen schuin en licht bol naar boven, met een afgeronde koepel onder de kop.
- **Windingen als spiraal:** elke winding bolt aan de rand iets uit (1,4–1,8 px). Onderaan is hij rond afgerond, want hij ligt óp de winding eronder, en daar zit een inkeping van ±3,5–4 px voor de pekelring. De gleuven liggen rechts 3–4 rijen hoger dan links. Zo loopt het als een opgerolde slang omhoog en zijn het geen losse treden.
- **Zware voet:** de breedste rij zit onderaan (rij 51–56), met daaronder een ronde boog naar de grond.
- **Staartspits rechtsonder**, zoals in A: komt onder de onderste winding vandaan en wijst naar rechtsboven, met een gleuf erboven.

## Varianten
| | D | E |
|---|---|---|
| Pixels | **2158** | **2131** |
| Kader (met staart) | 61 × 55 | 62 × 55 |
| Breedte van de voet (zonder staart) | 55 px | 56 px |
| Windingen | 4 | 3, dikker |
| A (ronde 1) ter vergelijking | 1697 px, 61 × 48 | |

Vergelijking: Hippowdon 2145, Camerupt 2295, Torkoal 2342, Wailord 2359, Sandaconda 1609, Silicobra-Uyuni 990. D = 2,18× en E = 2,15× de pre-evolutie.

## Controle (check2.py)
- Geen losse pixels, geen gaatjes.
- Flanken: geen horizontaal randstuk langer dan 4 px. Het enige stuk van 6 px is de bovenkant van de bevroren kuif (zo ook in A).
- **Grondlijn:** de onderste rij is 15 px recht, met daarboven aan beide kanten een trede van 9 px. Dat is de rondende onderkant van de voet op de grond. Ter vergelijking: Wailord 13, Hippowdon 22, in A was het 33 px.

## Eerlijk oordeel
- Beide lezen op 1× en 2× als één brede zoutkegel met een slangenkop bovenop. Ze zijn even zwaar als Hippowdon, waar A duidelijk kleiner was. In de overlay zie je dat de massa vooral onderin en aan de flanken is bijgekomen.
- De "pannenkoeken" zijn weg: de omtrek is één lijn met kleine, ronde uitstulpingen. De windingen lezen in het silhouet daardoor rustiger dan in A. Dat volgt uit Jordi's wens van één kegel. De turquoise pekelringen in de kleurronde maken ze daarna duidelijk.
- **D (4 windingen):** fijner, meer "stapel windingen". Van de twee is dit de meest letterlijke voortzetting van A.
- **E (3 windingen):** dikkere, zwaardere ringen. Hij leest meer als drie grote rollen slang en minder gelaagd. Mijn voorkeur, omdat hij het meest "bulky wall" zegt.
- De kop is nu klein ten opzichte van de massa (±14 % van de pixels). Voor een wall-eindvorm is dat bewust: de kop is de punt van de zoutkegel.

## Lessen
- Treden ontstaan door scherpe inkepingen op een bijna verticale flank. Een gladde omhullende met per winding een kleine uitbolling en een ronde onderkant leest als één kegel.
- Een spiraal (gleuven links en rechts op een andere hoogte) haalt het symmetrische kerstboom- of taarteffect weg.
- Een korte, scherpe inkeping (alleen de laatste 2 rijen) geeft puntige lipjes, die als takken lezen. Rond de onderkant van elke winding af over de onderste helft.
- Laat het midden niet per winding verspringen (dat geeft kartels op de gleuf), maar laat het tussen de windingen glijden.
- Een lage, koepelvormige variant werd een "broodje" met schouder naast de kop. Voor "kegel" moet de top smal blijven (±14 px halve breedte).

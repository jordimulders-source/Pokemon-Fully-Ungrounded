# Potoo-poppetje ronde 1: notities (maker)

Script: `pop3d_potoo.py` (vanuit de repo-root: `python3 docs/concept/sprites/potoo/poppetje/pop3d_potoo.py`), vel: `vel_ronde1.png`.
Geen Blender, geen mesh: dezelfde soort renderer als de lama (z-buffer, vlakke kleur, één schaduwtoon, lijn bij dieptesprong),
uitgebreid met **volumes met snijvlakken en holtes** (ellipsoïde ∩ halfruimtes − holtes). Daardoor is de open bek één holle
onderkaak die om het scharnier openklapt, in plaats van losse stokjes/schijfjes. Mondkleur zit alleen op de binnenwand.

## Gemeten (oogstraal r = 1)
| maat | leidraad (duo links) | close-up | zijfoto (duo rechts) | poppetje |
|---|---|---|---|---|
| kopbreedte | ±11,7 | 9,1 | – | 10,3 |
| oogmidden → kruin | 3,9 | 5,0 | 2,8 | 3,5 (oog groter: 1,25) |
| oogmidden → bovenrand bek | ±1,5 | 1,3 | 2,4 (mondhoek) | ±2,6 (Jordi: ogen hoger) |
| bovenrand mondhoek → haakje | – | 5,9 (3/4) | 6,2 | ±7 (mondhoek recht onder het oog) |
| bekopening hoogte / breedte | ±1,0 | 0,8 | – | ±1,1 (overdreven grote bek) |
| lijf / kop breed | – | – | nachtfoto 1,6 | 1,15 (Pokémon: lijf kleiner) |

## Waar elke vorm vandaan komt
- **Kop**: brede koepel + iets plattere kruin (close-up, leidraad) + 'gezicht' dat breed en plat naar het haakje loopt (zijfoto: voorhoofd daalt in één bocht naar het haakje).
- **Mondhoek**: recht onder het oog en ver opzij (zijfoto, close-up); de kop is daar het breedst.
- **Bovenrand**: snijvlak door mondhoeken en haakje; van boven gezien een spitse boog (twee grote 'lens'-bollen), daardoor van 3/4 een rechte rand naar het haakje. Hoornrand wordt breder naar de punt (bovensnavel leest als hard deel, zoals in de open-snavelsprites).
- **Onderkaak**: de kop onder de gaplijn als holle schaal, 62° opengeklapt om het scharnier (plus 9° kop voorover); van voren een schild/U met spitse donkere punt, lichte kaakrand (close-up). Langer dan echt: overdreven grote bek.
- **Muil**: geestblauw/paars alleen binnen de rand; donkere V-keel in de bodem (close-up), achterwand achter het scharnier.
- **Haakje**: klein, donker, krult omlaag (close-up).
- **Veertjes tussen de ogen**: rijen kleine spitse veertjes van tussen de ogen naar het haakje, punt iets los (close-up); in een iets donkerder lila, zonder eigen lijntjes (geen ruis).
- **Lijf**: peervormig, breed direct onder de kop, geen hals; schouders/vleugels hoog naast de kop (leidraad); lange platte staart (nachtfoto, illustratie).
- **Kleur**: C2 (bijna wit met lila zweem, pikzwarte ogen zonder glans); een paar schorsachtige vegen op vleugel en flank.

## Bewust gestileerd
Oog 1,25× en hoger op de koepel; bek langer en verder open; lijf 0,85×; kop licht voorover.

## Open / zwak
- Het verre oog steekt in de spritehoek als zwarte bult buiten de kopomtrek (klopt met de close-up, niet met de leidraad).
- Van voren leest de kop wat als schedel (wit + zwarte ronde ogen + V-veertjes); in de spritehoek minder.
- Veertjes tussen de ogen zijn subtiel; op 64 px vallen ze weg.
- Muil is één vlak paars met keel; diepte komt alleen uit de rand.

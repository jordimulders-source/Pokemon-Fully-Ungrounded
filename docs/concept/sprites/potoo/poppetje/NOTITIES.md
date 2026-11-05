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

# Ronde 2 (vel_ronde2.png)
Reparaties op de punten van de coördinator:
1. **Geen helm/klep meer**: de kop is één koepel (`Ed`), het breedst vlak boven de gaplijn; de bovenkop wordt door dezelfde (nu verticale) lens gesneden als de kaak, dus het gezicht boven de rand is nergens breder dan de muil. De onderomtrek van de kop loopt in de mondhoeken over.
2. **Muil zo breed als de kop**: mondhoeken op de kopomtrek (`zc` = kopbreedte op de gaplijn); kaak op het scharnier even breed.
3. **Rand dun**: bovenrand één band van 0,22 + lijn; kaakrand = alleen het snijvlak van de schaal (0,35 dik). Donker alleen de kaakpunt. Kaakschaal ondieper (wig van opzij, zijfoto).
4. **Oog vlak boven de rand**: ruimte ½ oogstraal, x halverwege de koplengte (zijfoto); oog 1,15 r_e.
5. **Kopvorm**: ronde koepel, hoogste punt boven/achter het oog, voorhoofd in één bolle bocht naar het haakje (geen plat 'gezicht' meer).
6. **Kop : muil**: open muil ±60% van de hoogte kop+muil op de leidraadhoek.
Verder: keelholte achter het scharnier (`gul`) zodat er geen wit vlak in de muil zichtbaar is en geen paars buiten de rand; borst naar achteren (stak door de muil heen); schorsveeg op de borst smaller.

**Controle** (rij 2 van het vel): omtrek kop+muil (rood) en mondrand (oranje) met de hand overgetrokken op de foto's (`TRACES` in het script), uitgelijnd op het oog en geschaald op de oogstraal (foto-oog = 1 r_e), over de render op dezelfde hoek.
- Close-up (140°, 4° van boven): bovenrand, nabije kaakrand en kaakpunt vallen op de oranje lijn (afwijking < ½ oogstraal); de kruin van de foto ligt ±1 oogstraal hoger en verder naar achteren.
- Leidraad (140°, 4° van onder, kop 5° omhoog zoals op de foto): kruin en voorkant kloppen; de foto-muil hangt ±1 oogstraal verder omlaag en naar links (de foto is van onderaf, de kaak staat verder open). Bij meer openen past de close-up niet meer; nu een middenweg (66°).
- Hoek gevonden door de overlap van mondvorm en oranje lijn te meten over een reeks hoeken/kaakmaten.

# Ronde 3 (vel_ronde3.png)
Op de 10 punten van de keurder:
1. Bovensnavel = onderrand van het gezicht: dunne lichte rand, vóór rond het haakje hoornkleur (donkerder). Haakje: gebogen buis van ±1,5 r_e, donkerste accent, voorste punt van het profiel, hangt vóór de muil.
2. Onderkaak: diepe schep (dieper en langer, 66° open: punt ±6,5 r_e onder de gaplijn), eigen bevederde buitenkant met omtrek (`jawfur`, lijn op de grens), donkere punt; van opzij een wig vóór de borst.
3. Muil als holte: licht bij de rand (`mouth`), donkerder naar bodem/keel (`mouth2`), achterin een donkere keelholte (`throat`). Wat binnen de mondrand ligt en geen mondwand is, wordt in beeldruimte keelholte (floodfill): nooit vacht ín en nooit mondkleur buiten de muil.
4. Koepel lager (boven de gaplijn ±4,9 r_e), ruige kruin met veerplukjes (`tufts`); in de spritehoek is de muil minstens zo hoog als de koepel.
5. Ogen met smal licht ooglidrandje, geen glans, binnen de kopomtrek van voren, ¾ oogstraal boven de rand. **Afwijking:** 2,2 oogdiameters uit elkaar in plaats van ±1: met de ogen dichter bij elkaar (gemeten: z = 2,6/3,4/4,0) passen de overgetrokken close-up en leidraad duidelijk slechter (mondvorm-overlap 0,57→0,65); 3,7 is de middenweg.
6. Veertjes tussen de ogen: 6 donkerdere plukjes boven het haakje die de omtrek breken.
7. Schouders/vleugels lager: bovenkant ±op de gaplijn.
8. Vier getrapte slagpennen langs de staart; staart lang, smal, versmallend in het verlengde van het lijf.
9. Schors als korte gerichte vegen op vleugel, flank en kruin; haakje en kaakpunt de donkerste accenten.
10. Omtrek licht onregelmatig door veerplukjes langs kruin, wangen en borst (zoals de lama-wol).

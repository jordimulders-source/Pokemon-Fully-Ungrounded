# Sapa Inca – kleurronde 2 (alleen kleurreparaties)

Bestanden: `sapa_inca.png`, `sapa_inca.txt` (raster + palet; de ronde-2-regels staan onderaan en vervangen de oude), `bouw.py` (PNG + controles), `diff.py` (pixeldiff per zone t.o.v. ronde 1), `vel.py` → `vel.png`, `kijk.py`. Draaien vanuit de repo-root.

## Studie (extra voor deze ronde)
| | Wat ik overnam |
|---|---|
| Corviknight | rood oog = gekleurde iris met 1 px glans, geen apart zwart lid; donkere kop krijgt licht via middentinten |
| Honchkrow | snavel: lichte bovenkant, donkere onderrand/punt; donker lijf met lichtere rand en banden middentint |
| Pidgeot | gesloten vleugel = lichte voorrand + pennen met scheidingen in de schaduwtint, schuin naar de punt |
| Talonflame | felle voorrand (dekveren) als aparte band langs de vleugel |

## Wat er veranderde
1. **Gezicht:** geen zwart bovenlid meer; tussen de kroononderrand en de ogen ligt rij 22 in rood. Ogen: donkere iris (d), glans 1 px (w), lichtere okertint tegenover de glans (a). Snavel: bleke rug (w) loopt schuin van de basis tussen de ogen naar linksonder, met de donkere haakpunt (d/K) op x23–24, y26–27; de oude verticale balk is weg.
2. **Opgeheven vleugel:** voorrand 2–3 px lichter (l, dekveren), twee doorlopende penscheidingen in d van de pols naar de punt, de punt bovenaan licht gekarteld (l/K), dekveren op de onderarm met kleine d-schubjes.
3. **Borst en lijf:** lichte bovenkant linksboven (y), kernschaduw rechts en onder (a, 3–4 px breed), rand naar het donkere lijf via een middentint (a → l → m → d) in een boog in plaats van een harde ovaal; geen veertekening. Lijf: lichte rand (l) linksboven aan hals en schouder.
4. **Staart:** roestbruin t met r-schaduw, aan de beenkant een zwarte scheiding en aan de buitenkant een donkere omlijning (d), zodat hij rechts als eigen strook leest.

## Pixeldiff
- Alpha-diff met het silhouet en met ronde 1: **0** (1560 px).
- Kroon (alle kroon- en kwastpixels uit de onderlaag, zonder de kopkoepel): **0 px**.
- Kop (x22–33, y19–27): 25 px · vleugel (y18–33, x34–54): 47 px · borst/lijf (y34–52): 62 px · poten/staart (y53–62): 16 px · rest: 0.

## Controles
- 15 kleuren + transparant; aandeel zwart 0,14.
- Open randen: 3 px, dezelfde als in ronde 1: de 2 px dunne linkerscheen (x24, y57–59) als pseudo-omlijning in g.
- Losse pixels: alleen bedoelde enkelingen (stippen, glans, irissen, oorschijf, snavelpunt, schubjes).

## Zelf gekeken (1× en 10× naast ronde 1, licht en donker)
- Het gezicht oogt rustiger dan in ronde 1, niet bozer of vreemder: de zwarte balk boven de ogen is weg en de snavel leest als haak naar linksonder.
- De borst is nu bol in plaats van een geplakt ei; de vleugel heeft een lichte voorrand.

## Eerlijk: wat nog niet klopt
- **Gezicht op 1× blijft klein:** ogen zijn 2–3 px; je leest vooral "rood masker met bleke snavel". Op 1× zie je de ogen nauwelijks als ogen, al lezen ze niet meer boos. Groter kan niet zonder het silhouet te veranderen.
- **Vleugel:** de penscheidingen (d op m) zijn op 4× zichtbaar maar op 1× nauwelijks; de vorm van het bevroren silhouet (smal blad met ronde top) leest nog steeds een beetje als een opgeheven arm.
- **Staart:** beter van het been gescheiden, maar nog steeds een smalle strook van 2–3 px; op 1× een roestbruin randje, geen echte staart.
- Rechte onderrand van de kroon (silhouet, bevroren) en de pseudo-omlijning van de linkerscheen staan nog.

## Lessen
- Een bleke snavelrug die schuin naar de punt loopt (1 px per rij) plus een donkere punt leest als haak; een even brede bleke kolom leest als balk.
- Op een klein oog in een rood masker: donkere iris + 1 px glans + warme tint tegenover de glans; zonder zwart lid oogt de blik rustig.
- Een ovaal die zacht overloopt in een donker lijf: per rij de rij g → a → l → m → d, waarbij de a-band naar onderen breder wordt (kernschaduw).

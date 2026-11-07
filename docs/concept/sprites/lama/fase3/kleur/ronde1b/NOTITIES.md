# Lama fase 3: kleur ronde 1b (maker, 5 nov)

Vanaf ronde 1, met de hand, in `bron/segmenten.txt` (per rij `y x0 pixels`); `bron/bouw.py` plaatst alleen en controleert.
**Alpha-diff met `silhouet/ronde2.txt`: +0 / −0** (`alpha_diff.txt` = `bron/controle_uitvoer.txt`).
Opdracht: de 8 zwakke punten van ronde 1 plus het oordeel van Claude ("blokkerig en plat, losse vlakken, kop als helm").
**Jordi (letterlijk):** "ja het hoofd is nu wat te klein ook" / "maar dat heeft puur met inkleuring te maken" / "want in het origineel ziet het er wel goed uit" / "nee kijk vooral naar hoe het origineel het doet" / "daar is het hoofd prima".
De maatstaf voor de kop is daarom **de onderlaag** (`labels.txt`); fase 2 dient alleen als voorbeeld van pixeltechniek.

## Palet (herindeeld, 16)
`n` (donkerbruin) is eruit. Bombín, vlecht en hoeven doen nu `k` met lichtjes in `d`/`S`. Gouden hooglicht = `H` (crème licht); `Y` is vervallen. Nieuw zijn **`R` rood licht** en **`G` groen licht**, zodat rood en groen elk 3 tinten hebben (groen: `G`/`g`/`D`). Alles is iets minder verzadigd: blauw 100/140/206 – 58/92/164 – 32/50/96 (dichter bij Swampert/Marill), rood 200/56/66, paars 148/66/124, goud 214/168/64.

## Per zone
1. **Kop (+oren), per pixel naar `labels.txt`:**
   - Crème tot aan de omtrek. Licht `H` linksboven (voorhoofd, snuit, hals vóór), schaduw `S` onder de kaak en rechts.
   - Omlijning `d` aan de lichtkant, `k` alleen onder de kin.
   - **Oog op de plek van de onderlaag (x23–25, y12–15):** zwaar vlak lid `SS` (y12), lidlijn `kkk` (y13), iris `k` met een crème lichtje laag vóór (`d H k`, y14), onderlid `d` (y15). In ronde 1 stond het oog 1–2 px naar voren.
   - Neusgat `k` (x16 y16), lipnaad `ddd` (y17), schaduw van de onderlip/kin `SSSS` (y18).
   - Pony `HH` (x20–21, y10–11), zoals de labels (`o`).
   - **Telling kop-pixels** (`bron/kopteller.py`; kopzone in de onderlaag = labels b/v/f/w/o = 73 px):

     | ronde | crème | `d` | donker (`k`) | waarvan van de hoedrand |
     |---|---|---|---|---|
     | 1 | 50 | 12 | 11 | 3 (y10 x19–21 lag over de pony) |
     | 1b | 51 | 14 | 8 | 0 (alleen lidlijn, iris, neusgat en de kinrand) |

     Er zijn geen donkere vlakken meer in de kopzone.
2. **Bombín (x20–24, y5–8; rand y9 x19–24 en y10 x22–25, gekanteld zoals de labels):**
   - Zwarte bol met een lichtje linksboven (`S` en `d`) en een rode band `Rrm` (y8).
   - De rand is één donkere lijn, aan de voorkant 1 px breder dan de bol. Aan de achterkant kan dat niet binnen het silhouet: de rand zakt daar naar y10 x22–25, zoals in de onderlaag.
   - Zwarte omlijning tegen de crème oren. Gemeld: de bol is 5 px breed, het kleinste dat nog dop + band + rand toont.
3. **Vlecht:**
   - Alleen waar de labels `p` hebben (x26–28/x26–27/x27–28, y12–22), dus achter en langs de hals en niet over de kop. In ronde 1b eerst 1 px breder gemaakt, dat is teruggedraaid na Jordi's correctie.
   - Knotten zigzaggen `dk`/`kd` (bruin op zwart, schuin afwisselend) met een lichtje `S` per 2–3 knotten. Rode tullma `Rr`/`rm` onderaan (y21–22).
   - De nabije vlecht is niet toegevoegd: het model toont hem niet.
4. **Voorpoten:**
   - De nabije als cilinder: `d` aan de lichtkant (tegelijk de scheidingslijn met de verre poot), `HH`, `C`, `S`, `k`.
   - Schouder bovenaan breed (y41–46) met een schaduwsikkel `SS` (y46–47) eronder; daarna de onderarm, met de knie zacht op y47.
   - De verre poot helemaal in `S` met `d`. Hoeven `k` met lichtjes (`kdSkdk`, `kdk`).
   - Achterpoten: dij van de nabije breed met een slagschaduwrij onder de rok (y46), de verre in `S`. Hoeven `kSdddk` / `kdddk`.
5. **Windsels:**
   - Beide in dezelfde volgorde: manchet (`HHH` + `y` + `d`), rood (`RR r m`), blauw (`UU B D`), groen (`GG g D`), geel (`yyy dd`), rood, manchet. Elke band heeft een lichtkant links en een schaduwkant rechts, en de nabije een `k` aan de schaduwkant.
   - De verre (x17–21, y50–56) in de donkere tinten (`yyyd`, `rmmm`, `BDDD`, `ggDD`, `yydd`, `rmmm`, `yddd`) met `k` aan de buitenkant. Zijn donkere rechterkolom (x21) is de scheidingslijn met de nabije band.
6. **Lijf/pak:**
   - Borst als één bol: groot licht `U` linksboven (x14–19, y30–35), basis `B`, schaduwsikkel `D` die de ronding volgt (rechts en onderaan, niet als trap).
   - **Rode bies als gebogen lijn langs de beenopening**: x26 y39 → x23–24 y40 → x21–22 y41 → x20–21 y42 → x21 y43, plus achteraan x41 y36–37.
   - Rug: licht bovenaan, sikkel `D` rechts.
7. **Cape en riem:**
   - Cape: voering `m`, een plooilijn `m` in het paars (x32, y30–33) en de schaduwkant `m` rechts.
   - Gouden zoom met afwisselend lichtje `Hy`/`yd`, zodat hij geen rechte streep is.
   - Riem `k H y d` met de plaat (x37–41, y32–37): zwarte rand, lichtje `HH` en een rode steen `r`/`m`.
8. **Ruches:**
   - Rood: `R`, `r`, `m`, met een geschulpte onderrand `mmrmmrmm`.
   - Goud: eerst een schaduwrij onder de rode ruche (`ydddddd`), dan `H`, `y`, en een geschulpte rand `yydd`.
   - Groen: `G`, `g`, `D`, met een schaduwrij bovenaan en een geschulpte zoom `ggDk`.
9. **Pompons:** 6 bolletjes van 1×2 (licht op y28, schaduw op y29), met telkens 1 px pak ertussen: rood, geel, groen, paars, rood, geel.
10. **Omlijning:**
    - Crème: `d` aan de lichtkant, `k` aan de schaduwkant en onderaan.
    - Blauw: `D` links, `k` rechts.
    - Cape: `m`.
    - Open randen: 4, alleen in de oren van 2 px (pseudo-omlijning).

## Zelfgenoemde zwakke punten (eerlijk)
1. **De bombín leest op 1× nog steeds klein:** de bol is 5×4 px en het silhouet heeft er geen eigen vorm voor. Op 2×/4× is het een hoedje met band.
2. **De vlecht is op 1× een donkere zigzagstreep achter de hals.** Hij leest beter dan in ronde 1, maar is maar 2 px breed (het model).
3. **De kop blijft op 1× smal naast het brede lijf.** Dat is de verhouding van het silhouet (W3); in kleur zit hij nu wel tot de rand vol crème.
4. **De pompons blijven een gespikkelde rij** op 1×, al zijn ze nu gescheiden.
5. **De gouden zoom** met afwisselende lichtjes leest op 4× als een stippellijn.
6. **De poten zijn nog vrij recht** onder de knie; de schoudersikkel is maar 2 px.
7. **De verzadiging** is iets terug, maar de outfit blijft het drukste deel naast Gen 3.

## Bestanden
`ronde1b.txt`, `lama3.png`, `normal.pal`, `vel_ronde1b.png` (onderlaag | 4× licht/donker | 1×; onder op 2×/1×: ronde 1b, ronde 1, fase 2 en 5 studiesprites), `alpha_diff.txt`, `bron/` (segmenten.txt, bouw.py, vel.py, kopteller.py + kopteller_uitvoer.txt, labels.txt, licht.txt).

## Lessen
- Een palet van 16 met 6 kleurgroepen: laat de donkerste groep (bombín, vlecht, hoeven) de omlijning `k` delen, dan komt er een slot vrij voor de derde tint van rood en groen.
- De maatstaf voor de kop is de onderlaag, niet de vorige sprite; tel de kopzone met de labels (`kopteller.py`).

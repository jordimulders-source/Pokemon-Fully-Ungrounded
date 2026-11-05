# Lama fase 3: kleur ronde 1 (maker, 5 nov)

**Basis:** silhouet ronde 2 is bevroren (Jordi: "niet erg, ga maar inkleuren"). **Alpha-diff met `silhouet/ronde2.txt`: +0 / −0**
(bewijs: `bron/controle_uitvoer.txt`, gemaakt door `bron/bouw.py`). Alles is met de hand getypt in `bron/segmenten.txt`
(per rij `y x0 pixels`, één letter per paletindex). `bouw.py` plaatst alleen en controleert; er is geen tint- of vormlogica.
De labels uit de render (`bron/labels.py` → `labels.txt`, `licht.txt`) dienden alleen om af te lezen welk onderdeel waar zit.

## Game Freak-studie (Emerald `anim_front.png`, bovenste 64×64, op 8×)
| sprite | kleuren / px | tinten per groep | omlijning | licht | massa/spieren | overlappende ledematen |
|---|---|---|---|---|---|---|
| Entei | 15 / 2011 | bruin 3 + omlijning, grijs 3, geel 2 | zwart aan schaduwkant en onderaan; boven en links donkerbruin | linksboven, hooglicht op schouder en kop | grote schaduwvlakken onder de buik en achter de schouder, gekarteld als vacht | verre poten in de donkerste bruintint, gescheiden door een donkere lijn; **grijze ringen om de poten** met donkere bovenlijn en lichte onderkant (direct bruikbaar voor de windsels) |
| Arcanine | 12 / 2622 | rood/oranje 3, crème 3 + zwarte strepen | zwart rond, maar aan de lichtkant de crème schaduwtint als rand | linksboven | de manen en het lijf zijn bollen met een schaduwsikkel rechtsonder | verre voorpoot helemaal in de donkere roodtint; alleen een donkere lijn scheidt hem van de nabije |
| Tauros | 15 / 1589 | bruin 3, haar 3, grijs 2 | zwart onderaan en rechts; bovenrand donkerbruin | linksboven | romp als één bol met lange schaduwband onderaan | verre poten donkerder en dunner, geen zwarte lijn ertussen maar de schaduwtint |
| Hariyama | 15 / 2409 | huid 3, crème 3, marine 2 | donkerblauw rond de lichte delen, zwart alleen rechtsonder | linksboven | buik als grote bol: hooglicht linksboven, sikkel rechtsonder | arm voor het lijf: omlijning alleen aan de schaduwkant, lichtkant scheidt door kleurverschil |
| Machamp | 14 / 2030 | grijs 4 + geel 3 | zwart rond, binnenlijnen in de donkerste grijstint | linksboven | spieren als korte gebogen schaduwhaakjes in de donkerste tint | dij achter dij: de verre krijgt de schaduwtint, de nabije het hooglicht aan de lichtkant |

Conclusies voor de lama: 3 tinten + omlijning per groep; zwart alleen aan de schaduwkant en onderaan; aan de lichtkant een
donkere tint van de groep (crème → bruin `d`, blauw → `D`, cape → `m`); de verre poot in de schaduwtint van de vacht, gescheiden
door de omlijningsbasis van de nabije poot (geen zwarte lijn); ringen (windsels) als horizontale banden over de hele beenbreedte.

## Palet (16, `normal.pal`)
| letter | kleur | gebruik |
|---|---|---|
| `.` | 152 208 160 | transparant |
| `k` | 38 24 30 | omlijning schaduwkant, pupil, vlecht |
| `H` `C` `S` | 250 244 224 / 232 212 176 / 190 164 128 | crème vacht (bont, foto 4): licht, basis, schaduw; `S` is ook de basis van de verre poten |
| `d` | 140 86 50 | bruin: omlijningsbasis van crème, staart, schaduw van goud, knotten van de vlecht |
| `n` | 78 48 38 | donkerbruin: bombín, vlecht, hoeven |
| `U` `B` `D` | 88 132 224 / 46 82 176 / 26 38 98 | blauw worstelpak: licht, basis, schaduw/omlijningsbasis |
| `r` `m` | 220 44 60 / 128 24 64 | rood (bies, halsband, rok, windsels, tullma, edelsteen) en wijnrood (schaduw van rood, band van de bombín, schaduw/rand van de cape) |
| `p` | 164 52 128 | paarse cape |
| `Y` `y` | 255 226 120 / 226 168 40 | goud licht en basis (zoom, riem, plaat, manchetten, gele ruche) |
| `g` | 44 152 88 | groen (halsband, rok, windsels) |
Gedeelde tinten: `d` (crème, goud en staart), `m` (rood en cape), `D` (blauw en de verre windsels). Groen heeft maar één tint;
de zoom van de ruche doet `k`.

## Per onderdeel
- **Oren (y1–8):** crème met `k` aan de schaduwkant; 2 px breed, dus pseudo-omlijning (§8): 4 open randen (`C` naast transparant op x20 y2–3 en x25 y3–4) zijn bewust.
- **Bombín (x19–26, y5–10):** dop `n` met lichtstreep `d` links, `k` rond; band `rrm` op y8; rand twee rijen (y9: `d`/`n` van boven, y10: `k` onderkant), 1 px breder dan de dop aan elke kant. Onder de rand een schaduwrij `S` op de kop, met links de crème pony `HH`.
- **Kop:** één crème familie, licht `H` links (snuit, voorhoofd), schaduw `S` onder de kaak en langs de lip (y17–19). Neus `k` op de snuitpunt (x15 y16), lipnaad `dd` (y19).
- **Oog (x21–25, y12–15, zoals fase 2):** zwaar vlak bovenlid in vachtkleur (y12), rechte zwarte lidlijn (y13, 4 px), iris `kk` met een klein crème lichtje laag vóór (`H` x22 y14, met `d` ervoor), onderlid `dd`. Geen zwart rondje met witte stip.
- **Vlecht (x26–28, y12–22):** de verre vlecht achter de hals (het model toont alleen die). Strengen als knotten: elke 3 rijen `d` (licht), `n`, `k` (scheiding), met `k` aan de rechterkant. Onderaan de rode tullma `rm` (y21–22).
- **Halsband (y23–27):** 5 rijen: rood, rood, groen, geel (`Y` links, `y` rechts), rood, licht links, schaduw rechts. **Pompons** op y28: om de pixel `r` `Y` `g` `p` `r` `Y` (6 zichtbaar; de 7e valt achter de cape-zoom op x27).
- **Worstelpak:** borst (x13–27, y28–40) als één grote bol: hooglicht `U` linksboven, basis `B`, schaduwsikkel `D` rechts en onderaan, `k` aan de onderrand. Rug (x37–49, y23–33): `U` bovenaan, `D` en `k` rechts. Rode bies `r` op x41 y36–37 (waar het model hem toont).
- **Cape (x28–35, y22–40):** voering `m` (x28), gouden zoom vóór `Yy` (x29–30), paars `ppp` met `m` als schaduw rechts, zoom achter `y` (x35). Aan de nabije kant hangt de cape-rand als een kolom `m` langs de borst (x13, y25–37) met een gouden puntje onderaan.
- **Kampioensriem:** gouden band (x33–40, y22–45) `Y`/`y`/`d`/`k`; de plaat (x37–41, y32–37) heeft een omlijning `k`, binnen `Y` met een rode steen `r`/`m` (x39 y34–35).
- **Rok:** drie ruches. Rood (y33–36, `r` met een `m`-onderrand), goud (y37–40, `Y` → `y` → `d`), groen (y41–45) met een geschulpte zoom `kggk…` op y45.
- **Voorpoten:** **twee poten door kleur**. De verre (x17–21) helemaal in `S`, met `d` aan de lichtkant. De nabije (x22–33) als cilinder: `d` (omlijningsbasis, en tegelijk de scheidingslijn met de verre poot), `HH`, `CCCC`, `S`, `k`. **Windsels, beide even netjes in dezelfde volgorde:** manchet goud, rood, blauw, groen, geel, rood, manchet goud. De nabije zit op y52–58 (lichte tinten), de verre 2 rijen hoger op y50–56 (donkere tinten: `y`, `m`, `D`, `g`, `y`, `m`, `d`), met `k` aan de buitenkant. Hoeven `n` met `k`.
- **Achterpoten:** de verre (x32–40) in `S` met `d` links en onderaan de hoef `knnnk`. De nabije (x38–49) als cilinder `d`/`HH`/`CCCC`/`S`/`k` met de hoef `knnk`. Bovenaan ligt een schaduwrij `S` onder de rok.
- **Staart (x43–47, y21–25):** bruin `d` met lichtje `S` en schaduw `n`, `k` rond (bont: het enige zichtbare bruine vachtdeel).

## Controles (`bron/controle_uitvoer.txt`)
- 1512 px, 15 kleuren + transparant, **alpha-diff 0** met `silhouet/ronde2.txt`.
- Open randen: 4, allemaal in de oren van 2 px (pseudo-omlijning, bewust).
- "Losse" pixels (geen gelijke 4-buur): 92. Die zijn bewust: details van 1 px (pompons, edelsteen, knotten van de vlecht, lichtjes, de geschulpte zoom, overgangen in de omlijning). Er is geen ruis in de grote vlakken.

## Zelfgenoemde zwakke punten (eerlijk; volgens de norm = terug naar de maker)
1. **De bombín leest op 1× nauwelijks:** het is een donker blokje van 6×6 tussen de oren. Op 4× is hij duidelijk (dop, rode band, rand), maar op 1× gaat hij bijna op in de oren. Het silhouet geeft hem geen eigen vorm.
2. **De vlecht leest op 1× als een donkere streep achter de hals**, niet als een vlecht; de knotten zijn pas op 4× zichtbaar. De nabije vlecht is in het model niet te zien.
3. **De crème poten zijn vrij plat:** rechte verticale kolommen `HH`/`CCCC`/`S` van 8–10 rijen (rechte lijnen ≥ 4 px), zonder knie of spier. Het buffe zit nu alleen in de massa, niet in de shading.
4. **De schaduw op de borst** loopt als een diagonale trap en niet als een echte bolle sikkel; dat is nog iets te vlak vergeleken met de buik van Hariyama.
5. **De pompons** (y28) lezen op 1× als een gespikkelde rij, dus bijna ruis.
6. **Op 1× vormen de twee windsels** (verre en nabije, naast elkaar) samen één regenboogblok. Op 4× zijn het duidelijk twee ringen.
7. **De outfit is erg verzadigd** (vijf felle kleurgroepen); naast Gen 3 oogt het drukker. De crème vacht, die bont moet zijn, valt alleen in kop, hals en poten op.
8. **Groen heeft maar één tint**, dus de groene ruche is plat.

## Lessen
- Een eerste kleurronde zonder alpha-diff-problemen: typ per rij segmenten (`y x0 pixels`) en laat het bouwscript elke afwijking van het bevroren silhouet weigeren.
- De gid-labels van de render (`labels.py`) laten precies zien waar de verre en nabije poten, windsels, cape-zoom en riem vallen. Zonder die labels had ik de windsels op de verkeerde poot gezet (ze zitten op verschillende hoogtes).

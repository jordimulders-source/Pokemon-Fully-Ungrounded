# Silicobra (Uyuni) – ronde 2, frontsprite frame 1

Bestanden: `silicobra_uyuni.png` (64×64, geïndexeerd, 15 kleuren, transparency=0), `silicobra_uyuni_raster.txt` (het met de hand bewerkte tekstraster = de bron; `scripts/bouw.py` maakt er de png van), `vel.png` (basis, ronde 1 en ronde 2 op 4× licht/donker, 1× licht/donker, referenties), `scripts/controle.py` (diff en randen), `scripts/vel.py`.

Opdracht (coördinator na ronde 1): korst/kuif leest als baksteen → onregelmatige veelhoeken met Y-naden; oog is een blokje → ring terug, licht gebogen lid over een rond oog; pekelzak leest als edelsteen → zachte ronde zak. Jordi (letterlijk) erbij: "vooral de buitenste lijn is te zwart" → selout.
Bevroren: silhouet van ronde 1 buiten de zak, gezicht en snuit, voet, krul.

## Wat ik deed
**Korst en kuif (geen baksteen meer).** Alle rechte naden weggehaald en het patroon opnieuw getekend als barstnet van een opgedroogde zoutvlakte: minder en grotere platen (bovenop A en B, de hoek C1, achterop C2 en een grote D, naast het oog F). De naden lopen schuin in trapjes van 1–2 px en komen drie aan drie samen in Y-punten, nooit vier in een kruis: bij (34,20) en (35,21) op de hoek, en midden op de achterkant bij (36,24) met drie armen (omhoog naar de kuif, schuin omlaag naar de rand en schuin omlaag naar de nek). Elke plaat heeft een lichte rand linksboven en wordt naar rechtsonder donkerder; naden in middentint (`d` in het licht, `e` in de schaduw). Gecontroleerd met een script: geen horizontale of verticale naad van ≥ 3 px in de korst (de enige melding is de mondlijn van de basis in het gezicht, bevroren). Op 1× leest het als een gebarsten korst, niet als metselwerk.

**Oog.** De turquoise ring is terug, rond en onderaan U-vormig (geen punt meer). Het bovenlid (huid in zouttinten, licht linksboven) valt over de bovenste helft; de lidrand is een lichte boog (hoekjes rij 23, midden rij 24), daarboven een zachte oogkontour in middentint, zodat er geen turquoise bril rond het lid staat. Iris: donker direct onder het lid, lichter onder, spleetpupil, glanspixel linksboven. Leest loom, niet boos.

**Pekelzak.** Facetten weg: één zachte zak met een vloeiende omtrek (rechts 40-41-42-42-41, onderaan achter de krul langs), een glanslicht als gebogen boogje linksboven (`q a a q` met uitloop omlaag), middentint in het midden en een donkere onderkant waar de pekel zakt (`s` → `t` onderaan). Twee belletjes. De schouder bovenaan rechts loopt nu in één trap onder de korst door in plaats van in een schuine rechte lijn.

**Selout (Jordi).** De buitenomlijning is niet meer overal bijna-zwart: aan de lichtkant (boven, links) een warm grijs-oker `h` (124,108,90), op de overgang `K` (100,86,76), rond de pekelzak donker turquoise `t`, en alleen rechts/rechtsonder en onder de voet een warm bijna-zwart `O` (54,44,42), geen puur zwart. Voorstel per randpixel gemaakt op de richting van de buitenkant en daarna met de hand nagelopen (ruis K/O op de rechterkant weggehaald, onderkant voet `O`). Het silhouet verandert hierdoor niet.

## Diff-bewijs t.o.v. ronde 1 (`scripts/controle.py`)
| Zone | Alpha erbij | Alpha eraf | Gewijzigde pixels (kleur of alpha) |
|---|---|---|---|
| Korst/kuif | 0 | 0 | 133 |
| Oog | 0 | 0 | 41 |
| Pekelzak | 10 | 0 | 82 |
| Rest (gezicht, voet, krul) | 0 | 0 | 23, alleen buitenrand (selout); gecontroleerd: 0 wijzigingen binnen de omlijning |

De 10 pekelzakpixels: de bolling rechtsboven (rij 33–35) en de opening tussen zak en krul, die nu met zak gevuld is (de zak loopt achter de krul langs). Pixels: 1001 (ronde 1: 991). Open randen 0, losse pixels 0.

## Checklist SPRITE_NORM
1. Leest als echte Pokémon op 1×: ok (vel, naast Sandshrew-A, Lanturn, Torkoal, Shuckle, Sandaconda).
2. 3/4 links-voor: ok, ongewijzigd.
3–4. Ledematen/Escher: n.v.t. / ok; zak achter de krul, buik vóór de zak.
5. Curven: zak en kuif zonder rechte stukken ≥ 3 px in de omtrek, behalve de verticale rand van de kop (bevroren silhouet).
6. Kop: ongewijzigd t.o.v. ronde 1.
7. Ogen: bovenlid donkerst, iris donker boven/licht onder, glans; geen bril.
8. Kenmerken op 1×: kuif, korst, zak, half oog lezen.
9. Omlijning: selout per kleurgroep, bijna-zwart alleen rechtsonder/onder; licht linksboven; geen open randen.
10. Geen Chernobyl: gezicht = basis.

## Eerlijk oordeel
- Korst: leest nu als een gebarsten zoutkorst met Y-naden, niet als baksteen of Nacli.
- Pekelzak: rond en vloeibaar, geen geslepen vlakken meer.
- Oog: rond met ring en een gebogen half lid, loom. Het oog is iets minder prominent dan in de basis, omdat de bovenste helft nu huid is; dat is het halve lid zelf.
- Selout: duidelijk zachter dan ronde 1, zie het vel op licht en donker.
- Zelf zie ik geen open zwak punt meer.

## Lessen
- Een selout-voorstel op de richting van de buitenkant geeft op trapjes ruis (K/O om en om); daarna per kant met de hand gelijktrekken.
- Barstpatroon: begin met de Y-punten en trek van daar drie armen naar de rand; dan ontstaan vanzelf veelhoeken in plaats van rijen blokken.
- Een zak tegen een ander lichaamsdeel: laat hem erachter weglopen (de omlijning van het voorste deel sluit hem af), niet met een eigen schuine rand ervoor stoppen; dat gaf de edelsteenvorm.
- Een volledige 1 px-ring rond een oog met een huidkleurig lid erin leest als een monocle; laat het lid de bovenkant van de ring bedekken.

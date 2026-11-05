# DJ Rotom – kleur2 (frontsprite frame 1, grotere kop)

Jordi: "ja dan moet het middenstuk misschien wat groter om de ogen enzo goed te kunnen uitbeelden";
"silhouet naar sprite is niet 1 op 1 te vertalen, dus ga gewoon aan de sprite werken";
"maak meerdere versies desnoods als je het niet zeker weet".
Leidraad: `silhouet3/s1.25` (kop + spits ×1,25). kleur1 blijft als naslag in `../kleur1/`.

## Varianten (zelfde palet, speakers, bliksem, ogen en grijns)
- `dj_rotom_A.png`: display met rechte bovenrand en twee hoorntjes; equalizer met **4 brede blokjes** (2 px, 1 px zwart ertussen, lichte bovenste blok).
- `dj_rotom_B.png`: display met een **golvende bovenrand** (hoeken 2 rijen hoger dan het midden); equalizer met **5 smalle staafjes** (1 px, 1 px zwart ertussen).
Kopgrootte: alleen ×1,25 (geen twijfel: de kopvoorkant wordt 15 px en het gezicht past ruim).

## Bestanden
- `dj_rotom_A.png`, `dj_rotom_B.png` (64×64, geïndexeerd, transparency=0), `normal.pal` (= kleur1), `vel.png`.
- `bron/bouw_kleur2.py <A|B>`: neemt kleur1 over, maakt de zone x14–34 / y0–57 leeg en tekent daar met de hand de kop
  (rij voor rij, `p(y,x,'...')`), zet de bliksem uit kleur1 erin en legt er een gloed van 2 px omheen.
  Uitvoer: `dj_rotom_A.txt`/`_B.txt` (de tekstrasters). `render.py`, `vel.py`, `controle.py`, `palet.py`, `zet.py`.

## Wat er uit kleur1 komt (niet opnieuw getekend)
- Palet (16 kleuren) en de gloedopbouw (buiten `1`, binnen `2`).
- Rechterspeaker volledig. De enige wijziging: x35, y32–38 van `6` naar `7`, als naad tegen het zijvlak van de kop (7 px).
- Voorkant linkerspeaker met de conussen (x0–13): ongewijzigd.
- Bliksem met de witte noot: dezelfde pixels als in kleur1 (dikker, zelfde maat), 5 rijen omhoog (y14–25).
- Opbouw van de ogen: wit rondom, zwart opzij, iris donker boven en licht onder. De ogen zijn 1 rij hoger gemaakt (6),
  er is een glans `f` in de iris bijgekomen, en ze staan schuin zoals in de bron (bovenkanten naar buiten, het verre oog 1 rij hoger).

## Nieuwe opbouw van het middenstuk (zone x14–34)
| deel | plek | opbouw |
|---|---|---|
| zijvlak linkerspeaker | x14 + naad x15 | `6`, met `7` als naad; de kop staat ervóór |
| spits | y26–32, voet x25–29 | opbouw van kleur1, 1 rij langer; lichte streep `4` links |
| kop voorvlak | x16–30 (15 px), y32–57 | omlijning `6` links/boven, lichte bovenrand `4` (y33), lichte linkerrand `4` tot y44, verder `5` |
| kop zijvlak | x31–34 | `6`, bovenrand `7` |
| ogen | links x18–22 y36–41, rechts x26–30 y35–40 | ±4×6, schuin |
| grijns | x21–27, y42–44 | mondhoeken `8` omhoog, 3 witte tandjes, zwarte onderlijn |
| display | A x17–29, B x18–29; y46–54 | zwart, onderin equalizer `e` met de bovenste blok in `2` (lichter groen) |
| snoer | y51: x14–16 en x30–34 | `8`, loopt door tot in beide speakers |

Gemeten in `silhouet3/vervormd_1.25.png` / `s1.25/onderlaag.png`: kop x16–35 (met zijvlak), bovenkant y32–33,
ogen y36–42, grijns y43–44, display x18–30 y45–54, snoer y±51. Dit is toegepast met de kleine verschuivingen hierboven.

## Checks (`bron/controle.py A B`)
- Open randen (alles behalve de buitenste gloedtint naast transparant): **geen** (A en B).
- Losse pixels: **geen** (A en B).
- Gewijzigd t.o.v. kleur1: A 531 px, B 534 px. Buiten de zone x14–34/y0–59 alleen de 7 naadpixels op x35 (bewust).
- Omtrek t.o.v. s1.25: +55 / −95 px (A en B gelijk). Waar:
  - bliksem: +10 / −46. De bliksem heeft de maat van kleur1 gehouden; s1.25 heeft de onverdikte bronbliksem, die 3 rijen hoger staat met een langere staart linksonder (y23–29).
  - spits en bovenkant van de kop (y26–33): +27 / −13. De gloed loopt 2 px om de kop heen; het kleine gloedbultje links van de spits is weggelaten.
  - links van de kop en onderaan: +18 / −23. Buiten de zone is de omtrek van kleur1 (= silhouet B) aangehouden; s1.25 wijkt daar zelf 56 px van B af.
- `tools/concept/sprites/check.py` draait niet (Hoenn-dex weg; zie kleur1).

## Checklist SPRITE_NORM
1. Leest op 1×: ja. Naast Heat, Wash en Frost een Rotom-vorm, en het gezicht leest nu meteen als DJ Rotom (brede kop, schuine ogen, lachje, groot zwart display met groene equalizer).
2. 3/4 links-voor: ja. Zijvlakken rechts, het verre oog hoger, de rechterspeaker vóór de kop.
3. Ledematen: n.v.t. Alle onderdelen van de bron geteld.
4. Geen Escher: de kop staat vóór de linkerspeaker (naad x15) en achter de rechterspeaker (naad x35).
5. Vorm: de kasten zijn bewust recht (zoals Frost); de conussen zijn met de hand rond.
6. Kop: ×1,25 volgens de leidraad, zodat ogen, grijns en display ruimte hebben.
7. Ogen: geïntegreerd, met de Rotom-opbouw plus glans.
8. Kenmerken op 1×: ogen, display en equalizer lezen; de tandjes en de noot pas vanaf 2–3×.
9. Omlijning per kleurgroep, licht linksboven, geen open randen: ja.
10. Geen Chernobyl: niets zwevends; bliksem, spits en snoer zijn verbonden.

## Wat nog niet (helemaal) klopt
- De tandjes zijn op 1× een witte streep onder de ogen; als tandjes lezen ze vanaf 3×.
- De equalizer heeft 4 (A) of 5 (B) kolommen in plaats van de 9 in de bron; meer past niet met 1 px zwart ertussen.
- De golvende bovenrand van B is subtiel (2 rijen). A leest rustiger, B lijkt meer op de grijns uit de bron. **Keuze voor Jordi.**
- De bliksem staat lager dan in s1.25, omdat de maat van kleur1 bleef en hij aansluit op de spits.

## Lessen
- `bron_vervormd`/`vervormd_*.png` → 64-raster: eerst bijsnijden tot de alpha-bbox, zoals in `maak_silhouet.py` (zonder dat zit alles 2 rijen te hoog).
- Een vergrote kop in de sprite: werk in een zone, neem de rest pixel voor pixel over en leg de gloed opnieuw 2 px om het lijf. Dan blijven de randen dicht en de bevroren delen gelijk.
- Een equalizer met staafjes van 1 px leest op 1× als "ılı". Brede blokjes van 2 px of een rij lichte bovenblokjes lezen meer als blokjes.
- Een grijns als recht streepje leest als een neutrale mond; zet de mondhoeken 1 rij hoger.

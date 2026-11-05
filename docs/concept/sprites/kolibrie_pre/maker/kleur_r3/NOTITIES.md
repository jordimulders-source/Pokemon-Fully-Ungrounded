# Kolibrie pre-evo – kleur ronde 3 (maker, 2 nov)

Basis: kleur r2 en `kleur_r2/KEURING.md` (9 FAILs). Het silhouet blijft bevroren.
Jordi, letterlijk: "fluweel als kleur" · "deze pre evo mag wel een veel mildere kleur hebben, veel minder mysterieus" · "ja beetje het idee zoals dat fletchling nog niet fire is" · "Moet echt cute zijn".
Smaakkeuzes van Claude (voorlopig): bovensnavel blijft donker; blauwgroen als keelglans; een zachte fluweelglans op de kap (1 hooglichttint), verder mat.

## Bestanden
- `rijen_r3.txt`: met de hand, één teken per paletindex.
- `raster.txt`, `kolibrie_pre.png` (geïndexeerd), `normal.pal` (JASC).
- `vel.png`: r3 4× op licht en donker; r3 en r2 naast Fletchling, Taillow, Natu en de eindvorm (2× en 1×, licht en donker) en foto 1.
- Scripts: `bouw.py`, `palet.py`, `controle.py`, `vel.py`.
- Palet als r2; alleen D (gele omlijning) is iets geler: 232,166,44 in plaats van 222,150,40.

## Aftekenlijst per FAIL
| # | FAIL (keurder) | wat ik deed | stand |
|---|---|---|---|
| 1 | open randen (geel naar de gaap, `3` aan de buikonderrand) | `controle.py` telt nu **elke** kleur naast transparant behalve 1 en 2. Twee uitzonderingen met reden: **A** (donkerste snavel/pootkleur: snavel en pootjes zijn zo dun dat ze zelf de omlijning zijn) en **D** (de omlijningstint van het geel, door de keurder aangewezen). Gaaprand naar D: (14,14) (13,15) (14,16) (14,17) (11,18) (12,18) (13,18). Licht geel C binnenin: (13,14) (14,15) (15,16) (15,17) (14,18) (15,18). Buikonderrand (21,39) en (24,40) naar 2; staartrand (39,41) naar 2 | **0 open randen** |
| 2 | rugrand 4 px donker (y28–38) | rugrand is nu `E 1`: 1 px omlijning (1) met daarbinnen de vleugelschaduw E. Geen band van 2-en meer | ok |
| 3 | buik in rechte verticale stroken, geen grens, geen dons | buikgrens als boog: smal bij de kin, naar rechts uitbollend op de borst (tot x28–29 op y29–33), smaller onderin. Hooglicht 7 linksboven op de bolle borst, schaduw 5 langs de boog. De grens springt om de rij 1 px (dons, foto 5), geen losse pixels. Tussen buik en vleugel een flank 4 met kernschaduw 3 | ok |
| 4 | oog klein, glans vult de bovenrij | oog 5×5: donker bovenlid 1 (hoekjes 2), binnenkant 3 breed (x25–27), glans alleen een verticaal streepje van 2 px F op x25 (y15–16), reflectie E onderin (26–27,17) en (25–27,18). Leest als donker kraaloog met één glanspunt, zoals Starly en Fletchling | ok |
| 5 | keelvlek leest als kruimel aan de bek | weg van de bekpunt, naar de keelzijde achter de mondhoek: drie glanzende keelveertjes in een boog (8 met 9-glans) op (18–19,21), (21–22,22), (23,23), als gespikkelde keel (foto 1) en voorbode van de keelglans van de eindvorm. Verworpen tussenstappen: een plusvorm, en een vlek onder het oog (las als traan) | ok |
| 6 | vleugel leest als schaduw | eigen plaat in de kaptint (B, koeler en dieper dan de flank), schaduw E aan de rugkant. Lichte gebogen voorrand 4 (1 px). Een slagpenlijn E met een lichte rand 4 die diagonaal naar de vleugelpunt loopt (y35–40). De flank ervoor is 4/3, zodat vleugel en lijf twee delen zijn | ok |
| 7 | verre poot zwarte klodder, nabije vaag | nabije poot met een licht puntje B (27,42) en tenen A; verre poot met tenen A/1 om en om (31–34,43) en A bovenaan (32,42), geen blok 1 meer | ok |
| 8 | leest niet als kolibrie | de drie dingen die de keurder noemt staan er nu als eigen onderdeel: dunne donkere bek met gele gaap, glanzende keelveertjes, ingeklapte vleugel als plaat met penpunt. Kap (fluweelviolet met één zachte glanstint 4) als familie met de eindvorm | ok |
| 9 | minder "af" dan Fletchling/Taillow | delen lezen nu los: kap, oog, bek, keel met keelglans, bolle borst, flank, vleugelplaat, staart, pootjes | ok |

## Diff tegen r2 per onderdeel
| onderdeel | gewijzigde pixels |
|---|---|
| vleugel, rugrand, flank rechts | 142 |
| borst, buik, flank | 33 |
| staart | 13 |
| keel en keelvlek | 11 |
| oog | 9 |
| kop en kap | 8 |
| bek en mondhoek | 7 |
| buikrand en pootjes | 4 |
| **totaal** | **227** |

## Checks (`controle.py`, strenger dan in r1/r2)
- **Alpha-diff tegen silhouet r2: 0.**
- **Open randen: 0** (alleen 1, 2, A en D naast transparant).
- **Losse pixels:** alleen bewuste accenten (ooglidhoekjes, glanspixels van de keelveertjes, snavelpixel, licht puntje op de poot, hoekjes van de onderrand). Geen ruis.
- Aandeel zeer donker (1 + A): 0,137. 15 kleuren plus index 0.
- Zelf bekeken op 1×, 2× en 4×, op licht en donker, naast r2, Fletchling, Taillow, Natu, de eindvorm en foto 1.

## Wat nog niet klopt
- Ik zie geen fouten meer in de punten van de keuring.
- **Eerlijk over de kolibrie-read:** zonder lange snavel (bewust: een jong) moet hij het van de keelveertjes, de dunne donkere bek en de vleugel hebben. Op 1× zijn de keelveertjes klein (5 px).
- **Grotere keelvlek: vraag voor Jordi, geen fout.** Een grotere glansvlek liep in deze ronde twee keer vast (las als kruimel, plus-teken of traan). Volgens de keurder is "keel of nek, en hoeveel glans" een vraag voor Jordi, niet voor meer pixels.

## Lessen
- Een controlescript moet alle kleuren naast transparant tellen en de uitzonderingen bij naam noemen. Mijn r1/r2-script liet geel en 3 door, en daardoor meldde ik "0 open randen" terwijl er 9 waren.
- Een vlek onder het oog leest als traan, een kruis van 5 px als plusteken. Keelglans werkt als een paar kleine schubjes in een boog langs de keel.
- Een vleugel leest als vleugel door een eigen tint (hier de kaptint) plus een lichte voorrand en één penlijn. Een scheidingslijn in dezelfde tint als de flank leest als schaduw.

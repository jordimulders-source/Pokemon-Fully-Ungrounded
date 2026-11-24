# r4 checklist (zelftoets maker, vóór keurder)
Basis: r1 + neus van r3 (opdracht aangepast door Jordi: "kraag van r1 was prima", "broek weer precies hetzelfde fout",
"het moet gewoon een tuinbroekvorm zijn, niet met volledig rechte lijnen, het bovenlichaam moet geen pixelblur zijn, gewoon nette vormen,
kijk naar het model en zorg voor genoeg kleurtinten en schaduw"). Bouw: `bouw.py` (alleen pixelopdrachten, geen middeling), meting: `meet.py`.

| Citaat | Toets | Uitslag |
|---|---|---|
| "geen rechte lijnen" | `meet.py`: crème tegen vacht/hand/voet (buitenlijn niet meegeteld), runs > 3 px | 0 (r1: 11, o.a. r41 10 px, r35/36 7 px, kol 20/37 7 px). Tintgrenzen binnen crème > 3 px: 0 (r1: 11) |
| idem, silhouet | buitenlijn ongewijzigd (= model) | rechterbeen buitenrand x52 r48-56 en linkerbeen x15 r49-53 blijven recht: dat is het modelsilhouet, niet aangeraakt. Open punt |
| "Het moeten geen effen vlakken zijn" | 3 crèmetinten r1 (7 / 6 / F), schaduw als sikkel per vorm | borststuk: sikkel rechts + zakboog; buik: onderrand als boog, sikkel naast arm/hand; plooien buik/dijen uit het model; rechterbeen: sikkel 1→4 px breed + F-rand; linkerscheen: licht links, F-sikkel rechts. Crème 420 / schaduw 178 / donker 42 px (r1 414/190/23) |
| idem, ±40 px-regel | grootste eentintige crèmevlak | FAALT: licht crème is één samenhangend vlak van 420 px (8-buren; bib + buik + dijen raken elkaar), schaduw max 101 px (linkerscheen). Onder 40 px komen kan alleen met een 4e crèmetint of banding (beide tegen SPRITE_KERN ≤3 tinten / geen banding). Keuze nodig |
| "A maar moet netter" | broek tot de enkels | ja; manchetten als boog (voet hoger aan de zijkanten), links x18-24, rechts x44-50 |
| "het moet gewoon een tuinbroekvorm zijn" | borststuk + twee bandjes + broek | bandjes r1 (x21-22 en x35-37, r30-33), borststuk met curve-randen, bruine lijfzijkanten tot de taille, zoom (taille) als boog over de bib, broek tot de enkels. Leesbaarheid bib↔broek: matig (zelfde crème); keurder laten kijken |
| "bovenlichaam ... geen pixelblur, gewoon nette vormen, kijk naar het model" | losse vlekjes weg, vormen uit het model | plooi onder de rechterschouder als één lensvorm (r34-39), armcontour als één bruinlijn (x45→44, r35-41), lichtvlak onderarm (r1, staat in het model), onderarm-onderkant als boog; vlekjes (48,30-31),(41,33),(47-48,29),(11-12,27) weg; linkerarm: licht linksboven (4), schaduw onder (2) (model is daar vlak, kleur naar Gen 3) |
| "ja kraag van bibarel overnemen" | VERVALLEN ("kraag van r1 was prima") | kraagzone diff 0 t.o.v. r1 |
| patroon bovenlichaam / broekkleur r1 | crème = r1-tinten, geen kaki-band | ja, alleen r1-paletindexen 7/6/F; r3-modelschaduw niet gebruikt |
| tanden wit, ogen Bibarel, neus rood | diff t.o.v. r3 boven y26 | 0 (neus van r3) |
| rest bevroren | stam, potlood, staart, klep, gezicht | diff 0 (script: buiten de benoemde zones 0 px) |
| techniek | palet, silhouet, tintvlakjes | 15 kleuren + transparant; silhouet gelijk aan r1; crème-clusters < 3 px (8-buren): alleen 3 r1-pixels (32,32),(34,32) in de kraagbolletjes en (42,44) naast de hand |

Per zone t.o.v. r1 (totaal 208 px, buiten zones 0): neus 3, borststuk 48, lijfzijkanten 5, taille 5, zoom 13, broek 90, enkels 7, bovenlichaam 21, linkerarm 16. Kraag 0.

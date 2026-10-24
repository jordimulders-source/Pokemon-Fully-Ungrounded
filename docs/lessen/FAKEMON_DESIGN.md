# Fakemon-ontwerp: principes

Aangeleverd door Jordi (23 okt), samengevat uit fakemon-gidsen (o.a. YouTube-video's over Sugimori's werkwijze, r/fakemon, en een klassieke fakemon-gids). Lees dit **vóór elke ontwerp- of spriteronde** van een nieuwe Pokémon. Zie ook `docs/concept/sprites/KEURING_RONDE5.md`.

## Vaste werkwijze per fakemon (Jordi akkoord, 23 okt; doel ≤ ±5 rondes)
Waarom: alpaca en olinguito kostten 15 rondes, Cuyby 3 en Cuychu 4. De rondes gingen op aan details vóór het silhouet klopte, zelf geconstrueerde lijven, goedgekeurde delen die opnieuw werden aangeraakt, lessen die niet werden afgevinkt, en Jordi die als eerste keurder fouten vond.
1. **Ontwerp:** concept + referentiefoto + modeltekening; Jordi kiest. Geen pixels.
   - **Bouwtype bepaalt de moeite** (24 okt): bol-/vachtvormen zonder losse ledematen (Cuyby 3 rondes, Cuychu 4) gaan snel: het werk zit in kleur, schaduw en gezicht. Viervoeters en wezens met armen/klauwen (olinguito 30+, alpaca 17) mislukken op constructie (poten in 3/4, klauwen, kop). Daar: **volledig een echte Pokémon als basis** (pose + poten), alleen het uiterlijk veranderen.
   - **Referentiemateriaal is de grootste versneller** (23 okt): Cuychu en de alpaca gingen na Jordi's foto's (langharige cavia, alpaca) in een paar rondes goed; de olinguito pas na Galar-Linoone (gezicht), Sandslash (klauwen) en Poochyena (lijf). Zonder referentie gokken agents en draait het rondes rond. Daarom per fakemon vóór het pixelen verzamelen in `docs/concept/sprites/<naam>/referenties/`: (a) 1–3 foto's van het echte dier (Jordi levert of Claude zoekt), (b) 2–3 echte Pokémon-sprites van hetzelfde bouw-/posetype uit de checklist (skelet), (c) per kenmerk een sprite die het goed doet (ogen, klauwen, vacht). Vraag Jordi bij twijfel om een foto of een "zo bedoel ik het"-sprite.
2. **Silhouet op een echt skelet:** romp/poten van een passende Gen 3-sprite als onderlaag, overtekend in de verhoudingen van het dier. Eerst alleen het silhouet in één kleur; Jordi keurt op 1× "leest dit als X?".
3. **Volledige sprite:** kleur, shading, ogen; §0-checklist (`SPRITING.md`) punt voor punt afgevinkt in NOTITIES.md.
4. **Onafhankelijke keuring vóór Jordi kijkt:** een agent vergelijkt met ≥ 10 echte sprites (KEURING.md, nodig/polijsten); de nodige punten meteen repareren. Jordi ziet alleen de gerepareerde versie.
5. **Reparatierondes:** alleen de punten die Jordi noemt. Goedgekeurde delen letterlijk bevriezen; grote of ongevraagde wijzigingen alleen als variant naast het origineel.
- **Claude kijkt zelf eerst** naar elk resultaat (1× en 3×) vóór het naar Jordi gaat, en stuurt het terug als het duidelijk niet klopt (ronde 17/18 olinguito gingen ongezien door: "Chernobyl", "prutswerk"). Een onderdeel verplaatsen = de hele vorm eromheen laten kloppen (neus verschuiven zonder de snuit mee te nemen is zinloos).
- **Driekwartpose: bouw een 3D-poppetje** (olinguito v2, 24 okt): met platte vormen ging het drie rondes mis (kop veranderde, poten verstrengeld, staart los). Met `docs/concept/ontwerp/olinguito_v2/scripts/pop3d.py` (bollen/ellipsoïden, yaw/pitch, tekeningen als textuur in diercoördinaten) is 'meer draaien' één getal en kiest Jordi uit een vel met hoeken; daarna één onderdeel per ronde. Hergebruiken voor elke viervoeter.
- **Schetsrondes (Jordi, 24 okt):** geen changelogsectie en geen uitgebreide notitie per schets; alleen script + vel committen. Changelog, `ONTWERP.md` en Stand van zaken pas bijwerken als de **sprite definitief klaar** is (Jordi, 24 okt), niet bij een gekozen ontwerp of tussenstap.
- Max. 2 sprite-agents tegelijk; agents schrijven alleen in de map van hun sprite (lessen onder "Lessen" in NOTITIES.md, Claude zet ze over naar SPRITING.md).

## Kernprincipes
1. **Begin bij de eindvorm.** Sugimori en Game Freak ontwerpen vaak eerst de eindvorm en vereenvoudigen, verkleinen of halen weg voor de basis- en middenvorm. Klein beginnen en details toevoegen geeft rommelige ontwerpen. *(Wij deden het omgekeerd: fase 1 eerst. Volgende ronde: eindvorm vastleggen, dan terugrekenen.)*
2. **Een sterk silhouet.** Knijp je ogen toe: herken je het wezen aan de omtrek alleen (Pikachu, Lucario, Gengar)?
3. **Geen "dier met een hoed".** Een goede fakemon is een idee of mythe in een wezensvorm, geen echte hond/kat/vogel met strepen en een blad aan de staart. Combineer twee of drie ongelijke concepten (dier + voorwerp, folklore, natuurverschijnsel).
4. **Beperkt palet:** 2–3 hoofdkleuren die bij type of lore passen. Geen neon-verlopen, ingewikkelde patronen of te veel tekeningen.

## Werkvolgorde
1. **Concept:** een idee dat vanzelf komt (niet forceren).
2. **Ontwerp:** het concept tot een geloofwaardig Pokémon-wezen maken: meerdere bronnen, geabstraheerd en vereenvoudigd tot één geheel.
3. **Invulling:** naam, grootte, types, vechtstijl, moves, leefwijze, vormen/sekseverschillen.
4. **Basisdata:** stats, level-up-moves, abilities, evolutie.
5. **Kleine data:** TM/tutor/egg-moves, egg groups, geslachtsverhouding, lengte/gewicht, shiny, Pokédex-tekst.
6. **Triviale data:** sprites, voetafdruk, vangkans, groeitempo enz.
*(Sprites zijn stap 6: pas als het ontwerp vastligt. Dat is precies waar wij eerder misgingen.)*

## Pokémon zijn geen dieren
- **Eevee** is geen vos, kat of konijn: oren, kop, kraag, poten en staart komen van verschillende dieren of zijn verzonnen. Geen enkele Pokémon is een rechttoe-rechtaan weergave van één basisdier.
- Ga dus vrij te werk met het basisdier: verander, combineer, verzin.

## Pokémon zijn simpel
- Geen detail dat niet op een kleine sprite past. Schubben zijn groot genoeg om los te tekenen, of er zijn geen schubben. Vacht is dik genoeg om als vacht te lezen, of het lijf is glad.
- Liever een paar grote tekeningen dan veel kleine. Geen extra kenmerken om het kenmerk.

## Pokémon hebben types
- Soms volgt het type vanzelf (giftig dier = Poison, waterdier = Water, plant = Grass, vleugels = Flying).
- Anders het type in het ontwerp verwerken, maar creatief: niet elke Fire-type een vlam, niet elke Water-type blauw. **Heatmor**: een miereneter is niet Fire, dus kreeg hij elementen van een vlammenwerper, smederij en verbrandingsmotor in plaats van een brandende staart.

## Pokémon zijn geen hybriden
- Ook een mix moet als één natuurlijk geheel voelen, niet als aan elkaar genaaide delen. Abstraheer de geleende delen tot ze algemeen lijken en laat ze opgaan in het geheel.
- **Growlithe/Arcanine**: tijgerstrepen, maar je denkt 'hond'. **Vaporeon**: geen zeemeermin (voor zoogdier, achter vis); de vis-elementen (horizontale staartvin, rugvin over rug en staart, kraag en wangvinnen als snorharen) zijn geabstraheerd en ingevlochten.
- Daarom bestaan er geen klassieke griffioenen: die zijn letterlijk twee dieren aan elkaar.

## Pokémon zijn geen mensen
- Ook humanoïde Pokémon lijken niet op een mens in een pak: platte gezichten, **nooit een menselijke neus**, genoeg 'vreemd' om een monster te blijven. Een 'man in kostuum'-gevoel maakt elk ontwerp kapot.

## Toepassing op onze lijnen (Claude, 23 okt)
- **Eindvorm eerst:** voor alpaca, olinguito en nachtaap eerst de eindvorm vastleggen (bombín-lama, Robin Hood-wasbeer, maangenezer) en fase 1 daaruit terugrekenen.
- **Twee of drie concepten mengen:** alpaca = alpaca + bokser + cholita; olinguito = olinguito/coati + dief/Robin Hood + (welk voorwerp of welke mythe?); nachtaap = nachtaap + maan/Mama Killa + Nazca-spiraal + genezer. Elk deel abstraheren tot één geheel.
- **Niet humanoïde in kostuum:** vooral bij de eindvormen (cholita, Robin Hood, genezer) oppassen voor 'man in pak'.

## Referentiefoto's (Jordi, 23 okt)
- **Onthoud de Pokémon-filosofie:** een foto van het echte dier is inspiratie, geen blauwdruk. Neem alleen de herkenbare kenmerken over (silhouet, ogen, één typisch detail) en houd het gestileerd, simpel en schattig; nooit een realistische weergave van het dier.
- **Verzonnen kleurvlakken mogen, als ze werken** (Jordi, 23 okt): een kleur of tekening die het echte dier niet heeft (ander gezicht, andere poten) is toegestaan zolang de soort herkenbaar blijft en het één geheel oogt. Bij de alpaca werkte het niet: een crème gezicht en andersgekleurde poten maakten hem tot schaap. Twijfel → één vachtkleur.

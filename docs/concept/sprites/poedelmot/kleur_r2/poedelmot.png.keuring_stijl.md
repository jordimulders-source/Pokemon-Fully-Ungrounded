# Keuring stijl: poedelmot kleur r2

Bron: `docs/concept/sprites/poedelmot/kleur_r2/poedelmot.png` (64×64, geïndexeerd, 12 kleuren + transparant, 1782 px). Gelezen: SPRITE_KERN, SPRITING, FAKEMON_DESIGN, FAKEMON_CHECKLIST, Dragonfly Cave-gidsen (txt, delen omlijning/shading/vacht). Vergeleken op 8× met Venomoth, Dustox, Beautifly, Masquerain, Butterfree, Altaria, Venonat, Swablu (`graphics/pokemon/*/anim_front.png`).
Keurder: stijl/Pokémon-gelijkenis (niet de gelijkenis met het model). Coördinaten (x,y) = pixels in de 64×64-sprite.

## Blinde indruk (vóór het lezen van de docs)
- Op 1× leest het als een pluizig motje met twee grote zwarte ogen en twee grote donkere geveerde sprieten. Schattig, het idee "poedelmot" komt over. Het is duidelijk een wezen, maar het leest half als knuffel/pluizenbol.
- Wat stoort: de vleugeltekening leest als losse letters ("C", "Ez") en dus als ruis. De onderkant is een tros witte bolletjes, wattenbolletjes eerder dan pootjes, met donkere stompjes eronder. Lijf, kop en vleugel lopen in elkaar over: het wit heeft bijna geen schaduw, dus is er weinig volume. De sprieten zijn het donkerste deel en trekken alle aandacht. Veel randen zijn recht.

## Punt voor punt
| Punt | Oordeel | Bevinding |
|---|---|---|
| Leesbaarheid 1× | voldoet (krap) | Leest als mot-Pokémon (vgl. Venonat/Butterfree-schattigheid). Onderkant en vleugelpatroon zijn op 1× ruis. |
| Omlijning / selout | voldoet | Buitenrand: 77× `2`, 53× `1`, 46× `4`, 5× `3`. Geen lichte randpixels, geen open randen. Lichte kant links heeft selout `4` (x9–14, y26–45), de schaduwkant donker `2`. Zwart `1` op de rand alleen bij de sprieten (ontwerp). Geen om-en-om-wisseling gevonden. |
| Donker-aandeel | wijkt af (licht) | `1`+`2` = 0,268 van de pixels (Gen 3 ±0,13, band 0,10–0,25). Dat komt door de zwarte sprieten (ontwerp), maar samen met het vrijwel schaduwloze wit wordt het een harde zwart-wit-sprite. Venomoth en Dustox lijnen hun vleugels in kleur af. |
| Tinten per kleurgroep | wijkt af | Crème `A`(L248)/`9`(233)/`8`(204)/`C`(172) zijn 4 tinten in één groep. Ook warm `7`(218)/`6`(188)/`5`(156) lopen door het crème heen (bijv. rij y44–45, x17–33: `a7aa7…9979978898`). Dat zijn eigenlijk 7 lichte tinten door elkaar. |
| Helderheidsstappen | wijkt af | `A`→`9` is maar Δ15 (doel ±30–40): niet te onderscheiden, het wit leest als één vlak. `7`(218) ligt 15 onder `9`, waardoor vleugel en lijf geen eigen kleurgroep zijn. Altaria/Swablu zetten wit tegen een duidelijke koele schaduw (Δ±35) en krijgen zo volume. |
| Shading / lichtrichting | wijkt af | Het licht staat linksboven, maar de kopkoepel (x15–34, y27–40), de kraag en de rechterkant van het lijf hebben vrijwel geen schaduwsikkel aan de rechter-/onderkant. Er is geen slagschaduw van de kop op de vleugel (x34–40, y30–45). Plat, "gebleekt". |
| Banding | wijkt af | Een 1 px band `6` loopt parallel aan de rechter vleugelrand (x59–61, y21–34), met `9` ertussen vóór de lijn: dat is banding langs de omtrek in plaats van een schaduw die de vorm volgt. |
| Pillow shading | wijkt af (deels) | De pluimen onderaan (x14–24, y44–54; x44–52, y46–55; x34–41, y54–60) hebben een witte kern met rondom een donkerdere ring en een volledige donkere omlijning. Dat zijn kussentjes of wattenbollen, geen vacht. |
| Losse pixels / kleine clusters | voldoet (grotendeels) | 15 clusters < 3 px: de sprietnerf `6` (lijn, mag) en de reflectie `B` in de ogen (29,34), (31,37), (17,38), (29,38). Wel ruis: de krabbels `6`/`7` in het wit van de vleugel (x45–58, y21–33 en x44–52, y38–45) zijn 1–2 px brede kronkels die als letters lezen. |
| Rechte stukken / dozen | wijkt af | Rechte horizontale lijnen van ≥ 8 px: de grens van de achtervleugel y36 x41–53 (13 px) en y46 x44–52, de snuitboog y42 x22–30, de onderkant van het achterlijf y54 x34–41, en de bovenrand van de rechterspriet y18 x41–52 (12 px zwart, plat). Bij een pluizig dier hoort geen liniaal. |
| Jaggies in curven | wijkt af | De bovenrand van de linkerspriet (x2–20, y17–30) en van de rechterspriet volgen een stijf 1-1-2-patroon, met een platte top en daarna een knik. De sprietbaarden staan op een vast raster (`(x−y//2) mod 4`) en lezen daardoor als machinale arcering, niet als veren. |
| Ogen | voldoet (krap) | Grote zwarte amandelogen met een 2×2 witte glans linksboven en een grijze reflectie onderaan (vgl. kraalogen in de gids). Verre oog x14–20, nabij x25–33: het perspectief klopt. Wel wijkt af: de reflectie `B` is grijs (L114), niet gekleurd, en het oog is ±35% van de kopbreedte. Dat leest als knuffel. Venonat en Butterfree hebben gekleurde ogen met binnenstructuur. |
| Pootjes / perspectief | wijkt af | De klauwtjes zijn donkere stompjes van 1–2 px die recht omlaag hangen: (19–22, 55–57), (24–29, 57–59), (35–40, 59–61), (44–47, 57–59). Ze staan wel op verschillende hoogtes (goed), maar lezen op 1× als druppels/vuil. Dustox en Butterfree tekenen pootjes als kleine, afgelijnde, schuine vormen in de lijfkleur. |
| Vormen / vacht | wijkt af | Vacht hoort volgens de gids een gekartelde schaduwgrens met plukjes te hebben (Altaria-wolk: grillige rand + plukschaduw). Hier zijn de randen van kop, kraag en pluimen glad en rond. De poedelmot is juist een vachtdier. |
| Scheiding kop/vleugel/lijf | wijkt af | De kop (wit), de verre vleugel (wit, x9–15) en de voorvleugel (wit/`7`) hebben dezelfde helderheid. Alleen de dunne lijn `2` scheidt ze, nergens een schaduw van overlap (E2). |
| Paletgebruik | wijkt af (licht) | 12 van de 15 kleuren gebruikt, waarvan ±7 lichte bijna-gelijke tinten. De ruimte gaat naar onzichtbare verschillen in plaats van naar één heldere schaduwgroep (koel grijs-lila zoals Altaria). |
| Compositie / 3/4 | voldoet | Kop links-voor, vleugel rechts als tegenwicht, verre vleugel klein links. Niet symmetrisch. Past bij Masquerain/Beautifly. |

## 5 belangrijkste reparaties (op volgorde van impact)
1. **Volume in het wit:** voeg `A` en `9` samen tot één hooglicht/basis-paar met een stap van ≥ 30. Maak één heldere koele schaduwgroep (bijv. L±175 en L±140, grijs-lila zoals Altaria/Swablu) en zet die als sikkel rechtsonder op de kopkoepel (x26–34, y34–41), de kraag (x18–36, y41–46) en elke pluim. Zet een slagschaduw van de kop op de voorvleugel en de kraag (x34–40, y30–45).
2. **Vleugeltekening:** vervang de 1–2 px krabbels (x45–58, y21–33; x44–52, y38–45) door 2–3 grote, gladde vormen die van de vleugelbasis naar de rand waaieren (aders/schulpen zoals Venomoth/Butterfree). Elke vorm ≥ 3 px breed en in één tint (`6`), geen letters.
3. **Rechte lijnen weg:** buig de achtervleugelgrenzen y36 (x41–53) en y46 (x44–52) tot een boog die de vleugelronding volgt. Maak de snuitboog y42 (x22–30) en de onderkant y54 (x34–41) rond. Geef de bovenrand van de rechterspriet (y18, x41–52) een oplopende curve 1-2-3-… in plaats van een plat dak, en haal de rand-`6` op x59–61 (banding) weg.
4. **Onderkant als vacht, niet als wattenbollen:** laat de pluimen overlappen met gekartelde, plukkerige randen en schaduw in de haarrichting (gids §7), zonder een volledige donkere ring om elk bolletje. Maak de klauwtjes (19–22, 55–57), (24–29, 57–59), (35–40, 59–61), (44–47, 57–59) kleine schuine pootjes van ≥ 2 px, afgelijnd en in perspectief (verre hoger en donkerder), geen hangende streepjes.
5. **Sprieten minder machinaal en minder zwaar:** breek het vaste baardraster met onregelmatige, taps toelopende baarden die de nerfcurve volgen. Zet aan de belichte bovenrand de omlijningsbasis `3`/`4` in plaats van zwart (zoals SPRITING §13 bij Cuyby). Zo zakt het donker-aandeel richting ≤ 0,22 en wordt het gezicht weer het brandpunt.

Vergelijkingsvellen (scratch): `/tmp/claude-0/-home-user-projectgrounded/00176e0d-eaf6-508f-a6c5-463bdec7182b/scratchpad/keur_stijl/vergelijking_8x.png` (poedelmot, Venomoth, Altaria, Dustox op 8×) en `.../keur_stijl/vergelijking.png` (9 sprites op 5× en 1× licht/donker).

Oordeel: FAIL

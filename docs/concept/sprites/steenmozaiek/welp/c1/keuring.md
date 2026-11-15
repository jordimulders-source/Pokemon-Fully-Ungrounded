# Keuring welp c1 (A/B/C), 15 nov – onafhankelijke keurder

Bekeken: 12× (alle drie), 7× naast p8, 3× en 2× naast de volwassen vorm, Regirock, Golem, Claydol, Relicanth, Growlithe en Vulpix, en naast Jordi's foto (`referenties/chavin_jaguar_beeld_jordi.png`).

## Metingen
- **Silhouet:** alpha-diff met p8 = **0 px** voor A, B en C. Bbox (7,18)–(57,63) gelijk.
- **Gezicht:** in de zone x5–19, y25–41 is de indexstructuur 100 % gelijk aan p8 (oog, tong, tanden, neus intact; alleen het palet is anders).
- **Palet A:** 1 (30,24,26) L26 · 2 L58 · 3 L96 · 4 L132 · 5 L168; stappen 32–38, prima Gen 3-contrast. C: zelfde ramp in grijs. B = A + index 8 (174,152,181) lila, 66 px in de groeven.
- Buitenlijn 1 px, gesloten; geen losse korrels in de gravure.

## Blind oordeel (de hoofdvraag eerst)
Op 3× en 1× leest geen van de drie meteen als **uit steen gehouwen beeld**. Hij leest als een **grijze/greige kat of wolfswelp met spiraal-tatoeages**. Het "huisdier" van p8 (bruin) is weg, maar er is nog geen steen. Er zijn drie oorzaken:
1. **De kop is een lappendeken.** De vlakken 3/4/5 op de kop liggen in diagonale blokken die de lichtrichting tegenspreken: het voorhoofd is donker aan de lichte kant (index 3, x12–18 y21–24) en licht aan de achterkant (index 5, x19–24 y20–24), de wang is licht achteraan (x24–28 y27–30). Op 3× leest dat als **vachtvlekken/camouflage**, en dat is precies Jordi's eerdere klacht: "willekeurige lijnen op het hoofd".
2. **De steen is te donker en te modderig.** Het grootste deel van de massa is index 3/4 (L96–132). Het beeld op de foto is licht kalksteen (L±170) met donkere groeven. Regirock en Relicanth lezen als steen door **lichte vlakken met harde, donkere details**; hier is het een middengrijze massa.
3. **De gravure leest als getekend, niet als ingesneden.** De groeven zijn 1 px index 2 zonder consequente lichte lip. Een kerf in steen heeft een donkere kant en een opgelichte rand ernaast (zoals bij de Claydol-ringen en de Regirock-stenen).

Wat wél goed is: er staan weinig motieven en ze zijn groot (schoudervoluut ±12 px, heupspiraal ±13 px), het zijn geen dubbele spiralen, en de schoudervoluut is hoekig zoals bij Chavín. Dat is een duidelijke verbetering ten opzichte van p8. Silhouet en gezicht zijn netjes bewaard.

**Zou Jordi dit mooi vinden?** Nog niet. Hij ziet het steengevoel ("het belangrijkste") niet genoeg, en de kop roept zijn klacht over willekeurige lijnen op. De kleurrichting (A of C) zal hij waarschijnlijk wel beter vinden dan p8.

## Per variant
- **A (greige, monochroom gegraveerd): FAIL, beste basis.** Deze kleur ligt het dichtst bij de foto en past bij het warme bruin van de volwassen vorm.
- **B (greige + lila/crème inleg): FAIL, niet verder mee.** De lila lijnen lezen als met krijt getekend (p8-gevoel: "lijnen tekenen"). Inleg hoort volgens de SPEC bij de evolutie ("welp = gegraveerde steen, bij de evolutie ingelegd tot mozaïek"); op de welp neemt dat het contrast tussen de fases weg. Op 1× maakt B de spiralen wel het best zichtbaar. Dat los je in A beter op met een lichte lip.
- **C (grijs, gegraveerd): FAIL.** Hetzelfde als A. Grijs leest iets meer als "steen" maar ook meer als **grijze wolf/kat**, en het staat koud naast de warme volwassen vorm. Kies tussen A en C pas ná de reparaties; dan is de tint een keuze voor Jordi (beide tonen).

## MOET (voor A, en hetzelfde voor C)
1. **Kop als één gehouwen volume (alleen schaduw, indexstructuur van het gezicht niet aanraken):**
   - Voorhoofd en schedeldak licht vanaf linksboven: x11–20, y20–25, index 3 → 4/5 (licht linksvoor), dus het donkere blok x12–18 y21–24 weg.
   - Schaduwsikkel aan de achter- en onderkant van de kop: x24–30, y21–31 naar 3 (rand naast de buitenlijn 2). De lichte achterwang x24–28 y27–30 (index 5) gaat naar 4/3.
   - Snuit: bovenkant licht (5), onderkant/kin donker (3/2). Geen losse diagonale vlakken meer; hoogstens 2 grote vlakken per kopzijde.
   - Oog, neus, tanden, tong en mondlijn: diff 0 (bewijzen met script).
2. **Steen lichter maken (palet, geen pixels):** de hele ramp ±25–35 L omhoog, met dezelfde stappen. Bijvoorbeeld 2 → L±75, 3 → L±115, 4 → L±150, 5 → L±185 (A warm greige houden). Dan staan de groeven (index 2) als donkere kerven op licht steen, zoals op de foto. Controleer daarna of het oogwit (index 9 L179, 10) nog tegen de kop afsteekt; zo niet, dan het vlak rond het oog index 4 laten.
3. **Groeven als kerf:** elke groeflijn (index 2) in de schoudervoluut (x27–41, y33–44), de heupspiraal (x36–50, y47–56), de kraaglijn (x26–32, y33) en de borstbanden (x24–34, y52–54) krijgt een consequente **lichte lip (index 5) aan de onderkant/rechterkant** van de groef en blijft donker aan de bovenkant. Eén regel voor de hele sprite (licht van linksboven: de onderrand van een kerf vangt licht). Op 1× moeten de motieven dan zichtbaar zijn zonder lila.
4. **Hooglicht:** een paar pixels hoogste steentint (een nieuwe of samengevoegde index, L±205) op de bovenkant van kop/oor links (x8–14, y19–21), de schouderbult (x30–36, y32–33) en de voortenen. Dat zijn de harde glimpunten die Regirock en Golem "steen" maken. Hooguit 10–15 px.

## MAG
- De horizontale borstbanden (y52 en y54, x24–34) zijn kaarsrecht over een ronde borst ("geen rechte stukken waar het dier rond is"). Laat ze 1 px meebuigen met de buik, of houd er één over.
- De heupspiraal heeft ±4 ringen in 13 px en is daarmee aan de drukke kant ("dubbele spiralen hoeft niet"). Eén ring minder maakt hem groter en rustiger.
- De staartpunt (x50–54, y49–53) kan een groefje krijgen, zodat ook de staart bij het beeld hoort (de foto heeft een gegraveerde staart). Niet nodig.
- Index 6 (8 px) en 14 (8 px) zijn bijna-dubbele tinten; samenvoegen geeft een plek voor het hooglicht (MOET 4).

## Eindoordeel
**FAIL (alle drie).** Ga door met **A** als basis (C als alternatieve tint om Jordi pas na de reparaties te laten kiezen) en laat **B** vallen. Silhouet en gezicht zijn in orde. Het probleem zit alleen in de licht/schaduw van de kop, de lichtheid van het steen en het kerf-effect van de groeven.

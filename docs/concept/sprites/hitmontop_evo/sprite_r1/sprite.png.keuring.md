# Keuring sprite_r1/sprite.png (Hitmontop-evolutie, capoeira)

Bron: `docs/concept/sprites/hitmontop_evo/sprite_r1/sprite.png` (8×, 2× en 1× bekeken, plus raster met coördinaten), vergeleken met `docs/lessen/SPRITE_KERN.md`, `docs/concept/sprites/hitmontop_evo/SPEC.md`, `referenties/pose_eenhandsstand.webp` en `graphics/pokemon/hitmontop/anim_front.png` (bovenste 64×64). NOTITIES.md van de maker en de andere keuring (`vel_r1.png.keuring.md`) niet gelezen.

## Stap 1: blinde indruk
Een bruin wezen met een grote, platte Hitmontop-achtige kop links (bruine "pot"-haarsnit met een klein knobbeltje erop), dat op één dunne arm met een ronde hand balanceert. De kop kijkt de kijker aan, stuurs. Rechtsboven een blauwe massa met twee blauwe uitlopers: links een lange, bijna horizontale buis met een blauwe bal (met lichte schijf) aan het eind, rechts een verticale buis met een klauwvoet die naar rechts wijst. Rood koordje hangt rechts omlaag.
Wat raar is (blind):
- Op 1×/2× leest het rechterbeen + broek als **een blauwe zwaan/gans** (broek = lijf, been = hals, klauwvoet met witte klauwen = kop met snavel). Het linkerbeen leest als **een arm met een blauwe bokshandschoen/bal**, niet als been.
- De kop zit zonder nek tegen de romp geplakt; kop en romp delen één rechte onderlijn.
- De romp is een vormeloze bruine vlek met schuine strepen; de vrije arm is er niet, alleen een losse lichte bol (hand?) en een los rood vlekje midden in de borst.
- Haar: een geribbelde helm/pot, en aan de linkerkant loopt het bruin door tot onder de kaak (haar langs wang/keel).
- Geen V-split: één been plat naar links, één recht omhoog.

## Stap 2: per onderdeel

### (a) Hoofdvraag: leest het op 1× als Hitmontop-evolutie in eenarmige handstand met V-benen?
- Lijkt op: steunarm recht verticaal omlaag (x33–38, y45–63) met ronde hand op de grond; kop laag naast de steunarm en kijkt de kijker aan; heup is het hoogste punt van de romp; cordão hangt omlaag. Gezicht is herkenbaar Hitmontop.
- Wijkt af in: de V-split leest niet. Linkerbeen loopt van (44,18) naar (16,9), ±18° in plaats van ±45° omhoog; rechterbeen staat loodrecht. Het silhouet is geen omgekeerde driehoek/Y maar een scheve T met een zware kop links. Benen lezen als arm-met-bal en als zwaan. **Hoofdvraag: niet gehaald.**

### (b) Kop
- Lijkt op: Hitmontop-ogen, wenkbrauwen en mond, bruine tinten; kleine tan hoorn bovenop (x16–19, y25–27).
- Wijkt af in: **geen Eddy Gordo-dreads**; het haar is een pot/helm met regelmatige verticale strepen (`cddh`-patroon, x10–31, y28–32) en geen enkele lok die hangt of is opgebonden. Bruin haar loopt aan de linkerkant door tot de kaaklijn (x2–9, y33–44): haar op wang/keel, precies wat Jordi niet wil. Onderkant kop is een rechte lijn van 20 px (y45, x12–32). Kop is ±28×20, platte ovaal, groter dan de romp.

### (c) Anatomie
- Steunarm: goed op zijn plek, één arm, ronde hand. Grijs-witte manchet bij de pols (y54–55) is Hitmontops enkelring op de verkeerde plek.
- Vrije arm: **ontbreekt**; alleen een lichte ellips (x44–48, y29–32) als hand en een rood vlekje (x34–36, y32–33) als armband zonder arm. Leest als losse bol en een wondje.
- Nek: geen; kop raakt romp met een verticale zwarte naad (x28, y33–44).
- Romp: ongevormde vlek x29–49, y24–45 met drie evenwijdige schuine donkere strepen (banding), geen schouder, borst of taille.
- Benen: twee, aan de broek; aantallen kloppen, maar richting (zie a) en leesbaarheid niet.
- Voeten: twee Hitmontop-voeten aan enkels; de linker toont de zool frontaal (leest als bal).

### (d) SPEC-punten
- Kleine hoorn: ja (klein, mag iets duidelijker van het haar los).
- Lange aansluitende blauwe broek: **nee**; de broek is bij de heup een zak/trechter van ±18 px breed (x42–61, y15–28) tegenover beenbuizen van 4–6 px. Niet aansluitend.
- Langer lijf: matig; de romp is wel lang, maar zonder vorm.
- Langere benen met kleinere blauwe klauwvoeten: benen lang, maar **voeten even groot als bij Hitmontop** (links 13×13, rechts 15×11), niet kleiner in verhouding.
- Koordjes aan broek: ja (x51–56, y28–40, hangt goed). Aan bovenarmen: steunarm ja (y48–50, het staartje steekt opzij i.p.v. omlaag te hangen); vrije arm alleen een rood vlekje.
- Ronde handen: ja.

### (e) Netheid (SPRITE_KERN)
- Tinten binnen de norm (huid 4 incl. selout, blauw 4 incl. donkere rand).
- Banding/strepen in romp en haar (parallelle lijnen op vaste afstand).
- Rechte stukken: onderkant kop (y45), bovenrand linkerbeen als lange rechte trap.
- Lichte kleur op de buitenrand: witte klauwen rechtsboven (x58–62, y3–4) en grijs/wit aan de linkervoet (x1–4, y11–13; x9–11, y1–2).
- Hand raakt de onderrand van het vel (y63); rechtervoet raakt de rechterrand (x63, y3 en y6). Geen marge.
- Belijning broek: zwart bovenaan, donkerblauw (`#525A94`) aan de rechterkant; rustig, wel consequent per kant: ok.

## NODIG
1. **V-split**: linkerbeen ±45° omhoog naar linksboven (voet rond x6–14, y2–10, been vanaf de heup schuin), rechterbeen schuin naar rechtsboven in plaats van loodrecht; samen een duidelijke V/Y-silhouet.
2. **Zwaan-lezing weg**: rechtervoet niet als "kop met snavel" bovenop een rechte "hals" (x48–63, y0–15); voet in lijn met het been, gestrekt of geflexed zoals op de foto, klauwen niet als witte blokken op de rand.
3. **Linkervoet** niet frontaal als bal met schijf (x1–13, y1–13): zijaanzicht/gestrekt zodat het een voet aan een been is.
4. **Voeten kleiner** in verhouding tot de benen (SPEC), beide.
5. **Broek aansluitend**: de zak bij de heup (x42–61, y15–28) terug naar een broek die de heup en benen volgt, geen trechter.
6. **Haar opnieuw**: Eddy Gordo-achtige dreads (lokken naar achter/opgebonden, die door de zwaartekracht omlaag mogen vallen), alleen vanaf de schedel; het bruin langs wang/kaak (x2–9, y33–44) weg; geen streeppatroon.
7. **Vrije arm tekenen**: gebogen over buik/heup (zoals de foto), met bovenarm-koordje; nu alleen een losse hand-ellips (x44–48, y29–32) en een rood vlekje (x34–36, y32–33).
8. **Nek/schouder**: kop verbinden met de romp via een schouder bij de steunarm; geen kop die met een rechte onderlijn (y45) tegen de romp is geplakt. Onderkant kop rond.
9. **Romp vormgeven**: schouder → borst → taille → heup met schaduw als sikkel, de drie schuine strepen (x30–48, y24–44) weg.
10. **Marge**: niets op rij 63 of kolom 63 (hand y63, voet x63).

## POLIJSTEN
- Steunarm-koordje: staartje omlaag laten hangen (zwaartekracht), niet opzij (x37–38, y48–50).
- Grijs-witte manchet aan de pols (y54–55) weg of verklaren; hoort niet in de SPEC.
- Hoorn iets duidelijker los van het haar.
- Witte/grijze pixels op de buitenrand van de voeten vervangen door omlijning.

## Herstelbaar?
Niet met kleine reparaties. Goed en te bewaren: positie en vorm van de steunarm + hand, het gezicht (ogen, mond, hoorn), het cordão aan de heup. Opnieuw opbouwen: haar, romp met vrije arm en nek, en de hele broek/benen/voeten-zone (de V-split is een pose-fout; volgens SPRITE_KERN los je die niet op met kleurrondes). Dus: pose van de onderkant behouden, bovenhelft (benen) en romp opnieuw vanaf de posefoto, kop alleen nieuw haar.

8× bekeken: ja. 1× (en 2×) bekeken: ja.

Oordeel: FAIL

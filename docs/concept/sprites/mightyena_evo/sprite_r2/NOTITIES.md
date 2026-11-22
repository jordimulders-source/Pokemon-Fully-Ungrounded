# Mightyena-evolutie frontsprite, ronde 2 (alleen kleur, na keuring r1 "BIJNA")

Bestanden: `mightyena_evo_r2.png` (64×64, P, index 0 transparant, 13 kleuren incl. transparant, palet = r1), `bouw.py` (basis = r1; meet op het model op spriteschaal), `vel.png` (r2 8× | r1 8× | model op dezelfde schaal 8× / close-ups 12× kop+bek+oog, opgeheven poot, manen, poten naast het model / 1× op wit, licht, donker naast Mightyena 1× + model 1×).
Bouwen: `cd mightyena_evo && python3 sprite_r2/bouw.py` (argument erbij: raster printen).

**Silhouet en lijnen: alpha-diff met r1 = 0** (assert in bouw.py). Zwart: alleen (0,10) en (1,11) zijn veranderd (→ selout, punt 6). Ogen (geel/rood), bek, tong en tanden: 0 pixels veranderd.

## Afwijkingen
- t.o.v. de kale reductie: **403 van 2087 px**: kop (oren, voorhoofd) 60, ogen-zone 22 (alleen snuit/rand, geen ooppixels), bek/snuit 53, manen/staart/vacht 88, grijs lijf 80, opgeheven poot 46, poten 54.
- t.o.v. r1: **283 px**: kop 26, ogen-zone 6, bek/snuit 29, manen/vacht 44, grijs lijf 108, opgeheven poot 43, poten 27.

## Per punt van de keuring (stappen in bouw.py, pixels t.o.v. r1)
1. **Manen, 39 px:** strengen uit het model. De donker/middengrijze modelpixels (klasse D, L ≥ 46) in de manen worden in de haarrichting samengevoegd met een lijnfilter van 5 px in drie richtingen (langs de rug (43,37), voorin steiler (1,1.6), achterin vlakker (1,0.5); per pixel de beste). Een streng is een D-pixel met ≥2 D op de lijn of een tussenpixel met ≥3, en minstens 3 px groot. De streng krijgt tint 3; de bovenrand van een streng van ≥4 px wordt tint 4 (alleen als die samenhangend ≥2 px is). De rest van de manen wordt 2. Alle losse 3/4-pixels uit de keuringslijst zijn weg of maken nu deel uit van een streng van ≥3 px. Opruimen achteraf: losse 3/4-clusters < 3 px → 2.
2. **Zwarte poten, 43 px:** per rij de eerste vachtpixel(s) rechts van de linkerlijn → tint 3; 2 px breed waar de poot ≥6 px breed is, anders 1. Geldt voor voorpoot, middelste poot, achterpoot en de opgeheven poot. Tenen en klauwen (lichte modelpixels onderaan) blijven.
3. **Hooglicht op het lijf, 113 px:** de band uit r1 langs de manen is terug naar 6. Nu ligt tint 7 als bolling in een ellips per vorm: schouder (18,33), rug (33,31) en dij (46,35). De ellips blijft minstens 2 px onder de rand van de manen of de lijn, alleen op 6; stukjes < 3 px gaan terug.
4. **Losse vlekjes, 7 px:**
   - (44,30) en (14,37): het modelcluster is groter (vast aan manen/poot), dus elk kreeg een tweede pixel naar het modelcluster toe.
   - (16,37), (23,39), (24,40), (16,41), (49,44): in het model 0–1 px, dus buurtint.
   - (38,47): was in r2 al geen vlek meer.
5. **Kop, lichtkant, 18 px:** tint 7 op 6-pixels direct onder/rechts van de selout van oor en schedel, en een bolling op het voorhoofd boven het nabije oog (ellips (11,10)). De donkere modeltekening (5) op de kop blijft; ogen, bek en tanden onaangeroerd.
6. **Linkerrand bij de oorvoet, 2 px:** (0,10) en (1,11) van zwart naar selout 4; de rand x0–1 y6–13 is nu één seloutlijn.
7. **Snuit, 35 px:** één tint donkerder (3→2, 4→3) in het vachtdeel van de kop onder de ogen (x0–14, y17–28). Vorm, neusgat, zwarte lijnen, bek en tanden blijven.
8. **Opgeheven poot, 34 px:** gemeten zonder omlijning tegen het model op schaal.

   | | model L | r1 | r2 |
   |---|---|---|---|
   | opgeheven poot | 54 | 64 | 56 |
   | voorpoot | 53 | 64 | 68 |
   | middenpoot | 42 | 47 | 52 |
   | achterpoot | 43 | 54 | 58 |

   Volgens de meting is de poot even donker als de andere poten. Hij heeft nu dezelfde tinten: basis 2, modelpixels D → 3 (geen 4 meer), plus de lichtkant uit punt 2.

## Controle (`controle.py`)
- 13 kleuren en zwart 19,1 %.
- Geen lichte kleur op de buitenrand en geen seloutpixels tussen zwart (om en om); het aantal randovergangen selout↔zwart ging van 10 naar 8.
- Losse zwarte pixels zitten alleen in het gezicht en komen uit het model: (3,15), (6,19), (4,20) en (11,21).
- Tintvlekjes < 3 px die overblijven:
  - modeltekening op kop/oren (2);
  - een 3/4-paar aan het begin van een streng: (22,8), (27,18–19), (53,30);
  - tenen en klauwen;
  - één 3 in de snuit (5,16).

## Twijfels
- De hooglichtbollingen zijn ellipsen. De schouder leest op 8× als een lichte vlek van ±5×4 px, wat goed is; de dij is kleiner.
- Voorin de manen zijn de strengen kort (3–5 px), omdat het model daar weinig D-pixels heeft. Ik heb geen strengen bijgezet waar het model ze niet heeft.

# Onweerswolk-Swablu frontsprite, ronde 4

Jordi over r3: "nee de lijnen zijn veel te hard nu, het ligt aan dat er meer dan 2 kleurtinten moeten zijn om minder blur te hebben. De belijning moet juist zachter en niet zwart. Kijk desnoods naar de snavel van de echte swablu qua vorm en hoe die belijnd is".
Bestanden: `swablu_r4.png` (64×64, geïndexeerd, index 0 transparant, 15 kleuren incl. transparant), `swablu_r4_8x.png` (op wit), `vel.png` (`vel4.py`: r4 | r3 | model | echte Swablu op 8× / kop+snavel 12×: r4 | model | echte Swablu / 1× op 4 achtergronden + model 1×), `bouw.py` (op `sprite_r3/swablu_r3.png`).
Silhouet bevroren: alpha-diff met r3 = 0.

## Studie echte Swablu (graphics/pokemon/swablu/anim_front.png)
- **Kop:** omlijnd met donker blauwgroen (56,104,128), een donkere tint van het lijf, geen zwart. Zwart staat alleen onderaan lijf en poten en aan de rechterkant van de kuif: buitenkant, schaduwzijde.
- **Wolk:** wit (248), lichtlila (200,200,224), lila (152,152,192) + grijze selout (128,128,144); nergens zwart.
- **Snavel:** wit vlak met lila schaduw onderaan, een grijze/lila onderlijn en een open bovenkant (het wit raakt de kop); geen gesloten ring.
- **Oog:** zwart + blauwgroen.

## Wijzigingen t.o.v. r3: 127 px
- **Zwart → gekleurde selout (75 px).**
  - Kopomlijning, sprieten, de onderwolk-binnenlijnen en de bovenrand van de donkere wolk → nieuwe tint selout donker (46,60,78), een donkere leisteen. Een lijn die de kop raakt is altijd deze tint, zodat de kopring één kleur heeft.
  - Lijnen van en tussen de lichte bollen, ook hun buitenrand rechts en de rand bollen/onderwolk rechts → wolk donker (96,108,126). Dat is de selout van de bollen, zoals de grijze selout van Swablu's wolk.
  - Zwart blijft alleen in het oog en op de buitenkant schaduwzijde van de onderwolk en het staartje (achtergrond onder of rechts, y ≥ 38): 48 px.
- **Onderrand kop/onderwolk (11 px):** rij 37 wolk diep → selout donker (de lijn raakt het lijf; één tint met de kopring).
- **Rand linker bol/onderwolk (5 px):** de diagonaal (19,35)–(15,36) wolk diep → wolk donker (zachter, selout van de bol).
- **Snavel zoals de echte Swablu (19 px), op de plek en maat van het model:**
  - Bovenkant open: (22,27) wolk midden, (23,27) (24,27) wolk licht, (25,27) kop midden. Alleen (21,27) houdt een selout-stip.
  - Links: (21,28) selout, (21,29) (21,30) wolk midden (model: donkergrijs).
  - Rechts: (26,28) midden, (26,29) (26,30) wolk donker (schaduwzijde).
  - Mondlijn (21,31) (22,31) (25,30) wolk midden. Onderlijn (22–25,32) wolk donker. Onderkaak blijft wolk licht; wit vlak en glans blijven.
- **Tussenstap (17 px):** waar binnen één materiaal twee tinten verspringen (wit naast midden, midden naast diep, licht naast donker vogel), krijgt de donkerste pixel van de grens de tussentint. Elk materiaal heeft zo 3 tinten met een stap ertussen; lijnen zijn niet aangeraakt.

## Palet r4
0 transparant · 1 zwart (13,17,24) (alleen oog + buitenkant schaduwzijde onderwolk) · wolk 2 diep (68,78,96) 3 donker (96,108,126) 4 midden (126,138,156) 5 licht (164,176,192) 6 wit (210,216,228) · vogel 7 donker (68,90,110) 8 midden (106,130,152) 9 licht (150,174,194) · geel 10 oker (200,158,40) 11 geel (248,214,64) · 12 selout donker (46,60,78) · 13 snavelwit (214,220,230) 14 glans (250,251,253).
Lichte bollen: wit/licht/midden + selout wolk donker. Onderwolk: midden/donker/diep + selout donker; zwart alleen buitenkant onder/rechts. Kop: licht/midden/donker + selout donker.

## Twijfels
- De snavelbovenkant is nu open (grijs → licht → kop). Op 1× leest de snavel daardoor als wit vlak met een grijze onderkant, minder als ovaal dan in het model; dat is de Swablu-manier.
- De selout donker (46,60,78) ligt nog vrij donker tegen de kop. Iets lichter (bijv. (60,78,98)) is zachter, maar valt dan dicht bij vogel donker.
- De onderwolk houdt zijn zwarte onderrand (8 rijen); bij de echte Swablu zit zwart alleen onder lijf en poten. Als Jordi ook daar geen zwart wil, kan dat diep/selout worden.

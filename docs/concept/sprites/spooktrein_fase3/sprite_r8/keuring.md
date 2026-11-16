# Keuring spooktrein fase 3, r8 (16 nov, verse keurder)

**Oordeel: FAIL** (één hoofdpunt: verhouding geest : schoorsteen, Jordi "nu past de verhouding niet meer met hoe die uit de schoorsteen komt"; verder kleine netheidspunten).

## Hoofdvraag
- Op 1×/2× leest het als één Pokémon: pompoenkop-locomotief met groene grijns, spookwielen en een rookstaart. Grote gezicht (ogen + zigzag) leest en is bevroren. Naast Gengar/Haunter/Magcargo/Claydol: drukker (veel roestvlakjes), maar het model is dat ook.
- Kleine geest: ogen (wit glanspixel in donkere ring links, donker blok rechts) en open grijns (x21 r9-10, bodem x21-25 r11, rechts x26 r10 / x27 r8-9) volgen het natieve model; leest op 2×, op 1× niet (model op 1× ook niet).
- Maar de geest is ±1,4× te groot t.o.v. de rest (natief ×1,06 met gedupliceerde rij/kolommen, de rest ×0,744) en komt **zonder hals** uit de schoorsteen: hij zit als brede klont op de rand. "Geest die geniet van de snelheid" leest daardoor minder: hij lijkt erop te liggen in plaats van eruit te stromen.

## Metingen geest/schoorsteen
| | natief model | r8 |
|---|---|---|
| schoorsteenrand (breedte) | x26-39 = 14 | x12-22 = 11 |
| hals in de opening | x30-36 ≈ 7 (0,5 × rand), r20-22, iets rechts van het midden, versmalt over 2-3 rijen vanaf de kop | geen; onderkant r14 x15-37 (23 px), r15 x16-25 (10 px rechte lijn) = 0,9-2,1 × rand |
| kopbreedte (zonder arm) | x29-47 ≈ 19 = 1,36 × rand | x14-33 ≈ 20 = 1,8 × rand |
| kopmidden t.o.v. randmidden | +5,5 (0,4 × rand) naar rechts | +6,5 (0,6 × rand) |
| hoogte geest | r6-21 = 15 (op 0,744: ±11) | r0-15 = 16 |

## MOET
1. **Geest-schoorsteenverhouding naar het model** (zone x14-37, r0-15; rand x12-22 r15-17 blijft). Onderkant als hals: ±5-6 px breed (0,5 × rand), op x≈16-21, die de opening in r15 in loopt (in de rand verdwijnt), vanaf de kop versmallend over 2-3 rijen (r12-14), geen rechte 10-px onderlijn. De brede onderrij r14 x15-37 en r15 x22-25 weg (wit/transparant), behalve de hals. Kop/arm niet vervormen.
2. **Schaal van de geest**: in het model is de kop 1,36 × de rand; in r8 1,8 ×. Voorkeur (accuraat): de geest dezelfde reductie als de rest geven (eerst de duplicaten DUPR r12 / DUPC i15,i23 uit `geest8.py` weghalen = exact natief gezicht, dan schrappen naar ±0,75-0,8, nooit door ogen/mond/arm), dan op 2× toetsen of de grijns nog leest. Lukt dat niet (Jordi 16 nov: "als dat niet lukt, moet die groter worden"): kop zo klein als het gezicht toelaat (≤16 px = ≤1,45 × rand) en de groei omhoog/rechts vanuit de hals, nooit aan de onderkant.
3. Vlekjes in vlakken → buurtint: (5,38) K→8, (15,38) K→8, (2,31) 12→8, (2,38) 12→8, (17,39) 12→8, (20,37) 12→8, (12,41) 12→6, (5,44) 12→2, (7,45) 6→8, (18,30) 6→1, (8,21) 12→9.
4. Groen in de bruine buitenlijn: (3,25) 6→9, (13,19) 6→9, (22,17) 6→1, (1,56) 6→1.

## MAG
- Geest: lichtkant (linksboven, r1-8 x13-20) buitenlijn 5 i.p.v. 6 als selout.
- Vage spookwielen in de rookstaart (model x≈50-58, r30-38) iets duidelijker als ring in 5/4.
- Gloed/wielen gebruiken 4 groentinten (2,3,5,6); mag als gloed, anders 3 schrappen.
- (9,56) K tussen de koeienvangerlatten → 11.

## Gemeten, in orde
13 kleuren + transparant; brons/grijs elk 3 tinten; vaste buitenlijn 42 % zwart, zwart rechts/onder, gekleurde selout (9/12) links-boven; licht linksboven (7 alleen r21-26 x6-10); wielen en koeienvanger "wat simpeler" zoals toegestaan; grote gezicht niet gekeurd (bevroren).

## Ter info voor Jordi
De geest groter maken (16 nov) en "in verhouding met hoe die uit de schoorsteen komt" (vandaag) botsen bij een schoorsteen van 11 px: op modelverhouding (1,36×) is de kop ±15 px. Wil Jordi de grote kop houden, dan blijft alleen de hals als oplossing, of een bredere schoorsteen (ontwerpwijziging, niet zonder Jordi).

Vel: `keuring_vel.png`.

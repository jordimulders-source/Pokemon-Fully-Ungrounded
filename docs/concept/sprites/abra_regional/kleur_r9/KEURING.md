# Eindkeuring regionale Abra, kleur_r9 (verse keurder, 15 nov)

Getoetst: `abra_r9.png` en `abra_r9_curve.png` tegen `../referenties/gemini_gekozen.png` en `../kleur_r1/natief.png` (spritepixel (x,y) = natief (2x−1, 2y−14)), op 1×, 8× en 12× naast het model, naast de echte Abra/Kadabra/Sneasel (eerste frame `anim_front.png`). Gids: Dragonfly Cave (`SPRITING.md` §0–8, `FAKEMON_CHECKLIST.md`), `SPRITE_KERN.md`, `GEMINI.md`; SPEC: "Volg echt zoveel mogelijk dit model", vlekjes en streepjes behouden, geen mond, ogen dicht, geen rood accent. Bevroren en niet getoetst als ontwerp: ogen, pose, kleuren A, vlekjes, rand-zwart.

## Hoofdvraag: is dit een nette, af Gen 3-sprite die trouw is aan het model?
**Ja, na de schouderreparatie.** Op 1× leest hij als een slappe, ingezakte Abra met opossumstaart; de kop met de gesloten ogen, de twee donkere schouderplaten, de lus van de staart en de hangende handen staan op de plek en in de maat van het model (silhouet = 2×-reductie van het model, afwijkingen ≤ 1 px en per pixel gelogd in r1–r9). Licht linksboven consequent, 9 kleuren, rand-zwart 42,7 % (Abra 40,3, Kadabra 40,8, Sneasel 41,5). De enige echte slordigheid die nog op 8× opviel, was de knoop op de rechterschouder (Jordi's punt); die is weg. De drukte in de rechterhand en de vlekjes zitten in het model en blijven.

## Schaduw
- Licht linksboven: kop h/b links, s rechts; platen 3 met 1 rechts/onder; linkerarm lichte band links; staart licht aan de binnenkant van de lus. Geen pillow shading (hooglicht kop (21–25, 22–26) linksboven, zoals het model).
- Slagschaduw onder het lijf (staartaanzet (45–49,46–47) K, dij 3/1) klopt.
- Banding: niet gevonden (de snuitbanding van r7 is in r7 al opgelost).

## Kleuren
- 9 kleuren + transparant, palet en indexen gelijk aan r7 A/r8. Huid h/b/s + T (lichte selout) + L (lijn); platen 3/2/1; K. Geen nieuwe tinten in r9.
- Kleine tintclusters < 3 px: 67, alle 67 al in r7 A en door de r7-keurder tegen modelblokken gecontroleerd (vlekjes/knokkels, "behoud die vibe"); r9 voegt er geen toe en haalt er 2 weg.

## Belijning
- 1 px; geen 2×2-zwartblokken; geen vulkleur op de rand; geen randpixel die alleen tussen de andere lijnkleur ligt (script).
- Rand: K 106, L 103, T 39 (r9). Zwart onder en tegen de donkere platen, L/T aan de lichtkant en op de handen/voet, zoals het Abra/Kadabra-recept van r8.
- Zwart totaal 17,4 % (Abra 18,0, Kadabra 18,7).
- Rechte stukken in de omtrek (≥ 4): rechts x35 rij 20–23 (kop, model ook recht), x45 rij 29–33 (schouderbult, = model), x44 rij 34–40 (lijf, r9) / rij 34–38 (r9_curve), x43 rij 40–44; links x20 rij 25–33 (kop links, r9; r9_curve 6), x18 rij 19–22 (oor), x24 rij 36–39. Allemaal recht in het model op natieve resolutie (r8 LOG §2); de curve-variant is Jordi's keuze.

## MOET (uitgevoerd in `maak_r9.py`, beide versies)
| # | pixels (x,y) | nu → | reden |
|---|---|---|---|
| 1 | (46,31) | K → transparant; (45,31) 1 → K | spijkertje: 1-px-punt in de schouderbocht ("nooit een punt in een curve"); model is daar een halve pixel (46,5). Rand x45 rij 29–33 = de bult van het model |
| 2 | (44,33) | L → K; (44,32) K → 1 | dubbele lijn: losse L tussen plaatnaad en buitenlijn; model hier één zwarte massa. (44,32) naar plaatvulling om een 2×2-zwartklont te voorkomen |
| 3 | (43,35) | K → 1 | (43,34) was een 1-pixel plaattint ingesloten door 4 × K; model (43,35) half vulling: lijfstrook x43 loopt door tot de naad |
| 3b | alleen r9_curve: (45,34) | K → transparant; (44,34) 1 → K | uitsteeksel onder de schouder, buiten het model (rij 34 = 44,75); anders 6 recht op x45 |

## MAG (bekeken, niet uitgevoerd)
| # | pixels | voorstel | waarom niet |
|---|---|---|---|
| a | (22–27,20) | kopbovenkant met een dipje (6 vlak) | model: 20,0–20,5, de dip is een halve pixel; 6 vlak is de nette vertaling (ook echte Abra heeft een vlakke kruin) |
| b | (32–43,60) | binnenrand staartlus minder vlak (12 T) | model 60,0–60,5 over dezelfde breedte: echt vlak; een dip maakt de staart 1–2 px dun |
| c | (38,27)(39,27) | → 1: dubbele zwarte bovenrand van de rechterplaat vereenvoudigen | model heeft daar een donkere rand + naad (KK/K1 op 27,0): het is de opstaande rand van de plaat, geen ruis; leest op 1× als donkere bovenkant |
| d | (40,34) K → 1, (40,35) L → K | plaatonderrand 4,2,2 i.p.v. 3,3,2 (model ±4,3,2,1) | raakt de bovenkant van de rechterarm (L-rand); winst kleiner dan het risico, 3,3,2 loopt al geleidelijk |

## Ter info voor Jordi (ontwerp, niet uitgevoerd)
- De schouderpunt is nu iets ronder/stomper dan in het model (model steekt een halve pixel verder uit op rij 30–32). Wil je hem spitser: (46,30) en (46,31) allebei K (punt van 2 px hoog) is de Gen 3-manier; één pixel geeft weer een spijkertje.
- Keuze r9 of r9_curve staat nog open (kop links / lijf rechts / linkerarm binnen / rechterarm); de schouder is in beide gelijk.

## Na uitvoering
r9: 5 px, silhouet −1; r9_curve: 7 px, silhouet −2; ogen ongewijzigd; rand-zwart 42,7 / 42,5 %; zwart totaal 17,4 / 17,3 %; 9 kleuren. Op 8× en 12× naast het model nagekeken (`schouder.png`, `vel.png`): de schouder is één ronde plaat met een doorlopende naad, geen losse of uitstekende pixels meer.

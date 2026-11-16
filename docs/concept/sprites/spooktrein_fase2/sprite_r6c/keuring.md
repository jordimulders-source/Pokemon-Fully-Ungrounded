# Keuring spooktrein fase 2, sprite_r6c (16 nov)

**Oordeel: FAIL (dichtbij, alleen kleur).** Hoofdvraag: ja. Op 1× en 2× leest hij als een nette Gen 3-sprite van het model, naast haunter, banette, shuppet en magneton. Pose, wagen, wielen, scheuren, vuist, wolk en spookwiel kloppen. Silhouet en buitenlijn zijn in orde: selout (5) aan de lichtkant, zwart rechts en onder, en de wolk heeft nu een donkere onderrand. Het gat tussen de arm en het lijf (x22–24, y19–21) is trouw, want het model is daar wit. Twee meetbare punten houden hem nog tegen, allebei zonder vormwijziging op te lossen.
Niet beoordeeld: het gezicht (x25–41, y9–26), de weggegumde onderdelen en de staart.

Helderheid per index: 2=217, 6=203, 3=174, 11=162, 4=142, 7=137, 12=123, 10=107, 5=103, 8=100, 13=68, 9=55, 1=33.

## Reparaties
1. **Spookwiel als zebra (x21–31, y47–55)**: het wiel bestaat uit kolommen van 1 px die afwisselen tussen 3 en 5 (bijvoorbeeld rij 50 `bbddbbdbdd`, contrast 71). Het model is daar een egaal middengroen (gemeten 120–160), met alleen de ring en een paar lijnen licht (≥165). Eis: geen dambord of zebra, en de tint volgens het model. Neem het model over door 35 pixels van 5 naar 4 te zetten: (25,47),(30,47),(21,48),(24–26,48),(28–29,48),(23–26,49),(28–29,49),(23–24,50),(27,50),(29–30,50),(23–24,51),(27,51),(23–24,52),(26,52),(28–29,52),(21,53),(24–26,53),(24–25,54),(23,55),(28,55). Laat 5 staan waar het model < 115 is: (30,49),(21,54),(21–22,55).
2. **Flank met twee bijna gelijke donkere tinten (x24–52, y26–48)**: hier staan 13 (98 px) en 9 (71 px) door elkaar. Ze verschillen 13 in helderheid, en het model is op beide plekken even donker (mediaan 58 tegen 60). De eis is ±30–40 per stap. Kies in de flank één donkere tint: 9 op de randen en de onderkant, 13 voor de staanders en banden, of één van beide overal. Het r5-punt 2 is hiermee nog niet opgelost.
3. **Roest tegen het planksbruin**: 10 (107) tegen 8 (100) scheelt na de paletwijziging van r6c nog maar 7. In r5 was dat 16. De twee raken elkaar weinig (10 zit op de voorkant, 8 op de flank), maar waar ze samenkomen ontstaat ruis. Zet 8 terug naar ±91 (of donkerder) of 10 lichter, zodat het verschil ≥ 30 wordt. Meet daarna de flank opnieuw: nu sprite 108 tegen model 94.
4. **Kleine snippers (< 3 px, 8-verbonden, geen scheur)**: 9 op (20,39–40), (13,43), (5–6,43), 4 op (43,40), (51–52,41), (44,43–44), (46,60) en 3 op (9,29), (29,38), (35–36,44). Laat ze opgaan in het vlak eromheen, volgens het model.

## Punten uit r5
Opgelost: 1 (lichtkant van de vuist is nu 5), 4 (de wolk heeft een zwarte onderrand), 5 (rechterkant van de kop nu 167 tegen model 179, dus niet meer te licht), 6, 7 (grotendeels).
Deels opgelost: 3 (de banden in de flank zijn 9→13 gezet; de spikkels van 9 op de wagenrand vallen in de gezichtsbox).
Niet opgelost: 2 (contrast 13/9, en 10/8 is slechter geworden, zie punten 2 en 3).

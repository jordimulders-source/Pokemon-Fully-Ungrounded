# Poedelmot: kleur r12

Gebouwd vanaf r11. Alleen drie zones zijn aangepast; de rest is bevroren (diff buiten de zones = 0, alpha-diff 0). Handgetekende rijen staan in `stappen/legs12.py` en `stappen/spriet12.py`, toegepast met `stappen/apply.py`.

## Gedaan
1. **Voorpoten A/B**
   - Het witte kraagplukje uit r11 is weg (zat niet in het model).
   - Kraagpunt op (20–22,48–49) in crème, met een aansluitlijn (20–22,50) waar beide poten onder de kraag vandaan komen.
   - Aanzet van A: lijn (16–17,48) → (18–19,49) → (20,50).
   - Aanzet van B: boog (23,49) → (24–28,48).
   - De overlaplijn van A over B staat alleen op x21 (y51–54).
   - B ligt achter A en is aan zijn linkerkant crème (schaduw). Beide pluimen hebben een crème/tan schaduw aan de onderkant en rechterkant; licht linksboven.
   - Klauwtjes: die van r10 (2 per poot, donkerbruin, schuin).
2. **Middenstuk**
   - Koel grijze plaat (nieuwe tint 8 = 172,160,156) met donkergrijze schaduw onderaan (9 = 124,112,110). Beide palet-slots waren ongebruikt.
   - Dunne segmentlijnen op x30, x34 en x40, plus een plukkerige kraaglijn op y48 (witte punt op x33).
   - Het tan vlak is nu alleen de kleine plaat 35–39 × 49–52, met schaduw (5) onder, op de plek waar C eroverheen valt.
3. **Rechterspriet**
   - De nerf is een vloeiende boog: per rij 1,1,1,1,2,2,2,2,3,4,4 px, zonder terugstap.
   - De ribben zijn opnieuw uitgelijnd op de nerf (steil, 1 px), met korte tikjes erboven.

## Controle (`controle_uitvoer.txt`)
Alle checks schoon:
- alpha-diff 0, open randen 0
- losse pixels 0, clusters < 3 px 0
- indexen 123456789ABC

## Zwakke punten
- **Ribben:** niet fijner dan in r11. Periode 3 is op 64 px het minimum; met periode 2 worden het blokjes of een schaakbord. Op 12× lezen ze nog grover dan in het model.
- **Klauwtjes:** niet herzien. Ze blijven stipjes van 2–3 px op de vaste silhouetrand.
- **Pose:** A/B lezen beter als poten onder de kraag, maar het "schuin naar linksonder hangen" komt vooral uit het bevroren silhouet. Binnen de omtrek kon alleen de schaduw dat versterken.
- **Paletrol:** 8/9 hadden in r9 een andere rol (8 grijsroze klauwschaduw, 9 vleugelcrème). Ze waren in r11 ongebruikt en zijn nu hergebruikt voor het middenstuk.
- **Keuring:** niet onafhankelijk gekeurd.

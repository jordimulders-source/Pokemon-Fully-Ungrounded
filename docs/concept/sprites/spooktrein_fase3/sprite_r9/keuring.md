# Keuring spooktrein fase 3, r9 (16 nov, verse keurder)

**Oordeel: FAIL** (trein zelf; hoofdpunt is de schoorsteen). Al het groen is volgens Jordi goed ("al het groen is goed nu, nu de trein zelf nog") en bevroren: geen punten op groene pixels (2,3,4,5,6,13).

## Hoofdvraag
- 1×/2×: leest als één Pokémon, pompoenkop-locomotief met grijns, geest uit de schoorsteen, rook en spookwielen. Past naast Gengar/Haunter/Magcargo/Claydol qua formaat (vult wel 64×64 helemaal).
- **Schoorsteen te kort/dik: ja.** Model: rand + een duidelijke pijp eronder (natief: rand r21-24, pijp r25-29 = 5 rijen, van 13 naar 10 px versmallend). r9: rand y14-17 (1-op-1, goed), pijp maar y18-19; y20-21 zijn de pijpkolommen x15-18 al roestbruin (8) en lezen als ketel. Daardoor zit de rand plat op de kop.
- Kopvorm: model is een ronde pompoen; r9 heeft links een rechte muur (x0 van y30 t/m y47), het model raakt x0 alleen op y33-39 en springt bij y43-47 in naar de koeienvanger.
- Koeienvanger en roestplaten: vereenvoudigd zoals toegestaan ("wat simpeler").

## Metingen (ijzer)
- Buitenlijn ijzer: linksboven 9/12/11 als selout (18/6/1), zwart 3; rest 23 zwart, 9 gekleurd: klopt.
- Roest 7/8/9, grijs 10/11/12 + zwart: binnen de norm.
- Schoorsteen = dambord van 1-px tinten (7/10/11/12/9 door elkaar, y15-19 x12-21).

## MOET (allemaal ijzer; script `keuring_moet.py`, resultaat `keuring_voorstel.png`)
**A. Schoorsteenpijp verlengen en opschonen (model: lichte linkerkant, naad, donkere rechterkant)**
1. Pijp loopt door op y20-21: (14,20) 1→11, (15,20) 8→7, (16,20) 8→10, (17,20) 8→10, (18,20) 8→1; (15,21) 1→11, (16,21) 8→10, (17,21) 8→10, (18,21) 8→1. (x19-21 en de schaduwrij y22 blijven.)
2. y19: (13,19) 12→11, (15,19) 10→7, (16,19) 11→10, (17,19) 11→10, (18,19) 9→1 (naad doorlopen zoals y18 x18).
3. Rand, lichtkant selout i.p.v. donkerste grijs: (12,15) 12→11, (13,15) 12→11, (11,16) 12→11; (13,16) 10→7.
4. Ring y17 egaal: (13,17) 7→10; (21,17) 9→12.

**B. Kop links rond (naar het model)**
5. y30-32: x0 9→0, x1 8→9.
6. y40-42: x0 9→0.
7. Insnoering kop/koeienvanger: (0,43) 1→0, (1,43) 8→1; (0,45),(0,46),(0,47) 1→0; (1,47) 9→1.

## MAG
- Koeienvanger (y48-59): model heeft 4-5 smalle bladen met roest ertussen en een iets smaller geheel onder de kop; r9 heeft 3 brede grijze platen met rechte zwarte kolommen x4/x11/x17 over 10 rijen (zuilen). Eén extra naad of roest (8/9) per plaat zou dichter bij het model komen.
- Grote lichte plaat linksboven (7, x3-9 y22-31) is groter en lager dan in het model (x6-11 y20-25 licht, daaronder grijs): onderste rijen y28-31 x3-7 naar 10.

## Ter info voor Jordi
De pijp kan niet langer dan y18-21 zonder het (bevroren) groen of de kop te verschuiven: de geest staat al op y0. Wil Jordi de hoge pijp van het model, dan moet de hele trein ±2 rijen zakken of krimpen.

Vel: `keuring_vel.png` (r9 | r9 + MOET | model, 7× en 1×/2×).

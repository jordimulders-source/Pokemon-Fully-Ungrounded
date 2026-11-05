# Keuring kleur ronde 4 (verse, onafhankelijke keurder, 2 nov)

Gekeurd: `ronde4.png` / `ronde4.txt` / `ronde4.pal` (+ `vel_ronde4.png`) op 1x, 2x, 3x en 8x, op licht (236) en donker (32,32,40). Naast de render `silhouet_v2/onderlaag_s1a_256.png`, het bevroren silhouet `direct_s1a.txt`, de lijn (`fase1_olinguito.png`, `fase2_coathief.png`) en 12 echte sprites (anim_front frame 1 + normal.pal): zangoose, sneasel, linoone, zigzagoon, ursaring, teddiursa, furret, sentret, mightyena, raticate, absol, sandslash. Eerst zelf geoordeeld; `KEURING_ronde1.md` en `NOTITIES_ronde4.md` pas daarna gelezen. De maker noemt zelf staarthaak, bovenarm, zakmond en nabije klauw als zwak; dat zijn dezelfde punten die ik vond (zelfgenoemd zwak = fail, SPRITE_NORM).

Coördinaten (x, y), 0-geteld zoals in `ronde4.txt`; paletindex als hexteken. Bevroren (niet als FAIL gerekend): warmer grijsbruin, crème handen/klauwen, verre oog, buidel eigen bruintint, borst, klauwvorm, masker, pose, silhouet.

**Uitslag: FAIL (6 van 10).** Sterk: de kop leest op 1x direct als wasbeer, de pose leest, de verre klauw is een leesbaar paar met inkeping, de omlijning is Gen 3 (4 aan de lichtkant, zwart aan de schaduwkant), het oog is een echt Pokémon-oog, en de lijn klopt (rood oog, crème klauwen, ringstaart; gemiddelde luma 88 tegen Coathief 80, olinguito 71). Wat faalt is hetzelfde rijtje als in ronde 3: de nabije hand/arm, de staarthaak, de zakmond en te weinig hooglicht. Ronde 4 veranderde alleen het palet en 17 staartpixels.

| # | Punt | Oordeel |
|---|---|---|
| 1 | Alpha-diff 0, randen, losse pixels, ruis | **PASS** |
| 2 | Kop en oog | **PASS** (neus: voor Jordi) |
| 3 | Klauwen leesbaar 1x/2x | **FAIL** (verre ok, nabije = crème klodder op de crème buik) |
| 4 | Buidel als dievenzak | **FAIL** (leest als zak, maar de opening niet op 1x) |
| 5 | Volume | **FAIL** (verre dij één vlak 5, weinig hooglicht op romp) |
| 6 | Selout/omlijning | **PASS** |
| 7 | Staart: ringen, haak | **FAIL** (haak = donkere knots op 1x/2x) |
| 8 | Leesbaarheid 1x | **FAIL** (bovenarm onzichtbaar, onderarm = zwart vierkant) |
| 9 | Palet, contrast, hue shift, lijn | **FAIL** (7 en 8 zijn dezelfde kleur; hooglicht 4,5% van de sprite) |
| 10 | Afgekeurde dingen | **FAIL** (indruk "klauwen uit de buik" via de nabije hand) |

## 1. Alpha, randen, ruis: PASS
- Alpha-diff met `direct_s1a.txt`: **0** (1682 px); txt = png (0 verschillen).
- Randpixels: alleen 1, 2, 4, b, c naast transparant; geen lichte tint aan de rand, geen anti-aliasing aan de buitenkant.
- Geen losse pixels (geen pixel met ≤ 2 buren).
- Kleinigheid (geen fail): (51,20) een losse 8 in de donkere staartkop leest als spikkel; verdwijnt met reparatie 4.

## 2. Kop en oog: PASS
- Nabij oog (20–22, 11–12): zwart bovenlid (19–22, 10), iris donker boven (e) en licht onder (f), glans a op (20,11) linksboven. Dat is een Pokémon-oog, geen stip; op 1x een rood-oranje puntje in het masker, zoals bij olinguito en Coathief (lijn ok).
- Masker over de neusrug, stopt achter het oog (x 25), witte wenkbrauw en snuitrand, oren met lichte binnenkant en een selout van 4: ok. Licht linksboven op de schedel (3 op (14–18, 5)): ok.
- Twijfelpunten die het bevroren masker raken (dus niet als FAIL): zie Voor Jordi 1 en 4.

## 3. Klauwen: FAIL
- **Verre klauw (x 5–16, y 33–45): PASS.** Twee klauwen tegen elkaar, inkeping alleen bij de punt (x 9, y 42–45), c-selout aan de lichtkant, 1 aan de schaduwkant, vast aan de donkere onderarm. Leest op 1x en 2x.
- **Nabije klauw (x 21–27, y 26–34): FAIL.** Vorm volgt de bevroren klauw (twee klauwen x 22–23 en 25–26, inkeping (24, 32–33)), maar de klauwen zijn 9/8 en de buik er direct onder ((21–27, 35–37)) is ook 9/8. De zwarte punten op y 34 zijn het enige wat ze scheidt. Op 2x en 1x: een witte rechthoek met twee zwarte streepjes ("tand"/dobbelsteen), geen klauwen. De rug van de hand ((24–27, 26), (23–26, 27)) is a, de lichtste kleur van de sprite: de hand trekt alle aandacht maar heeft geen vorm.
  - Reparatie (alleen kleur): rug van de hand a → 9 behalve (24,26) (één glans); slagschaduw van de hand op de buik: (21,34) 9→8, (24,34) 9→8, (21–26,35) 9→8, (27,35) 8→7. Dan staan de twee klauwpunten op een donkere rand en lezen ze als twee punten. (Raakt de bevroren borst alleen als schaduw; Claude toetst.)

## 4. Buidel: FAIL
- Leest als bruine dievenzak op de rug (goed), sluit onderaan geleidelijk aan op de rug ((33–38, 32–35) 5/4 → b, goed), plooi d van (36,25) naar (42,29) leest als vouw. Geen jetpack.
- **Opening:** de zakmond is alleen (36–38, 19) 2 onder de bovenrand (36–39, 18) 1: één rij van 3 px. Op 1x een streepje, op 2x nauwelijks (maker: idem).
  - Reparatie: (36,20) en (37,20) d → 2, zodat de mond 2 rijen diep is aan de schouderkant en naar rechts ondieper wordt; lip d op (38–41, 20) houden. Eventueel (35,19) 1 houden en (35,20) b → 1 als mondhoek.

## 5. Volume: FAIL
- Romp: 3/7 linksboven ((16–20, 21–22), (16–19, 23–26)), 6 midden, 5 rechts: licht klopt, maar het hooglicht is een klein blok tegen de rand; het midden van de romp (x 19–28, y 21–33) is één vlak 6.
- **Verre dij (x 16–28, y 39–50):** 76 px egaal 5 binnen een rand 4, zonder één tweede tint. Op 2x/8x een plat bruin vlak, groter dan de nabije dij. Gen 3 houdt verre poten in de schaduwtint, maar geeft ze wel een lichtrand (Mightyena, Zangoose).
  - Reparatie: een 1-px lichtrand 6 langs de bovenkant van de verre dij: (22–24, 40), (21–23, 41), (20–21, 42), (19, 43); rest 5.
  - Romp: 7 als zachte boog verder het lijf in: (19–21, 23–27) 6 → 7 (alleen waar het nu 6 is), zodat het hooglicht de bolling volgt in plaats van een randstrook.

## 6. Selout/omlijning: PASS
- Lichtkant: 4 langs romp (x 15, y 21–28), schedel en oren (12–14, 1–7), crème c langs de verre hand; schaduwkant en onderkant 1. Donkere delen (masker, staart, onderbenen) zwart met 4 binnenin: de overgang uit de Dragonfly Cave-gids. Zwart-aandeel van de rand 0,69 (Sentret 0,67, Mightyena 0,79): binnen de Dark/Gen 3-band.

## 7. Staart: FAIL
- **Haak (x 48–57, y 18–29):** de terugkrullende punt (48–50, 22–28) is van de schacht gescheiden door een 1-lijn op x 51 naast 2/4: donker op donker. Op 1x en 2x is de staartkop één donkere knots (maker: idem). Een haak zonder opening in het silhouet leest alleen met een lichte band over de bocht (Furret, Sentret: lichte ringen lopen over de krul).
  - Reparatie: lichte ring over de bocht: (51,20) 8→9, (52,20) 4→a, (53,20) 4→9, (54–55,20) 2→8, (51–52,21) 4→9, (53–54,21) 2→8; randpixels blijven 1/4. Binnenlijn x 51 (y 23–27) houden, maar de schacht ernaast (52, 23–27) 4 → 5, zodat de lijn contrast heeft; punt (49, 22–27) 4 houden als lichtkant.
- **Ringen:** de bovenste lichte ring (50–56, 30–33) buigt (∩ aan boven- en onderkant), de onderste lichte ring (44–52, 36–45) heeft rechte schuine grenzen (parallellogram). → de grenzen van de onderste ring in het midden 1 px hoger dan aan de randen, in dezelfde richting als de bovenste ring.

## 8. Leesbaarheid 1x: FAIL
- Leest: wasbeerkop, sluipende pose op 2 poten, verre klauw, zak op de rug, ringstaart, donkere onderbenen, nabije voet op de tenen.
- **Bovenarm (x 30–34, y 21–28)**: de streep 4-7-6-5-4 verdwijnt op 1x in de romp (vacht op vacht; maker: idem).
  - Reparatie: (31, 21–24) 7 → 3, zodat de arm een eigen hooglicht heeft dat lichter is dan de romp ernaast.
- **Onderarm (x 28–33, y 28–33)**: 6x6 vrijwel egaal 2 = een zwart vierkant naast de witte hand ("dobbelsteen").
  - Reparatie: bovenkant als lichtkant: (28–31, 29) 2→4, (28–29, 30) 2→4; elleboog (33, 29) 2→4; de 1-rij onderaan (29–33, 33) houden. Dan leest het als een schuine buis van elleboog naar pols.

## 9. Palet: FAIL
- Warm grijsbruin, lumastappen vacht 58 / 86 / 114 / 145 / 182 (±30, gelijk aan Zigzagoon). Hue shift: schaduw naar rood (h 21–26), licht naar geel (h 34–37), verzadiging hoger in de schaduw: correct en passend bij Gen 3-bruin (Ursaring, Zigzagoon). Crème a→9→8 schuift naar oker: ok. Buidel b/c/d eigen roodbruin: ok. Familie met de lijn: ok.
- **7 (162,142,116, luma 145) en 8 (172,150,118, luma 153)** verschillen 8 luma en 2° tint: twee paletplekken met dezelfde kleur (Dragonfly-regel 1). Waar de crème schaduw de grijze hooglichtkant raakt (buik/dij (27–29, 34–37)) vloeien ze in elkaar.
  - Reparatie: 8 echt oker maken (±184,146,96: zelfde luma, verzadiging ±0,48 tegen 0,28 van 7), of 7 lichter grijs (±174,158,134).
- **Hooglicht te schaars:** 7 + 3 = 76 px (4,5% van de sprite); Zigzagoon 28%, Linoone ±45% in de twee lichtste tinten. SPRITING §5: te weinig hooglicht = te donker/dof. Opgelost met reparaties 5 en 8.

## 10. Afgekeurde dingen: FAIL
- Niet terug: grijs blok, jetpack, rechthoekig bruin vlak, horizontale pose, traan, trapjes, koevoetarmen, willekeurige binnenlijnen. Goed.
- Wel (twijfel = FAIL): op 1x is de bovenarm onzichtbaar en de onderarm een zwart vlak, dus de witte nabije hand lijkt op de buik geplakt: dezelfde indruk als "klauwen die uit de buik steken". Opgelost met de reparaties bij 3 en 8.

## Belangrijkste reparaties (volgorde)
1. Nabije hand: a → 9 op de handrug, slagschaduw 8 onder de klauwpunten (21–27, 34–35).
2. Nabije onderarm (28–33, 29–30) bovenrand 2 → 4, elleboog (33,29) → 4.
3. Bovenarm (31, 21–24) → 3.
4. Staarthaak: lichte ring over de bocht (51–55, 20–21), schacht (52, 23–27) → 5.
5. Zakmond (36–37, 20) → 2.
6. Verre dij: lichtrand 6 (19–24, 40–43).
7. Romp: 7 verder naar binnen (19–21, 23–27).
8. Palet: 8 → oker (±184,146,96) of 7 lichter.

Elke reparatie is kleur binnen het silhouet (alpha-diff blijft 0); samen ±45 px.

## Voor Jordi (geen opdracht aan de maker)
1. **Neus:** neus en masker zijn allebei zwart en versmelten (10–12, 11–13); de snuit eindigt in een zwarte klodder. Een eigen neus (2 met één 4-glans, 1 px los van het masker) of zo laten (masker over de neusrug was jouw wens)?
2. **Slagschaduw onder de nabije hand** (reparatie 1) raakt de bevroren borst, maar alleen als schaduw van de hand. Akkoord?
3. **Lichte ring over de staartbocht** (reparatie 4) verandert het ringpatroon bovenaan (in de render is de haak donker). Akkoord, of mag de haak donker blijven en als knots lezen?
4. **Witte wenkbrauw** (19–25, 8–9) is een rechte balk van 7 px; samen met het lichte schedelvlak, het zwarte masker en de witte snuit leest de kop op 2x als horizontale banden (helm-risico). Valt onder het bevroren masker: zo laten of de wenkbrauw 1 px laten buigen boven het oog?
5. **Buideltint** ligt dicht bij Coathiefs vacht (maker noemt het): bewuste knipoog naar de vorige fase of liever donkerder/roder?

# Guaraná fase 2, ronde 6 (verse maker): afwerking in de stijl van fase 1

Jordi (letterlijk) over r4/r5: "links is wat netter, moet nog steeds wel wat meer afgewerkt worden, kijk naar hoe fase 1 kleuren en schaduwen etc doet".
Over r5 (via coördinator): "grotendeels prima, maar hier en op andere plekken heb je horizontale lijnen getrokken over de hele plant heen"
(aantekening `sprite_r5/jordi_horizontale_lijnen.png`: middelste tros rond de half dichte ogen M2/M3).

Bestanden: `guarana2_r6.png` + `normal.pal`, `vel.png` (r6 | r5A | fase 1 op 8×; trossen 12×: r6 | r5A | model op schaal; 1× op licht/donker),
`voor_jordi_r6_8x.png` (r6 | fase 1, 8×, wit), `toets.png` (r6 | fase 1 | Dundragoon | Skinguin op 8×, eigen toets).
Bouwen vanuit `guarana_fase2/`: `python3 sprite_r6/fid.py && python3 sprite_r6/eig.py && python3 sprite_r6/bouw6.py && python3 sprite_r6/vel6.py`.
Meten: `strepen.py SPRITE` (horizontale donkere rijen), `ruis.py SPRITE...` (losse pixels), `dump.py SPRITE x0 x1 y0 y1` (raster + oog + eigenaar),
`zoomc.py` (uitsneden). Hergebruikt uit r5: `gemeen2.py`, `klassen2.py`, `kaal.py`, `schaduw.py`, `vrucht.py`, `vruchtseg.py` (vruchtellipsen = dezelfde vormen als r3–r5).

## 1. Hoe fase 1 het doet (gemeten op `guarana/af/guarana.png`)
Palet fase 1 = index 0–11: rood lijn (120,28,32) / schaduw (176,56,48) / midden (224,80,56) / licht (240,136,104); groen lijn (58,86,46) /
schaduw (84,122,64) / midden (122,160,80) / licht (166,198,108); zwart; oogwit. Per materiaal 3 tinten + 1 lijn, geen 4e tint, geen glans apart.
- **Rode vrucht** (vruchten ±5 px): vulling 55 % midden, 28 % schaduw, 17 % licht. Midden is de basis. Licht = één blokje van 2–4 px in de
  linkerbovenhoek, direct onder/naast de lijn. Schaduw = sikkel van 1 px breed langs de rand rechtsonder (tegen de naad of de zwarte buitenlijn),
  soms diagonaal. Naden tussen vruchten 1 px lijnrood (outline base); vrucht is aan alle kanten omlijnd, dus elke vrucht leest los.
- **Groene rank** (buis ±6–7 px breed): 51 % midden, 27 % schaduw, 22 % licht. Licht als brede baan aan de linker-/binnenkant van de buis
  (2–4 px), midden in het midden, schaduw 1–2 px rechts/onder. Dunne krullen = 1 px lijngroen.
- **Blad**: fase 1 heeft geen blad.
- **Oog**: wit 3-5-5-5-3 rond (onderkant '..KKK..' 3 px), pupil 2×2 zwart; rand linksboven lijnrood (selout), rechts/onder zwart (in fase 2
  variant A: lijnrood, Jordi's keuze).
- **Lijnen**: zwart alleen op de buitenlijn aan de schaduwkant (rechts/onder); lichtkant lijnrood/lijngroen; binnenlijnen nooit zwart.
- **Rust**: 18 losse pixels in de hele sprite (meest lijnpixels in krulletjes), 6 tintvlakjes < 3 px. Grote rustige vlakken.

## 2. Wat ik op r5A deed
Bevroren en met asserts bewezen: **alpha-diff 0** (silhouet), **buitenlijn diff 0**, **pupillen diff 0**. 487 px anders dan r5A, alle binnen
het silhouet. Palet = **exact fase 1** (index 0–11, 12 kleuren incl. transparant; 12–15 leeg): glans (12), diep rood (14), tussengroen (13)
en diep groen (15) vervallen.
- **Rood, per vrucht** (vrucht = r5-vlak tussen de naden, gesplitst per vruchtellips uit `vrucht.py`): midden als basis, hooglichtblokje
  2–6 px linksboven (groeit vanuit de lichtste pixel; toon = bolnormaal + 10 % modelhelderheid), schaduwsikkel ±25 % langs de rand
  rechts/onder. Achterste (geplakte) vruchten een stap donkerder: schaduw als basis, midden als hooglicht. Naden van r5 blijven.
  Rood nu S/M/H 37/47/16 % (fase 1 28/55/17; meer schaduw door de achterste vruchten).
- **Groen, per deel** tussen de groene lijnen: buis zoals de fase 1-rank (normaal uit het vervaagde deelmasker, licht linksboven,
  + modelhelderheid): schaduw/midden/licht ±28/44/28 %; donkere strengen in de twist (model donker) alleen schaduw + midden.
  Blad: lobtinten van r5 (uit het model) behouden, 13/15 → schaduw; lichte lobben ≥ 3 px kregen hooglicht aan de lichtkant (17 px).
  Groen nu s/m/h 29/46/26 % (fase 1 27/51/22).
- **Losse pixels**: vulpixel zonder gelijke buur in hetzelfde vlak → buurtint (diagonale sikkelpixels mogen, zoals fase 1).

## 3. Horizontale strepen (Jordi r5): gevonden en opgelost
`strepen.py`: rijen ≥ 3 px donker (zwart/lijnrood/diep rood/lijngroen) binnen het silhouet die over een vrucht/oog lopen. r5A: 21, r6: 10.
Gevonden in r5A:
- **Middelste tros, rij 18 x21–27** (de omcirkelde): diep rode sikkel van de achterste vrucht (x21–24) + platte onderrand van het half
  dichte oog M2 (x25–27) = 7 px streep. Daarboven rij 16 x24–34: naad + ooglid M2 + zwart + onderrand M1 (4 px plat).
- **Middelste tros, rij 21 x21–23**: platte onderrand van het half dichte oog M3, aansluitend op groen.
- **Linkertros, rij 26 x13–17**: onderrand oog L2 (4 px plat) loopt door in de rand van L3; rij 28 x7–10: platte onderrand half dicht oog L1.
- **Rechtertros, rij 26 x47–56**: onderrand R1 (4 px) + ooglid R4 + onderrand R2 (4 px) achter elkaar.
- Kleinere: naadpixels die een oogrand horizontaal verlengden op (52,25), (12,27), (20,27), (16,28), (18,29), (53,32), (13,33), (22,25).
Oplossing (pupillen en oogwit bovenin onaangeroerd):
- **Half dichte ogen L1, M2, M3, R4**: ooglid bovenaan blijft; de platte onderrand wordt een halve maan ('.KWWK.'/'..KK..', smal '.KWK.'/'..K..'),
  zodat het lid een korte boog op zijn eigen vrucht is. 2 px oogwit + 2 px rand erbij per oog (8 nieuwe px in de vrucht eronder).
- **Middel-ogen L2, M1, R1, R2**: onderste witrij kreeg randhoeken, onderrand van 4 naar 2 px ('.KWWK.'/'..KK..'), zoals het fase 1-oog;
  de vrijgekomen hoekpixels zijn vrucht.
- Naad/diep rood dat een oogrand horizontaal verlengt → vrucht; diep rood vervalt helemaal.
Wat overblijft (10): binnen één oog (pupil + rand, 3 px onderrand van grote ogen zoals fase 1: rij 14, 23, 24, 25, 33), twee grote ogen
rechts die elkaar raken (rij 34 x47–50, 4 px), een korte naad van 3 px tussen twee vruchten (rij 27 x28–30), de aanzet van de stam onder
de middelste tros (rij 30 x24–27) en de dunne horizontale tak naar de rechtertros (rij 21 x35–41: 1 px lijnrood + lijngroen, tak van 2 px
dik die alleen uit lijn bestaat, al sinds r4).

## 4. Eigen toets op 8× (naast fase 1, Dundragoon, Skinguin: `toets.png`, `vel.png`)
- Zelfde palet en dezelfde tintlogica als fase 1: leest als dezelfde lijn. Stam en ranken zijn nu buizen met licht links en schaduw rechts
  (r5: lappendeken van 4 groentinten). Glans-oranje (12) is weg, hooglicht zit als blokje linksboven per vrucht.
- Strepen door de trossen zijn weg; de half dichte ogen lezen als lid + halve maan.

## Wat nog afwijkt
- **Trossen blijven drukker dan fase 1**: 15 ogen en ±40 vruchtvlakken van 3–8 px in 3 trossen; niet elke vrucht is rondom omlijnd
  (de r5-naden volgen de modelvruchten, waar die elkaar overlappen ontbreekt een naad), dus sommige vruchten lezen alleen via de tint.
- **Losse pixels**: 152 tegen 18 in fase 1 (fase 1 is kleiner en heeft geen blad). Het merendeel zijn lijnpixels in diagonale naden en
  1-px vulling in dunne ranken/lobben tussen twee lijnen; vlakjes zijn niet gladgestreken (SPRITE_KERN: rustiger maken ≠ pixelblur).
- **Blad** blijft donkerder en gestreepter dan de rank (lobben van 2 px met lijn ertussen, uit het model).
- Achterste vruchten maken het rood iets donkerder dan fase 1 (S 37 % tegen 28 %); diepte uit het model.
- Ogen: de half dichte ogen zijn nu een halve maan (2 px wit + 2 px rand erbij); dat is een vormwijziging aan het oog op verzoek
  (Jordi r5 via coördinator), pupillen ongewijzigd. Even laten bevestigen dat ze nog "half dicht" genoeg lezen.
- Niet keurder-getoetst.

# Guaraná fase 2, ronde 8 (start van r7)

Jordi over r7 (letterlijk): "Het bovenste oog links en het rechtsbovenste oog rechts mogen naar het midden kijken. 2e oog van rechts rechts ontbreekt
een pupil en midden zitten onder een stukje links wat ook nog niet genoeg herkenbaar is als een oog, midden boven is niet helemaal goed afgewerkt ook,"
en "Voor de rest is de afwerking nog niet zoals fase 1, qua kleur etc toch? dat moet nog gefixed worden, verder is die netjes dus niks aanpassen".

Bestanden: `guarana2_r8a.png`, `guarana2_r8b.png`, `normal.pal` (= fase 1-palet, 12 kleuren incl. transparant), `voor_jordi_r8_8x.png`
(r8a | r8b | fase 1, 8×, wit), `log.txt` (alle handpixels met oud → nieuw).
Bouwen vanuit `guarana_fase2/`: `python3 sprite_r8/bouw6b.py && python3 sprite_r8/bouw8.py && python3 sprite_r8/vel8.py`.
Silhouet: alpha-diff 0 t.o.v. r7 (assert). Pupillen van de overige ogen (r7) ongewijzigd.

## Reparaties
1. **L2 (bovenste oog linkertros) en R2 (rechtsboven rechtertros) kijken naar het midden.** Pupil 3 px (L-vorm, zoals r5–r7):
   - **r8a**: pupil midden in het wit (kijkt recht vooruit);
   - **r8b**: pupil richting het midden van de sprite (L2 naar rechts, R2 naar links).
2. **R6 (rechtertros, onderste rij, 2e oog van rechts) had geen pupil**: de 2×2 van r7 viel samen met de zwarte buitenlijn (één zwarte klont).
   (44,34) weer wit, pupil 2 px op (45,34)(45,35): middenkolom, onderste helft; wit links, boven en rechts. Het oog is door de buitenlijn
   afgesneden (7 px wit), daarom geen 2×2.
3. **Middelste tros, stukje links onder = M3**: gemeten in het natieve model (natief (70,82) → sprite (21,20)): daar zit een **half dicht oog**
   (dik ooglid, halve maan wit, pupil links). Dus oog gehouden en duidelijk gemaakt: het lid was schaduwrood, dezelfde tint als de vrucht erboven,
   waardoor het oog wegviel. Lid + linkerhoek nu lijnrood: `.LLL.` / `LKWWL` / `.LWL.` / `..L..`. Zelfde voor M2 (lid onder de bovenste vrucht).
4. **Middelste tros boven**: de bovenste linkervrucht (x23–28, y12–15) en de vrucht van M1 (x29–32, y11–13) opnieuw ingekleurd als fase 1-vrucht:
   hooglicht linksboven, midden, schaduwsikkel rechtsonder, één naad van 1 px (x29) i.p.v. een dubbele (x28–29); de hooglichten van de
   M1-vrucht stonden rechts, nu links. Een groene lijn over de hele bovenkant gaf een streep van 8 px en is niet gedaan.
5. **Kleur als fase 1**: tint voor tint vergeleken (zelfde palet: lijn/schaduw/midden/licht per materiaal). Achterste vruchten hadden een donkerdere
   set (schaduw als basis) → nu dezelfde tinten als fase 1. Verhoudingen op die van fase 1 gezet:
   rood S/M/H **28/55/17 %** (fase 1 28/55/17; r7 37/47/16), groen s/m/h **28/50/22 %** (fase 1 27/51/22; r7 29/46/26).
   Methode zoals r6 (per vrucht bol met licht linksboven, per groen deel buis), alleen de aandelen veranderd.

## Wat nog afwijkt
- 121 px (a) / 125 px (b) anders dan r7: 30 handpixels (log.txt), 6 pupilpixels, de rest is de kleurverdeling (punt 5) binnen de trossen en groen.
- Trossen blijven drukker dan fase 1 (15 ogen, kleine vruchten); blad houdt zijn lobstrepen uit het model. Losse pixels ±150 (fase 1: 18),
  vooral lijnpixels in schuine naden en 1-px vulling in dunne delen.
- Horizontale donkere rijen ≥ 3 px: 12, allemaal binnen één oog (onderrand/lid van 3 px, zoals fase 1), twee ogen die elkaar raken (rij 34
  x47–50), één korte naad (rij 27) en de dunne tak naar de rechtertros (rij 21).
- Niet keurder-getoetst.

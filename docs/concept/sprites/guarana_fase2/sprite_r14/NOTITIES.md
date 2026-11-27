# Guaraná fase 2, ronde 14 (start r13): trossen groter, vruchten rond

Jordi (letterlijk): "een stuk beter, maar nu zijn een hoop van de vruchten te rechthoekig. En ik realiseer me nu dat het helemaal niet ten koste van de
sprite gaat als de vruchttrossen gewoon wat groter maken, had ons een hoop moeite gescheeld, overlappen is toch niet erg, zolang ze elkaar maar niet overlappen"
+ "ja en er moet iets ruimte tussen zitten, desnoods schuif je de linker maar iets naar links".

Bestanden: `guarana2_r14.png`, `normal.pal` (= r13 = fase 1-palet, 11 kleuren gebruikt), `voor_jordi_r14_8x.png` (fase 1 | r14 | r13, 8×, wit),
`afstand.png` (fase 1 | r14 | r13 op 1× en 2×). Bouwen vanuit `guarana_fase2/`: `python3 sprite_r14/bouw14.py && python3 sprite_r14/vel14.py`.
Hulp: `zoek.py` (welke schalen passen), `controle.py` (diff met r13, ruimte tussen trossen, roodverdeling), `recht.py` (rechte stukken buitenrand),
`dump.py`/`zoom.py` (tekstraster / uitsnede 14×).

## Werkwijze (`bouw14.py`)
- Liaan, takken, lussen, blad en ranken = r13 (0 px anders buiten de trossen, gecontroleerd).
- De oude trossen (rood/wit + hun zwarte rand) gaan eruit; elke tros wordt opnieuw opgebouwd uit de vruchten van het model (`model.png`):
  per vrucht midden, maat, open/half dicht/dicht/peer en volgorde voor/achter afgelezen in modelpixels (tabel `TROSSEN`), via dezelfde ijking als r9–r13
  naar de sprite. Links 8 vruchten (4 oog, 1 half dicht), midden 9 (2 oog, 2 half dicht), rechts 8 (5 oog, waarvan R1 klein).
- Elke vrucht is een ronde vorm met het midden op een pixelmidden (rijen 3-5-7-9-9-9-7-5-3 e.d., peren lopen onderaan taps), 7–9 px.
  Fase 1-stijl: buitenlijn lijnrood linksboven / zwart rechtsonder, naad met een achterliggende vrucht lijnrood (aan de schaduwkant schaduwtint),
  hooglicht linksboven, schaduwsikkel rechtsonder langs de eigen rand, rest midden. Achterste vruchten worden door de voorste afgedekt.
- Ogen = fase 1-oog: rond wit 3-5-5-3 met 2×2-pupil (7×6 met schil), schil lijnrood links/boven, zwart rechts/onder. L2 (B) en R2 (q): wit 2-4-4-2
  met pupil precies in het midden. Pupillen: links (e, s; kleine ogen C en R1 met pupil 2 px), linksonder (D, M1, RT, R5), rechtsonder/onder (F). Half dicht (A, H1, M2): bovenste 2 rijen wit
  worden ooglid (vruchthuid) met een lijnrode lidrand, pupil eronder tegen het lid. Het oog ligt bovenop (de opengebarsten vrucht steekt naar voren).
- Afwijking van het model: open oogvruchten F, u (R5) en q (R2) iets breder (9 px) zodat het fase 1-oog erin past.

## Schaal per tros (sp = posities om de takpunt, sr = vruchtmaat; model→r13-maat = 1,0)
| tros | sp | sr | verschuiving | vrucht | omvang |
|---|---|---|---|---|---|
| links | 1,05 | 1,6 | **5 px naar links** (Jordi: "desnoods schuif je de linker maar iets naar links"), niet omlaag | 7–9 px | x0–17, y21–43 |
| midden | 1,05 | 1,6 | — | 5–9 px (M2/g grotendeels achter) | x19–37, y11–31 |
| rechts | 1,3 | 1,6 | — | 7–9 px | x39–60, y21–46 |
- Vruchten ×1,6 (≈ 8–9 px, fase 1-maat). De posities konden niet ook ×1,6: de onderste vruchten links in de middelste tros (f, g, M2) hangen boven de
  bovenkant van de linkertros. Grootste schaal waarbij links en midden ≥ 2 px uit elkaar blijven = 1,05 (`zoek.py`); rechts is vrij en kreeg 1,3
  (bij 1,4 te ver uit elkaar t.o.v. de andere twee). Daardoor liggen de vruchten links en midden dichter op elkaar dan in het model.
- Ruimte: links–midden 2 px achtergrond, midden–rechts 4 px (de stam ertussen), links–rechts ver uiteen. Onderkant blijft y51 (trossen tot y46).
- De linkertros is alleen als tros verschoven; de groene tak/blad niet (die waren netjes): de tros hangt nog direct onder het linkerblad (bovenkant y21–22).

## Wat is afgedekt
- 138 px groen (blad, takken, lussen, stam) en 41 px zwarte groenrand vallen onder de nieuwe trossen: midden over de onderkant van de lus en het blad
  linksboven, links over het blad onder de linkerlus, rechts over blad en de stam/rank onder de rechtertros.
- 63 px van de oude trossen vallen buiten de nieuwe (vooral rechts van de linkertros, door de verschuiving): achtergrond. 6 losse gaatjes (rondom dicht)
  zijn naad (lijnrood) of donkergroen geworden.
- Diff met r13: 835 px, waarvan 766 in de nieuwe trossen.

## Controle
- Roodverdeling lijnrood/schaduw/midden/licht: fase 1 39/17/34/11 · r13 41,3/16,9/31,8/10,0 · **r14 42,5/16,1/32,3/9,1** (binnen ±3 van 40/15/35/10).
- Geen nieuwe kleuren, geen dithering of blur (vlakke tinten per vrucht).
- `recht.py`: 7 stukken van 4–6 px op de buitenrand (toppen van vruchten tegen het blad, linkerrand bij x0, zijkant van een 9-px-vrucht); niets langer.
- Zelf bekeken op 1×, 2× en 8× naast fase 1 en r13: de ogen zijn weer zo groot als in fase 1 en lezen op 1×/2× als witte ogen; elke vrucht is een
  bol met eigen rand en sikkel. Zwakker: de linker- en middelste tros zijn compacter dan het model (zie schaal), daardoor overlappen de oogvruchten
  daar elkaar deels en wordt de tros wat drukker. Niet keurder-getoetst.

# Hoatzin fase 2, r22 (20 nov): vanaf r21, keurderpunten

`sh alles.sh` (bouw19 → poten22 → kleur22 → check → vel). check.py: dambord 0, om-en-om 0, klonten 0. 16 kleuren.
Silhouet = r21 behalve de poten (rijen ≥ 51). Oog, gezicht, snavel (pixels), buik en staart ongewijzigd.

## Palet
5 (#A8909F) en 15 (#9694AE) samengevoegd tot 5 = #A490A2: wingstrepen, lichte snavel/poot-tint.
Vrijgekomen 15 = kuif donkerbruin #47221C (model #3D1815/#522B25). Gevolg: de lichte snaveltint verschuift licht (#9694AE → #A490A2); pixels gelijk.

## Wijzigingen
1. Poten (`poten22.py`, vorm uit het model via `meetpoot.py`, achtergrondfractie ≤ 0,6): voeten los met spleet x24 (rijen 55–58) en x23 (57–58),
   rechtervoet vanaf x 25, zwarte brug rij 56 weg, steeltjes (18,59), (24,59–61) weg, tenen gescheiden ((28,59) lucht).
   Kleur: vulling 14, lichte rand 5 onder de bovenrand (alleen voorste poot), selout 2 aan de bovenkant, 14 aan de linkerkant van staande tenen,
   zwart alleen aan de schaduwkant; klauw = alleen de laatste pixel (16,57), (17,58), (25,60), (29,63), (37,57).
   Afwijking van de keurder: spleet op x23 alleen in rijen 57–58; in rijen 55–56 loopt daar de verre poot naar zijn voet (model), anders hangt die poot los.
2. Kuif: donkere kant van de plukken in 15 (bruin i.p.v. mauve 2), selout kuif 15 (ook de verre veren onder y 16); B en C doorgetrokken tot y 19
   zodat het blok op rijen 18–19 in strengen opgedeeld is, G liggend boven het oog.
3. Nek: donkere strepen onder het gezicht (rijen 26–33, x 15–22) per pixel uit het model (L < 46 → 2), 3 pixels bijgezet voor 4-verbondenheid.
4. Vleugel: slagpennen rustig vlak 3 (geen 4-vlekken), scheidingen 2, schachten 5; armpennen: modellijnen als lichte veerrand 4 over vlak 2
   (model is daar donker #422A3B met zwarte lijnen; vlak 2 behouden, dus geen vlak 3 zoals de keurder vroeg); dekverenband langs de voorrand
   = band 4 met twee modelstrepen 5 (`lijnen.BAND`) i.p.v. een dicht blok 5.

## Zwak
- Binnenvleugel (tertials) blijft vlak 3; vleugel/staart-grens niet aangeraakt (ligt bij Jordi).
- De linkervoet is één grijze plaat met klauw; de drie modeltenen zijn op deze schaal niet apart te maken zonder steeltjes.

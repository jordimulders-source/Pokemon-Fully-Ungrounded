# Hanan Pacha sprite r4 (maker): rapport
Basis = r3-png (bewezen gelijk aan sprite_r3/sprite.npy); `bouw.py` assert: buiten de twee opdrachtzones pixeldiff 0.
1. **Rechterklauw** (`voet.py`, zone X 31-40, Y 47-54, 55 px anders). Oorzaak in r3: schrappen haalde precies de natieve
   kolommen 79-80 en 87-88 weg = twee teenlijnen, en natieve rij 117. Nu: het natieve modelvak x 77-92, y 111-122 exact 2x
   (8x6) zonder schrappen, als voorste vorm op X 32-39, Y 48-53 (overlapt 1 kolom en 1 rij staart). Teenscheiding waar het
   model in de teenrijen een lijn heeft (3 tenen + 1 rand), teentoon uit de modelhelderheid, klauwpunt 2 px (ivoor 7 boven,
   14 onder) onder elke teen waar het model ivoor heeft (Ho-Oh/Moltres: tenen 2 tinten tegen zwart, klauwpunt 1-2 px licht).
   Gesloten omlijning links/rechts/onder tegen de staart, niet onder de klauwpunten (anders een rechte balk van 8 px).
   - **A** (`sprite.png`): teenscheidingen in donkerste goud (binnenlijn); **B** (`sprite_B.png`): teenscheidingen zwart.
2. **Rechte lijnen** (`lijnen.py`, `recht.py`, 18 px, magenta in `overlay_8x.png`): elke pixel van een recht stuk >= 4 px
   tegen het model gelegd (natief 2x2-blok per spritepixel, `kaart.py`/`bron.py`). 7 px hadden geen modellijn: lichtkant ->
   selout, binnenin -> kale kleur. 11 px zwarte binnenlijn geheel in goud -> donkerste goud 2 (zoals Ho-Oh). De voorrand van
   de rechtervleugel over het lijf bleef zwart (vorm over vorm). Niets gladgestreken, geen vlak aangeraakt.
   - De overige 28 rechte stukken >= 5 px staan genummerd in paneel 3 van `overlay_8x.png` en `rechte_stukken.txt` (met
     modelsterkte per pixel): bijna allemaal hebben ze een modellijn (sterkte 2+) onder elke pixel, dus ik liet ze staan.
     Kan Jordi met de nummers aanwijzen welke hij bedoelt? (o.a. 4/10 kraagonderkant + schouder, 17 middenschacht staart,
     2/3/5 onderste veren rechts.)
- **Zwak punt (zelf gezien)**: de tenen zijn 4 rijen lange rechte streepjes (nrs 13-15) en lezen op 8x als een "kammetje";
  op 1x/2x lezen ze als klauw. Kortere/gebogen tenen kan alleen door van het model af te wijken: niet gedaan zonder akkoord.

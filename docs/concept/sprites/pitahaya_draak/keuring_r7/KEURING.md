# Eindkeuring pitahaya-draak fase 1, sprite r7 (16 nov)

Gekeurd: `sprite_r7/pitahaya_r7.png` tegen het model (`model/model.png`, natief raster `sprite_r7/natief.png`, spritepixel (X,Y) = natief blok (3X+4..3X+6, 3Y+6..3Y+8)), r6 en af (afgekeurd door Jordi).
Jordi: "rechterarm zit vast aan het lichaam, kijk nog beter naar schaduw, kleur, belijning".
- **Vel:** `vel.png`. Bovenaan r7, de simulatie en het model op 8×, met de MOET-pixels gemarkeerd (rood/blauw, met hun nummer). Onderaan r6, r7 en de simulatie op 1× en 2×, op licht en donker.
- **Scripts:** `meet.py` (vulvlakjes, dambord, losse zwarte pixels, buitenlijn licht/schaduw, om-en-om), `sim.py` (past de MOET-lijst toe, met een assert op de oude index, en bewijst dat gezicht en silhouet diff 0 hebben), `vel.py` en `sim_vel.py`.
- **Simulatie:** `sim_moet_sprite.png` is geïndexeerd, heeft hetzelfde palet en index 0 is transparant. `sim_moet.png` toont arm en voet op 16× (r7 | sim | model) en daaronder beide op 2× en 1×.

## Oordeel: **FAIL, 8 px** (na de MOET-lijst PASS; de simulatie is gemeten)

### Eerst op het oog: is r7 beter dan r6?
**Ja.**
- **Rechterarm.** Bij r6 zat de arm vast: arm en romp hadden aan de binnenkant allebei tint 9/10 en er liep geen lijn tussen. Bij r7 is de arm lichter (10/11) dan de romp (9), zoals in het model. Er loopt nu een donkergroene lijn langs x 39 en het gat zit op x 38. Op 2× leest de arm daardoor als een eigen vorm, vanaf het gat tot de klauwen.
- **Romp en kop.** De romp is rustiger en heeft minder zwart. De rechterkant van de kop is minder streperig.
- **Wat nog mis is.** Bovenaan, bij de schouder, stopt de armlijn te vroeg. Daar lopen de lichte pixels van de schouder (37–39, 36–37) zonder lijn over in de romp. Dat is precies Jordi's "zit vast", nu nog over 2 px.
- **Rechtervoet.** De lichte tenen zijn verdwenen. De ruisstap heeft ze naar 9 gezet, terwijl het model daar drie lichte tenen toont. r6 had ze nog.

### Metingen (r7 → simulatie)
| meting | r6 | r7 | sim MOET | Gen 3 (Treecko / Cacnea / Bagon / Oddish) |
|---|---|---|---|---|
| zwart van de figuur | 16,5 % | 12,9 % | 12,8 % | 21,7 / 22,4 / 14,3 / 14,3 |
| zwart binnen de figuur | 6,9 % | 4,0 % | 4,0 % | 7,4 / 10,7 / 4,1 / 4,5 |
| dambord 2×2 | 3 | 9 | 9 | 21 / 9 / 5 / 16 |
| buitenlijn lichtkant (selout / zwart) | 58 / 14 | 67 / 5 | 68 / 4 | |
| buitenlijn schaduwkant (zwart / selout) | 72 / 3 | 75 / 0 | 75 / 0 | |
| om-en-om / lichte tint op de rand | 1 / 0 | 0 / 0 | 0 / 0 | |
| losse zwarte pixels binnen de figuur | 5 | 3 | 3 | |

- **Zwart aan de lichtkant (4 px na de simulatie).** Alle 4 liggen in het bevroren gezicht: (19,22–24) en (18,25).
- **Losse zwarte pixels (3).** (33,30) en (31,31) zijn de mond, die bevroren is. (29,37) is een punt van de onderlijn van de kop; het model heeft daar 4/9 zwart.
- **Dambord (9).** Daarvan zitten er 3 in schubnaden: (30,14), (39–40,20) en (21,31), dat laatste in het bevroren gezicht. Nog 5 zijn diagonale 1-px modellijnen in arm, romp en poten: (39,37), (35,39), (38,45) en (27–28,49–50). Het aantal ligt binnen de Gen 3-refs. Daarom staan ze niet in de MOET-lijst.
- **Tinten.** Roze heeft 3 tinten (3/4/5) met roze 2 als lijntint, groen ook 3 (9/10/11) met groen 8 als lijn. De helderheidsstappen zijn 36/38/36 bij roze en 32/33/37 bij groen, dus binnen ±30–40. De schaduw is iets koeler; de kleuraard klopt.
- **Licht en schaduw.**
  - Kop: licht linksboven en een schaduwsikkel rechts en onder.
  - Lijf: het licht valt waar het model het heeft (rechterarm, dijen, linkervoet). Het is geen pillow shading: de romp is donker omdat hij onder de kop ligt, zoals in het model.
- **Vulvlakjes < 3 px buiten het gezicht.** De groene en lichte punten in de kop zijn 1-px schubpunten die het model heeft. (20,45) is een klauwtip. De nieuwe tenen (zie MOET 3) zijn teenlicht uit het model, dus glans.
- **Banding.** De schaduwband rechts op de kop (x 42–43) wisselt in breedte en wordt onderbroken door naden en groene punten. Het is geen banding.

## MOET (8 px; elk punt is overgenomen uit het model)
1. **De armlijn loopt door tot de schouder** (Jordi: "rechterarm zit vast").
   - **Wat het model toont.** Een donkergroene lijn tussen arm en romp, op natieve pixels (115–117, 118) met lum 72/75/72, (117–119, 119) met lum 68/65/67 en (120, 120) met lum 79. Daarna loopt hij verder via (121, 121) met lum 58, die al in r7 staat als (39,38). In r7 stopt de lijn bij (39,38), zodat de lichte schouder er zonder lijn in de romp overloopt.
   - **(37,37): 9 → 8.**
   - **(38,38): 9 → 8.** Voor de diagonale stap is (38,38) gekozen en niet (38,37). Met (38,37) zou het lichte schouderstukje (37–38,36)+(39,37) in twee vlakjes van 1 en 2 px breken.
   - **Resultaat.** Een doorlopende lijn van 1 px: (36,36) onderlijn van de kop → (37,37) → (38,38) → (39,38–40) → gat.
2. **(42,37): 2 → 8.** Dit is een donkerroze pixel op de groene schouder. Het modelblok heeft 3 px wit, 4 px groen, 2 px lichtgroen en geen roze. Het is de bovenrand van de arm aan de lichtkant, dus groene selout, zoals (41,37) en (43,37).
3. **Lichte tenen van de rechtervoet terug.** De ruisstap van r7 zette ze naar 9; het model toont drie lichte tenen. De nieuwe waarden zijn per blok de dichtstbijzijnde groene tint bij het modelgemiddelde (9 = 99, 10 = 132, 11 = 169).
   - (35,53): 9 → 11 (modelgemiddelde 154, minimum 107).
   - (36,53): 9 → 10 (gemiddelde 116).
   - (38,53): 9 → 11 (gemiddelde 162, minimum 161).
   - (39,53): 9 → 10 (gemiddelde 145).
   - (41,53) = 11 stond er al (gemiddelde 144).
4. **(35,54): 1 → 8.** De linkerkant van de eerste teen is de lichtkant van de buitenlijn: links ligt transparant, eronder (35,55) zit zwart. Het modelblok is licht (gemiddelde 153, 1 natieve px donker). Dat maakt deze pixel selout. Het is de enige zwarte pixel aan de lichtkant buiten het gezicht.

Na de simulatie:
- gezicht (x 18–36, y 22–34) en silhouet hebben diff 0;
- om-en-om blijft 0 en er komt geen nieuw dambord bij;
- er komt geen lijnpixel los te staan;
- zwart aan de lichtkant gaat van 5 naar 4, en die 4 zitten alle in het gezicht.

## KAN
- **(44,47): 8 → 9.** Dit is de punt van de derde klauw van de rechterhand. Het modelgemiddelde is 110 en het model laat daar een lichte klauwpunt zien. De klauwen lezen nu als een zwarte onderrand.
- **(25,52): 9 → 10.** Het modelgemiddelde is 132, op de linkervoet naast het teenlicht.
- **De zwarte klont onder de kin rechts, (35–40,33–36), laat ik staan.** Het model heeft daar twee lijnen die samenkomen (kinlijn en onderlijn van de kop) met donkerroze ertussen. Ik heb (37,34) 1 → 3 geprobeerd, maar dat maakt een nieuw dambord op (36,33). Dit is dus geen goede wissel.

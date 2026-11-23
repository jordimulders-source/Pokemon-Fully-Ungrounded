# Gnometrotter Rock: sprite r7 (23 nov)

Basis = r6. Jordi over r6: "linkerhand arm is nog niet de goede vorm, arm is een rechte lijn, rechterschouder mag ietsje ronder, punt van de muts en rots lijken een beetje 1 te zijn, het model weet verschil te creëren doordat de rots schuin is waar ze hier allebei recht zijn, haar links en tussen muts mag een lijn, verder is die qua silhouet goed, maar het kleurgebruik qua tinten moet nog een stuk beter".

Leveringen: `gnometrotter_rock.png` (64×64, P, palet byte-gelijk aan r6), `gnometrotter_rock_8x.png`, `naast_model.png` (r7 | r6 | model, 8×, zelfde uitsnede).
Scripts: `r7.py` (vormpunten 1–4 uit de meting → `na_vorm.npy`), `tint.py` (tintopbouw → `na_tint.npy`), `controle.py` (afleveren + tellen), `vgl.py`/`drie.py` (vergelijkingen). Meting: `meet6.npz` (zelfde als r6: lijnaandeel en helderheid per spritepixel uit `r8/gemini_r8.png`, gedeelde geometrie).

## Wat er gebeurd is
1. **Linkerarm + vuist** (zone 7) opnieuw uit de meting: de vuist loopt tot x 11 (twee lobben, scheiding x 9), lijn vuist|arm op x 12, de arm is een kort ovaal x 13–16 (was een lange rechte band x 9–16). **Silhouet:** (14,30) en (15,30) erbij als bovenlijn van de arm: de modelarm komt daar tot modelrij 30,7, dekking 26 % en 28 % (drempel 0,2 voor deze twee, zoals de stok 0,35 kreeg). Daardoor buigt de bovenrand van de arm.
2. **Rechterschouder:** de bovenlijn van het ovaal, die in het model zit (lijnaandeel ≥ 0,18), is gezet: rij 21 x 41–44 (6) en de hoek (46,22) (2, sluit aan op de lijn 2 naar de rugkam). Het ovaal is nu rondom gesloten.
3. **Mutspunt + rugrots** (zone 1, x 40–50, rij 4–19) opnieuw uit de meting, met tinten rechtstreeks uit de modelhelderheid: de lichte voorkant van de rots is een wig die naar linksonder smaller wordt; de knik loopt schuin (x 47 rij 10–12 → x 46 rij 14–15 → x 45 rij 16). Daarnaast een donkere zijkant (3), de mutspunt donker (3) met een lijn ertussen (x 44, 2).
4. **Haar L:** uit de meting (c/d/e). Lijn 2 tussen haar en muts op (18,13), (17,14) en (17,15).
5. **Tinten** (`tint.py`), na studie van Gnomad en Regirock op 8×: per vlak (4-samenhangend, tussen de lijnen) komt de tint uit 50 % vorm en 50 % gemeten modelhelderheid. Vorm = de plaats in het vlak (licht linksboven, schaduw rechtsonder), voor 30 % meegewogen met de plaats in de hele figuur. Daaruit volgen licht, midden en een schaduwsikkel die de vorm volgt. Kleine vormen (5–12 px, zoals de arm) krijgen hun eigen licht/midden/schaduw. Vlekjes onder de 3 px (bij kleine vormen 2 px) gaan op in de buurtint.
   - **Riem, stok en zolen zijn uitgezonderd.** Die hadden in r6 al licht, midden en schaduw per rij; met de vlakregel werden ze slechter (geprobeerd: de stok werd 2-3-3, de zolen verloren hun zijband).
   - Mutspunt en rots: tint rechtstreeks uit het model (punt 3).

## Controles
- **Silhouet:** alleen (14,30) en (15,30) zijn nieuw (arm, punt 1). Verder is de alpha-diff met r6 0.
- **Losse pixels:** 0.
- **Tinten per vorm:**
  - steen: 3/4/5 + lijn 2
  - licht steen (haar, baard): c/d/e + lijn 4
  - roze (neus, lijf, vuist, arm, hand R): 7/8/f + lijn 6
  - blauw: 9/a/b
  - arm R: alleen 7/8 (te klein voor drie tinten)

## Afwijking t.o.v. r6 per onderdeel (pixels)
| onderdeel | ≠ r6 | waarvan lijn/vorm | waarvan alleen tint |
|---|---|---|---|
| muts+rugkam | 95 | 14 | 81 |
| haar L | 5 | 1 | 4 |
| haar R | 11 | 0 | 11 |
| baard | 34 | 0 | 34 |
| neus | 10 | 0 | 10 |
| lijf (incl. schouderovaal) | 63 | 4 | 59 |
| arm L + vuist | 30 (+2 silhouet) | 7 | 23 |
| arm R | 7 | 0 | 7 |
| hand R | 8 | 0 | 8 |
| riem, stok, zolen | 0 | 0 | 0 |
| broek | 40 | 0 | 40 |
| **totaal** | **303** | | |

## Wat niet uit het model komt
- **Tinten:** de tintopbouw (punt 5) is een eigen keuze richting Gen 3, op verzoek. Ze is voor de helft gestuurd door de modelhelderheid. Vormen en lijnen veranderen er niet door.
- **Lijnkleur:**
  - De twee haarstrengpixels (17,15) en (17,17) zijn van lijnkleur 4 naar c gezet (los 1-px lijntje).
  - De schouderhoek (46,22) heeft lijnkleur 2 in plaats van 6.
  - De haar/muts-lijn is 2 in plaats van de haarlijnkleur 4, omdat die tegen de muts niet te zien is. Het model heeft daar een zwarte lijn.
- **Silhouet:** (14,30) en (15,30) komen uit de modeldekking (26–28 %), dus onder de gewone drempel van 50 %.
- Verder komen alle vorm- en lijnpixels uit de meting.

## Eigen kanttekeningen
- De muts heeft licht links en schaduw rechts, maar het hooglicht is minder groot dan bij Gnomad, omdat de modelhelderheid daar meetelt.
- Midden in de broek (kruis) zit veel 9 (schaduw en naden), omdat 9 tegelijk lijn en schaduw is.
- Arm R heeft maar 2 tinten.

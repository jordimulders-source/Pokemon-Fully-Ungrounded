# Nachtaap fase 2: kleursprite ronde 5 (F1–F4 uit `../ronde4/KEURING.md`)

Basis is ronde 4. Ik heb alleen in de zones van de keuring gewerkt. Het silhouet en de maanvorm van D2 zijn niet veranderd. F5 (kené) is niet aangeraakt.

## Bewijs
- **Alpha-diff:** 0 (1459 px, zowel tegen de `.txt` als tegen de `.npy`).
- **Open randen:** 0.
- **Pixeldiff t.o.v. ronde 4:** 40 px, waarvan 0 buiten de zones.

| Zone | Pixels |
|---|---|
| F1 maanpunt | 4 |
| F2 kruin | 7 |
| F2 kin | 3 |
| F2 rechterzijde | 4 |
| F3 oog | 2 |
| F4 handen | 14 |
| F4 achtervoet | 6 |

- **Palet:** alleen index 14 (`t`, de crème-omlijning) is donkerder: 92725c → 7a5a46. `t` komt alleen in de hand- en voetzones voor (met een script nagegaan). Buiten de zones is de sprite dus ook in RGB gelijk aan ronde 4.

## Wat er veranderde
- **F1:** de rechterpunt van de maan is wit op x 21, y 43–46. Zilverlila staat nog onderaan (y 47–48) en langs de rand. De vorm is gelijk aan D2.
- **F2 (kop ronder):**
  - **Kruin:** het middelste stuk (x 14–17) ligt 1 rij hoger (y 35). Op y 36 staat daar nu vacht `l`. De kruin wordt zo een boog van 2-4-2. De maanpixels zijn niet geraakt.
  - **Kin:** de uiteinden lopen 1 rij omhoog. Links (8,53), rechts (21,53); (21,54) is nu vacht in de schaduw.
  - **Rechterzijde:** de onderste 2 px buigen naar binnen. (24,48) en (24,49) zijn nu zwart; x 25 is daar `s`.
- **F3 (verre oog):** het verre oog is het **linker** (x 6–11). De kop draait naar links-voor, dus de beeldlinkerkant draait weg; het verre oor zit daar ook achter de kopomtrek. Aan de buitenkant van de iris is i → r gegaan op x 7, y 45–46. Daardoor is het oog geen kopie meer. De pupil blijft gecentreerd, de glans blijft linksboven en de blik blijft starend.
  - De keurder noemde als voorbeeld x 19 (het rechteroog). Dat zou het **nabije** oog donkerder maken. Graag bevestigen.
- **F4 (handen en voeten):**
  - **Verre hand:** 3 vingers, gescheiden door twee schuine `e`-lijnen in één richting, (6,57)–(5,58) en (8,58)–(7,59). Ze lopen naar de toppen linksonder. Geen dambord meer.
  - **Nabije hand:**
    - de duim zit links (x 10–12, onder de verre hand);
    - 4 vingers, met lijnen van de knokkel tot de top (x 13, 16, 19 op y 59–61);
    - de schaduwkant ligt rechts.
  - **Achtervoet:** de violette enkel zakt in het midden (x 35–36, y 57). Dat breekt de rechte crème bovenkant. Tenen met lijnen op x 33 en 35.
  - **Kleur:** de handen blijven crème. De donkerdere `t` geeft de vingers meer contrast.

## Eerlijk
- De handen staan nu op 6× en op 3× als handen en voet met vingers en tenen. Op 1× blijft de verre hand een lange, lage vorm. Dat komt door het bevroren silhouet (x 3–14, 5 rijen hoog), niet door de kleur. Meer kan alleen als het silhouet daar mag veranderen; dat is een vraag aan Jordi of de coördinator.

## Lessen
- **Een donkerdere omlijningstint voor één kleurgroep is een goedkope reparatie** als die index alleen in de zone voorkomt (eerst met een script nagaan). Het contrast van de vingerlijnen stijgt dan zonder extra pixels.
- **Vingerlijnen moeten in één richting lopen** (naar de toppen) en op de knokkelrij beginnen. Een afwisseling van twee tinten leest als dambord.
- **Controleer welk oog "ver" is aan de kopdraaiing, niet aan een voorbeeld** in een keuring: bij een kop naar links-voor is het beeldlinkeroog het verre.

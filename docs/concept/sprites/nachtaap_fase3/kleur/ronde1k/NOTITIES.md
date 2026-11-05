# Nachtaap fase 3: kleurronde 1k (5 nov), alleen de vuistarm, op 1j

Basis: `../ronde1j/nachtaap_fase3.png`. Dat is 1i plus de keurdersreparatie (21,45) 3→2 en (19,31) 3→4. Uitgelezen naar `bron/basis_1j.txt`.
Bron: `bron/ronde1k.txt` → `bron/bouw.py`; `bron/check.py`; `bron/vel.py`; `bron/zoom.py`.

Jordi (letterlijk): "de arm is nog steeds wat bollig, maar dat komt door de pols die opeens erg dun is, plus dat de arm connect met het hoofd, ik zie eigenlijk wel de pols zoals in het model zitten, misschien dat je dan het arm net los kan maken of zodanig bollig kan shaden zodat het niet een flabby arm is".

## Telling
- **67 px diff met 1j, waarvan 31 in de omtrek. Dat is boven het budget van ≤ 30.**
- Alle wijzigingen liggen binnen het armvak (rij 22–31, x9–22). Buiten dat vak: 0 px diff.
- Kop/kruin/kopomtrek (rij 27–31 t/m de K-lijn (13,27)…(17,31)) en de maan: 0 px diff.
- Per rij: 22: 4, 23: 5, 24: 5, 25: 9, 26: 10, 27: 9, 28: 8, 29: 7, 30: 5, 31: 5.
- Waarom boven budget: de lucht tussen arm en kop vraagt dat de hele onderrand van de arm over 6 rijen 1–2 px opschuift. Om de arm niet dunner te maken schuift de bovenrand ook 1–2 px mee (8 px breed, zoals 1j). Daarmee verschuift elke armrij volledig, rand én binnenkant.
- Een eerdere tussenstand (59 px) hield de bovenrand op zijn plek. De arm werd daar 6–7 px en taps naar 3 px achter de kop, en las als een stokje. Die heb ik niet opgeleverd.

## Per punt
1. **Pols zoals het model:** onder de vuist ligt een korte, smallere pols (rij 22: 5 px). De plooi is de bestaande D-rij 21 onder de vuist. Daarna wordt de arm geleidelijk breder: 5–6–7–8–8–8 px, horizontaal gemeten. Er is geen plotselinge versmalling meer. Achter de kop wordt de arm smaller (7–6–5–4) doordat de kop hem afdekt; bij (21–22,31) gaat hij over in de schouder/rugrand.
2. **Arm los van de kop:** de onderrand van de arm loopt in een rechte lijn van 45° (K x10…19). Op rij 27–31 ligt 1 px lucht tussen de K van de arm en de K van de kopomtrek: (14,27), (15,28), (16,29), (17,30), (18,31). Boven de kruin is rij 26 x8–13 leeg. De kop zelf is 0 px veranderd.
3. **Stevige cilinder:**
   - De kernschaduw S ligt direct boven de onderrand, over de hele lengte.
   - De lichtband L loopt door onder de bovenrand, van rij 23 tot rij 30. In het verticale stuk bij de schouder zit hij aan de rechterkant.
   - Er is geen lichte vlek meer in het midden; de rest is V.
   - Bovenrand: D. Rechterrand bij de schouder: K.

## Controle
- Open randen: 0.
- Losse pixels in het armvak: 0.
- korrel.py: 0 uitsteeksels.
  - Alleen de luchtspleet zelf geeft nieuwe inkepingen: (13,26) t/m (18,31), 6 px plus 1 tand.
  - Dat is de gevraagde scheiding van 1 px. Een diagonale spleet van 1 px telt per definitie als inkeping.
- Pixels: 1822 (1j: 1821).

## Eerlijk (wat op 1×/3× leest)
- Op 3× en 4× is de arm nu één rechte, stevige buis met een duidelijke pols, los van de kop.
- **Arm leest iets dunner dan in 1j.** Hij is even breed (8 px), maar de dubbele donkere lijn (arm-K, lucht, kop-K) neemt visueel een pixel weg. Op 1× valt dat nauwelijks op.
- **Arm is recht, het model gebogen.** In het model buigt de arm in een boog over de kruin naar rechts. In de sprite blijft het een rechte diagonaal; de vorm van de arm heb ik niet herzien.
- **Onderkant vuist en pols:** rij 22 x5–10 is één rechte K-lijn van 6 px. Dat is de onderkant van de vuist plus de onderkant van de pols. Op 8× is hij zichtbaar recht; op 1×/3× leest hij als de platte onderkant van de vuist.

## Lessen
- Een spleet van 1 px tussen twee ledematen kost aan beide kanten een omlijning. Het onderdeel dat moet wijken wordt dus 2 px verschoven. Begroot zo'n scheiding op ±2× de lengte × 2 randen plus het verschuiven van de shading, niet als een kleine reparatie.

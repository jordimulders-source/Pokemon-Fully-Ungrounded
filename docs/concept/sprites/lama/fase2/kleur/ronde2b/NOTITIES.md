# Lama fase 2: kleur ronde 2b (maker-agent, 2 nov)

Eén zone terug van Claude: de **wolhals** las als een gestapelde kegel of trappetjestaart (horizontale lichte banden boven donkere schulpranden, recht boven elkaar). De rest van ronde 2 is bevroren.

## Wat er veranderde (alleen de halszone)
`bron/hals.txt` (met de hand getypt, `rij x0 pixels`) overschrijft `raster.txt` van ronde 2 alleen in de hals (r16–26, x16–31). Kop, oog, kaaklijn, halsband en kleding blijven ongemoeid.
- **Cilinder:** licht en hooglicht links, basis in het midden, schaduw rechts (x26–29), een rand d/k. Onder de kin een **kernschaduw** (s, x18–20 r19–21), zodat de kop zacht uit een kraag komt in plaats van op een trap te staan.
- **3 verspringende ronde plukken** van verschillende grootte, elk met een lichte bovenkant (l/h) en een schaduwrand rechtsonder die de ronding volgt:
  - **A**: boven-midden achter de kop (r16–18, x21–24), met de rand op r18–19;
  - **C**: midden-rechts (r19–22, x23–26), met de rand op r22–23 (x24–27);
  - **B**: onder-voor, het grootst (r22–25, x18–22), met de rand op r25 (x21–22), net boven de halsband.
- Er lopen geen horizontale banden meer over de hele breedte. De plukken liggen diagonaal verspringend (A → C → B) in plaats van in rijen.

## Controles
```
mode P transparency 0 | pixels 1278 | alpha-diff 0
kleuren gebruikt: 16 | open randen: 0
diff t.o.v. ronde 2: 41 px in de halszone (budget ±60) | buiten de zone: 0
```
(`bron/diff_r2.py`; de zone is x16–33, y12–27.)

## Eigen keuring (8×, 4× en 1×, licht en donker, naast ronde 2)
- De hals leest als een wollige cilinder met losse plukken, niet meer als trappetje. De kop zit in een kraag.
- Op 1× is het verschil met ronde 2 klein maar rustiger: geen strepen meer in de hals.
- Ik zie geen zelfgenoemd zwak punt.

## Lessen
- Wolplukken mogen nooit in rijen onder elkaar liggen: dan lezen de schulpranden als horizontale banden (trappetje). Laat ze diagonaal verspringen, in verschillende maten, en leg de schaduwrand rechtsonder langs de ronding, niet als een horizontale streep over de hele breedte.
- De overgang van kop naar wolhals: een kernschaduw onder de kin (s) in plaats van een lichte band direct onder de kaak.

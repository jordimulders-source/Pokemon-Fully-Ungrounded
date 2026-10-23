# Olinguito ronde 21b: stevige poten in eigen hoeken

Basis: ronde 21 (klauwen, kaaklijn en alles wat bevroren is, blijven gelijk). Bouw: `bron/bouw_ronde21b.py`, dat de pootlagen van `ronde21/bron/bouw_ronde21.py` vervangt. Controle: `bron/check.py`. Vergelijking: `bron/vergelijk.py` → `compare.png`.

Aanleiding: de coördinator hield ronde 21 tegen omdat de vier poten dunne, kaarsrechte, parallelle stokken waren. Daarna kwam Jordi, letterlijk: "ja die poot achterin moet juist naar voren." Maatstaf voor de hoeken: Galar-Linoone en Poochyena.

## Wat er is veranderd (alleen de pootzone)
- **Nabije voorpoot:** dikker (8–9 px bij de schouder, 6–7 bij de pols) en schuin naar voren, zodat het gewicht op deze poot rust. De poot staat plat naar voren met teenrij. De klauwen hebben dezelfde grootte en vorm als in ronde 21 (1 px verder naar voren).
- **Verre voorpoot:** korter (perspectief) en in schaduwtint. Hij staat iets naar achteren gekanteld onder de borst (x28–34), met eigen klauwen (dezelfde als ronde 21). Tussen hem en de nabije voorpoot zit lucht.
- **Nabije achterpoot naar voren onder het lijf** (Jordi): de heupbolling zit achteraan (tot x48), de hak is zichtbaar als achterhoek van de dij (y44–46), en de scheen loopt schuin naar voren naar een voet op x32–39. De voet staat dus vóór de heup, zoals bij Poochyena. De hak raakt de staarthaak niet meer.
- **Verre achterpoot:** zoals bij Poochyena naar achteren, in schaduwtint, rechts achter de nabije (x41–47). De voet staat onder de staarthaak op y51, de hoogste van de vier.
- **Hoeken:** nabije voor naar voren, verre voor iets naar achteren, nabije achter naar voren, verre achter naar achteren. Geen twee poten lopen parallel.
- **Voethoogtes:** nabije voor y55, nabije achter y54, verre voor y53, verre achter y52.

## Bewijs (`python3 bron/check.py`, tegen ronde 20)
```
frame 1: buiten pootzone (excl. kaak) 0 | kop 0 | oren 0 | staart 0 | kaaklijn 3 px [(23, 39), (23, 40), (24, 39)] | pootzone gewijzigd 303 px
  open randen 0 [] | 1024 px, box 48x37 (x9-56, y19-55)
frame 2: buiten pootzone (excl. kaak) 0 | kop 0 | oren 0 | staart 0 | kaaklijn 3 px [(23, 38), (23, 39), (24, 38)] | pootzone gewijzigd 304 px
  open randen 0 [] | 1030 px, box 48x37 (x9-56, y18-54)
palet gelijk: True | transparency 0
```

## Checklist C
C1 ok (4 poten, 2 klauwen per voorpoot). C2 ok (4 voethoogtes, de nabije voorpoot is het laagst en het meest links). C3 ok (elke poot staat onder zijn eigen schouder of heup, geen Escher). C4 ok (hak en pols). C5 ok (schouder- en heupbolling). C6 ok (de verre poten zijn korter, hoger en in schaduwtint). C7 ok (alle vier staan op de grond). C8 ok (staart ongewijzigd). A6 beter (geen stokken meer, de kaak is licht gebogen).

## Zelfcheck (compare.png: ronde 20, 21, 21b fr1/fr2, Galar-Linoone, Poochyena op 1× en 3×; poten op 8×)
- Op 1× ziet hij eruit als een lopend dier op vier poten, niet als een tafel. Het gezicht is gelijk aan ronde 20 en niet vreemder.
- Wat niet klopt:
  - (a) **1024 px**: groter dan ronde 20 (996) en verder van ≤ 950, omdat de poten dikker zijn. Kleiner kan alleen met kortere poten (dan moet de romp hoger) of met kleinere klauwen.
  - (b) De verre achterpoot valt onder de staarthaak en leest op 1× als een donkere vlek onder de staart.
  - (c) De hak is een achterhoek van de dij, geen uitgesproken knik zoals bij Poochyena.
- De variant met de kop lager (ronde21/variant_kop_lager) is níet opnieuw gebouwd op 21b.

## Lessen
- **Poten "dikker en in eigen hoek":** geef elke poot eerst een richting (naar voren of naar achteren) en een breedteverloop (taps). Teken pas daarna de rijen. Vier kolommen van gelijke breedte lezen altijd als tafelpoten.
- **Achterpoot naar voren onder het lijf** (Poochyena, Galar-Linoone): heup achteraan, voet vóór de heup, hak als achterhoek van de dij. Een poot die naar achteren uitsteekt, botst bovendien met een staart die laag hangt.
- **Gebruik bij een coördinator-instructie over pose de referentie-sprite als maatstaf, niet de woorden.** "Hak schuin naar achteren" bleek fout. Galar-Linoone en Poochyena op 8× lieten meteen zien dat de voet naar voren staat.

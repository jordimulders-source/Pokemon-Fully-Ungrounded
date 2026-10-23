# Olinguito ronde 22: pootconfiguratie van Galar-Linoone en een diagonale stap

Basis: ronde 21b. Bouw: `bron/bouw_ronde22.py`, dat alleen de pootlagen van 21b vervangt. Controle: `bron/check.py` (uitvoer in `bron/check_uitvoer.txt`). Vergelijking: `bron/vergelijk.py` → `compare.png` (1× en 3× naast 21b, Galar-Linoone en Poochyena; poten op 6× met de voeten gemarkeerd).

Jordi, letterlijk: "olinguito wordt weer niet naar mijn feedback geluisterd. onder de tong van linoone hangt zijn rechter (voor ons linker) poot. In elk geval ziet dit er niet verkeerd uit, maar klopt het dat een olinguito met beide linkerpoten naar voren loopt en daarna beide rechterpoten, dat is meer een kamelen manier van lopen toch"

## Gemeten: Galar-Linoone (voetzool x, y)
| Poot | Linoone | Wat hij doet |
|---|---|---|
| Verre voor (zijn rechter, voor ons links) | x11–18, y49 | vooraan onder de kin/tong, het laagst, schuin naar voren, schaduwtint |
| Nabije voor | x29–36, y45 | onder de borst, kort en opgetild (staat het hoogst) |
| Nabije achter | x39–46, y48 | naar voren onder het lijf, voet vóór de heup |
| Verre achter | stompje x51–57, y40–41 | naar achteren, bijna verborgen |

Diagonaal: vóór staan **verre voor + nabije achter**, achter staan **nabije voor + verre achter**. Geen telgang.
Poochyena: nabije voor naar voren (licht), verre voor naar achteren onder de borst (donker), achterpoot onder het achterlijf. Ook diagonaal.
Ronde 21b had juist de telgang: nabije voor + nabije achter naar voren, verre voor + verre achter naar achteren.

## Ronde 22 per poot (voetzool x, y in frame 1)
| Poot | Ronde 22 | t.o.v. Linoone |
|---|---|---|
| Verre voor | voet x15–20, y51 (klauwen x12–17, tot y54) | zelfde rol en plek: vooraan onder de kin, schuin naar voren, schaduwtint (3), 2 kleine klauwen (KLAUW_VER uit 21b). Staat vooraan het laagst van de voorpoten, zoals bij Linoone. |
| Nabije voor | voet x26–35, y49 (klauwen x22–29, tot y53) | onder de borst, licht naar achteren gekanteld en iets opgetild (hoger dan de verre voorpoot), zoals Linoone's nabije voorpoot. Schouder, dikte en klauwen van 21b. |
| Nabije achter | voet x36–43, y53 | naar voren onder het lijf, voet vóór de heup (heup tot x48), hak ongewijzigd (y42–46). Alleen het onderbeen 1–4 px naar achteren voor lucht met de voorpoot. |
| Verre achter | ongewijzigd uit 21b, nu verder achter de nabije; zichtbaar x44–50, y51 | naar achteren, grotendeels verborgen, net als Linoone's stompje. |

Vóór staan nu de diagonale paren **verre voor + nabije achter**; achter staan **nabije voor + verre achter**. Dat is precies Linoone's stand.
Linoone → ons (x): verre voor 14 → 14, nabije voor 32 → 25–30, nabije achter 43 → 39, verre achter 54 → 46. De afstanden zijn compacter omdat onze kop groter is en het lijf korter.
Frame 2: de voorpoten gaan 1 rij mee omhoog (zoals in 20–21b); de achterpoten blijven staan.

## Bewijs (`python3 bron/check.py`)
```
== tegen ronde21b
frame 1: buiten pootzone (excl. kaak) 0 | kop 0 | oren 0 | staart 0 | kaaklijn 0 | pootzone gewijzigd 262 px
frame 2: buiten pootzone (excl. kaak) 0 | kop 0 | oren 0 | staart 0 | kaaklijn 0 | pootzone gewijzigd 262 px
palet gelijk: True
== tegen ronde20
frame 1: buiten pootzone (excl. kaak) 0 | kop 0 | oren 0 | staart 0 | kaaklijn 3 | pootzone gewijzigd 315 px
frame 2: buiten pootzone (excl. kaak) 0 | kop 0 | oren 0 | staart 0 | kaaklijn 3 | pootzone gewijzigd 318 px
palet gelijk: True
frame 1: open randen 0 [] | 1024 px, box 48x36 (x9-56, y19-54)
frame 2: open randen 0 [] | 1028 px, box 48x37 (x9-56, y18-54)
transparency 0 | mode P (64, 128)
```
Pootzone = y ≥ 40 (frame 2: ≥ 39), x 12–48, zonder staartpixels (dezelfde zone als 21/21b). De kaaklijn (3 px) is die van ronde 21 en is ongewijzigd t.o.v. 21b. In check.py telt "staart" nu alleen pixels die in ronde 20 echt staart zijn. Pixel (44,47) valt wel in het staartmasker, maar is in ronde 20 leeg en in 21b een pootpixel.
Formaat: 1024 / 1028 px (21b: 1024 / 1030). Het formaat is dus niet gegroeid.

## Checklist C
C1 ok (4 poten, 2 klauwen per voorpoot). C2 ok (vier verschillende voethoogtes en x-posities). C3 ok (elke poot onder zijn eigen schouder of heup; de verre voorpoot komt onder de kin vandaan, zoals bij Linoone). C4 ok (hak en pols). C5 ok (schouder- en heupbolling ongewijzigd). C6 ok (de verre poten in schaduwtint en dunner, 5 px tegen 8–9 px). C7 ok (de nabije voorpoot is iets opgetild, zoals bij Linoone; de andere drie staan). C8 ok (staart ongewijzigd). Lucht tussen de poten: minstens 1 kolom tussen de verre voorpoot en de nabije klauwen, en 1–2 kolommen tussen de nabije voor- en achterpoot.

## Zelfcheck (compare.png)
- Op 1× leest hij als een diagonale stap: de grijze klauwen vooraan onder de kin en de lichte klauwen onder de borst zitten niet meer naast elkaar in één lijn. Het gezicht is gelijk aan 21b (pixeldiff 0) en niet vreemder.
- Wat niet perfect is:
  - (a) De twee klauwparen staan dicht bij elkaar (x12–17 en x22–29). Op 1× lezen ze als "vóór en achter", maar de afstand is kleiner dan bij Linoone (18 px). Verder uit elkaar kan pas als de nabije voorpoot verder naar achteren gaat. Dan moet het onderbeen van de achterpoot nog verder naar achteren, en wordt de verre achterpoot bijna onzichtbaar.
  - (b) De verre voorpoot is een smalle donkere poot (5 px, zoals in 21b). Bij Linoone is hij voluit zichtbaar en dikker. Dikker (6 px) kostte ±15 px en ging over 1024 px, dus die variant is niet opgeleverd.
  - (c) De nabije voorpoot hangt iets opgetild met de klauwen omlaag (zoals Linoone). Op 1× is dat een "pootje in de lucht". Als Jordi hem liever plat wil, kan hij 2 rijen lager.

## Lessen
- **Eerst per poot de rol meten, dan pas tekenen:** schrijf per poot van de referentie op welke poot het is (nabij/ver, voor/achter), de voetpositie en of hij vóór of achter staat. Controleer de diagonale paren (vóór = verre voor + nabije achter, of omgekeerd) vóór je begint. 21b ging fout omdat "dikker en in eigen hoek" werd uitgevoerd zonder te checken welke poten samen vóór staan.
- **In 3/4 naar links is de verre kant de rechterkant van het dier.** Die verre voorpoot kan best vooraan en laag staan: bij 3/4-voor staat de voorkant dichter bij de kijker. Perspectief betekent hier dunner en een schaduwtint, niet per se hoger.
- **Een voorpoot naar achteren vraagt ruimte van de achterpoot.** Schuif dan het onderbeen van de achterpoot per rij iets terug (dx-tabel), zodat de hak en de dij bevroren blijven.
- **Pixelbudget:** een verre poot die eerst verstopt zat en nu vrij staat, kost meer pixels. Compenseer dat met een opgetilde (kortere) nabije poot, zoals Linoone dat ook doet.

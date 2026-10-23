# Olinguito ronde 21: poten en klauwen

Basis: `ronde20/anim_front.png`, met hetzelfde palet (`normal.pal`, byte voor byte gelijk). Bouw: `bron/bouw_ronde21.py`. Controle: `bron/check.py`. Vergelijking: `bron/vergelijk.py` → `compare.png`. Variant C9: `variant_kop_lager/` (bouw: `variant_kop_lager/bron/bouw_variant.py`).

Jordi, letterlijk: "nu zijn de klauwen weer too much, plus ik zie nog maar 1 poot. die andere mag iets zichtbaarder en de klauwen mogen qua grootte passen bij de poten. Misschien de achterste poot net als bij linoone wat meer naar de originele positie schuiven, maar het design hetzelfde houden". Aanvulling: "en probeer alle punten toe te passen verder." Daarom zijn ook C3/C5, A6 (kaak), D1 en C9 (alleen als variant) uit KEURING.md §5 meegenomen.

## De drie punten
- [x] **1. Klauwen passen bij de poten.** Het blok is de Sandslash-hand op ±2/3 grootte. Het is met de hand verkleind: 8×8 px nabij en 6×6 px ver (was 11×12). Elke poot heeft 2 klauwen: een smalle buitenklauw (9/a) en een brede binnenklauw (c/a). Ze zijn breed aan de basis en buigen naar links-onder, met een scheidingslijn (9) ertussen en een taps toelopende punt. Net als bij Sandslash groeien ze uit de pols naar voren. De klauwen zijn nu ongeveer zo breed als de poot (6–7 px), zoals bij Sandslash, waar ze bij de arm passen. Ze blijven het lichtste vlak van de sprite, dus nog steeds het kenmerk, maar ze zijn niet meer groter dan de poot.
- [x] **2. Beide voorpoten zichtbaar.** De verre voorpoot is een eigen poot in schaduwtint 3: kolom x28–33, van onder de buik tot een voet op y50. Hij heeft zijn eigen 2 klauwen, één tint donkerder (a/9 met omlijning 1), met de punten op y53, 2 rijen hoger dan de nabije (y55). Op y45–49 zit tussen de nabije voorpoot (x≤27) en de verre (x≥28/29) 1–2 kolommen lucht. Pas bij de klauwen raken de omlijningen elkaar.
- [x] **3. Achterpoot naar de originele positie.** De nabije achterpoot uit ronde 20 (`NABIJE_ACHTERPOOT`, ongewijzigde rijen) is als geheel **2 px naar achteren** verschoven (`HIND_DX = 2`). De voet staat op x36–42 en de heupbolling eindigt op x48, onder de achterkant van de romp, zoals bij Galar-Linoone en stap 1b (stap 1b x42–50 min de 6 px rompverkorting = x36–44). **Beperking:** meer dan 2 px kan niet, want dan valt de hak achter de bevroren staarthaak (x44–48, y46–50). Nu raakt de hak de haak op y47–49 met een omlijning ertussen, zonder kolom lucht (in ronde 20 zat er wel lucht tussen, op x43). De staart is als laatste laag letterlijk teruggeplakt, dus geen staartpixel is veranderd.

## Overige punten (KEURING §5)
- **C3/C5 voorpoten:** de nabije voorpoot is geen dunne schuine stok vanaf de kin meer. Hij heeft een schouderbolling (x23–32, y40–43, glans 5) en loopt bijna loodrecht naar de pols (x19–25). De verre voorpoot staat onder de borst (x28–33). Wel zit de schouder nog onder de achterkant van de kop. Dat geldt ook voor Galar-Linoone en Poochyena, omdat de kop over de borst valt (B6).
- **A6 kaak:** de onderrand van de kaak loopt nu in een lichte boog. Op y38 staat hij op x16–18, op y39 op x19–22 en op y40 op x23, waar hij overgaat in de keel en de schouder. Dat zijn **3 pixels in de kopzone**: (23,39) 1→3, (24,39) 1→3 en (23,40) nieuw 1. In frame 2 liggen ze 1 rij hoger.
- **D1 formaat:** **niet gehaald.** Frame 1 heeft 995 px (ronde 20: 996), frame 2 1001. De kleinere klauwen besparen ±50 px. Daar staat tegenover dat de voorpoten nu echte poten zijn: de nabije is dikker en de verre is een volledige poot met eigen klauwen. Onder 950 kom ik alleen met dunnere poten of nog kleinere klauwen. Dat heb ik niet gedaan, omdat Jordi de verre poot juist zichtbaarder wil. De variant met de kop lager komt wel uit op 961 px.
- **C9 kop lager:** dit staat alleen in de variant `variant_kop_lager/`. Kop, masker, oren en kaaklijn zijn letterlijk 2 rijen omlaag geknipt en geplakt. Er was geen opvulling nodig: de romp vult de vrijgekomen plek al. De top staat nu op y21, de rug op y32 en de kin op y40/41, tegen de schouder.

## Bevroren delen: pixeldiff-bewijs (`python3 bron/check.py`)
```
frame 1: buiten pootzone (excl. kaak) 0 | kop 0 | oren 0 | staart 0 | kaaklijn 3 px [(23, 39), (23, 40), (24, 39)] | pootzone gewijzigd 289 px
  open randen 0 [] | 995 px, box 48x37 (x9-56, y19-55)
frame 2: buiten pootzone (excl. kaak) 0 | kop 0 | oren 0 | staart 0 | kaaklijn 3 px [(23, 38), (23, 39), (24, 38)] | pootzone gewijzigd 293 px
  open randen 0 [] | 1001 px, box 48x37 (x9-56, y18-54)
palet gelijk: True | transparency 0
```
- Pootzone = y≥40 (frame 2: y≥39, omdat de voorpoten meegaan), x12–48, zonder staartpixels. Alles daarbuiten (kop, masker, oren, rug, staart) is pixel voor pixel ronde 20. De romprijen binnen de zone zijn letterlijk `LIJF` uit ronde 20, en de poten liggen eroverheen.
- Staart = alle niet-transparante staartpixels van ronde 20 (masker van ronde 20 met dx −6): diff 0. Alleen 4–5 transparante gaatjes binnen dat masker zijn nu heup of hak.
- Variant (los script, ook in deze map gecontroleerd): de kop is na de verschuiving van 2 rijen pixeldiff 0 ten opzichte van de kop van ronde 21. Buiten de oude en de nieuwe kopzone is de diff met ronde 21 0. Open randen 0, transparency 0, palet gelijk.

## Checklist C (en de rest kort)
- C1 ok: 4 poten, 2 klauwen per voorpoot (ook de verre), 2 oren, 1 oog en een staart.
- C2 ok: 4 voethoogtes: nabije voor y55 (laagst en meest links), verre voor y53 (rechts erachter, 2 hoger), verre achter y51 (tussen de twee nabije in), nabije achter y54. Tussen de vier poten zit lucht (x26–28, x33–34) of een omlijning.
- C3 deels: elke poot staat onder zijn eigen schouder of heup. Er staat geen verre poot vóór de nabije. De nabije voorpoot zit nog onder het achterste deel van de kop, maar dat komt door B6.
- C4 ok: de achterpoot heeft een hak (de vorm van ronde 20). De voorpoten hebben een pols die naar voren knikt.
- C5 ok: er zijn bollingen voor de schouder (nabij, met glans) en de heup (nabij, nu tot x48).
- C6 ok: de verre poten zijn korter, hoger en in schaduwtint, en de verre klauwen zijn een tint donkerder. De verre achterpoot loopt schuiner dan de verre voorpoot, dus ze zijn niet identiek.
- C7 ok: alle vier de poten staan op de grond en er hangt geen klauw in de lucht.
- C8 ok: de staart is ongewijzigd. C9: zie de variant.
- A1–A5 ok (A4: lucht tussen alle poten en in de staartlus). A6: de kaak is nu licht gebogen. Wel lijken de poten op 3× een beetje op kolommen naast elkaar, al is dat minder dan bij een kam (zie hieronder).
- B1–B7 ok: de kop is ongewijzigd, op 3 kaakpixels na. D2 54% (ongewijzigd), D3 ok, D4 48 breed. E1/E2 ok.
- SPRITING §0: licht van linksboven, omlijning per kleurgroep, 0 open randen, transparency=0, palet ongewijzigd, alles met de hand per rij of als handgetekend blok.

## Zelfcheck (compare.png: stap 1b, ronde 20, ronde 21 fr1/fr2, variant, Galar-Linoone, Poochyena, Sandslash op 1× en 3×; poten op 8×)
- Op 1× en 3× is het dezelfde Pokémon als ronde 20, en niet vreemder: het gezicht is gelijk. De klauwen zijn nu ongeveer zo groot als de poot. Op 1× lees je twee voorpoten, elk met een witte of grijze klauwvlek.
- Wat niet (helemaal) klopt: (a) 995 px, dus niet ≤ 950. (b) De hak raakt de staarthaak, zonder lucht (dat kan niet anders zolang de staart bevroren is en de poot 2 px naar achteren moet). (c) Onder de buik staan de vier poten op 3× vrij regelmatig naast elkaar. Ze hebben wel verschillende hoeken, breedtes en hoogtes, maar leggen ze het minder "in beweging" dan Galar-Linoone. (d) Op 1× is de klauw van de verre voorpoot klein (een grijs vlekje). Bij nog kleiner verdwijnt hij.
- Variant met de kop lager: de kop leest meer sluipend (P3) en is niet vreemder. Hij is wel iets minder "alert schattig". Dat is een keuze voor Jordi.

## Lessen
- **Een blok uit een referentie verkleinen = met de hand hertekenen op ±2/3,** met dezelfde structuur: een smalle buitenklauw, een scheidingslijn en een brede binnenklauw met een tapse punt. Bij kleiner dan ±6 px hoog verdwijnt de scheidingslijn en lezen 2 klauwen als 1 vlek.
- **"Eigen kolom met lucht" voor de verre poot:** laat de poten bovenaan overlappen (beide hangen aan de romp) en open de lucht pas vanaf halverwege, door de nabije poot 1 px per 2 rijen naar voren te laten lopen. Vier rechte, even brede kolommen lezen als een kam of tafelpoten (dat was mijn eerste poging): varieer hoek, breedte en voethoogte.
- **De pootzone verschuift in frame 2 mee met de voorpoten** (y≥39). Zet de romp-onderkant daarom letterlijk terug uit de `LIJF`-rijen van de vorige ronde, inclusief de borst die 1 rij hoger staat, anders ontstaan er open randen op y38–40.
- **Bewijs bij een bevroren staart met transparante gaatjes:** vergelijk alleen de niet-transparante bronpixels. Een gaatje dat nu poot is, is geen staartwijziging.
- **Verschuif je een onderdeel richting een bevroren buur** (hier de hak richting de staarthaak), meet dan eerst hoeveel ruimte er is. Een verschuiving die het bevroren deel zou raken, moet je melden in plaats van stilletjes klein maken of de buur overschilderen.

# Olinguito ronde 20: alle verbeterpunten in één ronde

Basis: `stap1b_kop/anim_front.png` (Jordi: "veel beter") met hetzelfde palet (`normal.pal`, byte voor byte gelijk).
Leidraad: Galar-Linoone. Skelet: Poochyena (poten en hak). Klauwen: Sandslash (`graphics/pokemon/sandslash`, nabije hand x4–14, y34–45).
Bouw: `bron/bouw_ronde20.py` (lagen, per rij met de hand uitgeschreven). Controle: `bron/check.py`. Vergelijking: `bron/vergelijk.py` → `compare.png`.

Jordi, letterlijk: "veel beter, het donkere vlak om het oog heen mag wat beter nog, een groot deel is meebewogen, maar de uiteinden niet. Plus het stuk boven de neus mag iets meer naar beneden. [...] olinguito mag je alle verbeterpunten nu in 1 keer gaan doen." Aanvullingen: "houd de olinguito klauwen maar op 2", "net als Sandslash". De klauwen zijn de USP van de lijn.

## De 5 punten
- [x] **1. Masker** (18 px per frame, alleen in de maskerzone):
  - *Uiteinden:* de onderlob die in stap 1b was blijven staan (y33 tot x33, lobpunt y34 x30–33, kaaklijntje y35 x31–32), is 5 px mee naar voren gegaan, net als het oog en de bovenlob. Het masker eindigt nu onderaan bij x28, één kolom achter de achterrand van de oogband (x27). Daardoor ligt het als één band om het oog, zonder de losse donkere staart onder de wang. De lobpunt kon niet letterlijk 5 px mee, want dan ligt hij op de crème kaak (bevroren). Daar is nu wang (4).
  - *Boven de neus lager:* de bovenrand zakt vóór het oog trapsgewijs met 1–2 rijen. Bij x19–23 blijft hij op y28, boven het lid. Bij x17–18 ligt hij op y29 en bij x13–14 op y30. Op y28 x15–18 komt voorhoofdsvacht (5/5/4/3), op y29 x14–16 vacht plus een glansrij (3). Er is geen nieuw crème of beige: het aantal 6/7/8-pixels in de kop blijft 65.
  - Oog, wenkbrauw op de maskerrand, oren, neus en grijns: pixeldiff 0 (zie hieronder).
- [x] **2. Achterpoot rechts met hak:** nieuwe nabije achterpoot (x34–45, y42–54) op het skelet van Poochyena. De dij is een bolling met een glansvlek (5) op y40–43. Aan de achterrand springt de hak naar achteren (x42 op y47–48, met een inham op y46). Daarna loopt het onderbeen schuin naar voren naar een platte voet op y52–54 (x34–40), met tenen in het patroon van stap 1b (`1231331`). De staarthaak heeft 1 kolom lucht (x43).
- [x] **3. Klauwen in Sandslash-stijl, 2 per poot:** de nabije hand van Sandslash staat pixel voor pixel op onze nabije voorpoot (x12–22, y44–55): twee brede, gebogen klauwen met de punten naar links-onder. Ze groeien uit de pols, met de scheidingslijn ertussen zoals bij Sandslash. Kleuren 1-op-1 vertaald: wit 6→c, crème 7→a, grijs 9→9, donkergrijs a→9, zwart f→1. Verre poot: dezelfde klauwen, één tint donkerder; alleen de punten steken onder de verre pols uit (x21–28, y46–53). Op 1× zijn de klauwen het opvallendste kenmerk.
- [x] **4. Verre voorpoot naar de grond:** de verre voorpoot staat nu als kolom in schaduwtint achter en rechts van de nabije (x28–31, y44–48). Zijn klauwpunten raken y53, 2 rijen boven de nabije klauwpunt (y55). Er zijn 4 voethoogtes: nabije voor y55, nabije achter y54, verre voor y53, verre achter y51.
- [x] **5. Romp korter / formaat:** de romp is 6 px korter (staart dx −6). De staart (J met haak) is letterlijk geknipt en geplakt: pixeldiff 0, in frame 2 net als in stap 1b 1 rij lager. Ook de kop is letterlijk overgenomen, op de maskercorrectie na. Breedte **48** (was 54). Oppervlak **996 px** (was 1118). **Niet gehaald: ≤ 950.** Ter vergelijking: Poochyena 989, Galar-Zigzagoon 1137. De rest van het oppervlak zit in de grote klauwen (USP). Onder 950 kom ik alleen met kleinere klauwen of een kleinere kop, en dat heb ik bewust niet gedaan.

## Bevroren delen: pixeldiff-bewijs (`python3 bron/check.py`)
```
frame 1: open randen ronde20 0 (stap1b 0): []
  kop (zonder maskerzone) pixeldiff = 0; oren = 0; staart (na dx -6) = 0; maskerzone gewijzigd 18 px
  996 px, box 48x37 (x9-56, y19-55)
frame 2: open randen ronde20 0 (stap1b 0): []
  kop (zonder maskerzone) pixeldiff = 0; oren = 0; staart (na dx -6) = 0; maskerzone gewijzigd 18 px
  1001 px, box 48x37 (x9-56, y18-54)
creme/beige in kop: stap1b 65, ronde20 65
palet gelijk: True | transparency 0
```
- Kopzone = stap 1b tot de achterste omlijning per rij (`head_mask`). Maskerzone = de 18 pixels uit `MASKER` (y28 x15–18, y29 x14–17, y33 x28–33, y34 x30–33, y35 x31–32). Oren x15–21 en x29–38, y19–25 zijn apart gecontroleerd.
- Staart = stap 1b x≥53 (y33–53) plus haakpunt x50–52 (y46–52), verschoven met dx −6.
- Animatie zoals in stap 1b: in frame 2 gaan kop, borst en voorpoten 1 rij omhoog en de staart 1 rij omlaag. Lijf en achterpoten blijven staan.

## Checklist (FAKEMON_CHECKLIST)
Sjabloon: kleine viervoeter/marter, fase 1, Dark/dief, P3 laag, skelet Galar-Linoone + Poochyena (+ Sandslash voor de klauwen), lange snuit met één oog. Kenmerken: klauwen (USP), J-staart en masker. De staart is het tegenwicht rechts.
- A1 ok: op 1× een gemaskerde marter of coati met grote klauwen. A2 ok: de klauwen breken de omtrek linksonder, de J-staart rechts. A3 ok (de staart hangt, zoals in stap 1b). A4 ok: lucht tussen alle poten (x29, x32, x43) en in de staartlus. A5 ok.
- A6 deels: het onderbeen van de achterpoot is geen rechte stok meer (hak). De onderkant van de kaak is nog recht, maar die is bevroren.
- B1–B7 ok: ongewijzigd t.o.v. stap 1b. Eén oog, de neus is het meest linkse punt, de kop overlapt het lijf.
- C1 ok: 4 poten, 2 oren, 1 oog, staart, 2 klauwen per voorpoot.
- C2 ok: 4 voethoogtes (55/54/53/51). De nabije voorpoot is het laagst en het meest links, de verre voorpoot staat rechts erachter en 2 hoger. Tussen de poten zit lucht of een omlijning.
- C3 deels: de nabije voorpoot begint nog onder de kin (x25–33). Hij staat wel verder naar achteren dan in stap 1b, en de verre voorpoot staat onder de borst (x28–31).
- C4 ok: de achterpoot heeft een hak naar achteren.
- C5 ok: de dij is een bolling in de romp.
- C6 ok: verre poten en verre klauwen in de schaduwtint.
- C7 ok: alle 4 de poten staan op de grond. De verre voorklauw hangt niet meer.
- C8 ok: de staart is letterlijk overgenomen.
- C9 deels: de pose is laag en de klauwen zijn naar voren geplant, maar de kop zit nog boven de rug (die mocht niet veranderen).
- D1 bijna: 996 px (doel ≤ 950; Poochyena 989). D2: kop y19–38 = 54% (grens, ongewijzigd). D3 beter: korte romp x38–46. D4 ok: 48 breed.
- E1 ok. E2 ok: de nabije poot heeft omlijning tegen de verre. E3: donker aandeel 0,34 (Dark mag).
- SPRITING §0: licht van linksboven, omlijning per kleurgroep, geen open randen (0), transparency=0, palet ongewijzigd, alles met de hand per rij.

## Zelfcheck (compare.png: stap 1b, ronde 20 fr1/fr2, Galar-Linoone, Poochyena, Sandslash op 1× en 3×; kop en klauwen op 8×)
- Op 1× en 3× is het duidelijk dezelfde Pokémon als stap 1b en niet vreemder. Het gezicht is gelijk; het masker is netter, zonder losse staart onder de wang. Het lijf is compacter (meer fase 1) en de witte Sandslash-klauwen springen er nu het meest uit.
- Wat nog niet klopt: (a) het gebied onder de buik met verre voorpoot, verre achterpoot en verre klauwpunten is op 3× wat druk, met donkere kolommen naast elkaar; (b) de nabije voorpoot is een dunne schuine stok vanaf de kin (C3); (c) 996 px, net boven 950; (d) de hak leest op 1× subtiel. Hij is op 3× wel te zien, maar minder duidelijk dan bij Poochyena.

## Lessen
- **Bevroren delen als masker-functie in het bouwscript** (kop per rij tot de achterste omlijning, staart als rechthoeken). Plak ze als laatste laag letterlijk terug en controleer met dezelfde maskers in `check.py`. Zo is pixeldiff 0 per constructie te bewijzen.
- **Een frame-2-animatie per onderdeel:** zoek eerst per onderdeel de verschuiving tussen de frames (hier kop/voorpoten −1, staart +1, lijf 0). Neem bij het letterlijk overnemen het onderdeel uit **hetzelfde frame** van de bron, want de staart van stap 1b is in frame 2 niet exact verschoven (3 px verschil).
- **Bij een verschoven kop in frame 2 gaat de borst eronder mee**, anders ontstaan gaten en open randen onder de kin.
- **Sandslash-klauwen letterlijk overnemen:** knip de hand uit (x4–14, y34–45), laat de gele arm weg en vertaal de 5 klauwtinten. Gebruik een middentint (a) voor crème, anders verdwijnt de scheidingslijn en lezen 2 klauwen als één witte vlek. Van de verre klauwen alleen de punten tonen, met een omlijningsrij erboven.
- **Een uiteinde dat niet kan meeschuiven** (de lobpunt zou op de bevroren kaak vallen): eindig de vorm op de nieuwe plek en maak de oude plek vacht. Een los lijntje dat dan overblijft, wordt ook vacht, anders blijft er een donker stipje over.
- De Read-weergave van grote PNG's is grof. Controleer pixelposities met een tekstraster, niet op het oog.

# Olinguito ronde 17: staart, masker naar de mondhoek, neus tussen de ogen

Jordi over ronde 16: masker en oren zijn "uitstekende verbeteringen". Te repareren: (1) de staart leest als schorpioen, (2) het masker moet doorlopen tot de mondhoek, en (3, nagekomen) "de ogen staan niet in verhouding met de neus": de neus zit voor de kijker links van de ogen, maar hoort ertussen.

**Bevroren (gecontroleerd):** `normal.pal` byte voor byte gelijk aan ronde 16. De delen `been_achter`, `lijf`, `been_voor`, `arm_achter` en `arm_voor` in `bron/delen_abs.txt` zijn identiek (diff). In het raster verschillen alleen pixels in de snuitzone (x9–33, y30–39) en in de staartzone (x ≥ 48). Oren, schedel, wenkbrauwboogjes, beide ogen (vorm en kleuren), de maskerlobben en de vleugel zijn ongewijzigd. In de hoofdversie staat het verre oog ook nog op zijn plek.

## Wat er veranderde
1. **Staart als hangende J (punt 1).** De staart buigt niet meer over de rug naar de kop. Hij komt laag uit de romp (bovenrand y34, gelijk met de rug), gaat naar achteren, buigt rond omlaag langs x57–62 en krult onderaan terug omhoog. Daar eindigt hij in een **ronde punt in vachtkleur** (x50–54, y46–49: omlijning 1, vulling 4/3, geen donkere punt). Hij is taps: 6 rijen dik aan de voet, de schacht 6 → 5 → 4 breed, de bocht 3–4 rijen, en de punt is weer 5 breed (pluizig, niet naaldfijn). Er zit lucht in: de zak tussen romp en staart (x54–56, y40–45) loopt door in het gat van de haak (x55–56, y47–48; ≥ 2 px). De punt houdt in beide frames 1 px afstand tot de dij. Twee subtiele ringen in schaduwtint staan loodrecht op de staart (x55 y36–37 en y42 x59–61). Animatie: de staart zakt in frame 2 1 px (`staart 1`), tegen de kop en armen in die 1 px omhooggaan. Hij hangt dus, in plaats van mee te veren.
2. **Masker tot de mondhoek (punt 2).** De grijns is ongewijzigd (zelfde vorm: 2 px vanaf de neus, een stap omlaag, 5 px, de mondhoek omhoog en de hoektand eronder). Hij is met de neus naar rechts verschoven. De mondhoek (30,37) sluit via (31,36) diagonaal aan op de onderpunt van de maskervleugel (31–32,35). Zo komt de grijns uit het masker. De crème wang onder het nabije oog ligt nu tussen masker en mondlijn in en loopt door tot de mondhoek.
3. **Neus tussen de ogen (punt 3).** De neus (dezelfde 3×3: `0a0 / 000 / 050`) staat nu onder de neusbrug van het masker en is van x9–11 naar x20–22 verschoven (y34–36). Het crème snuitvlak ligt eromheen en de maskerband krijgt boven de neus een inham van 3 px crème (y33 x20–22), zodat de zwarte neus niet in het donkere masker opgaat. Aan de verre kant sluit de wang rond: omtrek x14, 13, 12, 11 (4 rijen), 12, 13, 14–15, waar vroeger de snuit tot x9 uitstak. De onderkaak (room-schaduw) ligt nu onder de nieuwe mond. De kinlijn van ronde 16 (y38–40) is behouden.

## Meting ogen/neus (punt 3)
| | verre oog | nabije oog | midden tussen de ogen | neus | neus t.o.v. ogen |
|---|---|---|---|---|---|
| ronde 16 | x16–18 (midden 17), y30–32 | x24–28 (26), y29–32 | 21,5 | x9–11 (10), y32–34 | **11,5 px links van het midden, 7 px links van het verre oog**: buiten de ogen, dus profiel |
| ronde 17 | x16–18 (17) | x24–28 (26) | 21,5 | x20–22 (21), y34–36 | 0,5 px links van het midden, tussen de ogen |
| variant_ogen | x14–16 (15) | x24–28 (26) | 20,5 | x20–22 (21) | precies midden, verre wang smaller |

- **Afwijking:** de ogen zelf waren goed. Het nabije oog is 5×4 en het verre 3×3 (kleiner, 1 rij lager), de neus is 3×3, en die verhouding klopt met Gen 3-koppen. Fout was de **richting van de snuit**: de ogen stonden in 3/4, maar de snuit stak er in profiel naar links voorbij. Oog-as en snuit-as spraken elkaar dus tegen. De neuspunt lag 16 px van het nabije oog en 7 px van het verre: in 3/4 hoort hij tussen de twee.
- **Referenties:** in deze repo staan Poochyena, Mightyena, Zigzagoon, Linoone, Sneasel en Umbreon (expansion-sprites) bijna in profiel, met één zichtbaar oog. Daar ligt de neus wel voorbij het oog, maar daar is ook maar één oog. Bij Meowth, Aipom en Sentret (frontaal tot 3/4, beide ogen zichtbaar) ligt de neus op de as tussen de ogen en 1–3 rijen onder de onderrand van de ogen. Ronde 17 volgt dat: de neus begint 2 rijen onder de onderrand van de ogen.
- **Ingreep:** alleen de neus, de grijns en de kaak zijn mee verschoven en de verre wang is rond gesloten. Ogen, masker en schedel zijn niet opnieuw getekend.
- **variant_ogen** (`variant_ogen/`): het verre oog staat 2 px verder naar links, tegen de verre wangrand, en de verre maskerlob loopt mee (y30–33 x12–19). Daardoor staat de neus precies in het midden, en de verre wang wordt smaller, wat meer 3/4 geeft. Het oog zelf is pixel voor pixel hetzelfde. Kosten: het verre oog is aangeraakt, en de wangrand wordt aan die kant donkerder (masker). Het is een keuze voor Jordi; de rest is identiek aan de hoofdversie.

## §0-checklist (SPRITING.md)
1. **Lichaam én blik diagonaal:** ok, en beter dan in ronde 16. Met de neus tussen de ogen kijkt de kop nu echt 3/4 naar links-voor in plaats van ogen in 3/4 op een profielsnuit. Het lijf is ongewijzigd 3/4.
2. **Geteld en verbonden:** ok. 2 oren, 2 ogen, neus, mond met hoektand, 4 poten, 4 klauwen. De staart zit aan de romp vast (voet onder de rugrand, x50–53). bouw9: geen open randen in frame 1 en 2. De binnenrand van het staartgat (55–56,49) en de onderkant van de staartvoet (54–56,39) zijn bewust in omlijningskleur.
3. **Geen rechte lijnen:** ok. bouw9 vindt geen rechte randstukken > 4 px in beide frames. Staartomtrek rechts: 58, 59, 60, 61×2, 62×4, 61×4, 60, 59, 58. Onderkant: runs 2-4-2.
4. **Ogen geïntegreerd:** ok (ongewijzigd: bovenlid donkerst, iris donker boven en licht onder, glans; het verre oog is kleiner en geen kopie).
5. **Silhouet op 1×:** ok. De staart leest als de opgekrulde staart van een boomdier, zoals bij Aipom en Meowth: laag, achter het lijf en omlaag, met een ronde lichte punt. Hij leest niet meer als angel boven de rug. De kop leest als een ronde snuit van voren met een masker (wasbeer/kinkajoe). compare.png: licht en donker.
6. **Formaat:** 1107 / 1118 px (ronde 16: 1170 / 1187). Kleiner door de compactere staart en de kortere snuit, maar nog boven 602–903 (fase 1, Gen 2–3). Het lijf is bevroren.
7. **Pose niet stijf:** ok (ongewijzigd; de staart zwaait nu tegen de ademhaling in).

## Toon (Dark-types)
- Het palet is ongewijzigd. De meest gebruikte kleur blijft basis 3 (289 px), daarna omlijning/masker 1 (212) en schaduw 2 (208). Naast Poochyena en Umbreon blijft hij donker, met het goud van de ogen als accent. Het crème snuitvlak is iets groter dan in ronde 16 en maakt het gezicht op 1× leesbaarder. Het lijf blijft donker.

## Open punten (niet gevraagd, niet gedaan)
- Formaat boven de fase 1-bandbreedte (lijf bevroren).
- Hoofdversie of variant_ogen: keuze voor Jordi.

## Lessen
- **Een neus in de donkere maskerband verdwijnt:** zwart (16,12,18) naast masker (44,28,28) heeft te weinig contrast. Een inham van 1 rij crème boven de neus scheidt ze, en de maskerrand houdt zijn golf.
- **3/4-kop: controleer de neus tegen de oogmiddens**, niet alleen tegen het kopsilhouet. Als de neuspunt buiten de twee oogmiddens valt, leest de kop als profiel, hoe goed de ogen ook in 3/4 staan. Meet het met lijnen op 6× (compare.png, onderste rij).
- **Geen ogen in 3/4 op een profielsnuit:** oog-as en snuit-as moeten dezelfde richting hebben. Bij een korte snuit (kinkajoe, olinguito) ligt de neus 1–3 rijen onder de ogen, tussen de ogen.
- **Een hangende staart naast een lijf: houd de punt ook in het tweede frame los** van de dij. Een staart die in frame 2 omhoogveert (−1), zou hier de dij raken (punt y45 x52 naast de dij op x51). Een staart die omlaagzakt (+1) blijft vrij en geeft een natuurlijke tegenbeweging.
- **Zak en haakgat samen geven de lucht:** de ruimte tussen romp en staart die doorloopt in het gat van de haak, leest op 1× als één bocht. Elke binnenrand van dat gat moet omlijningskleur hebben (bouw9 vangt het).
- **Staart als rijen van 16 tekens (x48–63) met de hand uitgeschreven**, gecontroleerd met `assert len == 16`: sneller en foutlozer dan segmenten tellen.

## Bestanden
- `anim_front.png`, `normal.pal` (= ronde 16), `compare.png`. Bovenaan op 3× en daaronder op 1×, licht en donker: ronde 16, ronde 17 f1/f2, variant_ogen, Aipom en Sentret (staartreferentie), Poochyena en Umbreon (Dark). Onderaan de koppen op 6× met hulplijnen op de oogmiddens (blauw) en de neus (rood).
- Bron: `bron/kop17.py` schrijft de delen `kop` (ronde 16 + snuitpatch `WIS`/`ZET`) en `staart` (`STAART_RIJEN`) in `bron/delen_abs.txt`; de rest is ronde 16. Bouwen: `sh bron/bouw.sh <ronde17-map> [preview.png]`. Vergelijking: `python3 bron/vergelijk17.py <repo-root>` (na het bouwen van de variant).
- `variant_ogen/`: `anim_front.png`, `normal.pal`, `bron/` (dezelfde `kop17.py`, gebouwd met `OLI_VARIANT=ogen`: `sh variant_ogen/bron/bouw.sh variant_ogen`).

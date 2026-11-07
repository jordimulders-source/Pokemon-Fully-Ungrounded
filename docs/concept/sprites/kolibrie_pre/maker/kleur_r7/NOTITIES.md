# Kolibrie pre-evo – kleur ronde 7: volume in de kop, draai en geleend oog (maker, 3 nov)

Jordi, letterlijk:
- "het hoofd is nog steeds veel te 2d"
- "misschien moet er een draai plaatsvinden"
- "en ik vind het oog ook nog steeds niet mooi, is geen pokemon oog, steel er desnoods een"
- (eerder) Taillow is de maatstaf; "Hij mag voor deze vorm best wel een gedefinieerd oog hebben idd, die bij de kolibrie dan mysterieuzer wordt".

Daarnaast de r6-keuring (`kleur_r6/KEURING.md`, 8 FAILs). Twee varianten, beide met hetzelfde palet als r6.

## Bestanden
- **r7a** (alleen kopvolume, omtrek = r6): `rijen_r7.txt` → `raster.txt` (`bouw.py`) → `kolibrie_pre_r7a.png`.
- **r7b** (kop 3/4 naar de kijker gedraaid): `rijen_r7b.txt` → `raster_r7b.txt` (`bouw_b.py`) → `kolibrie_pre_r7b.png`.
- `maak.py` bouwt beide png's; `normal.pal` (palet ongewijzigd).
- `vergelijk_8x.png`: de koppen r6 | r7a | r7b | Taillow | Pidgey op 8×, plus een rij kandidaat-ogen met de keuze.
- `vel.png`: r6, r7a, r7b naast Taillow, Pidgey en Starly op 3× en 1×, licht en donker.

## Het oog: Starly, pixel voor pixel (uitzondering van Jordi: "steel er desnoods een")
- **Kandidaten op 8× (eerste frame):** Taillow, Starly, Swablu, Pidgey, Fletchling, Natu, Pichu, Togepi (rij onderaan `vergelijk_8x.png`).
- **Gekozen: Starly** (x27–29, y27–31 in zijn sprite). Een jong vogeltje met een helder, open oog: een zwart ovaaltje met een witte verticale glans en een lichte onderkant, met zachtere zijkanten. Op 1× leest het direct als Pokémon-oog, en vriendelijk.
- **Afgewezen:**
  - Taillow: het oog zit in een masker, half achter de snavel.
  - Pidgey: een zwart masker.
  - Fletchling en Pichu: een zwart blok met glans, kleiner en minder open.
  - Natu: een starend oog.
  - Swablu en Togepi: lijntjes of halve ogen.
- **Indeling** (5×5, ronde hoeken in de huidkleur):
  ```
  . 1 1 1 .      Starly: . 2 2 2 .
  2 1 7 1 2              1 2 6 2 1
  2 1 7 1 2              1 2 6 2 1
  2 1 5 1 2              1 2 5 2 1
  . 1 1 1 .              . 2 2 2 .
  ```
- **Omzetting naar ons palet:** zwart 2 → `1`, wit 6 → `7`, lichtgrijs 5 → `5` (lila licht), donkergrijze zijkant 1 → `2`. Alleen de hoekjes lopen over in de kap of het gezicht.
- **Plaats:** r7a x24–28, y14–18; r7b x21–25, y14–18.

## Kopvolume (r7a en r7b)
- **Hooglicht:** een gebogen vlek `4` op de koepel linksboven (breedtes 3-4-4-2), geen band langs de rand.
- **Kernschaduw `E`:** een sikkel langs het achterhoofd, smal bovenaan, het breedst (4 px) achter het oog, smal naar de nek.
- **Gezicht en wang:** rond en voor het oog licht `5`, eronder `4`, dan een schaduwsikkel `3` onder de wang naar de nek. Het oog staat zo op een gebogen vlak.
- **Onder de kop:** de borst direct onder de koplijn is `5` (slagschaduw van de kop), het borsthooglicht `7` begint pas een rij lager. Dat maakt de kop los van het lijf.
- **Tinten:** 4 in de kap (4, B, E, lijn 2) en 3–4 in het gezicht (5, 4, 3, lijn 2).
- **Kaplijn in r7a:** volgt nu een boog (stappen 3-2-1-1) van de snavelbasis naar het oog in plaats van een rechte 2-2-2-naad.
- **Kaplijn in r7b:** een koepel over het oog heen: x20–24 op y13, zakt naar de snavel en naar de nek. Hij volgt de bol van de gedraaide kop. Het gezicht wordt daardoor één groot omlijnd vlak met het oog in het midden.
- **Lijnen uit r6:** blijven allemaal (koplijn, kapnaad, vleugel, buik). Alleen de kapnaad kreeg een andere loop (boog/koepel), omdat de rechte naad de bolling tegenwerkte.

## r7b: de draai
- De kop is 3/4 naar de kijker gedraaid, zoals Taillow.
  - Het oog schuift 3 px naar het midden van het gezicht (x21–25).
  - Het voorhoofd schuift 1 px naar voren.
  - De bek zakt 2 rijen en schuift 1 px naar rechts, zodat hij uit het gezicht komt en schuiner naar voren-links wijst.
  - Hij blijft kort en open. In 3/4 zie je in de mond: de mondhoek is gevuld met oranje `D`, met het gele `C` aan de randen. Op 1× leest dat als een open bedelbek.
  - Het verre oog blijft verborgen.
- **Omtrek in de kopzone** (x ≤ 18, y10–21; binnen de toegestane zone x ≤ 34, y ≤ 24): **16 px erbij, 16 px eraf**, tegen r6 (alpha-diff 32). Het lijf is gelijk.

## Keuring r6: wat ik per FAIL deed (beide varianten)
| # | FAIL | wat ik deed |
|---|---|---|
| 1 | banding kruinhooglicht | vervangen door een vlek op de koepel (zie kopvolume); geen band van 3 px langs de rand meer |
| 2 | oog: witte reflectie rechtsonder (hol), losse (28,18) | vervallen door het Starly-oog (geen tweede witte reflectie). In r7a is (28,18) `3` geworden; in r7b staat het oog elders |
| 3 | keelveertjes twee streepjes | één vlekje `98/88` (2×2 met 1 glanspixel) midden op de keel (x21–22, y21–22). Het voorstel van de keurder (`998/888` direct onder de bek) las in r7 als een onderlip/tweede mond; daarom dit kleinere vlekje verder naar achteren |
| 4 | veerlijnen als hark | voorstel overgenomen: (37,32)→`4`, (35,34)→`4`, (36,35)→`4`, (40,35)→`E`. Lichte veerrand bovenaan, eindigt in de schaduw: overlappende veren |
| 5 | flank banding, licht fout | voorstel overgenomen: `4`→`3` op (30–33,35), (29–31,36), (28–30,37), (27–28,38). De flank ligt nu in de schaduw |
| 6 | vleugelvoorrand `4|1|4` | (31,28) en (31,29) → `B`; het licht blijft alleen bij de schouder |
| 7 | nabije poot als stempel | (25,43) → `F`: de voorste teen vangt licht |
| 8 | bovensnavel verdwijnt op donker | binnenrand van de bovensnavel in de gaapkleur `D`: r7a (12,12) (13,13); r7b (13,14) (14,15) |

## Checks (`controle.py`, streng)
- **r7a:** alpha-diff tegen r6: 0.
- **r7b:** alpha-diff tegen r6: 32 (16+16 in de kopzone, zie boven). Het lijf is gelijk.
- **Open randen:** beide alleen nog (25,43) `F`, de teen. Dat is een dun deel; de keurder noemde dit zelf als toegestaan.
  - Ook opgelost: twee nieuwe open randen aan de kruin linksboven, (20,11) en (18,12) in r7a en (19,11), (20,11) en (17,12) in r7b, nu selout `2`.
- **Losse pixels:** alleen bewust (glans en onderkant van het oog, ooghoekjes, glanspixel van de keelvlek, veerrand, licht teentje, snavelpunt).
- 734 px elk; aandeel zeer donker 0,193 (r7a) en 0,191 (r7b).
- **Zelf bekeken** op 8× (koppen naast Taillow en Pidgey) en op 3× en 1×, licht en donker, naast Taillow, Pidgey en Starly:
  - In beide varianten oogt de kop nu als een bol: licht linksboven, schaduw achter en onder, en het oog op een gebogen vlak.
  - r7b staat het dichtst bij Taillow: gezicht naar de kijker, oog in het gezicht, open mond zichtbaar. Ik zou r7b kiezen.
  - r7a houdt de vertrouwde profielkop.

## Wat nog niet klopt
Ik zie geen open punten.

## Lessen
- Een kop wordt pas bol als hooglicht en schaduw sikkels/vlekken zijn die de koepel volgen, en de kapnaad een boog over de bol is. Een rechte naad en een band langs de rand maken hem plat.
- Een 3/4-draai bij een vogel: oog naar het midden van het gezicht, snavel lager en uit het gezicht, en de mond in perspectief gevuld. Dat geeft meer volume dan extra tinten.
- Een geleend oog (Starly) lost "geen Pokémon-oog" in één keer op. Zet het pixel voor pixel om en pas alleen de hoekjes aan de huid aan.
- Een blauwgroen vlakje direct onder de bek leest als onderlip. De keelvlek hoort midden op de keel, los van de snavel.

# La Paz, ronde 2

Secondary op de Andes-primary. Opnieuw maken: `python3 tools/concept/tiles/la_paz_r2.py`.
Bestanden zoals in ronde 1, plus `vergelijking_1x.png` / `vergelijking_2x.png` (ronde 1 | ronde 2 | Mauville).

## Wat er veranderd is t.o.v. ronde 1
Gebouwd op Hoenn-tegels i.p.v. alles zelf getekend: zelfde textuurdichtheid, navy omlijning, grote daken,
Hoenn-ramen en -deuren. Grond, paden, kliffen, trappen, bomen, bloemen, borden komen uit de Andes-primary.

## Hoenn-basis (overgenomen tegels, omgekleurd)
- **Huizen**: het Mauville-huis met golfplaatdak (MauvilleCity x18–21, y11–14, Mauville-palet 7): dak met ribbels
  (calamina), muur, deur, boograam. Drie kleuren via palet 6/7/8 (baksteen + zink, oker + roestrood,
  lichtblauw + groen), plus een **baksteen-variant** van de muurtegels (zelfde indexen, `brickify`).
  Extra verdiepingen uit de Mauville-muur- en raamtegels (0x245–0x247, 0x229/0x22a/0x239/0x23a).
- **Markt**: kraam, potten, kisten, fruit van de Slateport-markt (SlateportCity x10–13, y41–43 en losse stukken;
  Slateport-paletten 9, 6, 7). Kasseien = Slateport 0x211 in warm grijs.
- **Primary (General)**: puna-grond, Hoenn-pad, stenen trap (0xAF), kleiterras (0x7C/0x79), bomen, bloemen, bord.

## Zelf getekend (in Hoenn-paletten)
- Plat betonnen dak (2 rijen) met watertank, wachtijzers, wasgoed (grijstinten van het huispalet, dus ook in 3 kleuren).
- Cholets: modulair (dak, kroonlijst in 3 kleurensets, verdiepingen met spiegelglas, feestzaal, chalet bovenop), palet 12.
- Kabelbaan: masten (oost-west, noord-zuid), kabels (bovenlaag), gondels; station = **Ekat & Heartlessdragoon**,
  'Cable Car', omgekleurd naar het Pokémon Center-palet (primary 0).
- Illimani (12×5) in primary-palet 4.

## Budget
- **337 / 512 tegels, 300 / 512 metatiles** (inclusief 22 tegels / 15 metatiles voor de kabelcombinaties van de mock-up).
- Tegels per onderdeel: cholets 72 + chalet 20, Illimani 51, station 48, markt/kasseien 40, Mauville-huis 25
  (+10 baksteen), plat dak 28, masten 19, kabels 2.
- Paletten: 6–8 huizen (drie kleuren), 9–11 Slateport (kraam, straat, waren), 12 cholet + kabelbaan.
- Ruim 170 tegels vrij voor wat de grote stad nog nodig heeft (Pokémon Center/Mart staan al in de primary).

## Nog niet goed / open
- Kraam: de Slateport-kraam laat een paaltje van de buurkraam zien (rechterkolom); bij inbouw één kolom smaller knippen.
- Gondels hangen als tegels; in de game liever een bewegend object langs de kabel.
- Kleiterras (General 0x7C/0x79) leest als rotsrand; voor hoge hellingen eventueel de gelaagde Fallarbor-wand.
- Alleen één huismodel (Mauville). Voor wijken kan een tweede Hoenn-huis (bijv. Lavaridge met pannendak, voor het
  koloniale centrum) erbij, zonder nieuwe paletten.
- Deuren: gedrag zoals Mauville (deuranimatie via de deurtabel); bij inbouw nalopen.

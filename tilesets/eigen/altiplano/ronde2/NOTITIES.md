# Altiplano, ronde 2

Secondary op de Andes-primary. Opnieuw maken: `python3 tools/concept/tiles/altiplano_r2.py`.
Bestanden zoals in ronde 1, plus `vergelijking_1x.png` / `vergelijking_2x.png` (ronde 1 | ronde 2 | Route 113).

## Hoenn-basis (Fallarbor-secondary, omgekleurd)
- **Adobe-huis met strodak**: het huis van Route 114 (x28–31, y2–5): oranje latjesdak → stro, groene planken →
  leemblokken (`adobify`, zelfde indexen), raam en deur blijven.
- **Queñua**: de bolle boom van Route 113/114 (0x204/0x205/0x20C/0x20D) met donker blad en roodbruine bast, op puna.
- **Klifwand**: de gelaagde wand van Route 114 (0x31E rand, 0x269 wand, 0x271 voet) in roodbruin.
- **Akker (chacra)**: de akker van Route 114 (x33–35, y6–8) op rode klei.
- **Droge puna en paja brava**: asgrond 0x218 en asgras 0x20A van Route 113 in strokleuren.
- **Pad**: het oranje pad van Route 114 (0x2E8/0x2EA/0x2F0/0x2F2) als onverharde weg.
- Uit de primary: puna-grond, **ichu** (hoog gras), bergketen + lucht, rotsjes (0xE0), bloemen, kantuta.

## Zelf getekend (in Hoenn-paletten)
- Pirca-muurtjes (horizontaal, uiteinden, verticaal) in de grijze stenen van primary-palet 3, poort van de lamakraal
  (hout uit het boompalet), apacheta (1×2), rond voorraadhuisje (2×3, adobe/stro-palet),
  bofedal (veen met poeltjes, Hoenn-dither naar de puna) in palet 12.

## Budget
- **146 / 512 tegels, 71 / 512 metatiles.**
- Paletten: 6/9 boom + klif (Fallarbor 6/9), 7 adobe + stro, 8 pad, 10 primary-palet 3 met puna-tinten (grond onder
  bomen), 11 droge puna/paja, 12 bofedal. Alle 7 in gebruik, wel met veel ruimte in de tegels.

## Nog niet goed / open
- Klifwand heeft nog geen hoek- en eindstukken in de mock-up (Fallarbor heeft ze: 0x268, 0x270, 0x278); bij een echte
  route meenemen.
- Bofedal is nog een rechthoek; grillige randen en geanimeerde poeltjes kunnen later.
- Pirca-hoeken ontbreken (alleen recht + uiteinden); een ronde kraal vraagt schuine stukken.
- Geen dieren in de tegels (lama's en vicuña's zijn Pokémon/NPC's).

# Alpaca ronde 5: lijf en poten met de hand, kleinere starterverhoudingen

Feedback op ronde 3/4 (Jordi): verhoudingen, ogen, clumsy vormen, shading en dynamiek moeten meer Gen 3 worden. Ronde 4 was "iets beter". Kleur en design blijven gelijk (zelfde `normal.pal` als ronde 4).

## Bestanden
- `anim_front.png` (64×128, 2 frames, index 0 transparant), `normal.pal` (gelijk aan ronde 4).
- `compare.png`: ronde 4, ronde 5 f1/f2, Torchic, Mudkip, Treecko, Ponyta, Mareep, Growlithe, Vulpix (GBA), op 3× en 1×, op een veldkleur en als silhouet.
- `bron/`: `sh bron/build.sh` bouwt alles opnieuw. `alpaca5.txt` is het pixelraster (ascii_sprite-formaat) om verder met de hand te bewerken.
  - `frame1.py`: kop, oren, gezicht, ogen en voorpoten per pixel (segmenten per rij).
  - `fix1.py`: handcorrecties (bolhoed, kin, borst, buik, poten).
  - `sil.py` + `cloud.py` + `shade.py`: silhouet en basisschaduw van wollijf/hals; daarna met de hand bijgewerkt.
  - `compose.py`: zet alles samen, selout-pass, frame 2 (stoot) en plaatsing.

## Wat er anders is dan ronde 4
- **Verhoudingen:** grote kop (±half van de hoogte) op een compact wolkenlijf, zoals Torchic/Mudkip; het lijf is kleiner en ronder, de poten langer en dunner (alpaca, geen schaap).
- **Kop:** wollen "teddybeer"-kop: de vacht zit alleen rond ogen en snoet, met wollen wangen die doorlopen in de hals. Lichte, ronde snoet met neusgat en een vastberaden mondlijn; onderkaak met alleen een smalle schaduwrand (geen paardenkaak).
- **Ogen:** Pokémon-ogen zoals Eevee/Vulpix: zwart met een witte glans van 2 px linksboven en een bruine iris onderin. Nabij oog 5×6, ver oog 3×4 (perspectief). De bovenkant is schuin afgesneden onder de hoedrand: vechtersblik.
- **Bolhoed:** ronde koepel met rode band en een rand met opgekrulde punt; leest nu als hoedje, niet als pet.
- **Wol:** het lijf is een wolk van bulten met elk een lichte sikkel linksboven en korte krullijnen waar een bult over de volgende valt; de fluffiness zit in de geschulpte contour, niet in ruis.
- **Shading:** licht van linksboven; wol 1/2/3 met selout 4, vacht 5/6/7, handschoenen 8/9/a. Een selout-pass zet zwarte randen linksboven om in de donkerste tint van het onderdeel (ook op de handschoenen).
- **Dynamiek:** driekwart naar links; kop naar de kijker, lijf wijkt naar achteren, verre poten hoger en donkerder. Frame 1: dekking met opgeheven handschoen, schuine achterpoot. Frame 2: stoot (handschoen 2 px naar voren, langere voorpoot), kop 1 px omlaag, mond open met tandje, staart wipt.

## check.py (`--stage 1`)
Hoogte 48, breedte 48, oppervlak 1300 (ronde 4: 46 hoog), 15 kleuren, schaduw 39 %, 5 losse pixels. LET OP: zwart aan de rand 0,63 (p90 0,578), weinig dithering, verschil tussen frames 0,27 (net onder p10: bewust subtiel). Geen back/icon (buiten deze opdracht).
species_info: `.frontPicSize = MON_COORDS_SIZE(56, 48)`, `.frontPicYOffset = 8`.

## Wat ik zelf nog zwak vind
- **Nog wat groot** voor fase 1 (oppervlak 1300, mediaan 912); de kop is bewust groot gehouden.
- **Het gezicht** is nog een vrij hoekig bruin vlak; de wangen en de snoet kunnen ronder, en de mondlijn is klein.
- **Poten:** de achterpoten zijn dunne stokjes met maar een kleine knik; Ponyta/Growlithe hebben echte gewrichten. De verre achterpoot is een stompje.
- **Hals/borst:** veel egaal wit; er mag meer vorm in (een tweede plukje, schaduw onder de opgeheven poot is nog vlak).
- **Wollijf:** de schaduw is nog deels uit een script; een Gen 3-spriter zou de krullen ritmischer zetten (Mareep).
- **Frame 2:** de open mond leest bijna als een tong.
- Nog te maken: back, icoon, shiny en varianten.

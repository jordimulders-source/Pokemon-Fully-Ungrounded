# Hitmontop-evolutie, sprite v2 ronde 1 (schone start)

Niets uit r1–r3 hergebruikt (geen raster, geen bevroren delen). Alles met de hand per rij geplaatst in `raster.py` (segmenten `put(y, x, "tekens")` en één tekenblok voor het haar); `raster.txt` is de uitgeschreven 64×64.

## Bestanden
- `pose_silhouet.png`: stap 1, met de hand opgegeven silhouet (`pose.py`) als rode omtrek over de gespiegelde foto, zwart vlak, naast Hitmonlee en Hitmontop (8× en 1×). Het fotomasker (gespiegeld, 61 px hoog) was de maat; kop en handen zijn Pokémon-groot gemaakt, de broek aansluitend.
- `kop.png`: kop + haar op 8× naast Hitmontops kop en rand en Hitmonlee's kop, op dezelfde schaal.
- `sprite.png` (64×64, geïndexeerd, 16 kleuren, index 0 transparant), `normal.pal`.
- `vel.png`: 8× en 1× (licht/donker, 2×) naast Hitmontop en Hitmonlee, plus close-ups van kop en benen.
- `controle.py`: samenhang, marge, kleuren, tintclusters < 3 px, lichte pixels op de buitenrand.

## Welk onderdeel komt uit welke sprite
- **Palet**: Hitmontops `normal.pal` (huid 2–5, blauw 6–9, rood 10–11, grijs 12–13, zwart). Index 14 (was donkergrijs) is nu donkerbruin `5A3418` voor het haar.
- **Ogen**: pixel voor pixel van Hitmontop (linkeroog 5 breed: `..KK. / .KWKK / KKKKK / KSKK.`; rechteroog 4 breed), alleen dichter bij elkaar gezet voor de kleinere kop.
- **Haar**: Hitmontops brede bruine rand met punten links en rechts en radiale donkere strepen. Gerestyled: de rand ligt nu als volume op de schedel, de strepen zijn de scheidingen tussen dikke lokken, de **linkerpunt** valt als twee dikke gedraaide lokken met de zwaartekracht omlaag langs de slaap (y32–40), de **rechterpunt** blijft een korte lok achter het oor (eindigt op y34, boven de hals). Donkerder bruin dan de huid (D/o/h), zodat het op 1× haar is en geen huid.
- **Hoorn**: Hitmontops bruine punt, klein (3 px) midden op de kruin.
- **Handen**: ronde bal zoals Hitmontops hand (lichte huid, witte glans 1 px).
- **Voeten**: Hitmontops blauwe voet met witte/grijze klauwen, kleiner (7×5) dan bij Hitmontop t.o.v. het been; met een strookje huid bij de enkel zodat broek en voet los lezen.
- **Kopmaat/verhoudingen**: Hitmonlee als maat (gezicht ±15×13 px; kop is niet groter dan de romp). Pose: gespiegelde foto.
- **Koordjes**: cordão van de tailleband omlaag (rood, met kwastje), prajiad om beide bovenarmen (steunarm: band + staartje dat langs de arm hangt; vrije arm: band dwars over de arm).

## Anatomiecontrole
- Haar alleen aan de schedel: ja. Linkerlokken beginnen aan de slaap boven het oor en hangen náást het gezicht (1 px lucht ertussen); niets op wang, kin of keel. Rechterlok eindigt op ooghoogte.
- Hals: ja, korte hals achter de kaak (x25–28, y35–41) in schaduwtint naar de schouders.
- 2 armen: steunarm (schouder onderaan de romp, recht omlaag, ronde hand op de grond, rij 62) en vrije arm (schouder bovenaan de romp, bovenarm schuin over de borst, elleboog steekt rechtsonder uit, onderarm omhoog, ronde hand op de heup over het blauw).
- 2 benen aan de heup, 2 voeten aan de enkels, klauwen aan de tenen.
- Eén samenhangend geheel (controle.py: 1 deel, 1221 px), marge ≥1 px (x4–61, y2–62), 15 van 16 kleuren gebruikt, geen lichte pixels op de buitenrand.
- Kleine tintclusters die overblijven zijn bedoeld: klauwpunten, losse pixels in diagonale lijnen (haarscheidingen, broekrand), het koordkwastje.

## Eerlijke zwakke punten
1. **Romp + vrije arm** is het zwakste deel: de bovenarm leest als band over de borst, maar de romp erboven en eronder heeft weinig vorm (geen duidelijke borst/buik); de onderarm achter de hand is kort en valt weg.
2. **Benen** zijn nog vrij buisvormig (rand-schaduw-licht-rand parallel); er is alleen een knie-accent en een iets dikker dijbeen, geen echte spiervorm.
3. **Haar**: de twee lokken links kunnen op 1× lezen als een zijstaart; Eddy Gordo zit vooral in de dikke lokken, niet in volume. Mogelijk wil Jordi meer lokken of ze langer.
4. **Gezicht** blijft het kinderlijke Hitmontop-gezicht (zonder mond-/wenkbrauwkeuze; mond is een streepje). "Ouder" zit vooral in lijf en verhouding, niet in het gezicht; uitdrukking staat in de SPEC nog open.
5. Steunarm is dun en recht (Hitmontop-dun) met een grote ronde hand: kan als "lolly" lezen.

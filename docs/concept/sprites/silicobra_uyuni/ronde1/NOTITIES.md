# Silicobra (Uyuni) – ronde 1, frontsprite frame 1

Bestanden: `silicobra_uyuni.png` (64×64, geïndexeerd, 14 kleuren, transparency=0), `silicobra_uyuni_raster.txt` (volledig tekstraster, één teken per paletindex), `rijen_x12.txt` (de met de hand getypte rijen 13–41, x 12–51; `?` = basispixel met het nieuwe palet), `vel.png`, `scripts/` (bouw, controle, vel).

Jordi (letterlijk): "een pallette swap is niet genoeg." / "Ik zie de zoutkorst 100% zitten en ook de pekelzak ziet er mooi uit. Het half dichtgevallen oog is ook goed te doen gezien de originele sprite [...] De zoutkuif is niks mis mee op zichzelf denk ik" / "En idd loom, trager zou prima zijn. Wat meer een wall" / "dan is A prima" / over schets A: "ik vind het best al prima, alleen mag je het nog iets netter afwerken".

## Game Freak-studie
| Sprite | Wat ik zie | Wat ik overneem |
|---|---|---|
| Sandshrew (Alola) | Tegels gescheiden door naden in een **middentint** (geen zwart); elke tegel heeft een lichte pixel op de linkerbovenrand (afgeschuinde rand) en wordt naar rechtsonder donkerder; tegels aan de rand van het lijf smaller. Leest als ijs door ijsblauw + wit. | Naden in middentint, lichte rand linksboven per plaat, smallere platen aan de rand. **Niet** de kleur. |
| Torkoal | Schild van grote donkere platen met naden; weinig, grote vlakken; de rand van het schild steekt iets uit het silhouet. | Weinig, grote platen; kuif als rand die het silhouet zwaarder maakt. |
| Shuckle / Relicanth | Korst/schild als aparte kleurgroep met eigen omlijning; platen volgen de ronding (Relicanth: vlakken met zachte overgang, geen raster). | Korst volgt de bol: naden lopen trapsgewijs schuin omlaag naar de rand (breedtegraden), geen plat raster. |
| Lanturn / Chinchou | Lichtbollen: wit glanslicht van 2 px linksboven, middentint, donkere rand rechtsonder; omlijning in een donkere tint van dezelfde kleur, niet zwart aan de lichte kant. | Pekelzak: glans 2 px diagonaal linksboven, donkere kant rechtsonder, donker turquoise rand aan de lichte kant, zwart alleen aan de schaduwkant. |
| Sandaconda / Silicobra | Zak en kop als één massa; het oog is een ovale ring met verticale spleetpupil; staartkrul met gat. | Ring, spleetpupil, krul en gat blijven; alleen materiaal verandert. |

## Wat ik deed
- **Werkwijze:** basis omgezet naar het nieuwe palet (olijf → zout, groen → turquoise of zout), daarna rij 13–41 met de hand getypt in `rijen_x12.txt` (kuif, korst, oog, pekelzak). Schets A als ontwerp aangehouden (vorm kuif en zak, kleuren, half oog, plaatsing van de platen); niets herontworpen.
- **Kuif:** drie platen bovenop (rij 13–17, max. 3 px boven het oude silhouet) met naden die naar het midden van de kop wijzen, en drie platen op de achterkant (max. 3 px uit). Onder de bovenste platen een schaduwlip (mid-oker), zodat het een rand is en geen grotere kop. Geen punten of kubussen.
- **Zoutkorst:** de vlekken zijn vervangen door grote veelhoekige platen; naden in middentint (`d` in het licht, `e` in de schaduw), geen zwart; per plaat een lichte rand linksboven; de naden op de achterkant lopen trapsgewijs schuin omlaag (volgen de bol), de platen worden aan de rand smaller.
- **Oog:** zwaar bovenlid (huid in zouttinten, licht van boven) tot halverwege; lidrand donker met licht hangende hoekjes; iris turquoise: donker direct onder het lid, lichter onder, spleetpupil, glanspixel. Lid recht, niet schuin naar de snuit: loom, niet boos.
- **Pekelzak:** turquoise, doorschijnend: donkere rand aan de lichte kant in donker turquoise (geen zwart), glans 2 px linksboven, middentint, donker rechtsonder met een iets lichtere teruggekaatste plek bij de rand, twee belletjes. Rechterkant rond (bolt 1–2 px uit, rij 33–41) en sluit aan op de staartkrul zonder de krul te raken behalve onderaan (rij 40–41, waar hij erachter wegloopt).
- **Kleur:** warm gebroken wit en grijs-oker (zout/klei), staart en voet in de bestaande beige/zouttinten; turquoise alleen in oog en zak. Staartkrul in zouttinten, gat transparant; staartpuntje bij de voet zouttint (geen turquoise).

## Diff-bewijs (`scripts/controle.py`, alpha t.o.v. `graphics/pokemon/silicobra/anim_front.png` frame 1)
| Zone | Erbij | Eraf |
|---|---|---|
| Kuif (kop, rij ≤ 31: boven/achterkant) | 92 | 0 |
| Pekelzak (rij 32–43, nek) | 10 | 0 |
| Rest (gezicht, voet, staart, krul) | 0 | 0 |
Pixels: 991 (basis 889). Open randen: 0 (elke pixel naast transparant is een randkleur). Losse pixels: 0. Eenzame kleurpixels alleen bewust (glans, belletjes, neusgaten, basisdetails).

## Checklist SPRITE_NORM
1. Leest als echte Pokémon op 1×: ok, herkenbaar Silicobra (zelfde silhouet/pose/gezicht) naast Sandshrew-A, Lanturn, Torkoal, Shuckle, Sandaconda (vel).
2. 3/4 links-voor: ok, ongewijzigd van de basis.
3. Ledematen: n.v.t. (slang); staart en krul tellen en zijn vast.
4. Geen Escher: ok; de zak ligt vóór de krul-overgang, de buik vóór de zak (zoals in de basis).
5. Lijf over echte sprite: ok (de basis zelf); kuif en zak volgen de bestaande curve, geen rechte stukken ≥ 4 px buiten de lidrand en de plaatnaden.
6. Kop: ongewijzigd behalve de kuif (+3 px), bewust (wall).
7. Ogen: bovenlid donkerst, iris donker boven/licht onder, glans; geen bril (ring zonder zwarte zijlijnen).
8. Kenmerken op 1×: kuif, platen, zak en half oog lezen op 1× (vel).
9. Omlijning per kleurgroep: zwart aan de schaduwkant en boven, gekleurde rand aan de lichte kant (bruin bij het gezicht, donker turquoise bij de zak); licht linksboven; geen open randen.
10. Geen Chernobyl: gezicht = basis; geen losse delen, geen crème vlakken uit het niets.

## Eerlijk oordeel
- Netter dan schets A: geen zwarte naden meer, de rechterkant van de zak is rond, de kuifplaten zijn rustig, het turquoise vlekje links op het voorhoofd uit de schets (fout in het schetsscript) is weg.
- Kanttekening (geen zwak punt dat ik nog kan oplossen zonder herontwerp): op 64 px lezen de platen als **veelhoekige tegels**, niet als zuivere zeshoeken; een zeshoek heeft ±6–7 px nodig en de achterkant van de kop is maar ±9 px breed. Zo deed schets A het ook. Wil Jordi meer "zeshoek", dan kan dat pas op de grotere evolutie.
- Mond (frame 2), rug, icoon, shiny: niet in deze ronde.

## Lessen
- Een gescripte schets als startpunt omzetten naar tekens en dan per onderdeel overtypen werkt snel; let op schetsfouten (hier: groene basispixels die het script als oogkleur zag).
- Twee evenwijdige naden (plaatgrens + kuifrand) op 3 px afstand lezen als strepen; laat de kuif zelf de buitenste rij platen zijn.
- Naden in perspectief: trapsgewijs 1 px omlaag naar de rand houdt ze rond zonder lange rechte lijnen.

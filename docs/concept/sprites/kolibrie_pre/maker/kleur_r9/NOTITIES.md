# Kolibrie pre-evo – kleur ronde 9 (maker, 3 nov)

Jordi, letterlijk:
- "de snavel is in r8 verknald"
- "r8 lager is goed wat betreft het hoofd"
- "met het snavel bedoel ik puur dat de verbinding aan de mond wat meer een lijn moest hebben, zoals bij andere pokemon, niet dat het hele snavel anders moest"

Keuring r8: alleen C3 (voorhoofd) telt; C1/C2 en het kapgrensadvies vervallen door Jordi's keuze.

## Opbouw (`maak.py`, met de hand opgegeven pixels)
1. **Kop = r8 lager** (`kleur_r8/raster_lager.txt`): kap en kapgrens (kleur, geen lijn), Starly-oog, keel zonder vlekje, lijf.
2. **Snavel = r7b, pixel voor pixel** (vorm én kleuren): rij 12–13 x ≤ 14 en rij 14–21 x ≤ 16 uit `kleur_r7/raster_r7b.txt`.
3. **Een donkere lijn waar de snavel aan het gezicht vastzit** (8 px), zoals bij Taillow en Starly, waar een donkere lijn snavel en kop scheidt en de mondhoek als lijn het gezicht in loopt:
   - snavelbasis schuin omlaag: (15,14) `1`, (15,15) `1`, (16,16) `1`;
   - mondhoek het gezicht in: (17,17) `1`, (17,18) `1`, (18,18) `2` (het uiteinde iets lichter);
   - basis van de ondersnavel: (17,19) `1`, (17,20) `1`.
4. **Voorhoofd als koepel** (keuring r8, C3; zone waar snavel en voorhoofd samenkomen):
   - omtrek links van boven naar beneden 23-20-18-17-16-15: looplengtes 3-2-1-1-1, een koepel in plaats van de trap 2-2-2-2;
   - (20,10) erbij (`2`), (18,11) erbij (`2`), (15,13) weg;
   - (14,14) weg: een **inkepinkje** tussen de bovenrand van de snavel en het voorhoofd, zodat de snavel vóór het gezicht zit;
   - vulling aangepast: (20,11) `4` (kruinlicht loopt door), (18,12) `B`.

## Bewijs (uitvoer van `maak.py`)
- **Oog:** 0 van de 21 oogpixels anders dan r7b.
- **Snavel tegen r7b** (zone x ≤ 20, y 9–21): anders zijn alleen
  - de 8 lijnpixels;
  - de 6 voorhoofd- en koepelpixels hierboven;
  - de kapgrens van r8 lager: (16,13) `2`, (20,13) en (18–20,14) en (17–18,15) `B`;
  - B3 van r8: (16,12) weg.
  
  Alle snavelpixels zelf zijn gelijk aan r7b.
- **Alpha-diff tegen r7b:** (20,10) erbij; (16,12), (15,13), (14,14) weg.
- **Buiten de snavelzone anders dan r8 lager:** alleen de koepel (20,10), (18,11), (20,11), (18,12) en de lijn (17–18,17–20).

## Checks (`controle.py`, streng)
- **Open randen:** alleen (25,43) `F`, de teen; door de keurder toegestaan.
- **Losse pixels:** alleen bewust (onderkant oog, uiteinde mondlijn (18,18), veerrand, teen).
- 732 px; aandeel zeer donker 0,201.
- Paletplekken 8 en 9 (roze/donker uit r8) worden niet meer gebruikt en zijn weer vrij.
- **Zelf bekeken** op 8× naast r7b, r8 lager, Taillow, Starly en foto 3 (`vergelijk_8x.png`), en op 3× en 1× op licht en donker naast Taillow (`vel.png`):
  - De snavel is die van r7b.
  - De donkere lijn langs de snavelbasis en de mondhoek die het gezicht in loopt, maken de verbinding duidelijk, zoals bij Taillow en Starly.
  - Het voorhoofd is rond, met een klein inkepinkje boven de snavel.

## Wat nog niet klopt
Ik zie geen open punten.

## Lessen
- "De snavel klopt niet" kan ook alleen over de verbinding gaan. Eerst vragen wat precies, of de kleinste ingreep doen, voordat je de hele snavel opnieuw tekent.
- De overgang van snavel naar kop leest als Pokémon-sprite met één donkere lijn langs de snavelbasis en een mondhoeklijn van 1–2 px het gezicht in.
- Een voorhoofd dat als gelijkmatige trap (2-2-2-2) op de snavel aansluit leest hoekig. Een koepel (3-2-1-1-1) met een inkeping van 1 px boven de snavel zet de snavel ervoor.

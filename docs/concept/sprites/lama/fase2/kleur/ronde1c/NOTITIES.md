# Lama fase 2: kleur ronde 1c (maker-agent, 2 nov)

De zes reparaties uit `../ronde1b/KEURING.md` (oordeel BIJNA), precies binnen hun zones. Al het andere is pixel voor pixel ronde 1b.

## Bestanden
- `lama.png` (P, 16 kleuren, transparency=0), `normal.pal` (ongewijzigd), `raster_grid.txt`.
- `vel.png`: ronde 1c op 4× licht en donker, ronde 1b op 4× ernaast, 1×, en op 3× en 1× naast de alpaca en 5 Gen 3-sprites.
- `bron/reparaties2.txt`: de nieuwe laag, met de hand getypt als `x y letter` per punt, bovenop `raster.txt` + `reparaties.txt` (ronde 1b).
- `bron/diff_r1b.py`: diff per keurderpunt; `bron/zoom_*.png`: 8×.

Bouwen:
```
python3 bron/bouw.py && python3 bron/controle.py && python3 bron/diff_r1b.py && python3 bron/vel.py
```

## Bewijs
```
mode P transparency 0 | pixels 1188 | alpha-diff 0
kleuren gebruikt: 16 | open randen: 0
gewijzigd per punt: halsband 17, aguayo 14, nagels 8, buiklijn 23, verre poten 28, spikkels 2 | totaal 92 | buiten de zones: 0
```

## Per punt
1. **Halsband (17 px).** Twee doorlopende rijen langs de U:
   - bovenrij in 2-px-blokjes geel/teal (x21–29), zonder rood en zonder vacht ertussen;
   - middenrij rood van x21 tot x29 (q vooraan in het licht);
   - rand m eronder;
   - pompons van 2 px (kleur + m eronder): roze x22, geel x24, teal x26, roze x28;
   - rechts draait de band in r/m omhoog achter de hals weg (x29–31, y25–27).

   Op 1× leest hij als een gekleurde halsband met franje aan de halsbasis.
2. **Aguayo (14 px).**
   - De linkerrand hangt af in segmenten 1-2-3: (39,26), (38,27–28), (37,29–31). De bovenhoek gaat naar vacht, de onderhoek naar m.
   - Geel links een hooglicht (h), rechts donker (d); blauw rechts n; rood had al q links en m rechts.
3. **Teennagels (8 px).** Twee nagels van 2 px per handschoen, licht boven en d onder (de onderkant is een rand):
   - nabij: h op (21,55) en (23,55);
   - ver: l op (28,61) en (30,61), in de schaduwtint.
4. **Buiklijn (23 px).**
   - De donkere band buigt: voorin naar y38 (x26–29), in het midden y39, achterin weer naar y38 (x44–47).
   - De schouder van de nabije voorpoot (x24–29, y39–40) en de nabije dij (x45–49, y39) lopen er licht (b/l) overheen.
5. **Verre poten (28 px).**
   - De lichtkant links is nu d in plaats van k (voorpoot x30 y44–56; achterpoot x39–42 y45–57); zwart alleen rechts.
   - Een gewricht in b maakt ze verschillend: een knie voorop de voorpoot (31,49) en een hak in de achterpoot (43,51).
6. **Spikkels (2 px).** (36,36) en (40,36) naar b.

Totaal 92 px (budget ±100).

## Eigen keuring (8×, 3× en 1×, licht en donker, naast ronde 1b)
- **Halsband:** de U is nu één doorlopende rode lijn met een gele/teal rand erboven en pompons eronder. Op 1× leest hij als halsband en niet meer als confettivlek. De bocht van de U is op 1× klein (2 px); dat is de ruimte die de hals op die hoogte biedt.
- **Aguayo:** hangt links af en buigt licht naar donker.
- **Nagels:** lezen op 1× als twee lichte puntjes onder elke handschoen.
- **Buik:** loopt rond, met schouder en dij eroverheen.
- **Verre poten:** geen zwarte paaltjes meer.

## Lessen
- Een band leest als ring door één doorlopende kleurrij (de rode middenrij) langs de U. Blokjes en pompons erboven en eronder zijn versiering; onderbreek de kernrij nooit met vacht.
- Pompons van 1 px lezen als confetti; met 2 px (kleur + schaduw) lezen ze als belletjes.
- Een nagel van 1 px grijs tussen zwart valt weg; licht boven donker (2 px) leest op 1×.
- Verre poten: ook aan de lichtkant de omlijningstint van de vacht, zwart alleen aan de schaduwkant. Eén gewrichtspixel maakt twee paaltjes tot twee verschillende poten.

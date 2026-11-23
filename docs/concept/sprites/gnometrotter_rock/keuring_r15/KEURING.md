# Definitieve eindkeuring Gnometrotter Rock r15 (23 nov)

Gekeurd: `sprite_r15/gnometrotter_rock.png` (= `af/gnometrotter_rock.png`, byte-gelijk). Model: `r8/gemini_r8.png`.
Maatstaf: Gnomad (`gnomad/af/`), steenjaguar/welp, bloedmaan, corona, Regirock. Eerst gemeten, niet strenger dan die sprites.
Bevroren en niet beoordeeld: silhouet en alle vormen, schouderovaal/ruglijn/binnenlijnen uit Jordi's krabbel (r15), rugrots, het drukke lijf, geen gesp, dichte oogstrook, ronde neus.

## Oordeel: PASS

Geen reparaties nodig. `raster.png` = sprite op 14× met raster en x/y-nummers; er zijn geen pixels gemarkeerd omdat er niets voorgesteld wordt.

## 1. Kleurtinten
| groep | tinten (helderheid) | lijn |
|---|---|---|
| gesteente (muts, rots, riem, stok, zolen) | 5 154 / 4 124 / 3 94 | 2 67 |
| baard en plukjes | E 223 / D 192 / 5 154 | 4 124 (lichte eigen lijn, zoals de snor van Gnomad) |
| roze lijf, armen, handen | F 206 / 8 183 / 7 139 | 6 105 |
| blauwe broek | C 205 / B 173 / A 134 | 9 97 |

- Elke vorm heeft ≥ 3 tinten; stappen 26–44, binnen de Gen 3-band en gelijk aan Gnomad.
- Tintvlekjes < 3 px (zonder omlijning): r15 8,8 % — r9 10,5 %, Gnomad 8,2 %, steenjaguar 13 %, Regirock 18 %. Binnen de maatstaf.
- Alle reparaties uit de r9-keuring zitten erin (nagemeten, o.a. muts (29,12)=2, (30,12)=4; baard (26,33)/(27,35)/(28,35); dij (25,47)=9).
- Geen pillow shading; mutsbanden volgen de kegel.

## 2. Schaduw
- Eén lichtbron linksboven, consequent: muts 5 links → 3 rechts; baard E links → 5 rechts; lijfplaten F/8 linksboven, 7 rechtsonder; dijen en voeten met glans B/C linksboven; handen F linksboven en 7-sikkel rechtsonder; stok licht links.
- Slagschaduw onder de muts (2-strook), baard op de riem (3) en riem op de broek: kloppen met dezelfde lichtbron.
- Volume per groot vlak is er (muts, rots, lijf per plaat, baard, broek, handen), niet alleen langs de rand.

## 3. Lijnen (Dragonfly Cave)
Gids, `docs/lessen/bronnen/dragonflycave_spriting_guide.txt`:
- r. 92–94: "The 'outline shadows' are always black (or ever-so-slightly off-black)".
- r. 421–423: "we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."
- r. 425–428: lichtere pixels nooit aan de buitenkant van de lijn, "lighter pixels on the inside of the outline are a far better idea".

Gemeten op de buitenrand (`sprite_r9/meet.py`):

| | boven | links | rechts | onder |
|---|---|---|---|---|
| r15 zwart | 26 % | 27 % | 90 % | 89 % |
| Gnomad zwart | 17 % | 24 % | 80 % | 83 % |
| steenjaguar zwart | 48 % | 60 % | 84 % | 90 % |

- Buitenrand bestaat alleen uit 1 (zwart), 2, 6, 9 en 4: elke kleur heeft zijn eigen donkerste lijntint; geen enkele lichte tint op de rand.
- Zwart boven/links alleen als Popplio-boog linksonder (neus (17,20–22), plukje (12–14,17–18), linkerhand (2–3,33–35), rechterhand (52,37–39), riemhoek (19,41)) en op de naar rechts aflopende schuinten (mutsrand (40,4)–(43,7), bovenarm (52–53,27)), net als bij Gnomad.
- Om-en-om zwart/kleur op één rand: 0 gevallen (script). Open randen/gaten: 0.
- Binnenzwart (44 px) alleen waar vorm over vorm valt: neus over baard, handen over stok/arm, riem over broek (incl. de schuine naad rechts (43–49,36–40)), kruis. Overige binnenlijnen in de eigen tint (2, 6, 9, 4). Geen onnodig zwart gevonden.
- Lijndikte 1 px; de 2×2-knopen uit r9 zijn weg.

## Niet als fout gemeld (gemeten, klopt of te klein om te tellen)
- (20,31) één E-pixel naast de 5-strook (19,31–32) op de baardrand: leest als schaduw van de arm op de baard met lichte rand; geen storing op 1×.
- De horizontale 9-lijnen op de broek (rij 45 en 47) liggen op de naden/dijonderkant van het model.
- Zwarte rand bovenop de bovenarm (52–53,27): zelfde behandeling als de schuine mutsrand en Gnomad; bovendien naast Jordi's bevroren schouderzone.

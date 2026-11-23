# Eindkeuring Gnometrotter Rock r9 (23 nov)

Gekeurd: `sprite_r9/gnometrotter_rock.png`. Model: `r8/gemini_r8.png`. Maatstaf: Gnomad, Gnomini, de welp, de steenjaguar, de bloedmaan, de corona en Regirock (eerste frame).
Bevroren en niet beoordeeld: het silhouet en de vormen, de rugrots, het drukke lijf, geen gesp, de dichte oogstrook.

## Oordeel: BIJNA (wordt PASS na de reparaties hieronder)

Er is geen structureel probleem. Wat overblijft zijn 14 pixels tint- en lijnkleur, op plekken waar het model zelf iets anders laat zien. Een proefversie met alle reparaties staat in `voorstel_r9_reparaties.png`:
- silhouet-diff 0;
- vergelijking op 8× met de gewijzigde pixels rood omkaderd, plus 1× en 2×: `vel_keuring.png`.

## 1. Kleurtinten

**Tinten per onderdeel (≥ 3):**

| onderdeel | tinten |
|---|---|
| muts | 5/4/3 + lijn 2 |
| baard en plukken | E/D/5 + lijn 4 (zoals de snor van Gnomad: lichte lijn 131 op crème) |
| lijf en handen | F/8/7 + lijn 6 |
| broek | C/B/A + 9 |
| riem, stok, zolen | 5/4/3 + 2 |

Alles OK.

**Helderheidsstappen:**
- grijs: 68 → 94 → 123 → 152 → 191 → 222 (stappen 26–39);
- roze: 115 → 150 → 193 (+ glans 212);
- blauw: 102 → 142 → 181 → 210.

Dat is binnen de Gen 3-band van ±30–40 en gelijk aan het palet van Gnomad.

**Vlekjes < 3 px**, met de omlijning eruit, als deel van alle pixels:

| sprite | vlekjes |
|---|---|
| r9 | 11 % (222/1989) |
| Gnomad | 10 % |
| corona | 9,5 % |
| steenjaguar | 13 % |
| welp | 20 % |
| Regirock | 18 % |

r9 valt dus binnen de maatstaf. De echte stoorvlekjes staan bij de reparaties.

**Banding en pillow shading:**
- De muts heeft drie banden van ≥ 2 px die de kegel volgen. Dat is normaal kegelschaduw, geen banding.
- Er is geen pillow shading: geen donkere rand rondom met licht in het midden.

## 2. Schaduw

**Lichtrichting:** het licht valt overal consequent van linksboven.
- muts: 5 links, 3 rechts;
- baard: E links, 4 rechts;
- platen: elk F/8 linksboven en 7 rechtsonder;
- broek: B/C linksboven op elke dij en voet;
- stok, zolen en handen: licht links, met een sikkel 7/9/3 onder en rechts (rechterhand: rij 39–40 helemaal 7).

**Slagschaduw:**
- Onder de muts op het gezicht (2-lijn rij 15–19): goed.
- Onder de riem op de rechterdij (9 op rij 42, x 35–39): goed.
- Op de riem onder de baard: x 22–28 op rij 38 is 3, terwijl de rest van de riem 5 is. Het model is daar licht (gemeten 134–151). Dit is dus een eigen keuze, maar een geldige Gen 3-slagschaduw van de baard op de riem. Laten staan.

**Volume per groot vlak:**
- Muts, baard, broek (bolle dijen met glans), handen en zolen hebben volume.
- Het lijf heeft volume per plaat, en het totaal is links lichter dan rechts.
- **Ter info voor Jordi:** de schouderschijf leest nog zwak als aparte vorm. In het model heeft hij een eigen dikte-rand en een donkere onderlijn. In de sprite heeft hij dezelfde 6-lijn als elke plaatnaad. Reparatie 5 maakt de rand schoner. Een zwarte onderboog (vorm over vorm, zoals de neus) zou volgens de gemeten regel mogen. Maar Jordi vond het zwart in r8 willekeurig, dus dat beslist hij zelf.

## 3. Lijnen (Dragonfly Cave)

Uit de gids (`docs/lessen/bronnen/dragonflycave_spriting_guide.txt`):
- "The 'outline shadows' are always black (or ever-so-slightly off-black)" (r. 92–94);
- "we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide";
- "lighter pixels on the inside of the outline are a far better idea".

**Gemeten op de buitenrand:**
- **Rechts/onder niet-zwart:** alleen op de schuine hoeken rechtsboven (mutsrand (34,0)–(39,3) en de handjes, telkens met één overgang naar zwart) en op de diagonalen linksonder (stok, riemhoek, broek in de spleet). Dat doen Gnomad en Gnomini precies zo. OK.
- **Zwart links/boven:** alleen linksonder bij uitstekende delen en als Popplio-boog:
  - neus (17,19)→(21,23), met 6 erboven en rechts;
  - plukje links;
  - linkerhand;
  - rechterhand (52,37–39);
  - zolen;
  - het gat onder de mutspunt.

  OK.
- Geen lichte kleur op de buitenrand, behalve de 4-lijn van baard en plukje (de eigen donkerste tint, zoals bij Gnomad). Geen open randen. Geen zwart en lijnkleur om en om.

**Binnenin:**
- Zwart staat alleen waar vorm over vorm valt: de neus over de baard, de vuist over de stok, de riem over de broek, het kruis.
- Binnenlijnen zijn verder de eigen tint (6, 2, 9).

**Dikte:** 1 px, met twee uitzonderingen (reparaties 3 en 4).
- 2×2-blokken van 6 op (40–42, 24–26) en (49, 26–27).
- Het model heeft daar geen lijn (gemeten 127 en 145 op roze vlakken van 175–195).

## Reparaties (alleen tint en lijnkleur; silhouet-diff 0)

Belangrijkste eerst. Het "model"-getal is de gemiddelde modelhelderheid per spritepixel, gemeten met `sprite/kijk.py`.

1. **Muts, willekeurige lichte pixels** (de klacht van Jordi over r7).
   - (29,12): 5 → 2. Het model heeft hier de vouwlijn (70/27).
   - (30,12): 5 → 4. Het model is hier middengrijs (91).

   Het losse lichte paartje midden in de donkere vouw verdwijnt; de vouwlijn loopt door zoals in het model.
2. **Zone onder de mutspunt / rugrots**, 1-px lichte streepjes tussen vijf lijntjes:
   - (41,16) 5 → 4;
   - (42,16) 5 → 4;
   - (42,17) 5 → 4.

   Model 110–123 = 4. De lijnen blijven, de vulling wordt één rustig vlak 4.
3. **Dubbele lijn tussen lijf en rechterarm:**
   - (49,26) 6 → 7;
   - (49,27) 6 → 7.

   Model 149 en 127, geen lijn. De armlijn (50,26–28) blijft. Daarna is de lijn 1 px.
4. **Dik knooppunt van naden in het lijf:**
   - (41,25) 6 → 8;
   - (42,25) 6 → 8.

   Model 127 en 145, geen lijn. Het 2×2-blok verdwijnt; de naad loopt (40,24)→(40,25)→(41,26)→ verder rechts.
5. **Dikte-rand van de schouderschijf:** (46,27) 6 → 7. Model 140, geen lijn. De rand op rij 27 wordt één band 7 en wordt niet meer onderbroken.
6. **Baard onderaan, om-en-om 4/5:**
   - (26,33) 4 → 5 (model 147, licht);
   - (28,35) 4 → 5 (model 142);
   - (27,35) 5 → 4 (model 98/29, donker).

   De strengen worden twee schone V-punten zoals in het model, zonder dambord.
7. **Onderlijn van de linkerdij heeft een gat:** (25,47) A → 9. Model 115, gelijk aan de 9-buren. Daarna loopt de lijn door.

Na deze 14 pixels: vlekjes 222 → 217 px, silhouet gelijk, verder niets veranderd.

## Niet als fout gemeld (gemeten, en het klopt)

- De verticale facetten van de rugrots (x 42–48) liggen op de modellijnen (gemeten).
- De lichte 4-lijn rond baard en plukjes: zoals de snor van Gnomad.
- De 9 op (21,43) in de dijglans: een modelnaad (97/25).
- A op (36,47) en (22,49): het model is daar ook midden.

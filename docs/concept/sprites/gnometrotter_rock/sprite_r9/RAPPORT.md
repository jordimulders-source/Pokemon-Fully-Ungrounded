# Gnometrotter Rock: sprite r9 (23 nov), zwarte lijnen en plaatnaden

Basis r8. Jordi over r8: "weer wat beter, maar de zwarte lijnen lijken wat willekeurig te zijn, dat is niet hoe dat in andere goede sprites gelukt is" en "alleen de lijnen van de stenen wijken af van het model ook, kijk daar goed naar, daarom lijkt het slordiger, er zijn teveel kleine vormen".
Silhouet en onderdelen zijn gelijk aan r7b/r8 (alpha-diff 0, op één twijfelgeval na, zie onder). Er zijn 188 pixels anders dan in r8; de wijzigingen staan per stap in `stappen/*.txt`. Het palet is gelijk aan r8.

## 1. Meting: waar staat zwart in onze goedgekeurde sprites (`meet.py`, `kaart.py`)
Buitenrand per richting (aandeel zwart):

| sprite | boven | links | rechts | onder | zwart binnenin |
|---|---|---|---|---|---|
| Gnomad | 17 % | 24 % | 80 % | 83 % | 67 px: riem (boven- en onderrand), spleet tussen de benen |
| Gnomini | 18 % | 39 % | 84 % | 96 % | 40 px: onderrand van de muts over het gezicht, boog linksonder van de neus, mond, benen |
| welp | 33 % | 20 % | 87 % | 91 % | 32 px: ogen, mond, onderkant van de poot |
| steenjaguar | 48 % | 60 % | 84 % | 90 % | veel; zwarte mozaïekstukken horen bij het ontwerp |
| **r8** | 21 % | 29 % | 79 % | 86 % | 45 px, zie 2 |
| **r9** | 26 % | 27 % | 90 % | 89 % | 42 px, alleen volgens de regel |

Wat die sprites steeds doen (gemeten, kaart in `zwart_kaart.png` en `zwart_ref_extra.png`):
1. **Buitenrand:**
   - De naar rechts en naar onder gerichte rand is zwart, als één doorlopende strook.
   - Niet-zwart op die kant komt alleen voor op schuine hoeken rechtsboven (muts, hand: eigen tint, met één overgang naar zwart) en linksonder.
   - Gnomad en Gnomini hebben géén pixel die puur naar rechts of puur naar onder kijkt in een andere kleur dan zwart (op 1 na).
2. **Links en boven** is de rand de eigen donkere tint. Zwart staat daar alleen aan de onderkant van uitstekende delen (onderkant van hand of voet linksonder, neus linksonder).
3. **Binnenin** staat zwart alleen als onderlijn waar een vorm óver een andere ligt:
   - de riem over de broek;
   - de rand van de muts over het gezicht (Gnomini);
   - de neus over de snor (boog linksonder);
   - de hand over de stok;
   - de spleet tussen de benen.

   Nooit als zijlijn van een vorm. De grens tussen baard en lijf is bij Gnomad alleen de donkere lijflijn 6, zonder zwart.

## 2. Wat in r8 die regel brak (rood/zwart in `zwart_kaart.png`, links r8)
- **Zwarte verticale lijn langs de rechterkant van de baard** (rij 23–36): zwart binnenin als zijlijn.
- **Zwarte boog in de schouderschijf** midden in het lijf ((40,23)→(44,26)): in Gnomad geen zwart binnen het lijf. De boog volgens de Popplio-regel blijft alleen op de neus, zoals in Gnomini.
- **Riem:**
  - Bovenrand onder de baard zwart en daarnaast grijs.
  - Onderrand (over de broek) juist grijs, met halverwege een gat. Rechts liep hij verder als blauwe 9.
- **Rechterarm en rechterhand:** de rechterrand (puur rechts en onder) was 6 en wisselde af met zwart (6,1,6,1 langs de arm).
- **Rechterbeen:** de linkerkant in de beenspleet (lichtkant) was zwart.

## 3. Aanpassingen (alleen lijnkleur; `stappen/zwart.txt`)
- **Baard/lijf:**
  - De grens is nu overal één lijn 6 (zoals Gnomad).
  - Op rij 29–33 lagen in r7b twee lijnpixels naast elkaar (6 en 4). De linker is nu baardschaduw 5, de rechter de lijn 6.
  - De onderkant van de baard is 4.
- **Schouderschijf:** de boog is 6.
- **Riem:**
  - Bovenrand overal eigen tint 2.
  - Onderrand één doorlopende zwarte strook van (23,42) tot de rechterrand, langs de schuine onderkant omhoog naar (49,36).
  - Links (x 19–22, lichtkant) blijft de blauwe lijn 9.
- **Arm R:** rechterrand zwart vanaf (51,26). De bovenkant blijft 6, met één overgang.
- **Hand R:** rechtsboven 6, vanaf het midden rechts zwart (zoals de hand van Gnomad).
- **Rechterbeen, linkerkant in de spleet:** 9. Alleen de bovenhoek onder het kruis blijft zwart.
- **Blijft zwart:** neusboog, vuist over de stok, onderkant van de arm R, kruis, gat onder de mutspunt, alle buitenranden rechts/onder.

## 4. Plaatnaden naar het model (Jordi: "teveel kleine vormen")
- **Meting (`naden.py`):**
  - Donkere modellijnen per kleurgroep: roze < 100, blauw < 80, steen < 55, licht < 95.
  - Daarvan het skelet (1 px dik) bepaald en per spritepixel geteld (`naad.npy`). Naad = pixel waar de skeletlijn door loopt (telling ≥ 4).
  - `overlay.py` legt het skelet over de sprite; `naden_12x.png` toont model | r8 | r9 met de modelnaden als rode stippen.
- **Lijf** (`stappen/lijf.txt`):
  - Alle naden van r8 die het model niet heeft zijn weg. Daardoor zijn de kleine plaatjes opgegaan in de grote vlakken.
  - Nu de platen van het model:
    - onder de neus;
    - klein plaatje links tussen baard en middenplaat;
    - plaat onder het haar;
    - grote middenplaat (linkerrand x 33–35 schuin, rechterrand x 41 → schuin naar linksonder);
    - linkerplaten boven en onder de naad op rij 29;
    - één grote plaat rechtsonder (onder de schijf en onder de middenplaat).
  - Weg zijn: de dubbele naad op rij 34–35, de rechte naad x 41 op rij 30–33, de naad (45,29) en de naden x 32/34–35 op rij 25–32.
  - Per plaat: licht (F of 8) linksboven, 8 in het midden, 7 rechtsonder.
- **Broek** (`stappen/broek.txt`):
  - De naad op rij 45 loopt nu door van de linkerdij tot x 34, zoals in het model.
  - Bovenaan de linkerdij een naad op (21,43), en (34–35,44) erbij.
  - De verticale naad x 28 (rij 43–44) en de stompjes (25,46) en (29,46) zijn weg.
  - De schuine naad van de rechterdij is een horizontale naad op rij 47 (x 39–46), zoals in het model.
  - Op rij 47 ligt de modelnaad boven het kruis (x 31–35).
  - Lichte tinten (B) linksboven in elk vlak.
- **Muts:** de vouwlijn loopt in het model van de top recht naar beneden. Hij is twee pixels omhoog verlengd ((35,4), (35,5)). De vouw-/randnaad lag al op de modelplek.
- **Rugrots:** in het model ligt de knik bijna verticaal op x ≈ 48. De sprite heeft de schuine knik van r7b. Niet aangepast, omdat Jordi zei "Rots op de rug is ook prima"; meld ik wel.

## Controles
- Silhouet-diff 0.
- Losse pixels 0.
- Buitenrand in vlakkleur 0.
- Zwart en lijnkleur om en om op de rand: 0.
- ≥ 3 vultinten per onderdeel (`scan.py`, `tinten.py`).
- **Twijfelgeval vorm:** de kolom (29,29)–(29,32) was in r7b een roze lijnpixel naast een grijze lijnpixel (30,y). Nu is (29,y) baardschaduw en (30,y) de enige lijn. Terugzetten kan door die 4 regels in `stappen/zwart.txt` om te keren.

## Eerlijk oordeel over de platen (Jordi: "als het echt niet mooi is, dan is dat ook een les en dan houden we het lichaam neutraal")
- **Op 8×:** het lijf is rustiger dan r8: minder en grotere platen, op de plek van het model. Het leest als stenen pantser.
- **Op 1× en 2× naast Gnomad:** het lijf is nog steeds drukker en donkerder dan het gladde roze lijf van Gnomad. De naden (6 op 7/8) geven op die grootte vooral een gevlekt roze.
- **Mijn oordeel:** beter, maar niet echt mooi op ware grootte. Een neutraal lijf (één vlak met alleen bol licht/schaduw, eventueel alleen de middenplaat) is een serieuze optie om naast deze versie te leggen.

## Bestanden
- `gnometrotter_rock.png`, `gnometrotter_rock_8x.png`
- `zwart_kaart.png`: r8 | r9 | Gnomad, rood = zwart op de buitenrand, donker = zwart binnenin.
- `zwart_ref_extra.png`: Gnomini, welp, steenjaguar.
- `naden_12x.png`: model | r8 | r9 met de modelnaden.
- `vel.png`: r9 | r8 | model op 8×; daaronder 1× en 2× naast Gnomad.
- Scripts:
  - bouwen: `bouw.py`, `zet.py`, `reg.py`;
  - meten: `meet.py`, `kaart.py`, `naden.py`, `nv.py`, `overlay.py`;
  - controleren: `scan.py`, `tinten.py`;
  - vellen: `vel.py`, `naden_vel.py`.

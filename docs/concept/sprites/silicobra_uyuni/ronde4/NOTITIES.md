# Silicobra (Uyuni) – ronde 4 (vanaf ronde 2): streepje weg, pekel als halsband

Jordi (letterlijk): "nee dat streepje moet gewoon weg bij ronde 2, bij ronde 3 lijkt het net alsof zn kop aan het afbrokkelen is. Daarnaast vind ik bij beide de pekelzak niet netjes afgewerkt. Bij de eerste zit die vast aan de staart, bij de ander is het een soort semi half aanhangsel dat ook niet lekker aansluit." / over `bespreking/pekelzak_opties.png`: "zie mijn 2 stipjes, het is 1 slordige pixel. de halsband zie ik zitten. 3 zit het dichtst in de buurt, maar is nog niet een volledige nette halsband, die mag wat voller. Maar ook niet zo onafgemaakt als 5".

Bestanden: `silicobra_uyuni.png` (64×64, geïndexeerd, palet van ronde 2, 15 kleuren, transparency=0), `silicobra_uyuni_raster.txt` (bron), `scripts/handwerk.py` (de met de hand getypte segmenten op ronde 2), `scripts/bouw.py`, `scripts/controle.py`, `vel.png` (basis, ronde 2 en ronde 4 op 4× en 1×, licht en donker, plus referenties).

## Wat ik deed
1. **Streepje:** de losse omlijningspixel (19,15) is transparant. De linkeromlijning van de kuif loopt nu (24,13) → (21–23,14) → (20,15–17) → (18–19,18): doorlopend, zonder uitsteeksel. Verder is de kuif niet veranderd.
2. **Halsband in plaats van zak:**
   - **Silhouet:** de zak van ronde 2 is weg en het nek-silhouet is terug naar de originele Silicobra. Alleen in de rijen van de band steekt hij 1 px uit (links rij 33–38, rechts rij 33–36), voor de dikte van de band; elders is het silhouet gelijk aan het origineel.
   - **Ruimte tot de krul:** de lucht tussen nek en krul is op rij 37–41 precies die van het origineel (rij 36: 2 px lucht door de uitsteek van de band).
   - **Vorm van de band:** een volledige band van links tot rechts over de hele zichtbare nek. De boven- en onderrand buigen in het midden 3 px omlaag; we kijken iets van boven op een cilinder. De bovenrand ligt aan de zijkanten op rij 33 en in het midden op rij 36; de onderrand loopt van rij 37–38 aan de zijkanten tot rij 40 in het midden. De band is 5–6 px hoog, met trapjes van hooguit 4 px.
   - **Shading:** licht links (`q`), middentint (`r`), donker rechts (`s`/`t`), en een donkere onderste rij. Linksboven loopt een gebogen glanslicht (`a`) dat 1 rij onder de bovenrand de boog volgt. Er zijn twee belletjes (34,36) en (31,38). Waar de band tegen transparant ligt, is de omlijning donker turquoise (`t`).
   - **Nek rond de band:** de bovenrand gaat onder de kin en de kop door. Boven en onder de band is de nek zout in de tinten van ronde 2, met een slagschaduw (`d`) direct onder de band. De beige buik komt onder de band weer tevoorschijn.

## Diff (`scripts/controle.py`)
| Zone | Alpha eraf | Alpha erbij | Kleur |
|---|---|---|---|
| Streepje (19,15) | 1 | 0 | 0 |
| Nek (rij 31–44, zonder de korst op rij 31) | 16 | 6 | 141 |
| Bevroren: kop met kuif, korst, oog, gezicht en snuit, voet, krul, palet, buitenlijn | 0 | 0 | 0 |

Nek-alpha ten opzichte van de originele Silicobra: alleen +1 px op (17,33), (18,34), (18,35), (19,36), (20,37), (21,38) links en (40,33), (40,34), (39,35), (39,36) rechts. Rij 31 x=41 is de korst van ronde 2 (bevroren). Open randen 0, losse pixels 0. Pixels: 990.

## Eerlijk oordeel
- Op 1× en 4× leest de pekel nu als een volle, nette halsband rond de nek: geen aanhangsel en niet vast aan de staart. De krul staat weer los, met de originele ruimte.
- Het streepje is weg en de kop is verder pixel voor pixel ronde 2.
- Kanttekening ter info, geen fout: de linkeromlijning van de kuif staat op rij 15–17 verticaal op x=20. Dat is de omlijning van ronde 2 zonder de losse pixel; volgens de opdracht verandert verder niets aan de kuif.
- Zelf zie ik geen open zwak punt.

## Lessen
- Een kenmerk dat "vastzit" of "aanhangt" lost op door het terug te brengen binnen het eigen silhouet (hier: de band op de nek, ±1 px voor dikte) in plaats van eraan te bouwen.
- Een band om een cilinder van iets boven: beide randen even diep (hier 3 px) omlaag laten buigen, met een glanslicht dat 1 rij onder de bovenrand dezelfde boog volgt.

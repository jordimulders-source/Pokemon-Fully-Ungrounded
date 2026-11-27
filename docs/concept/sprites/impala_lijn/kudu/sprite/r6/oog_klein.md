# Kudu r6: kleine zwarte ogen (K1–K4)
Jordi over A–D en S1–S6: "alle ogen zijn prutswerk, allemaal te lieflijk, zwarte vlekken of raar gepositioneerd, s1 is nog het beste maar ziet er raar uit, kijk naar andere pokemon met kleine zwarte ogen". Eerder: "kudu irl heeft een zwart oog"; "hij heeft een veel te lief oog".

Script: `sprite/oog_klein.py` (start = `r6/grid.json` met oog B; eerst alle A–D-oogpixels terug naar het lege oogvlak, zelfde regel als `oog_streng.py`, dan per variant één oog 1-op-1 uit een echte sprite, alleen omgekleurd naar het kudupalet). Vel: `oog_klein_varianten.png` (hoofd 8×, bron-oogregio 8×, hele sprite 2× licht + donker, 1× licht + donker). Elke pixel met bron in `oog_klein_pixels.txt`. Buiten het oogvlak verandert niets: diff met `kudu_r6.png` valt per variant binnen x 10–14, y 22–25 (10–12 px, met script gecontroleerd). Manen niet aangeraakt; `grid.json` niet gewijzigd.

**Plek:** zwarte kern op de modelpupil (x 11–12, rij 22–23; modelspleet rij 22, pupil rij 23, zie `oog_streng.md`). Geen modellid eroverheen (dat gaf bij S4 de zwarte vlek); de modelwenkbrauw (D, rij 21) blijft staan, met de vacht ertussen zoals in de bronnen.

**Zoeken:** script over alle Gen 1–3 `anim_front_gba.png` + `normal_gba.pal` (en apart Gen 4–9 `anim_front.png` + `normal.pal`): compacte bijna-zwarte vlekjes van 3–7 px, binnen het lijf, met hooguit 1 witte buur (geen oogwit). Kandidaten daarna zelf op 8–16× bekeken.

## Varianten
| | Bron | Wat (bron → kudu) | Waarom klein/zwart/niet lief |
|---|---|---|---|
| **K1** | Sawsbuck (Gen 5, hert), x 20–22, y 23–24 | Schuin smal oog: rij 1 lichtgrijs · zwart · grijs (→ 4 0 3), rij 2 zwart · donkerrood (→ 0 K) | 1 px breed zwart, geen ronde pupil; het lichte pixel ligt vóór de pupil (als bij een hert), niet als glans erop. Enige hertachtige bron |
| **K2** | Wailord (Gen 3), x 29–30, y 14–15 | 1×2 zwart met donkere lijfrand erachter (→ 0 D / 0 K) | Kleinst en kalmst: geen glans, geen wit, 2 zwarte px. Leest als een klein donker oog onder de wenkbrauw |
| **K3** | Kabuto (Gen 1), x 32–35, y 20–21 | Donkere rand · zwart · wit · donkere rand / zwart zwart (→ D 0 W D / 0 0) | Klein en zwart, maar met glans: twijfelgeval (levendiger dan K1/K2) |
| **K4** | Bidoof (Gen 4), x 45–47, y 27–28 | Donkerbruine rand + 3 zwarte px (→ K 0 0 / 0 D) | Geen glans, kijkt rustig naar voren-onder; twijfelgeval: 4 donkere px bij elkaar, kan op 1× naar "vlekje" neigen |

## Afgevallen na eigen keuring (niet gebouwd, staan als commentaar in het script)
- **Yungoos** (Gen 7, zware wenkbrauw boven klein zwart oog): 7 donkere px onder elkaar = op 1× een donkere veeg (zwarte vlek); vervangt ook de modelwenkbrauw.
- **Ampharos/Mareep/Sealeo** (2×2 zwart, glans linksboven): het klassieke ronde snoezige oog, zelfde soort als Ponyta B: te lief.
- Bekeken en niet bruikbaar (oogwit, kleur of te groot/rond): Xatu (3×3 rond), Doduo, Farfetch'd, Ursaring, Camerupt, Stantler, Mudbray, Herdier, Terrakion, Sandslash, Spheal (gesloten boogje), Zigzagoon (oog in masker; zonder masker gelijk aan K2), Girafarig.

## Oordeel Claude (streng: te lief? zwarte vlek? rare plek?)
- **K2 (Wailord)** en **K1 (Sawsbuck)** slagen op alle drie: klein, zwart, geen ronde glanspupil, op de modelplek.
- K3 en K4 zijn twijfelgevallen (K3 iets lief door de glans, K4 iets vlekkerig). Niet weggelaten omdat ze op 1× nog als oog lezen, maar ze zijn zwakker dan K1/K2.
- Geen van de vier heeft het zware lid uit het model; dat is bewust (lid over een zwart oog = S4-vlek). Wil Jordi het lid terug, dan kan het modellid (rij 22) alleen boven de lichte pixels van K1 komen; dat is een voorstel van Claude, niet gebouwd.

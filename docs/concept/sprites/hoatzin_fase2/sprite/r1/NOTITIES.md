# Hoatzin fase 2, r1 (19 nov), maker

Model: `../../MODEL.png`. Alles opnieuw: `sh alles.sh`.

## Resultaat
- `hoatzin.png`: 64×64, P-modus, 16 kleuren, index 0 transparant. Figuur 50×63 (x 6–55, y 1–63), tenen/staart op de onderste rij, 1815 px. `hoatzin_8x.png`, `normal.pal`.
- `onderlaag.png` (+ `_8x`): kale reductie in modelkleuren op dezelfde plek. **Silhouetverschil sprite ↔ onderlaag: 0 px.**
- `hoatzin_oogB.png`: variant oog met de 2 onderste ooghoeken donkerblauw (ronder); verder pixelgelijk.
- `vel.png`: r1 8× | model zelfde schaal 8× | Pidgeot | Swellow | 1×/2× op licht/donker/groen | kop 12×: r1 | model | onderlaag | oog B.

## Werkwijze
1. `pitch.py`: randsterkte → pitch 10,24 (fase 9,25) scoort het hoogst, maar de echte cellen zijn 5,12 (zichtbaar in de uitvergrote kop; les pitahaya). `natief.py` (uit Hummlet) met 5,12/4,0 → `natief.png` 200×200, figuur 146×182.
2. `zones.py`: zonekaart op het natieve model met alleen kleurregels: lijf/vleugel (M), lichte vleugelstrepen (W, L ≥ 150), kuif bruin (C), blauw gezicht (F), oog (E), snavel (S), buik (P), poten (T), staart donker (D), zwart (K). Ingesloten witte modelgaten ≥ 20 px (tussen de poten) = achtergrond (les awki). `zones_nat.png` = controlebeeld.
3. `bouw.py`: oppervlakgewogen reductie 182 → 63 rijen (factor 2,889), voorrang E ≥ 22 %, K ≥ 34 %, C ≥ 35 %, F/S ≥ 30 %, W ≥ 22 %, anders grootste zone; toon = gemiddelde van de zone in de cel. Onderlaag = dichtstbijzijnde natieve modelkleur.
4. `stappen.py`: stap A = zones/tonen op het palet (alleen kleurvertaling), daarna regels B1–B6 en C, elke wijziging gelogd (`stappen.log`).

## Palet (kleur naar opdracht/Gen 3, tinten uit het model)
1 lijn #1E1220 · mauve 2–5 (#32 1E 30, #5A3E52, #806276, #B294AA; stappen ±35–45) · kuif bruin 6–7 (#643420, #98522C; bruiner dan het model, opdracht 5) · blauw 8–9 · oog rood 10 (#D0344C) · buik 11–13 = #7A5270 #8E6280 #A57A98 (opdracht 2) · grijs 14–15 (snavel/poten).

## Afwijkingen t.o.v. de onderlaag (stap A = onderlaag in paletkleuren), per zone
| Zone | px | afwijkend | waardoor |
|---|---|---|---|
| lijf/vleugel (M) | 884 | 211 | buitenlijn 116, clusterfilter < 3 px 94, ontkorrelen 40 (overlap) |
| vleugelstrepen (W) | 178 | 33 | buitenlijn 7, filters; plus regel A: alleen kernen ≥ 60 % streep in de lichtste tint, rest één tint lager (opdracht 6) |
| kuif (C) | 131 | 6 | buitenlijn donkerbruin 4, ontkorrelen 2 |
| gezicht (F) | 27 | 3 | oog 3×3 rond de pupil |
| oog (E) | 7 | 2 | pupil = donkerste modelpixel (zwart), 1 ringrandpixel buiten 3×3 → blauw |
| snavel (S) | 15 | 5 | buitenlijn, clusterfilter |
| buik (P) | 161 | 14 | buitenlijn 13 (selout #7A5270 aan de lichtkant), clusterfilter |
| poten (T) | 73 | 29 | buitenlijn 21, clusterfilter |
| staart (D) | 120 | 17 | buitenlijn 10, clusterfilter |
| modellijn (K) | 219 | 94 | binnenlijn waar het model < 55 % zwart is → donkerste tint van de buurzone (87), losse zwarte pixels (7) |
| **totaal** | 1815 | 412 | silhouet 0 |

Niets met de hand getekend: alle wijzigingen zijn regels op gemeten modelzones; het oog (3×3 rond de donkerste modelpixel, midden model x 6,4 / y 20,6) is de enige reparatie per pixel.

## Zelf gezien en gerepareerd
- Rode oogvlek 3×2 met pupil onderaan → 3×3 met pupil in het midden zoals het model.
- Vleugelstrepen werden lichte vlekken/camouflage (drempel 0,30 + lichtste tint) → strepen in tint 4, alleen kernen tint 5; vergeleken 0,18/0,22/0,30.
- Kuif was één bruine massa (drempel 0,24) → 0,35: losse strengen met mauve ertussen zoals het model.
- Staart was een dambord zwart/donker → binnenlijnen alleen waar het model ≥ 55 % zwart is; staart in 2 tinten.
- 145 tintclusters < 3 px → clusterfilter; rest 50 (vooral 1–2-px kuifstrengen, selout op de rand en vleugelstrepen).
- Zwart/selout om en om op de rand → B6 (5 px).

## Resterende twijfels (voor Claude/keurder)
- Vleugelveren: het model heeft duidelijke veerscheidingen (lichte strepen, donkere spleten); in de sprite leest de vleugel vooral als een mauve vlak met diagonale lichte streken. Dit is de zwakste zone.
- Oog: 3×3 rood met zwart midden is wat hoekig; variant B (onderhoeken donkerblauw) is ronder. Geen glanspixel gezet.
- Buik (#8E6280) ligt in helderheid dicht bij lijftint 4; hij valt op door de paarsere tint, niet door contrast.
- Nek-/rugstrepen (zwart in het model) blijven deels zwart: korte lijntjes op nek/rug achter de kop.
- Licht/schaduw komt uit het model (geen extra Gen 3-sikkel gezet); selout aan de lichtkant, zwart aan de schaduwkant.

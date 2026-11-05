# Kolibrie pre-evo – silhouet ronde 2 (bekreparatie, 2 nov)

Jordi keurde r1 goed: "ja, met de twee bekpunten gerepareerd". Punten (Claude): 1) bekbasis te breed, de voorkant van de kop wordt een wig; 2) puntjes van beide snavelhelften zijn 2×2-knopjes, moeten taps toelopen tot 1 px.
Zone: x ≤ 22, y 8–23. Budget ±25 px. De rest is bevroren.

## Wat ik deed (met de hand, rij voor rij)
- **Bovensnavel:** schuift 1 px naar rechtsonder en loopt taps toe. De punt is 1 px (x8, y10), met daarachter een band die 3 px breed is in de rij (dikte ≥ 2 px) tot de basis op y13–15. De basis raakt de kop alleen nog op y14–15; boven de basis zit op y13 een inkeping (x14–15), zodat het voorhoofd als ronde kop leest (rand 18 → 16 → 15).
- **Ondersnavel:** 2 px dik (y18–19). De punt is 1 px (x9, y19); de knop onder de basis (x11–13, y20) is weg. De kin is rond: rand 14 → 15 → 15 → 16 (y20–23).
- **Gaap ongewijzigd:** 1–2 px bij de mondhoek (x13, y16–17), 4 px bij de punten.

## Telling en diff
- **15 pixels gewijzigd** (budget ±25), **0 buiten de zone** (diff r1 ↔ r2 met een script). Gewijzigd (x,y): (8,11) (11,11) (9,12) (12,12) (10,13) (14,13) (15,13) (11,14) (12,15) (13,16) (11,20) (12,20) (13,20) (13,21) (14,21).
- Totaal 732 px (r1: 743). Kop-oppervlak en kop-hoogte blijven gelijk (49% hoogte).

## Bestanden
- `silhouet.txt`, `silhouet_1x.png` (`render.py`)
- `uitsnede_r1_r2.png`: r1 en r2 op 8× met raster, zone in oranje
- `vel.png`: r2 op 4× en 1× naast foto 3 (gespiegeld) en r1 op 1× (`vel.py`)

## Controle
Zelf bekeken op 8× en 1× naast r1 en foto 3: de kop leest rond, de bek steekt er duidelijk als open bekje uit, beide punten zijn spits. Ik zie zelf geen open punten.

## Lessen
- Een open bek leest als bek, niet als wig, als de kop tussen de snavelhelften (de mondhoek) en erboven (de voorhoofdinkeping) zichtbaar blijft.
- Een snavelpunt is een enkele pixel aan het eind van een band van ≥ 2 px, nooit een 2×2-blok.

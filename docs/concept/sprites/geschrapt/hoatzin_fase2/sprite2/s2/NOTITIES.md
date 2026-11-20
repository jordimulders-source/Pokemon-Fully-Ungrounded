# Hoatzin fase 2, ontwerp 2, s2 (20 nov): betere overname-instellingen + Jordi's oog

Jordi: "je hebt precies genoeg ruimte voor mijn oog idee, zonder dat je iets anders hoeft te veranderen" · niet tekenen; snavel/kuif/pennen alleen via de reductie.
`sh alles.sh` bouwt alles opnieuw (`python3 fase.py` zoekt de rasterfase opnieuw). Basis = s1-pijplijn, met:

| instelling | wat |
|---|---|
| (a) rasterfase | 25 fases (DX, DY ∈ −0,5…0,5 spritepx) gemeten op fouten (dambord/barcode/klont = 0), grijs in de snavel, kuif- en oogpixels (`fase.py`). Gekozen **DX −0,25, DY +0,25** (snavel 13 px licht grijs tegen 9 bij fase 0; 0 fouten). ±0,5 geeft hetzelfde als een hele pixel verschuiven. |
| (b) wit-menging | cel zonder zuivere modeltint (dunne kuifspits): elke mengpixel krijgt de tint waarvan hij een verdunning met wit is, niet de dichtstbijzijnde (grijs). Kuifspitsen blijven bruin. |
| (c) penlijnen | modellijnen in het zwart alleen als ze ≥ 6 px lang zijn (PENMIN=6; 4/8/10 ook bekeken): ruisstreepjes weg, de lange scheidingen (voorrand vleugel, vleugel/lijf, staart) blijven. |
| (d) snavel/poten | cel met ≥ 25 % grijs vlak wordt grijs, ook als zwart-blauwe menglijn meer stemmen had. |

**Oog (variant B gekozen, 6 rood):** pupil = de zwarte pupilpixel van de reductie (9,30); rood = (9,29) (10,29) (8,30) (10,30) (9,31) (10,31) (3×3 zonder de twee hoeken aan de snavelkant; (8,30) en (9,31) waren al rood). Log: (8,29) 14→12, (9,29) 12→14, (10,29) 12→14, (10,30) 12→14, (8,31) 14→12, (10,31) 12→14. Ring = het blauwe vlak eromheen; de lijnrand van het gezicht blijft. **Handpixels: 6, allemaal in het oog (Jordi's instructie); verder 0.** Variant A (4 rood, plus) = `hoatzin_oogA.png`, 4 px. B gekozen: A leest als een rood kruisje/vizier; B als rond oog met de pupil naar de snavel. Beide op het vel (12× en 1×/2×).

## Afwijking van de onderlaag (afwijking.py), 483 van 1694 px
vleugel 290 (270 lijn, 20 tint) · grijs 76 (46 lijn, 20 silhouet = dunne poot/teen/snavel erbij) · crème 53 (42 lijn) · kuif 38 (27 lijn) · krop 20 · blauw 4 · oog 2. Alleen lijn/selout/opschoning + 6 oogpixels.
s1 → s2: 346 px anders (vooral door de rasterfase). Controle: dambord 0 · om-en-om 0 · klonten 0 · barcode 0 · 15 kleuren.

## Wat nog zwak is
- Vleugels: rustiger dan s1, maar nog steeds geen 4–6 leesbare pennen; de modellijnen tussen de pennen zijn < ½ spritepx en vallen weg. Penvorm zit alleen in de rafelrand.
- Kuif: meer spitsen dan s1 (stralend), maar een paar spitsen eindigen als zwarte lijnstreepjes tegen het wit rond het gezicht.
- Snavel: iets meer grijs, open bek leest nog niet echt.
- Poten: vooral lijn + leisteen.

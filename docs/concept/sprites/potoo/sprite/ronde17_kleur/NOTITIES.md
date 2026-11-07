# Ronde 17 kleur (maker) — notities
Omtrek: `ronde17_basis_v2/raster.txt` (hier `basis_85.txt`), alpha-diff 0. Het controlescript meldt 105 alpha-verschillen tegenover ronde 16; dat is de nieuwe onderkant.
`r7.py`: rijen 1–8 komen uit ronde 16. Rijen 9–62 zijn opnieuw met de hand geschreven, elke rij als één string van de linker tot de rechter omtrekpixel. Per rij is gecontroleerd dat hij precies tussen de omtrekpixels valt.
Keurderletters zoals de coördinator ze opgaf: N=5, M=4, J=3, E=2, B/C=9.
Palet: index 7 (warme hoorn) wordt nu alleen voor de klauwen gebruikt. E (donker) is de onderkant van de klauwen.

**Muil: 192 px** (9/A/B/D), plus het keelgat (7 px in 1).

## Gedaan
- **Snavelblok weg (B):**
  - x10–15, y9–15 is nu vacht, licht van linksboven, met selout 2 langs de lichtkant op rij 9–12.
  - Op y12, x11–18 loopt een dunne lichte lip in D.
  - De punt is (10,14) en (10,15) in D.
  - Waar het haakje zat (11,13–14), zit nu muil.
- **Wang (C1):** van de mondrand naar rechts eerst 5 (naar onder smaller), dan een sikkel in 4 (naar onder breder), dan 3 bij de vleugelgrens. De oude diagonale halsrandband is weg.
- **Muilschaduw (C2):** het dak onder de lip is 9, ook op (13–15,13), (13–14,14) en (11–12,15). De achterhoek (23–26,14) is 9 en sluit aan op de keel. De lichte bodem linksonder is gebleven.
- **Halsrand (C3):** een bocht, laag bij de kin op y31 x15–20, oplopend naar (30–32,27). 4 erboven, 3 als kern, 2 alleen onder de kin.
- **Onderkant (C4, C5, nieuwe omtrek):**
  - Geen vouwlijn meer. De buik is rond, met een sikkel in 4/3 rechtsonder.
  - Onder de buik ligt een gebogen schaduw in 2/3.
  - De staart is breder, met een lichte bol in 5 en losse bandjes. De lichte 1-px-rand langs de linker staartrand is weg.
  - De borst heeft vlakjes van 3 px of meer.
  - Vleugelpennen zoals in ronde 16, verlengd tot de nieuwe rechterrand.
- **Klauwen (Jordi):**
  - Klauw 1 op (25–26,42) in 7, (24,43) in 7, (25–26,43) in E en de punt (23,44) in E.
  - Klauw 2 op (30–31,43) in 7 en (29–31,44) in E.
  - Ze krullen naar voren en naar beneden, met de donkere onderkant op de gebogen schaduw. Er steekt geen pixel buiten de omtrek.

## Zelf nog zwak
- **Klauwen:** op 1× erg klein, ze lezen als twee bruine streepjes. Meer zou pixels buiten de omtrek vragen.
- **Muil:** de bovenkant van de muil is een brede donkere band; de muil leest breed en plat.
- **Lip:** de lichte lip is een rechte rij.
- **Halsrand:** dik onder de kin.
- **Vleugel:** nog blokkig.
- **Spikkels:** alle vijf even groot en even gevormd.
- **Controlescript:** 66 kleurclusters kleiner dan 3 px, vooral langs diagonale randen, de 3-rand van de kop, de klauwen en de penpunten.
- Niet blind getest.

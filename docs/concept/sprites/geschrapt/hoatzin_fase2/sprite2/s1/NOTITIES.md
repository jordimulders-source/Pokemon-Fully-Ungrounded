# Hoatzin fase 2, ontwerp 2, s1 (20 nov): kale overname van MODEL.png

Jordi (via Claude): "maar ga eerst maar niks opnieuw tekenen" · "en neem het model over" · kop niet groter dan in het model.
**Met de hand gezette pixels: 0.** Alles komt uit `sh alles.sh`: reduceer → lijnen → bouw → vel → check/barcode → afwijking.

## Methode
- `reduceer.py`: figuurmasker = alles behalve wit (buiten + de lucht tussen verre vleugel en kop, 7340 modelpx). bbox x97–929, y125–898; schaal 13,435 → 62×58, kolom 1–62, onderkant rij 62. Per modelpixel de dichtstbijzijnde modeltint (`klassen.py`, 20 tinten incl. 4 iristinten); per spritepixel de dominante tint van de vlakpixels (geen zwarte lijn, geen 3-px-rand naar wit, geen mengtint). → `onderlaag.png`.
- `bouw.py` (alleen technisch): masker alpha ≥ .45 (kuif/grijs/staartpunt ≥ .28); tint-eilandjes < 3 px opgevuld met de tint eromheen (zelfde zone); binnenlijn op de grens tussen onderdelen (op het achterste deel) + modellijnen die door het celmidden lopen (alleen in het zwart, stukken ≥ 4 px); buitenlijn 1 px: zwart, selout (donkerste tint) aan de lichtkant boven/links; 1–2 px brede delen houden aan de lichtkant hun modeltint; dambord/klont/barcode/losse tint opgelost door een pixel terug te zetten naar de modeltint of de lijn 4-verbonden te maken.
- `palet.py`: 15 kleuren = modeltinten, alleen helderheid uit elkaar (lijn 16 · vleugel 36/58/88 · crème 190/244 · krop 98/146/184 · kuif 128/182 · blauw 72/110 · rood · grijs 156). Grijs donker = vleugel licht (gedeeld, palet vol).

## Afwijking van de kale reductie (afwijking.py), 512 van 1697 px
vleugel 325 (313 lijn, 12 tint) · grijs 70 (43 lijn, 11 tint/selout, 16 silhouet = dunne poot/teen erbij) · crème 58 (47 lijn) · kuif 38 (23 lijn, 12 selout, 3 silhouet) · krop 20 · blauw 1. Alles lijn/selout/opschoning, geen nieuwe vorm.

## Controle
dambord 0 · om-en-om 0 · zwarte klonten 0 · barcode 0. Losse 1-px-tintpixels: nog ±30 (vooral tussen lijnen in de vleugel en in dunne delen).

## Oog (Jordi vroeg dit te noteren)
Na de reductie leest het oog **niet** als oog: een rood blok van 2×2 (8–9, 30–31) in het blauw, het zwarte puntje valt samen met de lijn links ervan (7,31) en de glans verdwijnt (< 1 spritepx). Het is wel rood-in-blauw op de goede plek. Optie "desnoods" (1 zwart, 4 of 6 rood, ring blauw) is níet gemaakt.

## Wat zwak is (eerlijk)
- **Vleugels**: modellijnen geven losse zwarte streepjes en kleine lichte vlekjes; geen 4–6 leesbare pennen-"vingers" zoals Honchkrow/Staraptor. Ruisig donker vlak.
- **Snavel**: grotendeels lijn/donker; het lichte grijs van het model is maar 2–3 px, open bek leest niet.
- **Kuif**: één bruine massa met één spits (8,18–21); de dunne plukken van het model zijn < ½ spritepx en vallen weg. Top van die spits is grijs (15) door mengtint brons/wit.
- **Poten**: vooral lijn + leisteen; het middengrijs van het model komt maar deels terug.
- Kop is klein (zoals het model, ±12 px breed).

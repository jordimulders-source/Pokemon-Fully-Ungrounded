# Regicosmo frontsprite, ronde 3 (maker)

r3 = r2 + alleen Saturnus opnieuw. Jordi (28 nov): "kan je de band van links niet pakken met de bol in het midden (dat je die dan wel rond maakt?)" · "en hij moet ongeveer even groot zijn als de ijsplaneet".
Bouwen: `cd docs/concept/sprites/regicosmo && python3 sprite/r3/bouw.py && python3 sprite/r3/vel.py`.
Bestanden: `regicosmo_r3.png` (64×64, P, index 0 transparant, 16 kleuren incl. transparant, 7 losse delen, bbox x1–63 y15–61), `vel.png` (r3 8× | r2 8× | model; Saturnus 16× r3 | r2 | natief model, naast de ijsplaneet 16×; 1×/2× licht en donker; naast Regiaqua/Regirock/Registeel gba).

**Bewijs:** diff r2→r3 buiten Saturnus = 0 px; Saturnus 88 px.

## Saturnus
- Bol: diameter 10 (r=5, middelpunt (56,0; 30,0)), x51–60, y25–34, net als de ijsplaneet (x1–10, y25–34). Strepen en tinten = de modelbol van Saturnus (cirkelfit natief c=(173,45; 55,04) r=8,60) geschaald naar 10 px: per spritepixel de meerderheid van de planeetkleuren in de natieve cel. Buitenlijn donkerrood/zwart zoals r2.
- Ringband als r2 (kanteling −28,1°, verhouding b/a, grijze middenlijn + donkere rand, voorkant over de bol, achterkant achter de bol), centrum nu op de bol, verlengd tot het past: a 7,27 → 8,48, b 1,68 → 1,96. Nieuw: grijs mag niet op de buitenrand; een lege buur buiten de ellips wordt ringrand (binnen x48–63), en zwart met een lege buur links/boven maar niet rechts/onder wordt bruin donker.
- Saturnus x48–63, y24–35; 2 px leeg tot Mars, maan verder weg. Lusgaten links (50–51,32) en rechts (60–61,27).

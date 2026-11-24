# Eindkeuring satelliet fase 2, r6 → r7 (omlijningsronde + Dragonfly Cave), 24 nov

Te keuren: `../sprite/r6/sprite.png` (oog a) en `../sprite/r6/oog_b.png`. Model (bevroren): `../paneel_varianten/panelen_80b.png`.
Alleen uitvoering; vorm, silhouet, verhoudingen en onderdelen niet aangeraakt.

## Oordeel: PASS (r7)

## Stap 1: omlijningsronde (`omlijning.py`, reproduceerbaar)
Regel (gids r. 80–170, 340–470): outline base = donkerste eigen tint van het onderdeel, zwart alleen als outline shadow aan de schaduwkant (licht linksboven), binnenlijnen niet zwart, 1 px. Uitvoering: elke zwarte pixel krijgt het voorste aangrenzende onderdeel (gewrichten > groot paneel ≈ lijf > klein paneel); wijst de lijn vanaf dat onderdeel naar links/boven, dan de outline base, anders blijft hij zwart.
- **Panelen → navy 9 (48,32,80)** (67 px): linker- en bovenrand van beide panelen, plus de rand waar het grote paneel over het lijf ligt. Rechter- en onderranden blijven zwart. De lichte framelijn (f/F) ligt al binnen de lijn als outline highlight.
- **Gewrichten/antennes/arm → donkerpaars 8 (92,58,116)** (15 px): bovenkant linker gewricht, rechter gewricht + arm naar het paneel, linkerkant rechter gewricht. Antennes hadden al geen zwart.
- **Lijf → donker lavendel 5 (144,120,164)** (8 px): naad lijf/klein paneel linksboven, tweede pixel van de dubbele naad rechts van de lensring (lijn is nu 1 px zwart + lijfschaduw). Toets: Togetic (115,123,131) en Glalie (120,120,152) gebruiken een even lichte outline base op wit; geen extra tint nodig.
- **Lens (gezicht) niet aangeraakt**: alle ringen en de pupil blijven zoals r6 (straal 6,6 rond het lensmidden plus de buitenrand linksboven). Daardoor zijn oog a en oog b identiek behandeld (script controleert dat geen omgetinte pixel in het oogverschil ligt).
- **Benoemd zwart gehouden** (om-en-om voorkomen, Popplio-regel): rechterrand groot paneel (54,32); begin onderrand groot paneel (28,47–48); rechterrand paarse lensring-band (27–28,30); boog linksonder lenshuis (11,36) (13,38–39) (14,38) (14–15,42) (15,41); brugpixels van de naadlijn (29,33) (29,37).

Controle: silhouet-diff 0, 90 pixels gewijzigd, alleen van zwart naar een bestaande tint; palet ongewijzigd (15 van 16, slot 15 vrij). Zwart 17,3 % → 11,7 % (Gen 3-metaal: Magneton 15,9, Lunatone 14,4, Baltoy 16,2, Metang 20,0).

## Stap 2: eindkeuring r7
- **Licht linksboven / selout**: in orde. Lichte kanten in eigen tint, schaduwkant zwart, zoals Metang/Claydol (linksboven 30–50 % zwart, rechtsonder 90–100 %).
- **Volume**: lijf wit → lichtlavendel → lavendel → donker lavendel aan de onderkant, sikkel volgt de vorm; panelen twee vlakken (licht boven, donker onder) zoals het model. Geen pillow shading, geen banding of dambord.
- **Losse pixels**: 3 nieuwe na de automatische stap, gerepareerd met de tint van de rest van die rand: (47,16) → 9, (45,19) → 9, (36,17) → 8. De resterende losse pixels zijn dezelfde als in r6 (antennebolletjes, oogglans, framepuntjes van de panelen, uit het model).
- **Leesbaar op 1×** (`vel.png`, licht en donker, naast Magnemite, Magneton, Beldum, Metang, Claydol, Lunatone): lens, lijf, panelen en antennes lezen; op donker blijven de panelen afgetekend door hun lichte frame.
- **Afgekapt**: niets. Het grote paneel raakt x = 63 en het kleine x = 0, maar beide hoeken zijn gesloten (lijn rondom).

## Ter info voor Jordi (geen uitvoering, niet veranderd)
- Oppervlak 1596 px, iets boven de fase 2-band (1100–1550) door de grote panelen; past bij "verhoudingen kloppen, niets afgekapt".
- Donker aandeel inclusief de navy paneelvulling is hoog (±34 %); dat is de ontwerpkleur van de panelen, niet de lijn.
- Oog b (één ring minder): beide varianten zijn technisch gelijk (zelfde omlijning, geen nieuwe losse pixels); de keuze is een ontwerpkeuze voor Jordi.

## Bestanden
`r7/sprite.png`, `r7/oog_b.png`, `r7/sprite_8x.png`, `r7/oog_b_8x.png`, `vel.png` (r6 8× | r7 8× met omgetinte pixels groen | model verkleind 8×, en 1× op licht/donker naast Gen 3), `omlijning.py`, `vel.py`.

# Sprite-werkwijze (compact)
Regels en eisen: `SPRITE_KERN.md`. Hier alleen de stappen en de commando's. Oude uitgebreide versie: `naslag/SPRITE_WERKWIJZE_oud.md`.

**Mappen:** `docs/concept/sprites/<naam>/` met `SPEC.md` (Jordi letterlijk, bevroren/open/afgekeurd), `referenties/`, `blender/`, `af/`.

| # | Stap | Wie | Klaar als |
|---|---|---|---|
| 0 | Types/evoluties uit de repo; SPEC en referenties klaarzetten | Claude | SPEC bestaat |
| 1 | Ontwerp: pose + kenmerken, foto van het echte dier | Jordi + Claude | Jordi kiest |
| 2 | 3D-model in Blender, rondom-vel (0–315°) + 3 driekwart-standen naast Taillow/Starly | Claude | Jordi kiest stand |
| 3 | Silhouet = render direct verkleind; vel = render met rode omtrek erover | Claude | Jordi keurt; bevroren |
| 4 | Kleur: studie (4–5 echte sprites op 8×) → tekstraster met de hand; toonkaart als schaduwgids | maker-agent | controlescript schoon |
| 5 | Claude 8× naast Taillow → verse keurder (blind eerst, PASS/FAIL met pixels) → reparaties via maker | Claude, keurder, maker | keurder GOED |
| 6 | Jordi ziet alleen de sprite; zijn punten → kleine benoemde rondes | Jordi | "prima" |
| 7 | `af/<naam>.png` + `normal.pal`; SPEC, CHANGELOG, Stand van zaken, lessen | Claude | gepusht |
Frame 2, rug, icoon, shiny, naam, data: later, voor alle soorten samen.

**Blender in de cloud (eenmalig per container):**
```
python3.11 -m pip install bpy scikit-image
apt-get install -y libegl1 libgl1-mesa-dri
```
Voorbeeldmodel: `docs/concept/sprites/kolibrie_pre/blender/kolibrie_pre.py` (huid = smooth union van afstandsvelden, kleurvlakken per vlak, snavel/ogen/pootjes los; Workbench-render, 512 px = 8×, ortho 64 BU = spriteframe). Silhouet/vel: `kolibrie_pre/blender/A/maak.py`. Toonkaart: model met alle kleuren wit renderen, verkleinen, 4 tonen.

**Controlescript (elke ronde):** alpha-diff met het bevroren silhouet (0 of alleen in benoemde zones), open randen, losse pixels, clusters < 3 px, lijst gewijzigde pixels oud→nieuw. Voorbeeld: `kolibrie_pre/blender/A/kleur_r9/controle.py`.

**Opdracht aan een agent bevat altijd:** `SPRITE_KERN.md`, SPEC-pad, bevroren delen + toegestane zones, Jordi's woorden letterlijk, gewenste uitvoer (raster, png, pal, vel, NOTITIES met zwakke punten), "niet committen".

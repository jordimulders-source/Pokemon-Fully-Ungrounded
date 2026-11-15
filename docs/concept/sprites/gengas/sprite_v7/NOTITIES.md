# Gengas sprite v7 (15 nov) – Gengar-gezicht als één blok op de r3-plek

Jordi: "oog en mond grootte van model is beter en van jouw versie de positionering" (positie = `sprite_r3`, Gengar-gezicht op x−6, y+5).
Keten: `python3 v7.py && python3 maak.py && python3 vel.py` (leest `../sprite_v6/raster.txt`; elke pixel met reden in `raster.txt.log`).
**Diff v6 → v7 buiten de zone x 8–33, y 28–47: 0** (v7.py meet het).

1. Ogen en grijns samen als één blok uit `graphics/pokemon/gengar/anim_front.png` op (x−6, y+5): onderlinge afstand oog–grijns = exact Gengar (in v6 stond de grijns 3 rijen te laag). v6-gezicht eerst weggehaald, gaten gevuld met de lijftint van de buren (zelfde selectie en tintkoppeling als v6).
2. Losse l (31,43), (30,44) → b (onderband eromheen).
3. Paletslot voor Gengars tandschaduw (2) of exacte tandlijn (3): goedkoopste vrij te maken tint is u → b (13 px, ΔE 8,6; daarna w → v, 18 px, ΔE 16,9). Maar alle u- en w-pixels liggen (bijna) helemaal buiten de gezichtszone, dus dat breekt diff = 0 buiten de zone. **Niet gedaan**; voorleggen. Winst zou klein zijn (Gengar 2 vs H ΔE 12,8; Gengar 3 vs G ΔE 16,0).
4. Bandrand: de onderrand van de donkere band boven het rechteroog liep 8 px recht op rij 28. Nu rond: rij 27 bij x24–25, rij 28 bij x26–27, rij 29 bij x28–34 (sluit aan op (34,29), al b), rij 28 bij x35, rij 27 vanaf x36. Tussen band en oog blijft rij 30 lijftint m (twee b-pixels uit de v6-oogvulling daar weg).

Zwakke punten (eigen): de onderrand van de band heeft nog een recht stuk van 7 px op rij 29 (x28–34), wel als ronde boog met trapjes 2-2-7-1; de grijns staat nu dichter onder het rechteroog (zoals Gengar), waardoor het gezicht compacter is dan v6; tandschaduw/tandlijn nog niet exact (punt 3).

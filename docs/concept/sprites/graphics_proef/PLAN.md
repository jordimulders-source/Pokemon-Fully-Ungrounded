# Plan overige graphics (27 nov, Jordi akkoord: "begin maar met je plan")

Doel (Jordi): "zo efficient mogelijk zo goed mogelijk alle andere graphics van de nieuwe designs maken". Lat: "alle extra designs allemaal net wat minder belangrijk dan de frontsprite 1, dus lichte afwijkingen zijn geen ramp".

1. Proefserie Gumfish / Sunperor / Hexpress (rug af als kandidaat; frame 2 Sunperor via Gemini).
2. Inventaris alle soorten (`INVENTARIS.md`): bouw, frame 2-categorie (G = Gemini, S = script).
3. Frame 2 per script (categorie S) door Claude/agents; categorie G in de Gemini-pakketten.
4. Iconen: algemeen bouwscript (`icoon/`), test op Gumfish en Sunperor, daarna batches.
5. Shiny's per lijn op vellen (skins-regel), Jordi keurt per vel.
6. Gemini-pakketten per batch van 8 (`pakketten/batch_NN/`): 8×-bijlagen + rug- en frame 2-prompts; Jordi plakt, Claude neemt over (`gereedschap/natief.py` → paletomzetting → benoemde reparaties).
Overworld: pas na rug (prompt heeft front + rug nodig); voor welke soorten is nog open.

## Stand frame 2 per script (27 nov)
- Af als kandidaat: 35 soorten in `frame2/batch_a/` en `frame2/batch_b/` + Gumfish/Hexpress (`frame2/`).
- Zwak per script: Cryomet, Spoetnik, satelliet, ruimtestation (zwakst), Purrpillar, guaraná 1, Swablu, Pincurchin, DJ Rotom.
- Eigenlijk Gemini (lokale pose): Muk regional, Shuppetto; eventueel ruimtestation. Prompts toevoegen aan de pakketten als Jordi dat wil.

- Jordi (27 nov): "Je kan gifs gaan maken voor designs waarbij dat goed past. Maar weet dat Gemini heel goed is in frame 2 maken dus dat wordt het issue niet" → zwakke script-soorten (+ Muk, Shuppetto) krijgen een Gemini frame 2-prompt in de pakketten.

## Overworld
- Jordi, 27 nov: "Voor overworld sprite moet je sowieso de legendaries en de ghost tempel. Rayquaza is vgm ook groter dan een normale sprite dus dat mag je met deze ook doen. De tempel mag zelfs zeer groot, dat men erin zou trappen alsof het een echte poort is naar een gebouw".
- Jordi: "We gaan toch geen following pokemon doen" → overworldsprites alleen voor wat in de wereld staat (legendaries, tempel, eventuele andere statics); niet voor alle soorten. Rayquaza-OW is 64×64 (gewoon 32×32).

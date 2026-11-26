# Creepy guaraná fase 2 (Grass/Ghost)
Fase 1 (af): `../guarana/` (SPEC daar = alle eerdere besluiten).

## Besluiten
- Uit fase 1 (Jordi, 25–26 nov): fase 2 "opengebarsten vol ogen die je aankijken"; de opengebarsten rode schil om het oog en gladde bolletjes (het guaraná-gevoel) komen in fase 2 ("akkoord").
- Jordi, 26 nov (keuzevragen):
  - Lijf: **vertakte liaan** (optie: "De liaan splitst zich: twee of drie ranken die elk een eigen tros ogen dragen (meerdere 'hoofden')").
  - Ogen: **"meerdere takken"** (antwoord op de vraag hoeveel ogen; geen aantal genoemd → geen aantal in de prompt).
  - Maat: **±64 px (vol kader)**.
  - Gemini: **zonder bijlage**.

## Gemini
- r1: `gemini/PROMPT_r1.md` (nieuw gesprek, geen bijlage).

## Ronde 1 (`gemini/r1.png`)
- Jordi (26 nov): "de vorm werkt goed, alleen ik vind de liaan net iets te basic en onderdesigned, wat zouden we daar evt nog mee kunnen?"
- Claude stelde 6 opties voor (getwijnde liaan, gegroefde stengel, echt guaraná-blad, rood in het jonge groen, dichte knopjes, grijpranken). Jordi: "we doen 1 en 3" = getwijnde liaan + echt guaraná-blad (samengesteld, 5 getande blaadjes; minder maar groter). Bijsturen in hetzelfde gesprek: `gemini/PROMPT_r2_bijsturen.md`.

## Ronde 2 (`gemini/r2.png`, bijgestuurd met 1 + 3)
- 64 px-test (`gemini/r2_test64_8x.png`, 64×51): liaan en blad lezen; de ±8 ogen per tros worden 2–3 px en vervagen tot ruis. Aantal ogen per tros is nooit door Jordi bepaald → als vraag voorgelegd.
- Jordi: "hebben we niet genoeg ruimte om de ogen te vergroten?" Ruwe test (`test_ogen/`, trossen 1,35× en 1,5× geplakt over het blad, daarna naar 64 px): bij 1,35× ogen ±4 px, trossen raken elkaar; bij 1,5× één rode massa, blad weg, ogen nog ±4 px. Grens = aantal vruchten op de breedte (3 trossen × 3 vruchten in 64 px → ±6–7 px per vrucht).
- Jordi: "maar dat vragen we aan gemini dan toch om te vergroten" → bijsturen r3 (`gemini/PROMPT_r3_bijsturen.md`): alleen ogen veel groter; aantal niet genoemd.

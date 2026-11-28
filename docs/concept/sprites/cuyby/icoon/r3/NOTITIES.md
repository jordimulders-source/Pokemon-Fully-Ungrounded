# Cuyby-icoon route 3 (28 nov)
- Model: Gemini r1 (`gemini_r1.png`, prompt in `PROMPT_DRIEKWART.md`), Jordi: "hij is ietsje anders geworden, maar dat is niet erg voor een icoon".
- `natief.png`: 16 px-cellen terug naar 1 px (30×33); `q.npy`: kleuren naar het frontpalet (kwantiseren als onderlaag).
- `bouw.py`: rijen/kolommen schrappen met één factor (0,55) in beide richtingen; bij details alleen kiezen wélke rij/kolom (oogglansen kol 19 en 29, neus rij 33). Kleur = dichtstbijzijnde pal3-index, behalve twee bijna-gelijke afstanden: crèmeschaduw → geelcrème 12 (2645 vs grijs 2434), oogbruin → donker 14 (3620 vs rood 3330).
- Ingrepen: alleen "los weg" en "omlijning dicht" (automatisch, gelogd door bouw.py). Frame 2: alles 1 px omlaag, rij boven de voet vervalt, oren blijven staan (spitsen 1 px).
- Rondes: r1 (21 hoog, te groot), r2 (warme tinten), r3–r5 (oren breder door extra kolommen: "de proporties kloppen niet meer" → fout), r6 (gelijke factor 0,6; "gaat de goede kant op, alleen iets te groot"), r7 (0,55), r8 (glans verre oog terug) = `af/`.
- Check: 15/17; hoekig/rond NEE: komt uit het model (Gemini maakte de zijkanten recht, "cuyby is wat uitgebold"). Ronder model = prompt r2.
- Palet 3 (`.iconPalIndex = 3`).

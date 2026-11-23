# Regional Claydol – Gemini r8: bewerking van onze eigen sprite (nieuw gesprek)
Jordi (23 nov): "ik stel voor nog een gemini ronde om dan te prompten wat we met het hoofd doen, pronpten ben jij beter in dan designen".
Waarom zo (Claude): elke reparatieronde voegde een lapje toe aan de kop ("allemaal losse vlakken, lijnen, krassen"). Een Gemini-bewerking van de sprite zelf tekent de kop in één keer opnieuw op ons eigen raster; wat niet genoemd wordt (krans, punt, lijf, staven, palet) kopieert Gemini (viscacha frame 2: "keep pixel grid and palette, change only X" werkte in één keer; Gemini doet handelingen/vormen in woorden goed, getallen en posities niet).
Terugzetten: middelste pixel per vak van het raster; daarna alleen een kleine opschoonronde.

**Bijlage:** `claydol_gemini_r3/r5/claydol_g3r5_paletB_8x.png` (de goedgekeurde 3-ogenversie met palet B, 8×). Nieuw gesprek, alleen deze ene bijlage.

```
The attached image is my own finished Pokémon front sprite (Gen 3, Ruby/Sapphire/Emerald style), shown at 8× size. Edit it.

KEEP EXACTLY THE SAME, pixel for pixel: the pixel grid, the palette, the outline, the crown of small round eyes around the head, the stone point on top, the body, the arms, the feet and the two separate staffs. Same size, same silhouette.

CHANGE ONLY THE FACE ON THE BIG ROUND HEAD:
- TWO big eyes instead of three. Same eye style as now: round, cream white, a dark ring around each eye, one short horizontal line in the middle (no pupils, no dots, no mouth).
- A clear stone nose ridge exactly in the middle between the two eyes.
- Three-quarter view facing left: the face (two eyes + nose) sits a little to the LEFT of the middle of the head; the right part of the head is the side of the head, turning away.
- The red painted line: one smooth arch above each eye, meeting in a V above the nose; after the arch above the right eye it curves smoothly into a horizontal line that goes around the side of the head, following its round shape.
- The rest of the head: one smooth round stone surface, lit from the top left, darker towards the bottom right, with only a few thin carved cracks. No patches, no extra lines, no extra patterns, no pink or faded red marks.

Do not change anything else. Keep the same pixel grid and the same colors.
```

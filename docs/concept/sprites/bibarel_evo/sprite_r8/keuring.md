# Keuring r8 (zelfde keurder als r7, 24 nov)

Meetplaatjes: `keuring/r7_r8_8x.png`, `keuring/gezicht_r7_r8.png`, `keuring/buik_r7_r8.png`. Diff r7→r8: 130 px, alles binnen x3–39 r16–54 (de opgegeven zones).

## Wat r8 oplost
- Borst en linkerbovenarm: geen stamkleur meer in de romp (alleen hand x13–17); de borstplooi is één vorm uit het model. Geen pixelblur meer. OK.
- Bovenrand borststuk: boog met inham op (29,35), niet meer recht. OK.
- Rechterrand crème: buigt naar het kruis, sikkel m dikker onderaan. OK.
- Zakje: k met middentint rechts en eronder, dus het leest nu als lichter vlak; gat onderzoom dicht. OK.
- Crème: 4 tinten 233/207/181/145 (stappen 26/26/36), grootste k-vlak 186 px. Bovenste helft (borststuk, lens x34–39 r35–44) heeft volume. OK.

## (a) Oogring grijs → tan
Geen probleem. De echte Bibarel-sprite gebruikt voor de oogring 168/144/120 (lum ±147); de nieuwe tan 176/138/96 (lum 145) zit qua helderheid er precies op (het oude grijs 140/120/100 was 124, donkerder dan het origineel). Alleen iets warmer; op 1× en 8× leest het oog even scherp. Geen reparatie.

## (b) Banding in de buik
Ja, onderin wel. In r45–51 lopen k | middentint | h | m als vier evenwijdige schuine stroken naar linksonder, elke grens schuift ±1 px per rij (k/midden-grens x29,27,27,26,25,24,24 is vrijwel een rechte 45°-trap). Dat is banding en tegelijk weer een "rechte lijn" in de schaduw. De lens bovenin (r35–44) heeft dit niet.

## Uitkomst: BIJNA
Eén reparatie (alleen tinten herverdelen binnen het crème van r45–53, silhouet en rest diff 0):
1. **Buik r45–53, geen evenwijdige stroken:** maak de k/midden-grens een bolle curve in plaats van een trap (lichte kern iets verder naar rechts op r46–48, dan snel terug). Laat de middentint uitlopen en stoppen rond r50 in plaats van tot r51 mee te lopen. Laat h onderin (r50–53) als sikkel breder worden en houd m alleen in de onderste rechterhoek. Elke tintgrens moet een andere richting en breedte hebben dan de buitenrand.

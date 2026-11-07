# Poedelmot silhouet ronde 2 (6 nov): alleen het silhouet, 64×64

Opdracht: massa van poppetje 5b overtrekken op de 50%-grens; poten, oren en kop met de hand; geen kleur.
Tijdens de ronde bijgekomen (Jordi 6 nov, letterlijk): "dit mag als inspiratie voor hoofd, gezicht en oren" (vilt-foto,
`referenties/vilt_hoofd_gezicht_oren.png`) en voor de ogen "zoals in deze foto" (= die vilt-foto). De eerdere tussenstap
"gezicht = tak-foto" is daardoor vervangen; ogen zijn nu kleine kraaloogjes zoals het vilt.

## Bestanden
- `bron.py`: rendert poppetje 5b (45°, pitch 8, zelfde kader als `poppetje_45_1x.png`) op 768 → `dekking_kaal.npy` (zonder
  poten en sprieten), `dekking_zonder_poten.npy`, `model50.txt`, `delen.npy`, `poten_ref.npy`, `spriet_as.npy`, `onderlaag_512.png`.
- `silhouet.py`: bouwt het silhouet → `ronde2.txt`, `delen.txt`, `silhouet_1x.png`, `silhouet_8x.png`, `delen_8x.png`, `glad_log.txt`.
- `controle.py` → `controle.txt`; `korrel.py` (lama).
- `keurvel.py` → `vel.png` (+ `vel.png.keuring.md`).

## Wat er gedaan is
- **Massa** (lijf, wol, vleugels): poppetje 5b op de 50%-grens. 10 afwijkingen, alle ≤ 1 px van de grens (`controle.txt`);
  0 korrels buiten de oren; één component. Alles 4 px omlaag geschoven zodat de onderste pompon op y62 staat.
- **Kop:** ronde wolbol (r 9,3) op de plek en maat van de poppetjekop, inspiratie vilt (bol direct op het lijf, oren bovenop
  de zijkanten). In de omtrek alleen de koepel tussen de oren.
- **Ogen** (alleen in `delen.txt`/`delen_8x.png`, rood): kraaloogjes naar het vilt gemeten: oog 0,15 × kopbreedte
  (22/145 px), hart-op-hart 0,34, hoogte 0,47 van de kop. Op 45°: nabij 3×4 px, ver 2×3 px, 5 px uit elkaar.
- **Oren:** plek en lengte uit de spriet-as van het poppetje; bladvorm naar het vilt (breed blad, schuin omhoog opzij,
  ±20°; breedte/lengte 0,37 zoals het vilt). Kamtanden 1 px met 1 px lucht aan de **bovenkant**; de onderkant is een
  gesloten bladrand (losse tanden gaven daar 1-px-gaatjes boven kop en vleugel).
- **Poten** (met de hand, capsules + pompon met twee zijlobben): voor nabij grootst en laagst (pompon tot y62);
  voor ver links, hoger (y57) en kleiner; nabije tweetal (midden + achter) rechts dicht tegen elkaar, achter hoger;
  verre tweetal als klein plukje onder de buik tussen de voorpoten (grotendeels verborgen, zoals op de tak-foto).

## Zwakke punten (eerlijk)
1. **Leest op 1× nog niet als mot.** Naast Butterfree/Venomoth is het een zware zwarte massa (vleugels + lijf één blok,
   de grote nabije voorvleugel overheerst); het leest eerder als vleermuis/gargouille op pootjes.
2. **Oren wijken af van het vilt:** het vilt heeft gladde bladoren met strepen erin; hier staan de tanden in de omtrek
   (opdracht: "tanden zichtbaar in de omtrek", tak-foto). Op 8× lijken ze op kammen/borstels met stompe punten; het vilt
   loopt spits uit en staat steiler omhoog. Die keuze (tanden in de omtrek of gladde rand zoals het vilt) is voor Jordi.
3. **Verre voorvleugelpunt** (massa poppetje) steekt als een hoorntje uit tussen het verre oor en de kop.
4. **Kop als eigen vorm** is in de omtrek alleen de koepel; onderaan valt de kop weg in lijf en vleugels. De kop is een
   cirkel (op de poppetjekop gelegd); in de kleurstap moet de wolrand de vorm geven.
5. **Poten:** voor ver staat schuin naar links (zoals de tak-foto) maar leest als een stut; het verre tweetal is nauwelijks
   te zien (alleen een plukje). Pompons hebben een platte onderkant (zijlobben) en lezen op 8× als laarsjes.
6. **Ogen** zijn op 1× klein (3×4 en 2×3 px), zoals het vilt; dat is Jordi's keuze, maar ze vallen in het silhouet weg
   (binnen de kop) en hangen helemaal van de kleur af.
7. `glad()` haalde één pixel met 90 % dekking weg (x11 y15, punt van de verre voorvleugel) om een trapje te sluiten.

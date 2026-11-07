# Keuring viscacha kleur r9 (verse keurder, 7 nov)

Bron: `kleur_r9/raster.txt` → `kleur_r9/viscacha.png` (controle: png == raster). Vergeleken met `kleur_r8/viscacha.png` (goedgekeurd), het model `referenties/gemini_gekozen_ronde6.png` / `kleur_r6/gemini64.png`, en Taillow en Raticate (de bovenste 64×64 van anim_front).
Coördinaten zijn (x, y), 0-based.

## 8× en 1×
- **8×:** r8, r9, het model, Taillow en Raticate naast elkaar, plus een close-up van rug en staart op 16× (r8 en r9). Het licht van linksboven leest nu duidelijk: hooglicht op het voorhoofd en de rug, een sikkel rechts op de bil en de staart licht aan de linkerkant. De dichtheid zit tussen Taillow en Raticate in.
- **1×:** op licht (wit) en op donker (40,40,56). Hij leest als knaagdier met gele pluimen, oor, oog en snorharen. Het hooglicht valt op 1× niet op als vlek. Op donker is hij net zo leesbaar als r8.

## Rug (Jordi: "bovenkant lijf mag iets minder vlak")
- **Lijkt op:** op de rug zijn 5 pixels met dekking bijgekomen ((35–38,28) en (32,29)), verder is de alpha gelijk aan r8. De bovenlijn loopt nu x29–31 op y30, x32–34 op y29, x35–38 op y28, x39–40 op y29 en x41 op y31. Dat zijn runs van 3‑3‑4‑2‑1: een vloeiende boog zonder knik en zonder losse bult. Het rechte stuk van 8 px uit r8 is weg.
- **Wijkt af in:** niets wezenlijks. De top (4 px vlak) ligt iets links van het midden van de rug, maar dat past bij de rug die naar de bil afloopt en bij het model.

## De vijf punten
1. **Contrast.** Lijf 5→4 = 32, 4→3 = 30, 3→2 = 43. Hooglicht B→5 = 32. Staart 4→C = 36, C→2 = 37. Verre poot E = 107, een stap onder 3 (129). Alles valt binnen de Taillow-band van 30–40. **Lijkt op** Taillow.
2. **Hooglicht linksboven.**
   - Waar: rug (35–37,29), (33–37,30), (33–35,31) en voorhoofd (12–15,27), (11–14,28), (11–12,29). Het zijn twee ovale vlakjes van 10–11 px, met 1 px basis tussen het hooglicht en de selout.
   - **Lijkt op** Raticate en Taillow: één lichte tint op het hoogste punt van de vorm. Ze zijn niet hard en niet vlekkerig, er zitten geen losse pixels bij en de rand loopt niet rondom.
3. **Staart van linksboven.**
   - De opbouw is nu selout 2 (lichtkant) | 4 licht (3 px) | C (2 px) | 2 schaduw | 1 omlijning, over de hele lengte (x51–60, y28–48).
   - **Lijkt op** de buisschaduw van Raticate's staart. Dit is cilindershading in de lengterichting en geen banding: de tinten hebben elk een functie en de breedtes zijn 3/2/1.
   - **Wijkt af in:** het model heeft juist een lichte rand rechts. Dat is bewust veranderd op verzoek (punt 3) en is geen fout.
4. **Verre poten een tint donkerder.**
   - Verre voorpoot: de schouder is nu E ((14–17,44–46)), de onderpoot 4/3 en de tenen E‑3‑E op (13–15,49).
   - Verre achterpoot: E is donkerder geworden.
   - Elke tint is consequent één stap verschoven ten opzichte van r8, dus de vorm is gelijk gebleven. **Lijkt op** E1 en Mightyena/Raticate.
5. **Bilsikkel zonder banding.**
   - Rechts op de bil ligt één 4-band die van 2 px (y34–36) via 3, 4 en 5 px (y41–45) breder wordt. De 3 verschijnt pas onderin, op (43–46,46–48).
   - De binnengrens loopt in een gelijkmatige diagonaal, en de oude 5‑4‑3‑1-lagen van 1 px zijn weg. **Lijkt op** Raticate's flank. Er is geen banding.

## Ontwerp en model
- Buiten de zones zijn 0 pixels gewijzigd (pixeldiff). Silhouet, poten, kop, pluimen, snorharen en het luie oog zijn gelijk aan r8.
- In het oor is de oude B (donkerbruin) samengevoegd met 2. Dat is visueel vrijwel gelijk (122,84,46 → 128,72,42) en het oor leest hetzelfde.
- De poten zijn onveranderd van vorm, zoals Jordi wilde.

## Nieuwe fouten?
- Er zijn geen tintvlakjes bijgekomen: de 29 clusters onder 3 px hebben allemaal een functie (tenen, teenlijnen, glans, oorrand, dijlijn, snorharen). Ook banding, pillow shading en open randen zijn er niet.
- Er zijn 16 kleuren, met ≤ 3 tinten per groep plus omlijning.
- Klein punt, geen afkeur: aan de rechterkant van de staart liggen een 2-schaduw van 1 px en de zwarte lijn over de hele lengte naast elkaar. Daardoor oogt die rand dik. Raticate doet hetzelfde.

## Reparaties
Geen.

Oordeel: PASS

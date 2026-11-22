# Keuring r5 vuurduivel fase 1: kleur en schaduw (`sprite_r5/vuurduivel_r5.png`)

Opdracht (bijgesteld): Jordi, letterlijk: "de oogvorm is goed, het kleur/schaduwwerk kan beter, over de gehele sprite". **Silhouet, lijnen en oogvorm zijn bevroren**; deze keuring gaat alleen over tinten binnen het silhouet, als voorbereiding op een kleurronde. Vel: `keuring_r5/vel.png` (r5 8× | model op dezelfde schaal | Houndour, Umbreon, Sneasel, Magcargo Gen 3 4× | r5-palet met helderheid L).

## Oordeel: **BIJNA** (vorm goed; kleurronde nodig)

Het grootste probleem: **het zwarte lijf is te donker en te samengedrukt.** De tinten d/m/l zijn L 26/50/71: stappen van ±22 in plaats van ±30–40. De donkerste vulling (L 26) ligt vlak bij de lijn (L 1), zodat de schaduwkant in de buitenlijn verdwijnt. Kop, lijf en armen lezen daardoor als één zwarte vlek met hier en daar een grijs plekje. Gen 3 doet "zwart" lichter en met een glans: Houndour lijn 16, vulling 41/57/82, glans 139; Umbreon 49/65/90, glans 148. Het model zit op ±24/48/60–72 (gemeten), maar kleur mag afwijken van het model; Gen 3 gaat voor.

## Volume per vlak

| Vlak | Bolling/sikkel/hooglicht, licht linksboven? | Oordeel |
|---|---|---|
| Kop | l-vlak linksboven op het voorhoofd (x16–23, y24–29), d-sikkel rechts op de wang (x31–37, y33–35) en de kin (y39–41): de richting klopt. Het l-vlak is een blok dat onderaan het breedst is (rij 29) en hard stopt; geen glans op de bolling. | half |
| Borst/lijf (x21–33, y41–49) | Eén m-vlak, 3 px l (23–24,44),(24,45), smalle d-rand rechts. Geen bolling. | **nee** |
| Armen | Beide alleen m + K; geen licht boven/donker onder; verre arm (rechts) even licht als de nabije. | **nee** |
| Oren | Linkeroor (x12–15, y29–35) helemaal d: het oor aan de lichtkant is het donkerste deel van de kop. Rechteroor heeft l/d/m. | **links nee** |
| Broek/vacht (x19–36, y50–56) | t bovenin (rij 50–51) over de hele breedte, B eronder: horizontale banding in plaats van twee dijen; b nauwelijks gebruikt (3 px). | **nee** |
| Poten/hoeven | Poten vlak B; hoeven gestreept t/b/t (rechterhoef rij 59–61, rij 60 = bbbb). | **nee** |
| Haarvlammen | Kleurverloop van het model (rood aan de basis, oranje, geel aan de toppen rechtsboven) is goed. Rechts van de kop (x29–38, y21–28) staan losse O-pixels in r (dambord). De stap r→O (L 77→145) is 68: er mist een middentint. | half |
| Hoorns | R/h/i (45/88/139) + K: hooglicht i links, 3 tinten, stappen 43/51. | **goed** |
| Staart | Stam rij 50–51 (x35–42) twee rijen puur K: geen bovenlicht. | half |
| Pijlpunt | Y midden, O, r rechts/onder, R-rand: richting goed. Geel is een streep van 1 px (x45–46, y37–40). | bijna |

## MOET (alleen tinten binnen het bevroren silhouet; lijnen en ogen blijven op hun plek)

1. **Zwart lijf: palet lichter en ruimer, gemeten op Houndour/Umbreon.** Vervang:
   - d (27,26,25) → **(41,38,38)** L≈39
   - m (51,50,50) → **(66,62,62)** L≈63
   - l (72,72,71) → **(98,92,92)** L≈93
   - nieuwe glans **(139,131,131)** L≈132, alleen op de bollingen (zie 2, 3), ≤ ±8 px in totaal (zoals Houndour 139 / Umbreon 148)
   - buitenlijn K (3,1,1) → **(16,16,16)** zoals Houndour/Umbreon/Gengar.
   Het lijf blijft zwart lezen (Houndour leest zwart met deze waarden).
2. **Kop:** het l-vlak als bolling: breedst bovenaan het voorhoofd en naar onder smaller langs de linkerkant (dus (16–17,29) en (22,28–29) → m; (19–24,24–25) blijft l). Glans 2×2 op (20–21,25–26). Linkerwang (16–18, 34–37): de pixels vlak naast de buitenlijn m houden en (17,35),(17,36) → l als kleine wangbolling. De d-sikkel rechts (31–37,33–35) en de kin (22–30,39–41) blijven, maar met de nieuwe d.
3. **Borst:** bolling linksboven: l op (22–26,43) en (22–25,44–45), glans op (23,44),(24,44); d-sikkel van 2 px langs de rechterrand (29–31,44–49) en onder de kin op de hals (y40–42, bestaat al). Het midden (26–29,45–49) blijft m.
4. **Armen:** nabije (linker) arm: bovenste rij l, onderste rij m (x17–21, y44–46); hand linksboven l. Verre (rechter) arm (x35–39, y43–46): bovenste rij m, rest d.
5. **Linkeroor (x12–15, y29–35):** vulling is nu (13–14,31–32),(14,33–34), alles d. Maak (13,31) → l en (13,32) → m (lichtere voorrand); (14,31–34) blijft d, zoals het model (lichtere rand, donker binnenoor).
6. **Broek: twee dijen in plaats van banden** (gemeten model: licht (132,96,72), donker (96,60,48); palet b/B/t blijft):
   - t als bolling op de linkerdij (19–25, 50–53) en linksboven op de rechterdij (29–31, 51–53);
   - B in het kruis/de plooi tussen de dijen (26–28, 51–55) en het midden van de rechterdij;
   - b als sikkel langs de rechterrand (33–35, 50–56) en onder de rafels (rij 54–56 tegen de buitenlijn);
   - de t-pixels rechts in rij 50–51 (x29–32) → B (dat is de schaduwkant).
7. **Poten/hoeven:** per poot links B, rechts b (sikkel aan de schaduwkant). Hoef als één vlak zoals het model (hoef lichter dan de poot, (132,96,72)/(144,108,84)): rechterhoef (35–36, 59–61) t, (37,59–61) B, rij 60 (35–36) bbbb → t (streep weg); linkerhoef is al t/B; alleen (21,59) b → B.
8. **Haarvlammen:** voeg één middentint toe tussen r en O, gemeten op Magcargo/Slugma **(222,90,32)** L≈127 (het model heeft hier (240,96,48)), zodat elke tong R-rand → r → midden → O → Y loopt. Rechts van de kop (x29–38, y21–28) de losse O-pixels ((33,24),(35,24),(32–33,25),(35,25),(35,26),(37,26)) samenvoegen tot twee schuine tongen in de middentint/O, met r eromheen: geen dambord. Vuur mag zo 4 tinten + selout hebben (Magcargo gebruikt er 5).
9. **Staartstam:** bovenste rij (36–41, 50) → d (nieuw), zodat de stam licht van boven krijgt; rij 51 blijft lijn.
10. **Pijlpunt:** het geel 2 px breed maken in de bovenste lob: (45,38),(45,39) → Y naast de bestaande (46,37–39); r als sikkel rechtsonder laten zoals nu.

## KAN

- Mond: binnenkant r (162,41,41) en tong p (198,98,92) zijn goed; eventueel de bovenste mondrij in R (donkerder keelschaduw).
- Lichte selout: de vlammen hebben aan de linker/lichte kant al r als rand; dat mag O worden waar de tong tegen de lucht staat (bv. (18–19,20)).

## Wat goed is
Hoorns (3 tinten, hooglicht links), de vuurrichting van het model, het mondpalet, de oogvorm (bevroren) en de lichtrichting op de kop.

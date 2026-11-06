# Keuring poedelmot kleur_r8 (onafhankelijke keurder, 6 nov)

Bron: `docs/concept/sprites/poedelmot/referenties/samengesteld.png` (uitsnede volgens `silhouet/sil.py`: x 139–854 → 62 px, y0 150, offset (1,17)), naast `kleur_r8/poedelmot.png`.
8×: model en sprite op 512 px naast elkaar (keurder-scratch `naast.png`, `boven.png`, `onder.png`).
1×/3×: naast Venomoth en Dustox (`graphics/pokemon/*/anim_front_gba.png`).
Alleen de twee maatstaven: (1) accuraat t.o.v. het model, (2) nette Gen 3-sprite volgens SPRITE_KERN. Silhouet: alpha-diff 0 (bevroren, klopt).

## Eis 1: accuraat t.o.v. het model
| Onderdeel | Lijkt op | Wijkt af in |
|---|---|---|
| Ogen | Plaats en maat kloppen (links x17–19, y32–40 smal; rechts x26–33, y32–41 groot), glans 2×2 wit linksboven in het rechteroog (28–29,34–35). | Tan ring rond het rechteroog (in het model rondom zichtbaar, vooral onder/rechts) is alleen 1 kolom `6` op x33/34; onderrand van de ring ontbreekt. |
| Kop/kruin/kin | Witte kop, crèmetint op de kruin tussen de sprieten (y26–29). | Kin: donkere boog `3` op y40 x25–27 en y41 x19–21/26–27 met lichte `9` ertussen (x22–25) leest als een **mond**; in het model is de kin een zachte tan overgang naar de kraag, geen lijn. |
| Sprieten (nerf, baarden) | Vorm en kleur (zwartbruin) uit het silhouet, lichte nerf `C`. | Nerf is een rechte diagonaal in trapjes van 3 px (links y18–28, rechts y19–26); in het model een **gebogen** nerf dicht langs de bovenrand. Baarden: patroon `1`/`4` om en om leest op 8× als **schaakbord**, niet als evenwijdige schuine ribben zoals in het model. |
| Vacht | Witte massa van kop/kraag klopt in vlakverdeling. | Kraag onder het gezicht (y42–48) is een vlak wit/`7`-vlak; de pluizige plukjes en haarstreken van het model ontbreken volledig. |
| Linkervleugel | Wit, juiste plek. | Binnenlijnen zijn donkerbruine `3`-strepen (x13 y31–37, x9–12 y30–36); in het model zijn het lichte tan veertjes/schelpjes bij de voet. |
| Rechter voorvleugel (rand, krullen) | Witte bovenrand (y20–22) en 2 px wit rechts. | Krullen zijn hoekige rechthoekjes: verticale `6`-kolommen op x47, x52, x56 (y26–35) en vierkante "C/E"-haakjes; model heeft **ronde golvende schubbogen**. De geschulpte witte buitenrand van het model is nauwelijks te lezen. |
| Rechter achtervleugel | Scheidingslijn y36–37 en lagere lob op de goede plek. | Zelfde hoekige krullen (y38–44, x45–55: `5555`, `6666`-blokken); verticale naad x38–39 (y36–44) is een **rechte kolom** waar de rand in het model rond loopt. |
| Buik | Tan `6`, plaats klopt. | Naden zijn twee rechte horizontale `9`-streepjes (y50 x34–38, y53 x34–38): leest als "=". Model: bolle, gebogen segmentplaten. |
| Pootjes/klauwtjes | Twee witte voorpootbollen (x15–29, y48–55), twee achterpoten (x34–40 y56–60, x42–47 y52–58). | Klauwtjes: grijze `8`-blob (x25–29, y56–57) leest als vlek, niet als bruine haakjes; `24242` (x35–39, y60) en `242` zijn om-en-om-pixels i.p.v. 2–3 duidelijke klauwtjes per poot zoals in het model. |
| Omlijning | Donkerbruin rondom, geen open randen. | Model heeft een pluizige rand op vacht/vleugels; sprite is overal glad (silhouet is bevroren, dus alleen via interne randtinten te suggereren). |
| Kleuren | Crème/wit/zwartbruin palet klopt van tint. | Te bleek en te weinig contrast (zie eis 2); de warme tan op wangen/vleugelvoet in het model is zwakker. |

## Eis 2: Gen 3-eisen
- **Contrast faalt**: helderheden A 247, C 232, 9 227, 7 204, 6 188, 5 151. Stappen 5–23 (C/9 bijna gelijk, A/9 20) tegen ±30–40 bij echte sprites; Venomoth/Dustox hebben duidelijk gescheiden tinten. Op 1× leest de sprite vaal.
- **Tinten per groep**: crème/wit gebruikt A, C, 9, 7, 6, 5 (6 tinten) in één materiaal; > 3 + lijn. Extra losse kleur `8` (grijs) alleen in de klauwtjes.
- **Curven zonder trapjes**: faalt bij krullen (hoekig), sprietnerf (3-px trapjes), naad x38–39 en buiknaden (recht).
- **Banding**: vleugelkrullen als evenwijdige verticale kolommen (x47/52/56) = banding-achtig raster.
- **Belijning**: geen zwart/lila-afwisseling op één rand (goed), maar `2`/`4` om en om op de klauwrand onderaan (x35–39 y60, x44–46 y58–59).
- **Clusters**: 0 clusters < 3 px, 0 losse pixels (goed). Geen pillow shading gezien; licht linksboven redelijk.
- De maker noemt zelf de krullen, buiknaden en sprietribben als zwak punt: volgens SPRITE_KERN = terug.

## Top-5 reparaties
1. **Krullen** (voor- en achtervleugel, x40–58 y24–44): vervang de verticale `6`-kolommen en vierkante haakjes door 4–6 brede, ondiepe bogen (3–5 px breed, 1–2 px hoog, open naar de vleugelvoet) zoals de schubbogen in het model; geen rechte stukken > 2 px.
2. **Sprieten**: nerf `C` als boog langs de bovenrand (1–2 px onder de rand, meebuigend), ribben als evenwijdige schuine lijnen van `4` om de 2 px (één richting, per rib 2–3 px lang) i.p.v. het `1414`-schaakbord.
3. **Contrast/tinten**: crème-groep terug naar 3 tinten + lijn (bijv. A 248, ~215, ~180), `C` en `9` samenvoegen, `8` schrappen (klauwen in `3`/`4`).
4. **Kin**: haal de donkere boog y40–41 x19–27 weg; zet een zachte `7`/`6`-sikkel onder het gezicht tegen de witte kraag, en voeg 3–4 korte `7`-plukjes in de kraag (y42–47) en langs de rand van de linkervleugel voor de vacht.
5. **Buik en pootjes**: buiknaden als 2 gebogen `7`-bogen (bol naar onder, 5 px breed) i.p.v. rechte `9`-streepjes; per poot 2 klauwtjes van 2 px in `3` met `4`-punt, zonder om-en-om-pixels. Rechte kolom x38–39 y36–44 laten meebuigen met de vleugelrand.

Oordeel: FAIL

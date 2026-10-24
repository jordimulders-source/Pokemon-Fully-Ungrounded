# Keuring kolibrie ronde 4: eindkeuring (24 okt, onafhankelijke keurder)

**Gekeurd:** `kolibrie.png`. Dit is de variant sleep uit ronde 3 met de staartreparaties 1–5.
- 64×64, P-modus, 16 kleuren, index 0 transparant, 1000 px.
- Vergeleken op 6× en 1× (licht en donker) met ronde 3 en met Swellow, Yanma, Ninjask, Crobat, Articuno, Honchkrow en Fearow. De andere referenties zijn ongewijzigd t.o.v. ronde 2 en 3.
- Vel: `keuring_vergelijking.png`. Boven ronde 3 en ronde 4 op 6×; onder ronde 4 op 1× (2× weergegeven) naast de referenties.

## Bevroren delen en budget
| punt | oordeel | toelichting |
|---|---|---|
| Diff buiten de staartzone t.o.v. ronde 3 (zelf nagemeten) | **PASS** | 0 pixels verschillen buiten x ≥ 42 vanaf rij 26 en x ≥ 36 vanaf rij 41. Het palet is identiek. Kop, kuif, lijf en vleugels zijn dus gelijk aan de in ronde 3 goedgekeurde delen. |
| 123 gewijzigde pixels t.o.v. een budget van ±45 | **PASS** | De vorm verandert 45 px (24 erbij, 21 eraf), precies het budget. De andere 78 zijn alleen omkleuringen langs de omlijning (punt 1) en het hooglicht (punt 5); die kon ik niet kleiner maken zonder pixels over te slaan. Er zijn geen ongevraagde wijzigingen. |

## Reparaties 1–5 uit ronde 3
| # | reparatie | oordeel | wat ik zie |
|---|---|---|---|
| 1 | Omlijning van de slierten in de juiste waarde; open randen in `6` dicht | **PASS** (op (18,37) na, zie hieronder) | **S1:** onderkant (50–56,36) is zwart; de buitenbocht is `5`/`1` aan de schaduwkant (rechtsonder). **S2:** onderkant zwart. **S3:** `117855` (zwart linksonder, `5` rechtsboven), in het bleke deel `5` tegen `b`. De schaduwkant is overal donkerder dan de lichtkant. De open-randcontrole vindt nog maar één pixel schaduwtint naast transparant: (18,37). |
| 2 | S2 en S3 als liggende vlam, niet als ster | **PASS** | **S2** (x 55–63, rij 38–42): ronde voet van 5 rijen, aflopend naar één punt bij (63,40). **S3** (x 56–62, rij 49–53): idem, met de punt bij (62,51) en de onderkant korter, dus niet gekopieerd. De losse punten boven en onder zijn weg. Op 1× op donker lezen ze als twee kleine vlammetjes die naar achteren waaien, niet als sterretjes. |
| 3 | Onderkant staartbasis niet recht | **PASS** | Treden 3-3-3 (rij 40 x 42–44, rij 39 x 45–47, rij 38 x 48–50), in het verlengde van de buikboog. De rechte lijn van 9 px is weg. |
| 4 | L-hoek van S1 wordt een boog | **PASS** | Bovenrand 5-3-2-1-1 en de binnenrand trapt mee. Op 6× een vloeiende opwaartse krul die in het vlammetje overgaat; geen hoek meer. |
| 5 | Hooglicht van S1 één tint terug | **PASS** | (51–55,34) van `L` naar `V`. S3, de nabije sliert, is nu het helderst. |

### (18,37), buikschaduw naast transparant
- Ligt in het bevroren lijf. Dezelfde pixel stond al in ronde 2 en 3 en stond op mijn lijst in ronde 3 (punt 1: "(18,37) onder de keel wordt `1`").
- Het is de enige open rand in de hele sprite. De kuifpixels met basistint naast transparant zijn pseudo-omlijning van 1–2 px (SPRITING §8) en mogen.
- **Oordeel: FAIL op eis 9, maar 1 pixel.** De reparatie is `6` → `1` op (18,37). De buikomlijning loopt dan door van (17,37) naar (19–21,38).
- Dit raakt de vorm niet en ook niet het gezicht. Het herstel van één omlijningspixel in de bevroren zone mag (opdracht van de coördinator). Na die reparatie is geen herkeuring nodig.

## Nieuwe fouten?
Ik heb drie dingen nagelopen. Geen ervan levert een nieuwe fout op.
- **Zwarte knoop bij de staartwortel** (x 42–54, rij 36–41): veel zwart waar de drie slierten uit de franje komen. Op 6× op licht is dat een donker kruispunt. Op 1× leest het als schaduw onder de staart, zoals bij Swellow en Honchkrow, en niet als gewricht of los deel. **PASS.**
- **Zwarte schaduwkant op donker:** op een donkere achtergrond valt hij weg, waardoor de linten dunner ogen. Dat is normaal voor een zwarte omlijning aan de schaduwkant (Honchkrow en Murkrow doen hetzelfde). Kop, vleugels en vlammetjes blijven goed leesbaar. **PASS.**
- **Rechte stukken:** het lint van S1 over de staartbasis is recht (rij 34 en 36, 5–7 px). Dat is een rechte staartveer zoals bij Swellow, dezelfde beoordeling als S3 in ronde 3. **PASS.**

## Alle eisen opnieuw

### SPRITE_NORM
| # | eis | oordeel |
|---|---|---|
| 1 | Leest op 1× als Pokémon van dit bouwtype (vogel) | **PASS.** Op licht en op donker overduidelijk een kolibrie met een lange, naar achteren slepende staart. Met Yanma en Ninjask in dezelfde rij is er geen insectlezing. |
| 2 | 3/4 links-voor | PASS |
| 3 | Delen vast | PASS. Alle drie de slierten komen uit de staartbasis. |
| 4 | Geen Escher | PASS. S1 (ver) boven, S3 (dichtbij) onder, met lucht ertussen. |
| 5 | Curven, geen rechte lijnen waar rond | PASS. Buikboog, staartbasis in treden, de krul van S1. |
| 6 | Kop | PASS. 23%. |
| 7 | Ogen geïntegreerd | PASS. Klein; bovenlid, glans (10,26), reflectie (11,27). |
| 8 | Kenmerken leesbaar op 1× | PASS. Snavel, kuif, doorschijnende vleugels, blauwgroene glans, drie vlammetjes. |
| 9 | Omlijning en licht, geen open randen | **FAIL (1 px):** (18,37). Verder PASS. |
| 10 | Geen Chernobyl | PASS |

### FAKEMON_CHECKLIST (vogel)
- A1–A6: PASS.
- B1, B2, B7: PASS.
- C1, C7, C8: PASS.
- D1/D2: PASS. Het formaat zit op Crobat-niveau qua vulling en kernmassa, zie ronde 3 §4.
- E1: PASS (na punt 5).
- E2: PASS.
- E3: PASS.

### SPRITING §0–§8
- §0.1–§0.7: PASS.
- §1–§7: PASS.
- §8: PASS, op (18,37) na.

### FAKEMON_DESIGN en SPEC
| punt | oordeel |
|---|---|
| Simpel | PASS |
| Beperkt palet en één geheel | PASS |
| Geen hybride | PASS |
| Ghost-sfeer (mystiek, niet eng) | PASS. Linten die vervagen naar geestlicht, met zachte vlammetjes. |
| Vleugels doorschijnend (Venomoth) | PASS |
| Staart met Articuno-dynamiek | PASS |
| Zielvlammetjes | PASS |
| Kop | PASS |
| Palet | PASS |
| Kuif | Bevroren vorm, Jordi's keuze (zie hieronder). |

## Eindoordeel: NIET GOED, op één pixel na
**Minimale reparatielijst:**
1. (18,37): `6` → `1`. Dit is de enige pixel.

Na deze reparatie is hij **GOED**. Een nieuwe keuring is niet nodig; een pixeldiff die aantoont dat alleen (18,37) is veranderd volstaat.

## Wat Jordi zelf moet beslissen (geen fouten)
- **Staart als silhouetwijziging:** de slierten slepen naar achteren in plaats van te hangen zoals in het goedgekeurde `silhouet_v6`. De hoofdversie op het bevroren silhouet (ronde 3, `kolibrie.png`) leest op 1× als poten. Daarom is deze variant het advies.
- **Kuif:** de drie veertjes komen samen in één steel. Op 1× is het een paars kuifje met lichte puntjes. Jordi keurde de vorm goed ("de jeguaka is goed"); alleen aanpassen als hij hem anders wil.
- **Formaat:** naast Swellow oogt hij lichter (slank, veel lucht, bewust zo). Qua dichtheid staat hij gelijk aan Crobat.
- **Staartlengte:** die loopt tot de rand van de box. Langer, zoals bij een echte langstaartsylfe, past niet in 64 px.

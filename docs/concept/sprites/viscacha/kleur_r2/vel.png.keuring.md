# Keuring viscacha kleur ronde 2 (onafhankelijke keurder, 7 nov)
- Bron: docs/concept/sprites/viscacha/referenties/gemini_gekozen_ronde6.png; vergeleken met graphics/pokemon/{pachirisu,emolga,dedenne,sandshrew,taillow}/anim_front.png (bovenste 64×64), plus kleur_r1/vel.png.keuring.md en kleur_r2/NOTITIES.md.
- Bekeken: kleur_r2/viscacha.png op 8× (nearest), 1× op licht (240) en donker (40), close-ups 14× van kop en romp met raster per 5 px, en raster.txt per pixel.

## Blind (vóór SPEC/bron/notities)
- Op 1×: een zandoranje springknaagdier (kangoeroerat/springmuis) in profiel naar links, voorpoot opgeheven, lange omhoogkrullende staart met gele gekartelde pluim. Leest als Pokémon-achtig wezen, Electric door het geel.
- Wat meteen opvalt op 1×: **een gele schuine band in de nek die als kraag/sjaal leest** (het eerste wat ik zag). Daarna: het lijf is één grote, vlakke oranje massa met een rechthoekige crème vlek op de buik; de rug is bovenop plat.
- Op 8×: netjes qua pixels (geen losse pixels, ≤3 tinten per groep), maar de rugcontour is een recht stuk met een trap, de vachttonen liggen in grote vlakke blokken en de schaduw rechts loopt als band evenwijdig aan de buitenrand. Losse donkere stip op de wang. Oren smal en hoog (licht vos/konijn).
- Naast Pachirisu/Emolga/Dedenne: nog niet zonder twijfel; de kraag en het vlakke lijf verraden hem.

## Per onderdeel (na SPEC en bron)
- **Pose / massa**: lijkt op de bron (gespannen, voorpoten op, achterpoten gebogen, staart krult omhoog) / wijkt af in: niets wezenlijks. Hoofdvraag pose: PASS. Kop staat volledig in profiel; de bron ook vrijwel, dus geen FAIL-punt.
- **Kop**: lijkt op de bron (profiel, ronde wang, oog) / wijkt af in: de kop heeft **geen eigen onder-/achtercontour**; de kopmassa (5/4) loopt rij 33–36 zonder lijn over in nek en borst. Daardoor wordt de gele pluk de enige grens tussen kop en lijf. Losse 2-pixel op (5,33) leest als wrat/stip, niet als mond. Neus (1–2,29) `11` is een inkeping in de snuitrand (mag, maar zwak). Kinlijn (6–10,37) `FFFFF` nog recht.
- **Oog**: Emolga-oog, leest als Pokémon-oog. OK.
- **Wangpluk**: lijkt op de bron (gele punt naar achter-boven) / wijkt af in: het geel is een **diagonale band van gelijke breedte** (4 px op elke rij, 26–31; 5 px op rij 32) van (20–23,26) tot (13–17,32), met een **platte, onomlijnde onderkant** op rij 32 midden in de wang. Direct ernaast loopt een parallelle 2-lijn (21,28)→(18,33) en een 33-schaduwstrook (19–23,28–34): drie evenwijdige diagonale strepen (geel, lijn, schaduw) = riem/kraag. In de bron is het een sikkel: brede ronde voet óp de wang achter/onder het oog, taps naar één punt die achter de kop uitsteekt. Coördinator-observatie **bevestigd**.
- **Oren**: lijken op de bron qua plaats; toppen nu rond (OK) / wijken af in: smal en hoog (verre oor 4–5 px breed over 9 rijen); bron heeft een grote, ronde schelp aan het nabije oor. Smaakpunt, zie "voor Jordi".
- **Lijf / rug**: lijkt op de bron (oker, schaduw rechtsonder) / wijkt af in: rugcontour rij 27 x28–36 is een **recht stuk van 9 px**, daarna een regelmatige **trap van 2 px per rij** (37–38,28), (39–40,29), (41–42,30) en dan 1 px. Geen vloeiende boog.
- **Toonvlakken**: coördinator-observatie **bevestigd**. Lichte rugplaat 5 (x22–38, rij 28–33) is een blok met getrapte onderrand; daaronder is het hele lijf (x12–44, rij 34–48) één vlak 4 zonder vormschaduw. De dijlijn 3 (33–35, rij 34–44) is een rechte verticale naad van ±10 rijen. Schaduw 3 rechts (x40–46, rij 33–50) is een band evenwijdig aan de buitenrand (banding), geen sikkel om de bil. Licht linksboven: richting klopt, vorm niet.
- **Buik / crème**: lijkt op de bron (strook onderaan) / wijkt af in: bovenrand rij 44 x27–34 is een **rechte horizontale lijn van 8 px**; op 1× leest de crème als rechthoekige vlek.
- **Voorpoten**: verre poot opgeheven, OK. Nabije poot (17–22,37–50) heeft nu een pols; nog vrij lange kolom, acceptabel.
- **Achterpoten**: perspectief klopt (verre voet hoger/links). Onderrand verre voet (22–29,58) nog 8 px recht; scheen nabije achterpoot (44–49,55–58) een rechte buis met parallelle strepen 2/4/3. Klein.
- **Staart + pluim**: één geheel met het lijf, pluim gekarteld en leest op 1× als één ding. OK. Kleine banding: B/CC/44/3 lopen over de hele staartlengte evenwijdig (rij 26–45); voor Gen 3 acceptabel.
- **Belijning**: geen zwart/selout om en om gevonden; zwart aan schaduwkant, selout 2/F/8 aan de lichtkant. OK.
- **Netheid/contrast**: controle.py klopt (0 open randen, 0 losse pixels, clusters alleen oog + pluimkern). Helderheidsstappen 5→4→3→2 ≈ 35/40/46, in lijn met Taillow.

## Reparatielijst (geprioriteerd, via de maker)
1. **Wangpluk als sikkel op de wang, kop eigen contour** (hoofdpunt, kraag):
   - Geel een tapse vorm geven: punt 1–2 px op (22–23,25–26), breedst (3–4 px) rond rij 28–30, voet afgerond op ±(13–16,30–31) binnen de wang; de platte rij 32 (13–17) terug naar wangtint 4/5, of 1–2 px met een 8-randje zodat het geel daar *eindigt* in een ronding.
   - De parallelle 33-strook (19–23,28–34) weg; schaduw 3 onder de kaak als korte sikkel onder de kop (±12–19, rij 33–35) die de ronde kop afsluit.
   - Een tapse binnenlijn 2/3 langs de onder-achterkant van de kop (±(12,35) → (17,34) → (19,32)) zodat de kop een eigen ronde vorm is en het geel óp die kop ligt, niet op de naad.
2. **Rugcontour als boog**: het rechte stuk (28–36,27) en de 2-px-trap (37–42,28–30) vervangen door oplopende/aflopende stukjes (bijv. 4–5–6–4–3–2–2–1), zodat de lengtes geleidelijk afnemen; massa zo min mogelijk veranderen, diff melden.
3. **Toonvlakken en schaduw**: dijlijn (33–35,34–44) korter en gebogen (sikkel langs de voorkant van de dij, verdwijnt halverwege); schaduw 3 rechts niet als rechte band langs de rand maar als sikkel om de bil (breed onder/achter, dun boven); lichte rugplaat 5 een vloeiende onderrand zonder trapjes; in het grote 4-vlak (x23–40, rij 34–43) één vormgevende overgang zodat de romp rond leest.
4. **Crème buik**: bovenrand rij 44 (27–34) als flauwe boog (midden 1 rij hoger of lager dan de uiteinden), geen rechte lijn.
5. **Kop-details**: losse 2 op (5,33) weg of omzetten in een korte, tapse mondlijn vanaf de neus; kinlijn (6–10,37) iets ronden.
6. **Klein**: onderrand verre voet (22–29,58) 1 px ronden; scheen nabije achterpoot (44–49,55–58) 1 px knik of tapse binnenlijn.

## Voor Jordi (geen FAIL-reden)
- Oren smal en hoog; de bron heeft een grotere, rondere oorschelp. Wil Jordi ze ronder/groter?
- Kop is klein t.o.v. het lijf naast Pachirisu/Dedenne/Emolga (minder "cute"); bron heeft dezelfde verhouding.
- Formaat 62 px breed, groter dan Pachirisu/Dedenne in hun frame.

Oordeel: FAIL

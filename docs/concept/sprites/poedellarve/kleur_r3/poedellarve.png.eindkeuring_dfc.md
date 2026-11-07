# Herkeuring poedellarve kleur r3: kleuren en schaduwen (Dragonfly Cave + Gen 3, 7 nov)

Alleen kleur en schaduw, zoals de eindkeuring van `af/` (`../af/poedellarve.png.eindkeuring_dfc.md`). Vorm en ontwerp niet gekeurd.
Sprite `kleur_r3/poedellarve.png`. Zelf nagemeten tegen `af/`: alpha-diff 0; 21 px anders, precies de lijst in NOTITIES.md; palet 7 = 226,216,200. Vellen (scratch): `eindkeurder/vel_r3.png` (8× + 1× licht/donker naast af/, poedelmot, Altaria en Wurmple) en `eindkeurder/r3_vs_af.png` (12×, af links, r3 rechts).

## Controles
| Punt | Oordeel | Meting / pixels |
|---|---|---|
| Reparaties 1, 3–7 | voldoet | Alle pixels zoals gevraagd: (35,44), (40,46), (44,49) en (14,41), (14,42), (13,43) zijn nu 3; (14,43), (14,44), (15,44), (13,54), (13,55), (14,55) zijn nu A; het oor (13,36), (13,38) is nu 7 en (14,39) is nu 6. |
| Reparatie 2 | voldoet, met één afwijking | (32,42), (32,43), (37,45), (43,47), (49,53), (50,54) zijn 2. (47,50) bleef 3, zie hieronder. |
| Randtelling 3 | voldoet | Boven 20, links 7, rechts 9, onder 0 (eerst: rechts 15, links 2). Van de 9 rechtsgerichte pixels zijn er 8 ook bovengericht (bulttopjes); alleen (47,50) staat puur rechts. |
| Randtelling 2 | voldoet | Onder 47, rechts 33, links 35. De 2's links in de bovenste helft zitten op de oortjes (x12–14 en x22–26, y33–40: kleine delen, donker leest beter) en op snuit/wang (13,44)–(13,49). Dat is de onderste helft van het gezicht, dus goed. |
| 2/3 om en om | voldoet | Volgens controle_uitvoer heeft selout 3 6 reeksen van 3–7 px, geen reeks < 3. Zelf langs alle randen nagelopen: geen 3,2,3. |
| Tintclusters < 3 px | voldoet | controle.py: 0. Zelf met 8-buren, zonder lijnkleuren: alleen de oortjes (3–4 px breed), de tapse naadeinden (31,45–46), (35,46–47), (44,50) en de glans (20,46), net als in af/. Het linkeroor is nu een 2-px-vlak 6 ((14,39), (15,39)) in plaats van 6/4/6/5 om en om: rustiger. |
| Lichtrichting | voldoet | Linksboven, zoals de poedelmot. Kruin, linkerkop en voorpoot zijn licht tot aan de lijn. Selout ligt op de linkerhelling en de top van elke bult, met zwart rechts en onder. De oogglans (20,46) en de schaduwkolom x30 lagen al zo. Naast de poedelmot op 8× is het licht nu hetzelfde. |
| Pillow shading | voldoet | De voorpoot is links licht en heeft schaduw rechts ((17,54–55) 7) en onder (6). |
| Contrast | voldoet | A→7 = 243→218 (25), 7→6 = 22, verder 29/35/40/49. Zelfde band als Altaria (25) en Cascoon (23). Op 1× leest de eerste schaduw beter dan in af/. |
| Banding, dithering, glans, palet, aansluiting op de mot | voldoet | Ongewijzigd ten opzichte van af/ (zie die keuring). |

## Afwijking (47,50)
Staartrand van boven naar beneden: (45,48) 3, (46,48) 3, (47,49) 3, (47,50) 3, (48,51) 3, (49,52) 3, daarna (49,53) 2, (50,54) 2 en (51,55) 2.
Met (47,50) op 2 wordt het 3,3,3,**2**,3,3,2: om en om, en dat is volgens SPRITE_KERN verboden. Met 3 is het één reeks van 7 die over de top van de laatste bult loopt en pas op de rechterflank overgaat in zwart. Dat is de normale Gen 3-overgang op een bol: de selout loopt over de top een stukje door naar rechts. **Akkoord met de afwijking.** Het alternatief, (47,50), (48,51) en (49,52) alle drie op 2, is ook goed en geeft een iets donkerdere achterkant. Het is niet nodig.

## Reparaties
Geen.

Oordeel: PASS

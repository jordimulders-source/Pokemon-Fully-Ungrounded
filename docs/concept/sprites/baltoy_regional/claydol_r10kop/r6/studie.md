# Studie ronde lijven (ronde 6, vóór het kleuren)
Bronnen op 12× in `vel.png`: Gen 3-Claydol (lijf, `graphics/pokemon/claydol/anim_front_gba.png`), Baltoy r19 (lijf), Golem (`graphics/pokemon/golem/anim_front_gba.png`; Golett heeft geen GBA-sprite).

1. **Tintgrenzen zijn gebogen en volgen de omtrek**: bij Claydol ligt het lichte vlak van romp en armen als een ovaal binnen een ring middentint; bij Golem volgt elke schaal en elk been een eigen boog. Nergens rechte horizontale banden; een rechte grens komt alleen voor waar een vorm over een andere valt (kop over hals).
2. **Aantal tinten**: 3 tinten + omlijning per kleurgroep (Claydol: licht/midden/donker olijf), een 4e (donkerste) alleen in de diepste hoek onderaan; geen dithering.
3. **Hooglicht** linksboven op elk bol deel, groot (± een derde van het vlak) en als één vlak, niet als streep; armen/benen krijgen elk een eigen klein lichtvlak bovenop.
4. **Sikkel**: de middentint loopt als een halve maan langs rechts en onder en wordt naar rechtsonder breder; het onderlijf ligt helemaal in de schaduwtinten (Claydol rij 53–55: donkerste tint als onderrand), zodat het als onderkant van een bol leest.
5. **Armen/voeten komen los** door een donkere naad of de omlijning plus een eigen lichtkap, maar ze delen dezelfde lichtrichting als de romp: de schaduwkant van de romp loopt door in de schaduwkant van de arm (Golem: rechterarm en -been in dezelfde donkere tint als de rechterflank).

Toegepast in r6: één lichtveld voor het hele lijf (romp, hals, armen, voeten) plus per deel een kleine eigen bolling; tinten 2/3/5/A/6 zoals de kop; daarna met de hand bijgewerkt (`HAND`, `FIX` in `r6.py`), vastgelegd als tekstraster `LIJF_A`.

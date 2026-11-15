# Hauntflare v13: kleurronde kuif, staart en handen (15 nov)
Opdracht (Jordi): "ok genoeg, de vlammen en handen moeten meer vlammen worden, stuur maar meteen naar eindkeuring voor kleur, schaduw en belijning". Basis `sprite_v12/hauntflare_v12.png`; alleen herkleurd, niets getekend of verschoven.

## Studie (Gen 3, 8x)
Typhlosion, Ponyta, Rapidash, Charmeleon, Magmar, Moltres, Magby: vlammen hebben geen zwarte lijn; rand rood (lichtkant) tot donkerrood; geel hart aan de basis/lichtkant, dan oranje, oranjerood, rode punten; 3-4 tinten; grenzen als gekartelde tongen die naar de punt wijzen (Typhlosion), geen rechte banden.

## Palet (alleen vlam/hand-plekken veranderd)
| idx | oud | nieuw | rol |
|---|---|---|---|
| 10 | (154,42,34) | ongewijzigd | donkerrode lijn schaduwkant (ook mond, daarom vast) |
| 11 | (216,64,48) | (224,48,40) | rood: lijn lichtkant, punten, schaduw |
| 15 | (238,116,124) ongebruikt | (240,104,40) | oranjerood (nieuw) |
| 12 | (244,134,89) | (248,160,48) | oranje |
| 13 | (248,184,80) | (255,224,96) | geel hart / vingertoppen |
Helderheid A 75 → B 100 → F 137 → C 174 → D 218. Index 11/12/13 kwamen buiten kuif/staart/handen nergens voor (script: componenten); index 10 wel (mond, (46,34)) en is dus niet aangepast.

## Wat er gebeurde
- Kuif (2 vlammen): geel hart tegen de bol, oranje en oranjerood in tongen naar de punten, rode punten; lijn lichtkant (linksboven) rood, schaduwkant (rechts) donkerrood i.p.v. zwart. Zwarte bollijn ertussen blijft.
- Staart: geel hart waar hij onder de bol uitkomt, tongen naar rechts, rode punt; onderrand en inkeping donkerrood i.p.v. zwart. Zwart dat de ring raakt (45,41) blijft zwart.
- Handen: rug geel/oranje linksboven, oranjerood midden, rood rechtsonder; vingers oranje lichtkant, gele toppen; lijn lichtkant rood; zwarte lijnen tussen de vingers en aan de schaduwkant blijven.
- 374 pixels herkleurd, waarvan 47 zwarte randpixels van vlam/hand (naar rood/donkerrood). Transparantie identiek; diff buiten kuif/staart/handen = 0 (assert in `v13.py`: elke gewijzigde pixel ligt in een vlam/hand-component of is een zwarte randpixel zonder bol/ring-buur).

## Eigen zwakke punten (na 3 eigen rondes)
- Hersteld: rechte verticale banden in kuif en staart (nu tongen), losse 1-px vlekjes (33,15), (50,14), (12,54), puntvinger rechterhand afwisselend C/F/D.
- Resterend, bewust: vingertoppen van 1 px breed zijn losse D/C-pixels ((57,41), (60,41), (53,45), (61,42), (26,57)); vingers zijn 1 px, dus kan niet anders (gloeiende toppen). Grote gele vlak links in de kuif (rij 16-19) is de bewuste Typhlosion-basis.

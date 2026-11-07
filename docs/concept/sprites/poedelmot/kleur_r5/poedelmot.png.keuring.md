# Keuring poedelmot kleur_r5 (onafhankelijk, streng)

Bron: `docs/concept/sprites/poedelmot/kleur_r5/poedelmot.png` (64×64, P, 12 kleuren gebruikt). Referentie `referenties/samengesteld.png`, uitsnede volgens `silhouet/sil.py` (x 139–854 → 62 px, offset (1,17)). Stijl naast `graphics/pokemon/altaria`, `venomoth` (anim_front, frame 0). `kleur_r4`-keuringen pas na dit oordeel gelezen.
8×: bekeken (ref | r5 naast elkaar). 1×: bekeken naast Altaria en Venomoth.

## Blinde indruk
Op 1× leest het als een wit **katten-/vossenkopje met twee gestreepte oren** op een **blok**, niet direct als mot. Kop en ogen zijn het sterkst. De rechterhelft (vleugels) leest als een plat crème vlak met strepen. De onderkant (pluimen, buik, pootjes) is een rommelige massa met losse bruine pixels. Naast Altaria/Venomoth mist het de ronde wolklobben en de gebogen aders.

## Gelijkenis per onderdeel
| Onderdeel | Lijkt op | Wijkt af in |
|---|---|---|
| Ogen | Nabij oog nu een schuin zwart amandel (x25–32, y33–40) met glans (28–29,34) en tan ring rechts/onder; ver oog smal (x17–20, y32–40). Plaats en grootteverhouding kloppen. | Glans in de bron is een bredere witte boog; hier 2 px. Ver oog: olijf `B` op (18–19,37–38) leest als vlek. Klein punt. |
| Kop / kruin / kin | Ronde kop, wit, juiste breedte. | **Kruin plat**: rij 27 x22–25 `4444` is een rechte tan lijn tussen de sprietvoeten; bron heeft daar een pluizige witte kuif omhoog. **Kin/mond**: rij 41 x18–29 `a43339999333` is een rechte donkere streep onder de ogen → leest als mond/kaaklijn; bron heeft geen mond, alleen zachte vacht. Geen pluizige kraag rond het gezicht (bron: geschulpte vachtrand). |
| Sprieten | Zwart kamvlak met lichte nerf `C` diagonaal (links (3,18)→(19,29), rechts (46,19)→(31,26)); baarden schuin. | Baarden `1313`/`3131` wisselen per pixel om-en-om (bijv. rij 22 x5–14 `1313115151`, rij 25 x33–48 `1131311313`): leest als ruis/raster, niet als kam. In de bron zijn de baarden lange donkere ribben met lichte tussenruimtes, ±1 per 2 px, haaks op de nerf. Sprieten lezen op 1× als oren (vorm ligt vast, maar de nerf aan de bovenkant versterkt dat). |
| Vacht | Wit grootste vlak, schaduw `7` rechtsonder de kop (x30–37, y38–45). | Geen vachtstructuur: bron heeft overal plukjes/geschulpte randen; hier gladde vlakken met losse `7`-vlekjes (rij 34–40 x13–16 `77`,`73`,`7`) zonder vorm. |
| Linkervleugel (achter de kop) | Wit lobje links (x6–12, y26–36) op de juiste plek. | **Geen scheiding met het gezicht**: geen binnenlijn tussen vleugel en wang, dus leest als wang/oorhaar. Bron: duidelijke donkere naad en geschulpte witte lob. |
| Rechter voorvleugel | Crème vlak met tan krullen, wit boven. | **Rechte lijnen**: verticale naad x37–39 over y30–46 (`7`/`3`-kolom), horizontale lijn rij 36 x38–57 (20 px recht `3`), rij 46 x39–52. Bron: gebogen aders die vanuit de vleugelvoet waaieren, geschulpte rand. Krullen `777`/`99` zijn vlekjes, geen bogen. |
| Rechter achtervleugel | Lob onder de voorvleugel, crème. | Onderrand rij 45–46 trapsgewijs recht; bron is één ronde lob met geschulpte rand. Inhoud `9`/`7`-banen parallel aan de rand (banding, rij 37–44 x46–56). |
| Buik | Tan segmentstrepen `4` (rij 49 en 52, x30–37) tussen de pluimen, zoals bron. | Strepen exact horizontaal en even lang; bron: gebogen ringen die de buikronding volgen. |
| Pootjes / pluimen | Vier witte pluimen ongeveer op de bronplekken. | Pluimen zijn rechthoekig (linker blok x15–29, y47–54 met rechte kolomnaden x23 en x30); bron: ronde bolletjes. Klauwen = losse bruine stipjes (rij 55–61: `242`, `48222`, `2442`, `24242`), geen pootjes in perspectief. Gat in de omlijning op (21,55). |

## Stijl (SPRITE_KERN)
- Belijning: selout grotendeels goed (`3` lichtkant links, `2` rechts/onder), bovenrand sprieten `2`. Maar om-en-om `1`/`3` in de sprieten en losse `4/8`-pixels aan de onderrand = ruis.
- Vormen: rechte stukken waar het dier rond is (vleugelnaden rij 36/46, kolom 38, buikringen, pluimblokken, kruin). Dit is het hoofdprobleem.
- Clusters: veel 1–2 px-vlekjes `7`/`9`/`3` in vacht en vleugel (machinaal-willekeurig), tegenover de grote lavendel-sikkels van Altaria.
- Leesbaarheid 1×: kop goed, rest vlak; leest eerder als "witte vos met oren" dan als poedelmot.

## Top-5 reparaties (vorm/belijning eerst)
1. **Vleugelnaden rond maken**: vervang de rechte lijn rij 36 (x38–57) en rij 46 (x39–52) door één geschulpte boog per vleugel (bogen ongelijk 5-4-6-3, `3`); verticale naad x37–39 (y30–46) als gebogen vleugelvoet die naar rechtsboven waaiert, met 2–3 gebogen aders `6` vanuit (38,32) naar de rand.
2. **Kin en kruin**: rij 41 x18–29 donkere streep weg (wit/`7`, kin alleen als zachte `7`-sikkel, laagste punt y42–43); kruin rij 27 x22–25 `4444` vervangen door 2–3 witte plukjes omhoog (x21–27, y25–28) met `3`-omlijning.
3. **Linkervleugel scheiden**: binnenlijn `3`/`7`, taps, van (12,27) naar (13,40) zodat de witte lob achter de kop apart leest; lobinkepingen op (9,31), (11,35).
4. **Pluimen en pootjes**: vier ronde bolletjes (kolomnaden x23/x30 krom, onderkant geschulpt) met `7`-sikkel onder; klauwen als 2 px schuine stompjes `2`+`4`, verre poten hoger en in `3`; losse stipjes (rij 58–61) weg, gat (21,55) dicht.
5. **Sprietbaarden als kam**: om-en-om `1/3/5` vervangen door doorlopende ribben (één `3`/`5`-streep per 2 px, 2–4 px lang, haaks op de nerf `C`), zwart ertussen egaal `1`.

Daarna pas: vachtvlekjes opruimen (grotere sikkels), buikringen licht gebogen.

## Na het oordeel: vergelijking met r4-keuringen
Opgelost: nabij oog (amandel, glans), sprietbovenrand `2` i.p.v. `1`, geen pillow shading, stap wit→schaduw groter, wit alleen aan de lichtkant van de vleugel. Nog open uit r4: sprietraster (nu streepjes maar nog om-en-om), naden y36/y45–46 recht, kruin, kinboog, linkervleugel-lobben, pootjes als stompjes, gat (21,55). Nieuw opgevallen: de rechte kin-/mondstreep rij 41.

Oordeel: FAIL

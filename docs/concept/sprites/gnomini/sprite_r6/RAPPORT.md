# Gnomini sprite r6: omlijning volgens Dragonfly Cave (22 nov)

Bron: `../af/gnomini.png`. Jordi: "Gnomini mag trouwens ook nog wel een dragonflycave keuring ja" (zelfde ronde als Gnomad r10–r11).
Gids (r. 89–91, 400–404, 425–428): outline shadows zwart; "the base outlining shade for every color" voor de rest van de lijn, 1 px breed; outline highlight in de lijn op de meest belichte randen; geen anti-aliasing buiten de lijn.
Outline base per onderdeel: muts 2 (donkerlila), huid/neus/armpjes 6 (donkerroze), broek a (donkerblauw, tint van de streep).

Script `r6.py`. Controles: silhouet (alpha) diff 0, palet ongewijzigd, alleen bestaande kleuren, wijzigingen alleen op de opgesomde pixels; muts-vorm, streep en grens roze/blauw ongemoeid.

**Zwart: af 140 px (14,8 % van 947) → A 80 (8,4 %) → B 83 (8,8 %).** A: 64 pixels gewijzigd.

## Per onderdeel (A)
- **Muts:** plooi van de omgeslagen punt (39,24), (39,25), (40,26), (40,27) zwart → 2 (binnenlijn; (39,23) was al 2). Onderkant van de rand over de neus (23..26,34), (21,35), (22,35), (27,35), (28,35) en over het lijf (30..31,36), (32..34,37), (35..37,38), (38..41,39) zwart → 2. Rand was bij x=30–31 2 px dik (rij 36+37): onderste rij (30,37), (31,37) → 7 (lijf in schaduw), zodat de lijn 1 px is en de muts zelf geen pixel verandert.
- **Neus:** zijkanten (20,36..40) en (29,36..40), onderkant (28,40), (21,41), (22,41), (23..25,42), (26,41), (27,41) zwart → 6 (binnenlijnen tegen muts, lijf en armpje; (20,39) is de lichtkant).
- **Armpjes:** (20,45) linkerarm tegen de broek en (43,46) rechterarm tegen de broek zwart → 6. Outline highlight 7 op de linkerarm linksboven (17,40), (16,41) (was 6).
- **Broek:** linkerkant (lichtkant) (20,47), (21,48), (21,49), (22,50) zwart → a. Binnenlijnen voetjes/kruis (23,51), (24,52), (25,53), (26,53), (27,54) en (40,52), (38,53), (39,53), (36,54), (37,54) zwart → a. Outline highlight b op de bovenkant van de linkervoet (20,51), (21,51) (was a).

## Welk zwart bleef en waarom
- **Schaduwkant (rechts/onder) tegen de achtergrond:** mutsflank en punt rechts (vanaf (45,23)), onderkant van de punt en het gaatje (41..46,26..27); onderkant van de mutsrand links (16,36), (17,37), (18,37), (18,38), (19,38) (rand naar beneden); rechterkant lijf (42,40), (43,41); onderkant en rechterkant van beide armpjes; rechterkant broek (41..43,47..51); onderkant/rechterkant beide voetjes en het kruis (29..34,54); linkeronderkant rechtervoet (35,55)..(38,58) (in de schaduw tussen de benen).
- **Knooppunten waar een binnenlijn op de zwarte buitenlijn uitkomt:** (42,39) muts/lijf rechts, (20,46) en (43,47) arm/broek, (28,54) voet/kruis: zo één overgang, geen losse lichte pixel in een zwarte lijn.
- Geen zwart en donkerlila om en om op één rand.

## B
Als A, plus zwart op 2 plekken: **(28,40), (29,40)** de diepste hoek rechtsonder de neus (schaduwkant, waar neus, lijf en mutsrand samenkomen; neus en lijf zijn allebei roze en scheiden in A alleen via 6) en **(40,52)** de kier tussen broek en rechtervoet (schaduwkant).

## 1×-controle
`strook_1x.png` (af, A, B op zwart en wit, 1× en 3×): in A blijven muts, neus, lijf, armpjes en broek gescheiden; de neus leest als bol door het hooglicht en de roze lijn, maar zwakker tegen het lijf dan in af (de zwarte ring om de neus las als een masker/ogen). B geeft de neus rechtsonder weer diepte zonder ring. De donkerlila mutsrand leest op zwart nog als rand.
Bestanden: `gnomini_A.png`, `gnomini_B.png`, `vergelijk_8x.png` (af | A | B | gewijzigd in A, magenta), `strook_1x.png`.

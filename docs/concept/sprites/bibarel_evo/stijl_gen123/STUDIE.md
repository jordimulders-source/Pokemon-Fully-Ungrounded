# Studie lijn- en kleurgebruik Gen 1–3 (24 nov, voor sprite_r17)

Jordi: "ik kan me er toch niet aan ontlenen dat het lijnen en kleurengebruik anders is dan bij andere sprites" · "gen 1 t/m 3 he" · "dat is geen goed vergelijkingsmateriaal, pak er 1 met een buikvlak" → hoofdreferentie **Kangaskhan** (bruin rechtop lijf met buikvlak, zoals onze bever met tuinbroek). Aanvulling alleen voor het palet: Ursaring, Teddiursa, Furret, Raticate, Linoone.

## Belangrijkste vondst: we vergeleken met de verkeerde bestanden
In deze repo staat `P_GBA_STYLE_SPECIES_GFX FALSE` (`include/config/pokemon.h`): `graphics/pokemon/<naam>/anim_front.png` + `normal.pal` zijn voor Gen 1–3-soorten de **Gen 4/5-stijl** sprites van de expansion. De echte Ruby/Sapphire/Emerald-sprite is **`anim_front_gba.png` + `normal_gba.pal`**. Alle eerdere keuringen (o.a. `keuring_r15`, `laad.py`) gebruikten `anim_front.png`, dus feitelijk Gen 4/5. Vel: `vergelijk.png` (r16 | Kangaskhan Gen 3 | Kangaskhan expansion-standaard).

## Kangaskhan (Gen 3) tegen onze r16, per onderdeel
| | Kangaskhan Gen 3 | Onze r16 |
|---|---|---|
| (a) buitenlijn | 1 px; zwart (16,16,16) onder en rechts, diep olijfbruin (82,65,16) boven/links; nergens een lichte tint op de rand | zelfde opbouw (zwart K rechts/onder, b links/boven). Geen verschil van betekenis |
| (b) binnenlijnen | lang en doorlopend in de donkerste eigen tint; elke vorm-over-vorm (arm, dij, buikrand) heeft een lijn, met de schaduwtint ernaast | korte losse b-stukjes; enkele gaten (dijlijn rechts (38,51)); broekrand linksonder zonder lijn |
| (c) schaduw | per vlak 3 tinten + lijn; schaduw D (156,123,65) is de grootste tint (435 px) en ligt als band langs de lijnen; buik: 2 tinten, lichte tint domineert, gouden schaduw als sikkel rechts/onder | broek/bruin-grens gaat via **mengtinten**: een band D (176,138,96) in het kruis en losse d-pixels tussen broekschaduw S en de bruine schaduw onder de arm; daardoor geen harde grens, leest zacht/"geblurd" |
| (d) palet bruin | tint bijna constant (h 38–44), licht iets geler en **minder** verzadigd (s 38), verzadiging loopt op naar donker (43→58→80); lijnkleur diep en verzadigd | rood-oranje bruin (h 31→22, schaduw schuift naar rood); hooglicht f is juist verzadigd/perzik (s 49); lijnkleur b iets grauw |
| (d) palet crème/buik | warm geel: (255,255,148) / schaduw (238,205,106), s 41–55; Teddiursa (255,246,164)/(255,213,123)/(213,172,82); Furret (255,238,148)/(230,197,74) | grijsbeige: (248,232,200)/(228,204,166)/(208,176,136), s 19–34; schaduw is grauw, niet goudkleurig |
| (e) lijnfragmentjes | weinig losse pixels; lijnen zijn lijnen, vlekken zijn tintvlakken | kraag vol kleine b-lusjes (bevroren bollen, laten staan); in het lijf enkele losse stukjes |

Contrast (L-stappen) is géén verschil: Kangaskhan 25/38 (+62 naar lijn), Ursaring 31/32/35, ons 37/37/36.

## Conclusie voor r17
1. Palet in Gen 3-opbouw: bruin met bijna vaste tint, licht geler en minder verzadigd, donker verzadigder; crème warm met gouden schaduw.
2. Mengbanden tussen crème en bruin weg: crème stoot hard op bruine schaduw (zoals bovenkant Kangaskhan-buik).
3. Gaten in binnenlijnen dicht, broekrand linksonder met donkere eigen tint (model heeft daar een lijn).
Niet gedaan (vorm/bevroren): extra binnenlijnen à la Kangaskhan-spieren tekenen, kraag/kop/klep/potlood/staart/gezicht aanpassen.

Scripts: `studie.py` (vel + paletladders).

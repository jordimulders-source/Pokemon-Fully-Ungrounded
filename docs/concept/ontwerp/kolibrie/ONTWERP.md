# Kolibrie (Ghost/Flying), eindvorm: schets v1 (24 okt)

Naar Jordi's posetekening + foto's (velvet-purple kroonkolibrie, langstaartsylfe, racketstaartkolibrie). Script: `../scripts/kolibrie.py`. Grove modeltekening om te checken of het idee klopt, geen pixelsprite.

- **Pose:** duikt schuin naar linksonder (drinkt nectar), twee bladvormige vleugels als V omhoog (nabije groter, naar links gekanteld), staart waaiert naar rechtsonder.
- **Palet (fluweel):** zwarte kop, violet lijf met schubbenglans, blauwgroene schouderglans, oranje vlekje op de vleugel, bleek lavendel als 'zielenlicht'.
- **Staart:** korte waaier (franje) + twee lange slierten met racketpunten (racketstaartkolibrie) als bleke **zielvlammetjes**: de zielen die hij begeleidt.
- **Kuif:** drie korte veertjes met bleke punt, naar de ***jeguaka*** (de verentooi van de Mbyá-Guaraní-rituelen). Mythe: Guaraní ***mainumby*** voedt de schepper Ñamandu en begeleidt zielen; positief, geen eng spook.
- **Oog:** groot en rond met een bleke gloeiring (mystiek, vriendelijk).
- Open: vleugels lichter/doorschijnender? Kuif als jeguaka of anders? Hoeveel slierten?

## Schets v2 (24 okt, Jordi's feedback op v1)
- Vleugels nu echte kolibrievleugels: lang, sikkelvormig, rechte voorrand, puntig; vanaf het midden naar buiten geleidelijk doorzichtiger (tot ±85%).
- Oog veel kleiner (klein zwart oog met een dun bleek randje).
- Derde staartsliert erbij (drie racketslierten met zielvlammetjes + franjewaaier).
- **Kuif als jeguaka: goedgekeurd** (Jordi, 24 okt).

## Schets v3 (24 okt): vleugelvorm
- Jordi: vleugels lezen nog niet als kolibrie. Nu: breed bij de schouder, lange smalle punt, rechte voorrand, holle achterrand, pennen in de lengte (naar foto 3).
- Transparantie: dekkend tot het midden, dan lineair tot ±90% doorzichtig aan de punt. Vel op een groene achtergrond zodat dat zichtbaar is.

## Schets v4 (24 okt): vleugels naar Jordi's vleugelfoto's
- Referenties: `docs/concept/sprites/kolibrie/referenties/jordi_vleugel_*.webp` + `jordi_pose_schets.png`.
- Vleugel = korte arm + waaier van 7–8 lange, smalle slagpennen met ronde punt, trapsgewijs over elkaar (voorste het langst), geschubde dekveren in lijfkleur aan de basis (zoals de illustratie). Transparantie ongewijzigd (vanaf het midden, tot ±90%).

## Schets v5 (24 okt): gewone vleugel
- Jordi: geen waaier, een normale vleugel; v4 was te klein en de vorm klopte niet. Nu één groot lemmet (±1:2,7): smalle wortel aan de schouder, breedst rond het midden, licht bolle voorrand, punt iets naar voren; lichtere schouder (dekveren) en drie pennenlijnen in de lengte. Groter (nabije vleugel ±55% van de boxhoogte). Transparantie ongewijzigd.

## Schets v6 (24 okt): vleugelvorm naar Jordi's close-up
- Referentie: `docs/concept/sprites/kolibrie/referenties/jordi_vleugel_closeup.png`. Lange driehoek/sikkel: breedst aan de schouder, rechte voorrand naar een scherpe punt, rechte achterrand met kleine zaagtandjes (de punten van de slagpennen, strak parallel, geen waaier), pennenlijnen parallel aan de voorrand, smalle dekverenrand in lijfkleur.
- Hele figuur 84% en lager in de box gezet zodat de grotere vleugels passen (`KCanvas` in het script). Oranje vlekje vervallen.

## Schets v7 (24 okt): opnieuw opgebouwd
- Jordi over v6: vleugels zitten niet goed op het lijf, oog zweeft, staarten niet af en los van het lijf, doorzichtigheid niet zichtbaar ("prutswerk").
- Nu: lijf als één druppelvorm (borst linksonder, achterlijf rechtsboven); kop rond en direct op de borst, oog midden in de kop; beide vleugels groeien uit de rug (nabije vleugel achter een geschubde rand dekveren die met het lijf versmelt); staart = franje + drie slierten die uit het achterlijf komen en eindigen in een druppelvormig zielvlammetje.
- Glasvleugel: alleen de vulling wordt doorzichtig (vanaf het midden tot ±90%), omlijning en pennen blijven staan; bokeh-achtergrond zodat je erdoorheen kijkt.

## Schets v8 (24 okt): 3/4-pose
- Jordi over v7: "veel beter"; verre vleugel en achterkant lijf klopten nog niet; pose meer 3/4 zoals Zapdos/Moltres (`referenties/jordi_pose_zapdos.png`, `jordi_pose_moltres.png`).
- Nu: compact eivormig lijf met de borst naar de kijker (lichtere borst met schubben, blauwgroene schouder), kop groter linksonder op de voorgrond, nabije vleugel uit de linkerschouder naar linksboven, verre vleugel achter het lijf vandaan naar rechtsboven, staart (franje + drie slierten) steekt achter het lijf uit naar rechtsonder.

## Stap 2: silhouet op een echt skelet (24 okt)
- Jordi: modeltekeningen liepen vast (horizontaal, vleugels fout; "Pokémon designen is geen cirkels-en-driehoekenwerk"). Gekozen onderdelen uit `referenties/skelet_kandidaten.png`: **vleugels Talonflame**, vleugeleffect (doorzichtig) **Venomoth**, staartdynamiek **Articuno**, kop **Ho-Oh of Fearow**.
- `docs/concept/sprites/kolibrie/silhouet/silhouet.py` → `silhouet_v1.png`: Talonflame als skelet (pose + vleugels), haviksnavel → lange dunne snavel, poten weg (ronde buik), Talonflame-staart → franje + drie slierten met Articuno-krul en racketpunt. De jeguaka valt in het silhouet binnen de nabije vleugel.

### Verhoudingen silhouet vs. foto's (24 okt; maat = lijflengte B, keel tot staartwortel; foto's geschat uit pixelcoördinaten)
| | foto's (illustratie, blauwe sabelvleugel, Costa, fluweel) | silhouet v1 (B = 25 px) |
|---|---|---|
| kop | 0,30–0,40 B | 0,46 B (Pokémon-kop mag groter) |
| snavel | 0,35 (fluweel) – 0,75 B | 0,79 B |
| vleugel | 1,3–1,9 B | nabij 1,2 B (verkort), ver 1,6 B |
| lijfdiepte | 0,40–0,50 B | 0,80 B → v2 ±0,6 B |
| staart (zonder slierten) | 0,5–1,0 B | franje 0,3 B + slierten ±1,2 B |
- v2: buik slanker gemaakt (Talonflame-borst was te diep); rest ongewijzigd.
- v3 (Jordi: kop/kuif te veel Talonflame; vleugel zit niet aan het lijf vast, zie `referenties/jordi_vleugelaanzet.png`): Talonflame-kop weg → ronde kolibriekop op een korte nek + jeguaka als kleine waaier van drie veertjes; nabije vleugel onderaan weggesneden zodat de wortel smal aan de schouder zit en er lucht tussen vleugel en kop is; verre vleugel 4 px naar de schouder geschoven, rug dichtgemaakt.
- v4 (`silhouet/silhouet_v4.py`; Jordi's correctie op v3 `referenties/jordi_silhouet_v3_correctie.png` + leidraadfoto `referenties/jordi_leidraad_kop_vleugels.webp`): kop als 'bovenhoofd' dat in de nek doorloopt, snavel uit de voorpunt; vleugels 85% en met een brede, rechte aanzet op de rug (nabije vleugel: rechte onderrand tot op de schouder; verre vleugel: rechte achterrand tot op het achterlijf, geen gat); lijf één gladde torpedo. Losse snippers worden automatisch verwijderd.
- v5 (`silhouet_v5.py`): silhouet automatisch uit de anatomiefoto (`referenties/jordi_anatomie_mango.png`) gesneden en gedraaid; pose bleek niet te passen (lijf horizontaal of snavel verkeerd), niet verstuurd.
- **v6** (`silhouet_v6.py`): Jordi's foto van een drinkende kolibrie (kop links, snavel schuin omlaag, vleugels als V, staart rechts) is de pose. De foto stond niet als bestand in de sessie; omtrek punt voor punt overgenomen in fotocoördinaten. Links de zuivere foto-omtrek, rechts met jeguaka (veertjes langs de kruin naar achteren; omhoog las als oren) en eigen staart. Verre vleugel 25 fotopx breder en snavel min. 2 px, anders breken ze op 64.

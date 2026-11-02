# Nachtaap fase 2 (Psychic-starter, middenvorm): SPEC

Werkwijze: `docs/lessen/SPRITE_WERKWIJZE.md` (kolibrie + olinguito v2). Opdrachten aan agents altijd met `SPRITE_NORM.md` + `SPRITE_OPDRACHT.md` + deze SPEC.

## Lijn (uit `docs/concept/POKEMON.md`)
- Tarsier-achtige baby → **nachtaap** (*Aotus*, de enige nachtactieve aap) → muriqui met de grote ogen van de eerdere fasen, met healer-outfit (kallawaya/yatiri) en subtiel zilveren maanmotief.
- **Lijkt gevaarlijk, maar is zachtaardig en een healer.** De Nazca-spiraalstaart groeit per fase: krulletje → **spiraal (deze fase)** → volle Nazca-spiraal.
- Type: Psychic (eindvorm mogelijk Psychic/Fairy). Nog niet in de repo; geen data in deze stap.

## Wat uit fase 1 meekomt (herkenbaar dezelfde lijn)
Fase 1 = `referenties/fase1_goedgekeurd.png` (ronde 12, variant spiraal, 950 px). Jordi koos concept **B** (dieper violet, bleke gezichtsschijf).
- Violette vacht, crème gezichtsschijf met de donkere middenstreep (wig) op het voorhoofd.
- Grote ogen (roze/magenta iris met glans): "de ogen zijn het belangrijkst" (Jordi). Bij een middenvorm relatief kleiner dan bij de baby, maar nog steeds groot.
- Kleine ronde oren, crème vinger-/teenkussens.
- Spiraalstaart, nu groter (meer dan één slag).

## Ontwerprichting (voorstel Claude, nog niet besloten)
- **Bouw van de echte nachtaap:** slanker en langer dan fase 1, langere armen en benen, ronde kop op een korte nek; het lijf wordt "aap", niet meer "tarsierbolletje". Formaat fase 2 ≈ 1,5–1,7× fase 1 → ±1400–1600 px (Vigoroth 1480, Monferno 1121, Kadabra 1642).
- **Niet op Aipom/Ambipom lijken** (ook paarse apen): het verschil zit in het nachtaapmasker (witte halvemanen boven de ogen, donkere strepen), de grote ogen, de slanke bouw en de spiraal (geen hand aan de staart).
- **Psychic uit de anatomie** (ogen, voorhoofd, spiraal, houding), geen spullen; eventueel één kleine hint naar de healer-outfit van fase 3 (zoals de alpaca een aguayo-band kreeg). Open vraag aan Jordi.

## Skelet-kandidaten
`referenties/skelet_kandidaten.png`: fase 1 naast Aipom, Monferno, Kadabra, Kirlia, Vigoroth, Grovyle, Medicham, Lombre, Grumpig, Primeape (3× en 1×, met oppervlak). De vorm zelf komt van een foto van een echte nachtaap in de gekozen pose (stap 1), niet van deze sprites; ze dienen voor formaat en bouwtype.

## Jordi's woorden (letterlijk)
- 2 nov: "Ik wil richting 1 en 2: nachtwaker met maangezicht. Hier wat inspiratie fotos, zon typisch hangende pose met ogen relatief recht in de camera kijkend (check welke andere sprites dat ook doen) zie ik zitten. Het lichaam wordt nu naar verhouding wat groter tov het hoofd"
- Gekozen richting: **nachtwaker** (echte *Aotus*-bouw, gehurkt/hangend, starende blik) **met maangezicht** (bleke schijf als maan, witte vlekken boven de ogen als sikkels). Lijf naar verhouding groter t.o.v. de kop dan in fase 1.
- Foto's: `referenties/foto1_tak_hangend.jpg` (hoofdkandidaat voor de pose: gehurkt over een schuine tak, lijf schuin achter de kop, ogen recht in de camera), `foto2_apenheul_jong_op_rug.jpg`, `foto3_etend.jpg`, `foto4_zittend_frontaal.jpg`. Overzicht: `referenties/vel_pose.png`.
- Sprites met een 3/4-lijf en een blik recht in de camera: `referenties/frontale_blik.png` (Zorua, Sableye, Slakoth, Mew, Espeon, Persian, Eevee, Pachirisu, Absol, Slowpoke, Delcatty, Quilava).
- 2 nov: "zoek wel een pose van een pokemon waar het rug een beetje boven het hoofd uitsteekt. Tak hoeft idd niet in beeld"
  → **geen tak**; rug steekt boven de kop uit. Kandidaten: `referenties/rug_boven_kop.png` (Sandslash, Dusknoir, Mamoswine, Piloswine, Camerupt, Lairon, Skuntank, Excadrill).
- 2 nov: "qua pose puur juist lairon, maar wel ander type pokemon" → **pose = Lairon** (laag gehurkt, kop laag vooraan, rug erachter hoger). "maar de manier waarop we werken is eerst 3d pose toch en daarna pas silhouet?" → ja: 3D-poppetje → hoek kiezen → silhouet. "gebruik de fotos echt als inspiratie ook" → massa en gezicht uit foto 1/4 (kleine ronde kop op een groot bol lijf, witte vlekken boven de ogen, donkere middenstreep en zijstrepen, donkere ring om het oog, lange vingers, hangende staart).
- 3D-poppetje: `pop3d/nachtaap3d.py` (renderer `pop3d/pop3d.py`, kopie van de olinguito); rasters `pop3d/hoeken.png` (staart omlaag) en `pop3d/hoeken_staart_omhoog.png`. Kleuren in het poppetje zijn alleen ter oriëntatie.
- 2 nov: "de voorpoten mogen nog iets meer teruggetrokken, verder mis ik het halve maan motief wat je voorstelde. De kleur mag imo iets donkerder dan van de eerste evo. Staart omhoog zie ik zitten (suggestie voor pose) Hoofdpose A2 is goed, al moeten we uiteraard de ogen nog anders vormgeven, plus een neutrale mond, maar dat was voor een latere fase toch"
  → **hoek A2 van het staart-omhoog-vel = lijf 40°, kop 80°** (Jordi: "nee dit hoofd is niet a2" toen Claude kop 65° nam; de vellen hadden dubbele labels, nu weggehaald), **staart omhoog**, voorpoten teruggetrokken, vacht donkerder dan fase 1, halve manen boven de ogen; ogen en neutrale mond in de kleurstap.
- 2 nov: "correct, we kunnen ook iets qua motief met het lichaam doen, want dat is nu wel erg effen" → pose lijf 40°/kop 80°/staart omhoog akkoord; lijfmotieven in `pop3d/motieven.png` (keuze open).
- 2 nov: "Nee dit is het niet helemaal. Ik wil de halve maan op het hoofd, met de uiteinden naar beneden wijzend. Is er iets van een patroon wat mysterieus is en zuid amerikaans, wat we redelijk netjes zouden kunnen uitwerken op het lijf? Het moet logisch zijn, zodat het gecentreerd is als je er van bovenop zou kijken"
  → één sikkel op het voorhoofd, punten omlaag; lijfpatroon gecentreerd op de ruggengraat: kené of chakana (`pop3d/motieven2.png`; keuze open). Afgekeurd: halve maan op de flank, sterren, maanfasen.
- 2 nov (met krabbel `referenties/jordi_krabbel_halvemaan.png`): "nee het enige witte op het hoofd moet de halve maan zijn, en die moet echt half het hoofd bedekken, zoals ik het heel slecht getekend heb hier, moet dus over de ogen heen vallen. Kené bevalt me wel, vertaalt dat goed naar een sprite denk je? Ik weet het nog niet zo met het borstvlak trouwens, vind ik er niet mooi uitzien"
  → kop: één grote witte halve maan (punten omlaag, over de ogen; daarna "de halve maan mag nog wat meer van het hoofd bedekken": groter); verder geen wit/licht vlak op de kop. **Lijf: kené.** Borstvlak afgekeurd.
- Over de lijn eerder: "in eerste instantie simpel houden: een aap met grote ogen, een genezer-concept en de Nazca-staart"; "de ogen zijn het belangrijkst; kijk naar Jigglypuff, Scream Tail en Espurr"; Psychic-concept: "niet ondersteboven hangen".

## Bevroren
- **3D-poppetje** (Jordi, 2 nov: "ja, maak er maar een silhouet van"): `pop3d/nachtaap3d.py` met `nachtaap(40, 'omhoog', 'kene', cam=(40, 8))`: lijf 40°, kop 80°, pitch 8, staart omhoog met spiraal, kené op de rug, één witte halve maan op de kop (bolkappen, punten omlaag, middenstuk tussen de ogen bolt in), geen borstvlak. Vel: `pop3d/kop_halvemaan.png`.

## Kleur (open, ronde 1)
- Jordi 2 nov over de ogen: "de ogen mogen meer rood dan fase 1, verder nog wat meer starend, maar buiten dat vergelijkbaar". Eerder: "we moeten uiteraard de ogen nog anders vormgeven, plus een neutrale mond".
- Vacht: "De kleur mag imo iets donkerder dan van de eerste evo" (poppetje: #5E4488, verre kant #45306A).
- Kop: "het enige witte op het hoofd moet de halve maan zijn" (zie bevroren poppetje). Lijf: kené in lichtlila, rustiger dan de maan. Geen borstvlak.

- Jordi 2 nov (na ronde 1): "het hoofd lijkt sowieso iets teveel op de 1e stage" + "incl ogen" → kop en ogen duidelijk anders dan fase 1: grote witte maan als kenmerk, ogen met kleinere iris, grote ronde pupil, donkere ring en starende blik (foto's), volwassener snoet.

## Silhouet
- Ronde 1 (2 nov): `silhouet/vel_silhouet.png`. Jordi: "er is een klein gat ontstaan tussen hoofd en lichaam in, verder prima" → nek-inham teruggedraaid.
- **Bevroren (2 nov):** `silhouet/silhouet_bevroren_1x.png` / `silhouet_bevroren.npy` (1459 px). Alpha-diff 0 in alle kleurrondes.

## Afgekeurd (niet herhalen)
- Fase 2 (2 nov): oranje borstvlak; bleke gezichtsschijf; twee kleine sikkels boven de ogen; halve maan op de flank; sterren; maanfasen.
- Uit fase 1 (`../FEEDBACK.md`): staart als overdreven rechte lijn; geen oren; geamputeerde verre arm/been; opgeplakte ogen of ogen die niet Psychic-gekleurd zijn; slaperige/verveelde blik; te cartoony; ondersteboven hangen.
- Modeltekeningen uit cirkels en driehoeken als bron van de vorm.

# Lama (alpaca-evolutie, Fighting-starter fase 2): SPEC

Werkwijze: `docs/lessen/SPRITE_WERKWIJZE.md` (verplicht; **Coathief is het voorbeeld**: Claude maakt de bron klaar, één maker-agent tekent met de hand, Claude controleert tegen de bron, een keurder keurt, dan pas Jordi). Basis en stijl: de goedgekeurde alpaca (fase 1), `../alpaca/ronde17/variant_kop/anim_front.png`; kopie in `referenties/fase1_alpaca.png` (+ `_4x`).

## Gegeven
- **Lijn** (POKEMON.md, besloten): alpaca → **lama** (groter, sterker; stamt af van de guanaco, lastdier van de Andes) → lama met **bombín** (cholita-luchadora). Lamoïden-lijn, geen vertakking.
- **Type:** Fighting (lijn); de soort staat nog niet in de repo, data volgt in een aparte taak.
- **Naam:** open.
- **Formaat fase 2:** 1100–1550 px, box ±47–53, kop ±30–35% van de hoogte (FAKEMON_CHECKLIST D1/D2). Fase 1 = 1019 px (box 37×53, kop 40%). Bouwtype: grote viervoeter (skelet Mightyena, Luxray, Arcanine, Liepard, Mudsdale).
- **Fase 1 (goedgekeurd), wat meegaat:** crème wol, lange hals, bijna zwarte ogen, rechte puntige oren met rode/roze oorkwastjes, korte snuit met splitlip, rode bokshandschoenen met een aguayo-band (veelkleurig) als manchet, aguayo-halsbandje.

## Jordi's woorden (letterlijk, eerder)
- (POKEMON.md / FEEDBACK) "vanaf fase 2 worden de handschoenen **wolkragen om de poten**"; "fase 3 mag meer bekleed zijn".
- (FEEDBACK) "moet **op 4 poten blijven staan**"; "niet te veel Hitmonchan".
- (FEEDBACK) "Alpaca-lijn: mag ook verwijzingen naar vechtsporten maken, niet per se Zuid-Amerikaans"; "Capoeira is voor de regionale Hitmontop"; fase 2 wordt "een andere vechtsport" (POKEMON.md).
- (FEEDBACK ronde 9) "de alpaca is geen alpaca, het is meer een schaap" → lange nek, vrijwel zwarte ogen, wollige kruin, duidelijke snuit met splitlip, rechte puntige oren.
- (SPRITE_OPDRACHT) kameelachtigen lopen echt in telgang; bij de alpaca bewust zo gehouden (24 okt).
- (Ontwerp, geen besluit) eindvormen niet steeds mensachtiger (Jordi bij de wasbeer, 2 nov); fase 3 variant A (vier poten) had de voorkeur.

## Jordi's woorden (2 nov, stap 1, letterlijk)
- "Ik maak een andere BJJ pokemon later. Het lijkt me leuk om een ontwikkeling in de traditionele Andes kleding die de llama draagt ook te doen. Qua vechtsport weet ik het nog niet, we kunnen er ook gewoon MMA handschoenen van maken. Qua kleur gaan we echt meer de lama kant op, maar de 3e vorm moet wel echt duidelijk anders en volwassener zijn nog dan de 2e vorm"

## Jordi's woorden (2 nov, bij foto's 1–5, letterlijk)
- "dit is een vrij goede angle, de eerste foto, de kleding lijn is goed, maar moet het vooral ook in design zien. Deze llama is nog niet helemaal volgroeid, maar wel duidelijk al een evolutie, marshtomp, charmeleon, monferno, prinplup idee. Begin nu toch te twijfelen of we evo 3 geen guanaco moeten maken. Kan je al iets met deze fotos? Vacht is goed om iets donkerder te maken dan de alpaca. Handschoen foto zit er ook bij"

## Besloten (2 nov)
- **Pose/hoek: foto 1** (`referenties/foto1_lama_driekwart_POSE.png`): staand, lijf driekwart naar links-voor, kop naar de kijker, staart omhoog, dikke vacht.
- **Fase 2 = tussenvorm:** nog niet volgroeid, maar duidelijk een evolutie (Marshtomp, Charmeleon, Monferno, Prinplup).
- **Kledinglijn goed** (voorstel hieronder); moet in het ontwerp zichtbaar worden.
- **Vacht iets donkerder dan de alpaca.** **Handschoen: MMA** (`referenties/foto5_mma_handschoenen.png`: kort, open vingers, polsband).
- Geen BJJ (wordt een losse fakemon).
- **Kledinglijn:** de lama draagt traditionele Andes-kleding, die per fase verder ontwikkelt (fase 1: aguayo-halsband en -manchetten, oorkwastjes → fase 2: meer → fase 3: cholita, bombín).
- **Handschoenen:** voorlopig **MMA-handschoenen** (vechtsport verder open).
- **Kleur: echt de lama-kant op** (lamavacht, niet de crème alpacawol).
- **Fase 3 moet duidelijk anders en volwassener zijn dan fase 2** (dus fase 2 niet al te volwassen of te vol bekleed maken; ruimte laten voor de stap naar fase 3).

## Referenties (`referenties/`)
- `fase1_alpaca.png` / `_4x.png`: de goedgekeurde fase 1.
- `schets_fase2_wolkraag_23okt.png`: oude modeltekening fase 2 (praatplaat, geen bron).
- `referentie_alpaca.webp`: alpacafoto die Jordi bij ronde 9 gaf.
- `foto1_lama_driekwart_POSE.png`: **de pose** (Jordi). `foto2_jonge_lama_frontaal.webp`: jonge lama (tussenvorm-gevoel). `foto3_kudde_oorkwasten_aguayo.webp`: rode oorkwasten, aguayo op de rug. `foto4_bont_bruin_wit.webp`: bonte vacht. `foto5_mma_handschoenen.png`: MMA-handschoenen.

## Lama vs. alpaca (voor herkenbaarheid)
- Lama: groter, langere kop en snuit, **banaanvormige oren** (gebogen naar binnen), minder wol op kop en poten, rug recht, staart hoger; vaak bont (bruin/wit, zwart).
- Alpaca: kleiner, korte snuit, korte rechte oren, wolkruin.
- Andeslama's dragen **oorkwastjes** (gekleurde wol in de oren): sluit aan op fase 1.

## Open (stap 1, met Jordi)
- Verhouding A/B/C en vacht op `ontwerp/vel_ronde1.png`.
- Fase 3: lama of guanaco (Jordi twijfelt, 2 nov).
- Naam.

## Ontwerp (stap 1)
- 3D-poppetje `ontwerp/pop3d_lama.py` in de hoek van foto 1 (lijf 40°, kop +24°), met kleding: rode oorkwasten, pomponsnoer, aguayo over de rug, rode MMA-handschoenen met zwarte polsband en de twee teennagels eruit. Praatplaat + bron voor het silhouet (maker-agent), geen sprite.
- `ontwerp/vel_ronde1.png`: rij 1 verhoudingen A (kop 29%, lange hals) / B (34%) / C (39%, kortere hals), rij 2 vacht (licht karamel / karamel / bont) op B.

## Voorstel kledinglijn (Claude, 2 nov, nog niet goedgekeurd)
Echte lamatooi uit de Andes: bij de *señalakuy*/*t'ikachay* (merkfeest) krijgen lama's gekleurde wolkwasten in de oren en wollen pompons/linten; als lastdier dragen ze een geweven lap (aguayo/costal) op de rug.
- Fase 1 (alpaca): aguayo-halsband, aguayo-manchetten aan de bokshandschoenen, oorkwastjes.
- Fase 2 (lama): grotere oorkwasten, een pompon-halssnoer, een **aguayo-lap over de rug** (lastdier); **MMA-handschoenen** (open, kort, de twee teen-nagels steken eruit zoals vingers) met aguayo-band als pols.
- Fase 3 (cholita): bombín, vlechten, manta, pollera; volwassen bouw.

## Bevroren
- (nog niets)

## Afgekeurd (niet herhalen)
- (nog niets voor fase 2; voor de lijn zie FEEDBACK.md: schaap-look, gesmolten vormen, niet-Gen 3-ogen/handschoenen)

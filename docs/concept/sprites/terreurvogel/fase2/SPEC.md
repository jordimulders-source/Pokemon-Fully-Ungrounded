# Terreurvogel-lijn – SPEC

Regionaal fossiel, **Rock/Fighting**, 2 fases. Tegenhanger van de glyptodon (Rock/Normal, wall). Achtergrond: `docs/concept/IDEEEN.md` → "Regionale fossielen".

## Jordi letterlijk (27 nov)
- "rock/fighting akkoord"
- "wordt dan een physical sweeper, snel, maar wel met die kenmerkende grote snavel"

- "hij hoeft niet per se van steen, je kan kijken hoe de archeops lijn dat bijv doet, die komt goed als een fossiel over"
- "De 2e fase moet echt in sprint zijn, enorme snavel"

## Feiten (Claude)
- Archen/Archeops in de repo: Rock/Flying; fossiel zit niet in steen maar in oertrekjes (klauwen aan de vleugels, lange benige staart, geschubde poten, felle "reconstructie"-kleuren); Archen kan nog niet vliegen, Archeops wel.
- De seriema (*Cariama*, Zuid-Amerika) is de nauwste levende verwant van de terreurvogels; *Psilopterus* was een kleine terreurvogel van ±70–80 cm.
- *Phorusrhacos* = bekendste naam; *Kelenken* = grootste schedel/snavel. Vliegloze loopvogels van 2–3 m: hoge haaksnavel als een bijl, kleine vleugels, lange sterke loopbenen, grote klauw.

## Model (27 nov)
`gemini/r7.png` (Gemini r6 + oog-bewerking r7). Jordi: "ok in de sprite zorgen dat het oog naar voren kijkt, we gaan het anders dan normaal doen, ik ben nog niet helemaal tevreden met de kleuren van het lichaam en de snavel, dus bouw maar de sprite en toon dan een paar pallette swaps. De snavel vind ik nog niet fossiel genoeg en het lichaam niet dreigend genoeg qua kleur, de pose prima nu".
- Eerder over het model: snavel geel, gezicht roze, lijf "roodbruin achtig" (r3); kop voorovergebogen, mond licht open, dreigend (r5).

## Model gekozen (Jordi, 27 nov): `gemini/r1_eenvoud.png`
- r1 met bijlsnavel, minder detail; verhouding ±64×40 zoals Lapras (64×39). Jordi: "we gaan deze doen" (na Claudes advies om r7 te houden). r7-sprite gestopt ("stop de eerdere maker maar"); tussenbestanden in `sprite_r1/`.
- **Jordi (27 nov):** "met wat kanttekeningen, de snavel is van staal, dat moet een soort stone axe worden" / "anders klopt het type niet meer". Uitvoering: snavelvorm uit het model, kleuren steen i.p.v. staal; facetten/barsten alleen als voorstel.
- **Jordi (27 nov):** "de vlekken en details in het lichaam zijn geen vereiste, daar mag je mee spelen zolang het maar netjes eruit ziet, ik wil wel de kleuren terug zien komen want het zijn mooie roestkleuren".
- **Jordi (27 nov):** "het silhouet is wel heel belangrijk" (silhouet = modelomtrek, bevroren).
- **Jordi (27 nov):** "en probeer het oog wat meer driekwart te laten richten ipv volledig naar links, als het oog dan groter moet worden dan moet dat maar" → 2–3 ogen 1-op-1 uit Gen 3-vogels als varianten.
- **Jordi (27 nov) over r2:** "spearow is goed, beide poten zijn nog effen vakken niet mooi detail" (oog = `sprite_bijl_r2/oog_B.png`).
- **Jordi (27 nov):** "en schaduw, silhouet, kleurtinten zijn nog zeker niet goed over de hele sprite heen" / "silhouet wel excuses" (silhouet is goed).

## Open
- Fase 1 (Jordi, 27 nov): "een kuiken met een enorme kop en snavel lijkt me wel humor, die dan heel uncanny cute is en heel onhandig erbij zit". Prompt: `../fase1/gemini/PROMPTS.md`.
- **Optie snavel (Jordi, 27 nov, over `gemini/r1.png`, grijze bijlvormige snavel):** "dit was stiekem ook wel een tof idee voor de snavel, houd dat als optie in gedachten".
- Snavelmaat (Jordi, 27 nov, met `referenties/jordi_foto1_kelenken_zittend.png`): "al is de snavel weer wat klein vergeleken met deze" / "misschien kan je dat ook uitproberen" → varianten ×1,25 en ×1,5 in de sprite.
- **Kleur gekozen (Jordi, 27 nov): "v8 vind ik tof"** (`swaps_r1/v8.png`: snavel steen warm grijsbruin, lijf antraciet, roest en poten uit het model).

# Pachamama (opper-legendary, Ground/Fairy)

## Jordi letterlijk
- 8 nov: Ground/Fairy "ook een goede ja".
- 27 nov, op Claudes voorstellen A (berg-moeder, *Virgen del Cerro*), B (viervoeter met akkers), C (moederfiguur), 2 (trio erin), offers, kleuren: "A en 2 zijn tof, maar is dat te doen in een 64x64 sprite?"; "B is ook mogelijk, maar je wil erg veel merk ik in een kleine sprite stoppen. Offers kan gewoon niet."; "Een abstracte vorm van moeder aarde vind ik wel tof, zolang het maar levend is, want elke pokemon is levend en heeft ogen".
- 27 nov: gekozen richting **1** ("1"): Claudes voorstel "de berg die leeft: berg-mantelvorm, gezicht in de top met grote ogen, eventueel sneeuw als haar/kap, twee armen als bergkammen die naar voren komen".

## Open
- Ogen open of dicht/slapend (gevraagd, nog geen antwoord) → prompt heeft variant A/B.
- Kleuren, naam, rol.
- Trio niet in het ontwerp (Claude advies "te veel"; Jordi niet expliciet besloten).

## Eigen invulling Claude in prompt r1 (schrappen als Jordi het niet wil)
- Sneeuw als kap ("eventueel" in het voorstel), aardetinten van een berg, "gentle/ancient" als uitstraling.

## Rondes
- **r1** (`gemini/r1.png`, prompt r1 met ogen A), Jordi (27 nov): "oke oke, conceptueel niet slecht, maar beetje bruinig in zijn geheel, plus teveel detail nog dnek ik?"
  - Daarna, op Claudes vragen (detail, gezicht menselijk?, kleur a groen / b Vinicunca / c blauwgrijs+roze): "mag ook denk iets abstracter, alsof het meer een beeld is of verafgoding dan echt een mens"; "ja vinicunca!" → prompt r2 (`gemini/PROMPT_r2.md`). Eigen invulling Claude in r2: "3–4 brede banden", sneeuwkap behouden, kleurnamen van de echte Vinicunca.
- **r2** (`gemini/r2.png`), Jordi (27 nov): "lijkt nu een pop met een jas aan". Analyse Claude: berg-zijn verloren door "no rock texture/cracks" (ronde zachte vorm, flipperarmen, masker opgeplakt). Prompt r3 (`gemini/PROMPT_r3.md`): bergvorm van r1 terug (hoekig, rotsige kammen als armen, piek) met eenvoud en kleuren van r2; eigen invulling Claude: "facetten", "gezicht uit de rots gehouwen".
- **r3** (`gemini/r3.png`), Jordi (27 nov): "te lelijk gezicht en nu is het meer een soort golem". Analyse Claude: Gemini slingert (r1 te veel detail, r2 pop, r3 golem met vuisten en realistisch bebaard gezicht); r1 had de beste vorm. Prompt r4 (geschreven, vervallen vóór gebruik).
- Jordi (27 nov), over r1: "dit werkte veel beter, alleen de kleuren waren niet mooi". → Prompt r4 (`gemini/PROMPT_r4.md`): r1 als bijlage in een nieuw gesprek, alleen omkleuren naar Vinicunca ("ja vinicunca!"), vorm en details ongewijzigd.
- **r4** (`gemini/r4.webp`, r1 omgekleurd), Jordi (27 nov): "vertaalt dit naar een sprite? Deze is al beter, alleen het gezicht bij de vorige was qua kleur beter en een sneeuwkap ipv een hele sneeuwmuts was ook beter"; "het is niet erg als het detail minder wordt". Claude: hoofd (gezicht + kap) van r1 op r4 geplakt, pixelgelijk → `gemini/r4_met_kop_r1.png`. Jordi stuurde nog 2 varianten "voor het vergelijken" (r4b: rood/groen/oker met gekleurd gezicht; r4c: r1-hoofd, horizontale banden rood → roze → oker → turquoise van boven naar onder); die stonden niet op schijf, dus niet opgeslagen.
- **r4c** (`gemini/r4c.webp`; Jordi's tweede vergelijkingsplaatje), Jordi (27 nov): "is deze niet het beste dan?" (Claude was het eens; de samenstelling `r4_met_kop_r1.png` vervalt). **Bevroren model: `referenties/gemini_gekozen_r4c.png`** (r1-hoofd met sneeuwkap, horizontale banden rood → roze → oker → turquoise). Detail mag minder worden ("het is niet erg als het detail minder wordt").

## Sprite
- Legendary: volle maat (vult 64×64 zoals Gen 3-legendaries). Maker volgens SPRITE_WERKWIJZE "Gemini-model namaken"; rondes in `sprite/`.
- **Sprite r1** (`sprite/r1/`, maker; exacte 3×3-reductie van het natieve raster 199×199, figuur 60×54, 15 kleuren; 315/1851 pixels technisch aangepast, verslag in de rondes). Claude: silhouet, banden en armen goed; gezicht gevlekt (modellijnen vallen uiteen), oog 3 px zonder lichte iris, sneeuwkap gespikkeld grijs/wit.
- **Sprite r2** (`sprite/r2/`): kap per pixel opnieuw gemeten (dambord weg; grijze sneeuwschaduw rechts van de top), gezicht = modellijnen (≥4 modelpixels) + vlakken per gemeten tint; 78 px gewijzigd, rest diff 0. Open voor Jordi: oog (model, 3 px, iris valt samen met pupil) of Gen 3-oog; gezichtslijnen allemaal of alleen neusrug + wanglijn.
- Jordi over r2 (27 nov): "het gezicht is echt vreselijk"; "doe even beter het model namaken". **Sprite r3** (`sprite/r3/`, Claude per pixel tegen het model op 36×, `gezicht3.py`): oog 3×2 wit met iris-kolom (lid zwart erboven) waar het model het oog heeft, lichte neusrug + onderkant neus, één V van wanglijnen naar de kin, donkere zijkanten; vergelijking `sprite/r3/kop_r2_r3_model.png`.

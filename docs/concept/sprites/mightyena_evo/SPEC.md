# Mightyena-evolutie (Dark/Fighting)

## Jordi, letterlijk
- 9 nov: Mightyena-evolutie, "nog meer de hyena kant op" (een van zijn favoriete dieren, ook al leven hyena's niet in Zuid-Amerika).
- 22 nov: "laten we een mightyena evolutie ontwerpen".
- 22 nov: "ja het moet een duidelijke mightyena evolutie zijn, qua grootte en machtigheid, ik wil echt die typische hyena kop, misschien nog wel een beetje een pose met 1 poot alsof die geniepig aan het lachen is."
- 22 nov: "Dark/Fighting is wel een leuke buff en goede counterpart voor Obstagoon ook."
- 22 nov, over het voorstel "leider van de clan": "goed idee, dan wordt het een female only evolutie".

## Besloten
- Type **Dark/Fighting**.
- **Alleen vrouwtjes-Mightyena evolueren** (soort zelf 100 % vrouwtje); clanleider.
- Duidelijk een Mightyena-evolutie in grootte en machtigheid; typische hyenakop.
- Pose: "misschien" één poot, alsof hij geniepig lacht.

## Open
- Evolutiemethode/level, naam (grap *Almightyena* genoteerd). Poochyena-lijn moet terug in de dex.

## Voorstel Claude (niet van Jordi)
- Kleuren en tekening van Mightyena (zwart en grijs, rode ogen met geel oogwit) in de prompt, zodat het een herkenbare evolutie is; hyenakop = gevlekte hyena (breed, stomp, zware kaken, ronde oren, dikke nek, aflopende rug). Andere wens: aanpassen.

## Rondes
- Prompt r1: `gemini/PROMPT.md` (nieuw gesprek, geen bijlage).
- r1 (`gemini/r1.png`), Jordi: "prima eerste poging, maar de kop mag nog valser en meer hyena en de poot wat hoger voor die typische lach pose". Bijstuurprompt r2 (zelfde gesprek): `gemini/PROMPT_r2_bijsturen.md`.
- r2 (`gemini/r2.png`, kop hyena-achtiger, poot hoger), Jordi: "ik ben geen fan van de blik, hij lijkt nu meer evil dan echt geniepig". Ook: "en de mond is lelijk"; "verder is die perfect". Bijstuurprompt r3 (zelfde gesprek, alleen blik en mond): `gemini/PROMPT_r3_bijsturen.md`.
- r3 (`gemini/r3.png`), Jordi: "de mond wil ik graag open hebben". Bijstuurprompt r4: `gemini/PROMPT_r4_bijsturen.md`.
- r4 (`gemini/r4.png`, mond open), Jordi: "goed, maar het zijn wel kleine tanden, vertaalt dat naar een sprite? of zou je kunnen smokkelen door naar andere sprites te kijken". Claude: model is natief ±64 px (758 px breed → factor ±12); kale reductie `plak/r4_64_8x.png`, kop `plak/r4_kop_16x.png`: tanden vallen weg, bek ±5×4 px. Gen 3-Mightyena frame 2 (`plak/mightyena_koppen_12x.png`): bek open met witte hoektanden van 1×2 px, rode tong. Voorstel: in de sprite tanden van 1–2 px zoals Mightyena.

## Model gekozen (22 nov)
- **r4 gekozen**, Jordi: "yes ga maar los, de ogen zijn prima voor nu". Bevroren model: `referenties/gemini_gekozen_r4.png`.
- Toegestane afwijking: tanden in de open bek als witte hoektanden van 1–2 px zoals de Gen 3-Mightyena frame 2 (Jordi vroeg "of zou je kunnen smokkelen door naar andere sprites te kijken"; voorstel Claude, door Jordi met "ga maar los" aanvaard). Ogen: zoals het model ("prima voor nu").

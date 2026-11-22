# Lunatone-evolutie "bloedmaan" (werknaam open)

Lijn: Lunatone → deze evolutie. Tegenhanger van de Solrock-evolutie "corona" (`solrock_evo/`, branch fervent-hamilton). Type: Rock/Cosmic (Cosmic-besluit 21 nov). Evolutiemethode: open. Prompts en rondes: `gemini/PROMPT.md`, `r1/`–`r13/`.

## Model (bevroren)
`referenties/model.png` = Gemini v11 (`r11/gemini_v11.png`) met oog en neus van v5 (`r5/gemini_v5.png`) erop geplakt en de kleinste puinstukjes weg (`model/script/plak2.py`).

## Jordi letterlijk (22 nov)
- "hij is nu de brokkelende blood moon. Hij behoudt alleen oog en neus"
- "nu plak je hier de neus en oog op van lunatone die we al hadden, we halen wat puinstukken weg want dat is ruis en dan hebben we een model"
- "netter plakken"
- "ga maar met v11 verder, lunatone zelf is ook geen volledige driekwart sprite. v11 wordt je model, door het niet zo mooie knip en plak werk mag je ervan af werken, maar ga niet dingen opnieuw tekenen"
- Toegestane afwijking dus alleen: de plaknaden (rand rond het oog, overgang neus-lijf, resten van het oude oog en de oude neus van v11) mogen afwijken van het model, opgelost met wat het model zelf ernaast heeft. Niets hertekenen.

## Grootte
Eindvorm, zwevend: vult het 64×64-vak zoals het model (puin tot bijna de rand).

## Pose (23 nov)
- Jordi: "hij is mooi, maar wel volledig horizontaal"; Gemini v14/v15 mislukt ("dit is gedraaid, maar geen driekwart pose" · "nee dit is ook niet geslaagd").
- Jordi: "hij moet een x aantal graden draaien" / "naar rechts"; "lunatone is dus wel een driekwart sprite zie ik nu".
- r6 (oog naar links geschoven): "nee dit is niet gelukt, je draait hem de verkeerde kant op". Juist: gezicht schuift naar rechts (naar de voorkant), linkerrand van de bol komt achter de neus in beeld. r7 in de maak.

## Nieuw model (23 nov): Gemini v16
- Jordi over v16: "voor mijn gevoel is deze beter"; "alleen de rechterkant is niet meer rond" / "lijkt nu een opening te zitten"; bijsturen in Gemini (v17): "hij maakt het erger".
- Voorstel Claude, Jordi "akkoord": v16 wordt het model (`referenties/model_v16.png`); de rechterkant wordt rond gemaakt zonder tekenen: de ronde omtrek van boven/links/onder doortrekken naar rechts, bijgekomen strook vullen met de schaduwtinten die al rechts liggen. Gezicht, neus, barsten en puin zoals v16.
- Jordi: "en de brokkels mogen terug": de uitgebrokkelde stukken uit de rand worden overgenomen uit sprite r5 (zelfde gaten op dezelfde relatieve plek, pixels uit r5).
- Vorige kandidaat (model v11+v5): `sprite/r5/` blijft bewaard.

## Sprite v16 (23 nov)
- Jordi over het vel r2A | r3A | r3B | model: "r2a is wel de beste van dit lijstje" / "want daar lijkt die driekwart". De donkere rechterband van r2A blijft dus zoals hij is. r4 (vanaf r3B) gestopt.
- Jordi: "verder moet je over het hele lichaam slim met schaduw spelen voor het perspectief" / "ook rechts in het oog". v16_r5 vanaf r2A in de maak.
- Jordi over r5: "rechts in het oog moeten dus 2 donkerdere tinten komen dan de basis rode kleur om echt perspectief te tonen".
- Jordi over v16_r7: "de aansluiting neus op het lichaam mag iets netter nog, daarnaast mag je voor het oog nog net wat meer naar de al bestaande lunatone kijken, hij kijjkt namelijk iets teveel naar boven en lunatones oog is iets donkerder vanwege het perspectief, misschien dat die ook wat pixels naar rechts kan". r8 met oog op 0/2/4 px naar rechts als varianten.

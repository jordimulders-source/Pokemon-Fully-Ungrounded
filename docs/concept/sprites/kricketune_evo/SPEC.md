# Kricketune-evolutie (Bug/Fairy)

## Jordi, letterlijk
- (eerder, IDEEEN.md) "Kricketune-evolutie die echt een dirigent wordt."
- 22 nov: "Laten we met Kricketune aan de slag gaan"
- 22 nov: "die wordt bug/fairy"
- 22 nov: "hij moet ook een duidelijke 3e fase zijn"
- 22 nov: "groter en grootser dan kricketune"
- 22 nov, keuzes uit Claudes opties: arm wordt stokje; vleugels = rokpanden; pose armen omhoog.

## Besloten
- Type **Bug/Fairy** (Kricketune is in de repo puur Bug, Technician).
- Een dirigent.
- Duidelijk een 3e fase (Kricketot → Kricketune → deze), groter en grootser dan Kricketune; grootser = "als in een echte maestro, professioneel, die een zaal en orkest uitstekend beheerst", niet dikker/buffer.
- Stokje = één vinger die als stok én als wapen dient, zoals een krab één grotere klauw heeft (Jordi, 22 nov; vervangt "arm wordt stokje").
- De dekvleugels hangen als de slippen van een rokkostuum.
- Pose: midden in een maat, beide armen geheven.

## Voorstel Claude (niet van Jordi)
- In de prompt: kleuren, snor-antennes en krekelbouw van Kricketune, zodat het een herkenbare evolutie is.

## Open
- Fairy-kant in het uiterlijk, evolutiemethode/level, naam.

## Rondes
- Prompt r1: `gemini/PROMPT.md` (nieuw gesprek, geen bijlage).
- r1: `gemini/r1.png`. Claude: nog geen duidelijke 3e fase/niet grootser, los stokje, vleugels als cape i.p.v. rokpanden, frontaal, beentjes/onderlijf zakken weg. Jordi: "ja het stokje kan 1 vinger zijn die als stok fungeert en tevens als wapen, zoals een krab ook 1 grotere klauw kan hebben". Bijstuurprompt r2 (zelfde gesprek): `gemini/PROMPT_r2_bijsturen.md`.
- r2a (zelfde gesprek, `gemini/r2a_zelfde_gesprek.png`) en r2b (nieuw gesprek, `gemini/r2b_nieuw_gesprek.png`). Claude stelde r2a voor; Jordi: "ik vind 1 juist slecht, die is gewoon dikker/meer buff maar dat is niet per se fase 3". Verder vanaf r2b. Jordi: "grootser als in een echte maestro, professioneel, die een zaal en orkest uitstekend beheerst". Bijstuurprompt r3 (gesprek van r2b): `gemini/PROMPT_r3_bijsturen.md` (punten 2–4 uit r2 opnieuw). r3: Jordi "hij verandert niks, volledig nieuwe prompt" → `gemini/PROMPT_v2_nieuw.md` (nieuw gesprek). v2_r1 (`gemini/v2_r1.png`), Jordi: "nog niet helemaal top he". Jordi: "dan moeten we beter definieren hoe een maestro eruit ziet"; "uitstraling, kleding etc"; "indrukwekkende look". Claude stelde een maestro-definitie voor (uitstraling + white tie-kostuum in krekelonderdelen); Jordi: "ja het is vooral de outfit/het lichaam die wat meer moet hebben, het silhouet, kom maar met een prompt" → `gemini/PROMPT_v3_nieuw.md`.

## Model gekozen (22 nov)
- **v3_r1 gekozen** (`gemini/v3_r1.png`), Jordi: "ok dit is een model om mee te bouwen, want ik heb 2 issues en die kan je fixen, de ogen en de stok, die kan je gweoon van kleur veranderen zodat het een vinger is".
- Jordi: "en de kleding trouwens ook, is teveel kleding, maar die kan je in een sprite ook wat meer lichaamsvorm geven".
- Toegestane afwijkingen: (1) stok in de handkleur → vinger: gedaan in `model/v3_r1_vinger.png` (Claude, alleen kleur); (2) ogen: Jordi "het wijkt veel af van de kricketune insecten ogen" → Kricketune-ogen (bol in grijsbruin/donker met zwarte kern en witte glans, kleuren uit `graphics/pokemon/kricketune`) erin gezet: `model/v3_r1_vinger_ogen.png`, vergelijking `model/ogen_vergelijk.png` (Claude, voorstel); (3) kleding: in de sprite meer lichaamsvorm.

## Frontsprite
- Jordi: "ga maar bouwen dan kunnen we aan het einde het oog nog wat finetunen".
- r1 (maker, `sprite_r1/`): reductie 75×85 → 56×64 door schrappen; ogen uit Kricketune, vinger, kleding iets meer lichaamsvorm (+ variant zonder). Keurder loopt.
- Jordi op r1: "let op de positie van het linker oog", "die is niet natuurlijk", "naar de plek waar het oog in het model staat" (Claudes oogaanpassing in het model zette het te ver op de rand; plek = origineel `gemini/v3_r1.png`).
- Keurder r1: BIJNA (alleen ruis) → r3 (vest-onderrand, strik, losse pixels; kledingversie = basis).
- Jordi: "ja beide ogen zijn niet mooi, beetje uitgerekt" → oogstudie `sprite_r3/ogen_vel.png` (A Kricketune frame 2, B Kricketot, C Volbeat).
- Jordi: "A is het beste, alleen het rechteroog is aan de onderkant een beetje afgekapt, met schaduw en kleurtinten kan je dat fixen" → r4 = ogen_A + 4 px onderkant rechteroog ((32,17),(35,17) rood-schaduw 9; (33,17),(34,17) donker 2), Claude: `sprite_r4/`.
- Naam, Jordi: "Als naam kwamen Krickestra en Krickestro in me op".
- Jordi: "Krickestra klinkt wat beter, maar krickestro past beter. Doe maar stro voor nu." → werknaam **Krickestro**.

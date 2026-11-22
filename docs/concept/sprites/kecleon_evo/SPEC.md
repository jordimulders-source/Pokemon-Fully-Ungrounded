# Kecleon-evolutie (landleguaan, Grass/Fire)

## Jordi, letterlijk
- 9 nov: "dan hebben we bij deze onze Kecleon evolutie" (leguaan); evolueert zodra Kecleon op de Galápagos-locatie is (plaatsgebonden); Keccles evolueert ook daar. Welke leguaan en type: later.
- 22 nov: "kecleon evolutie" (start ontwerp).
- 22 nov, keuzes: leguaan = **landleguaan**; type = **Grass/Fire**; Fire zichtbaar via **kleur/huid** (warme schubben, geen echt vuur); pose **rechtop zoals Kecleon**; wat van Kecleon terugkomt (zigzagstreep, krulstaart, kegelogen, groen): **geen voorkeur**.

- 22 nov: "een van de andere kleuren wordt roze, hij staat een beetje voorover geleund, kecleon moet je herkennen aan wat design traits".

## Besloten
- Hoofdkleur geel en oranje, geen groen (22 nov); roze als een van de andere kleuren.
- Galápagos-landleguaan, Grass/Fire, rechtop op twee poten zoals Kecleon, Fire alleen in kleur/huid; een van de andere kleuren roze; een beetje voorover geleund; Kecleon herkenbaar aan wat design traits (welke: niet gezegd, aan Gemini gelaten).

## Open
- Naam, evolutiemethode (plaatsgebonden Galápagos, zie boven), welke Kecleon-kenmerken (Jordi: geen voorkeur; prompt laat het aan Gemini).

## Rondes
- Prompt r1: `gemini/PROMPT.md` (nieuw gesprek, geen bijlage).
- r1 (`gemini/r1.png`), Jordi: "leuk maar ik zie hier geen kecleon in terug, oog mond, de langere kuif en krulstaart mogen bewaard blijven"; "hij heeft ook iets teveel detail"; "of misschien gewoon de hele hoofdvorm moet vergelijkbaar zijn". Prompt r2 (nieuw gesprek, geen bijlage): `gemini/PROMPT_r2.md`.
- r2 (`gemini/r2.png`), Jordi: "de kleuren zijn echt gruwelijk lelijk, wat vind je van het model verder?"
- Voorstel Claude: kop + krulstaart van r2, zwaar landleguaanlijf van r1, grote rustige kleurvlakken. Jordi: "akkoord, geel en oranje als hoofdkleur, groen gaat weg". Prompt r3 (nieuw gesprek, geen bijlage): `gemini/PROMPT_r3.md`.
- Jordi: "ga maar bouwen". Claude bouwt het model zelf (geen nieuwe Gemini-ronde; `gemini/PROMPT_r3.md` niet gebruikt): natief raster 1024/10,24 (`model/natief.py`), kop (y<30 of x≤40) van r2 op het lijf van r1, krulstaart van r2 (x≥66, 2 px naar rechts) (`model/plak.py` → `combi_kop.png`); kleur (`model/kleur.py`): buik/kuif/oog/staart/klauwen geel, lijf oranje (lichtheid 3×3 gemedieerd voor rustige vlakken), roze alleen aan de kaak, groen weg → `model/model_v1.png`. Vel: `model/vel_v1.png` (r1 | r2 | v1).
- v1, Jordi: "De vorm is niet goed, het kleurgebruik is verschrikkelijk, door hele harde overgangen, rare losse pixels, vage lijnen, weinig schaduw en tint gebruik, probeer dat wat meer te gaan doen"; daarna: "voor kleur he", "silhouet is prima". **Silhouet van `model/combi_kop.png` bevroren**; kleur opnieuw met de hand door een maker-agent.
- r1-sprite (`sprite_r1/`, maker met de hand), Jordi: "maar de tinten kloppen niet"; welke: "alles" (niet zoals Gemini, oranje te fel, geel/oranje te dicht, schaduwtinten). Ook: "als je het hoofd van deze kecleon evo opeens effen inkleurt herken je er geen kecleon meer in"; "dat patroon behoud je maar dan met andere kleuren". r2: tinten gemeten uit het model, kleurpatroon van kop en staart behouden; voor de ex-groene zones varianten A (oranje/rood) en B (roze) ter keuze (keuze Claude: Jordi noemde geen kleur).
- Jordi: "en kijk ook naar de originele kecleon"; "die gele lijnen kan je wss precies zo behouden, omdat het groen oranje wordt" → **wat groen was wordt oranje** (variant A), gele lijnen/strepen blijven; B vervalt.

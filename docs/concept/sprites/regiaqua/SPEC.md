# Regiaqua (werknaam) – diepzee-Regi

Besluiten (letterlijk Jordi):
- 27 nov: "Regiaqua is een draaikolk golem, diep onderzee in een trog. water armen die een soort van zweven, geen benen, want de onderkant van de draaikolk is goed genoeg".
- 27 nov: armen zweven los van het lijf (vraag "zoals Rayman": "yes precies").
- 27 nov: "de stippen moeten echt stippen zijn, liefste ook niet in de hoofdkleur" (voorstel luchtbellen-spiraal afgewezen).
- 27 nov: "stippen van regi's lichten altijd op, maar je mag ze wel zo'n kleur geven" (= diepzee-lichtkleur).
- 27 nov: "Ze moeten echt passen tussen de andere regi's ook". Werkwijze: Gemini-modellen.

- 27 nov, typing: "ja ze zijn monotype" (= puur Water).

Open: patroon van de stippen, kleuren.
Prompt: `PROMPT.md`.

## Rondes
- r1 (`gemini/r1.png`, 27 nov): Jordi: "dit is al heel erg hoe ik hem in gedachten heb, check of de stippen kloppen met andere regi's en of die goed vertaalt naar een sprite".
- Check Claude (`gemini/r1_vergelijking.png`, `regi_stippen_gen3.png`): Gen 3-Regi's hebben 7 stippen van 2×2 px met 1 px tussenruimte, in een kleur die in tint afwijkt van het lijf (oranje op beige, geel op blauw, roze op grijs). Regirock = twee kolommen, Regice = kruis met lange horizontale rij, Registeel = zeshoek met middenstip. r1: 7 stippen (1 boven, 4 in een rij, 2 onder); patroon lijkt op dat van Regice; kleur cyaan op teal = zelfde tintfamilie. Verkleind naar 64 blijven silhouet, handen en stippen leesbaar.
- Jordi (27 nov) na de check: "regiaqua lijkt wel goed! in de sprites van regi's zijn het dus vierkantjes ipv stippen vanwege de grootte" (= in de sprite worden de stippen 2×2-vierkantjes zoals bij de Gen 3-Regi's).
- Jordi (27 nov): "ik tel dat alle regi's 7 stippen hebben en aqua ook dus dat is prima" → model = `gemini/r1.png`, stippen zoals r1 (als 2×2-vierkantjes). Sprite gestart (maker, `sprite/`).
- Jordi (27 nov): "als deze klaar zijn komen ze op het sprite sheet onder een apart kopje 'Legendaries'" → nieuwe sectie "Legendaries" in `showcase/maak_vel.py` (SECTIES).

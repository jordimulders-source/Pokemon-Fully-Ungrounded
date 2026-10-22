# Tilesets

- **`bestaand/`**: alle tilesets die nu in de game zitten, als overzichtsvel (metatiles van 16×16, 8 per rij, 2× vergroot, zoals in Porymap).
  - `primary/`: de primaire tilesets (grond, gras, water; gedeeld door veel kaarten).
  - `secondary/`: de secundaire tilesets (stads-, route- en grotspecifiek), getekend met een primary waarmee ze in de game echt gebruikt worden.
  - Opnieuw maken: `python3 tools/concept/tileset_sheets.py`.
  - Let op: hier staan ook de Ungrounded-specifieke sets (Area Zero, Spacetime, Ultra Space, Yoshi's Island, Ashfrost/sneeuw, …); niet alles blijft in Fully Ungrounded.
- **`nieuw/`**: nieuwe tilesets die Jordi vindt voor de Zuid-Amerika-regio. Dit is een **assetbibliotheek**: alleen wat we echt gebruiken, gaat de game in (en telt mee voor de ROM-ruimte); de rest blijft hier als bron. Graag per set een eigen map met de bronbestanden en een `BRON.txt` (waar vandaan, maker, licentie/credits), zodat we weten wat we mogen gebruiken en wie we moeten noemen.

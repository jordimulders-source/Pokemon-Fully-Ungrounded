# Silhouet nachtaap fase 3, ronde 1 (5 nov)
**Opdracht (Jordi):** "Maak een silhouet en dan gaan we een sprite bouwen"; maan (groter) en rugpatroon (op de rug, mee met de pose) komen in de sprite.
- Bron: `bron.py` = `../model2d/model.png` verkleind naar 64 (fill 0,97, onderaan uitgelijnd), 50%-dekking (`model50.txt`, `dekking.npy/txt`, `onderlaag_256.png`).
- `glad.py` → `ronde1.txt` (`glad_uitvoer.txt`): korrels weg met flips van 1 px naast de 50%-grens (dekking 0,2–0,8), bij gelijkspel dichtst bij 0,5.
- Staart: spleten tussen de windingen zijn < 1 px (dekking 0,2–0,45) en zijn gevuld, behalve waar ze aan de buitenkant grenzen; de windingen komen als lijnen in de kleur (zoals de spiraal van fase 2). Spiraalgat 3×4 px zoals in het model; 1-px spleet tussen staartwortel en buitenste winding dicht.
- Meting: 1796 px (model 1779), +22/−5, alles binnen 1 px van de 50%-grens; 0 korrels, 0 dunne delen (< 2 px), één geheel, één gat (spiraal).
- Onafhankelijke keurder: FAIL op de spiraalvulling (regel maakte de buitenrand van de staart 1 px dikker, 20 px) → gerepareerd; verder PASS.
- Eerlijk (komt uit het model): kop, vuistarm en healerhand + gloed vormen links één massa (kop leest pas in de kleur); de hand is binnen de gloed een rondje zonder vingers (vingers in de kleur); 1796 px is groot (Alakazam 1388, Slaking 2264, fase 2 1459), past bij een eindvorm.

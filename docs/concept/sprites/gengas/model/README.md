# Gengas model (15 nov)
Bron: `../gemini/r5_a.png`. Volgorde (scratch-map als argument; hier: deze map):
1. `nat.py r5_a.png 10.24 9.5 n10.png` – eigen pixelraster terug (99×99).
2. `parts.py n10.png . .` – lijf/ledematen scheiden (`cls.npy`, `lab.npy`; ledematen = componenten 1, 7, 8, 11).
3. `bol.py .` + `rond.py .` – cirkel op de lijfrand onder de oren; lijf wordt een echte bol (Jordi: "zorg wel dat het een bol blijft he"), deuken waar ledematen lagen gevuld.
4. `comp.py . indelingen_v1.png` – indelingen uit `specs.json` (positie x,y op canvas, lijf op 15,10; "achter" = achter de bol en donkerder).
Alleen modelschetsen: ledematen nog in Gemini-vorm, gezicht nog niet verplaatst.

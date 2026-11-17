# r13 (17 nov): oog met pupil, 3 varianten op `eind/pitahaya2_eind2.png`

Jordi: "zijn oog lijkt nu geen pupil te hebben".

Script: `maak_r13.py`. Elke pixel is met een assert gecontroleerd en de reden staat in `pitahaya2_r13_afwijkingen.txt`. Per variant zitten alle wijzigingen binnen het oog (x 12–18, y 37–42); buiten het oog is de diff 0 en het silhouet is gelijk. Er zijn geen nieuwe dambordjes. De nieuwe "losse" pixels zijn het oogwit en het grijs zelf (1 px wit naast de pupil, zoals Gen 3-ogen).

Gen 3-bron: **Feraligatr** (anim_front, frame 1, oog x 22–25, y 14–17). Dat is een links kijkend krokodillenoog onder een zwaar lid, met iris | pupil | iris, een pupil van 2 px hoog en grijs bovenin. Fase 1 heeft een oog van 1 px wit; daar valt geen pupil van over te nemen.

| Variant | px | Wat |
|---|---|---|
| A | 2 | (14,40) K→W en (15,40) W→K. Rij 40 leest wit \| pupil \| wit; de pupil hangt aan het lid, zoals in het model. Het oog is even groot als nu. |
| B | 5 | A, plus (17,40) r→W (groter wit rechts, zoals in het model; 1 px breder), (16,39) W→v (grijze schaduw onder het lid) en (17,39) r→K (het lid loopt door). |
| C | 6 | Feraligatr overgenomen, 1 px hoger: A, plus (16,39) W→v, (14,41) W, (15,41) K en (16,41) W. De pupil is 2 px hoog. |

Kiesvel: `kies.png` (`kies.py`). Daarop staan het model-oog en het huidige oog naast A, B en C op 12×, de kop op 8×, en de hele sprite op 1× en 2× (licht en donker).

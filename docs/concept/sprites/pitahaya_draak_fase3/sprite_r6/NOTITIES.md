# Pitahaya-draak fase 3, sprite r6 (maker): keurderpunten op r5

r5 kreeg PASS met en zonder tong. De buikvariant kreeg een technische FAIL op 3 punten. Daarnaast twee kleine punten in alle drie de versies. Basis zijn de r5-bestanden.

Script: `maak_r6.py`. De buikvariant komt uit `buik.py`; zone `RIJEN` is ongewijzigd t.o.v. r5. De log per pixel staat in `*_afwijkingen.txt`.

```
python3 maak_r6.py ../sprite_r5/pitahaya3_r5.png pitahaya3_r6.png
python3 maak_r6.py ../sprite_r5/pitahaya3_r5_zonder_tong.png pitahaya3_r6_zonder_tong.png
python3 maak_r6.py ../sprite_r5/pitahaya3_r5_buik.png pitahaya3_r6_buik.png --buik
python3 vel.py <tijdelijke map>
```

## Controle
| versie | px t.o.v. r5 |
|---|---|
| met tong | 4 |
| zonder tong | 4 |
| buik | 25 |

- Met en zonder tong: buiten de bekzone (x 0-12, y 26-38) pixelgelijk.
- Buik: buiten de buikzone pixelgelijk aan met-tong.
- Het silhouet is ongewijzigd.

## Per punt
1. **Buik, slagschaduw onder de kaak.** Rij 30 (x 17-22) is helemaal w, en (17-18,31) is ook w.
2. **Buik, sikkel in plaats van een band.** Breedte van de w-schaduw aan de rechterkant per rij:

   | rij | breedte |
   |---|---|
   | 31-32 | 0 |
   | 33-35 | 1 |
   | 36-40 | 2 (tegen rib/onderarm) |
   | 41 | 3 |
   | 42-43 | hele rij |

3. **Buik, pitjes.**
   - (23,36) → (24,36) en (25,39) → (26,39); beide vrij van de buitenlijn, de schaduw en andere pitjes.
   - (19,31) → (20,31), weg van de nieuwe kaakschaduw.
   - (29,38) → (28,38), uit de sikkel.
   - Er zijn 10 pitjes. (28,38) en (28,40) raken de sikkel aan de zijkant. (27,42) staat in de onderste schaduwrij, zoals in r5.
4. **Borst, alle versies.** (21,33), (22,33) en (26,33) → G. In de buikvariant vallen (21,33) en (22,33) in de buikzone; daar alleen (26,33).
5. **Verre hand, alle versies.** (10,43) zwart → g.

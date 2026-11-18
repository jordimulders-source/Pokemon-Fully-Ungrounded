# Pitahaya-draak fase 3, sprite r14: eindkeuring op r13 G (FAIL klein)

- Basis `../sprite_r13/pitahaya3_r13_G.png` (Jordi koos G). `python3 maak_r14.py` schrijft `pitahaya3_r14.png` en `pitahaya3_r14_afwijkingen.txt`; asserts: oude kleur per pixel, precies 7 px, silhouet gelijk, ≤16 kleuren. `python3 vel.py <tijdelijke map>`: kop 12× r14 | r13 G | model, hele sprite 8×, 1×/2× op licht en donker naast Salamence/Tyranitar/Sceptile.
- Pixels:
  1. (11,29) W -> w: schaduw achterin de bek consistent (model daar donker).
  2. (58,45) (58,46) (58,47) g -> G: banding in de rechter staartlus weg (zelfde opbouw als rij 48-53).
  3. (23,59) d -> r: rechtsonder de knots is het donkerst, niet links.
  4. (15,51) (16,51) h -> H: rafels aan de lichtkant niet donkerder dan aan de schaduwkant.

# Kelp-Oddish r6 = r5 + golvende rand op het middelste blad

Jordi: "kan je het middelste blad ook nog doen?" Basis `../r5/oddish_r5.png`; palet ongewijzigd; gezicht en lijf pixelgelijk (rijen ≥ 29 diff 0, assert in `bouw.py`).

Gewijzigd (y,x), 4 px op 2 plekken, elk 1 px inham waar de rand regelmatig/recht liep:
- Linkerrand (trap 38-36-35-34): (17,35) 6→0, (17,36) 9→6 (rand schuift 1 px in; het hooglicht houdt 5 px).
- Rechterrand (rechte zwarte rand x41, y18–21): (19,41) 1→0, (19,40) 8→1.
Silhouet, richting en top van het blad zijn gelijk; geen losse pixels.

`vel.png`: r5 | r6 | Oddish uit de game op 8×, eronder 1× op licht.

#!/bin/sh
# reproduceert uku_pacha_r5.png vanaf ../r4/raster_af.txt
set -e
python3 borst5.py
python3 scherp.py raster.txt raster_s.txt zone
python3 afwerk5.py
python3 raster2png.py raster_af.txt uku_pacha_r5.png
python3 check.py raster_af.txt
python3 vel.py

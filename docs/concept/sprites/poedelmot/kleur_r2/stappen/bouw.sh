cp onderlegger.txt raster.txt
for k in k_kop k_spriet k_ruis k_vleugel k_onder k_ver k_ruis k_fix k_lijn; do [ -f $k.py ] && { python3 schoon.py raster.txt $k.py || echo FOUT $k; }; done

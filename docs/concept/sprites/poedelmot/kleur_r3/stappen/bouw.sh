cp r2.txt raster.txt
for k in m_kleur k_kop3 k_vleugel3 k_onder3 k_spriet3 k_ruis k_fix3 k_lijn k_na; do [ -f $k.py ] && { python3 schoon.py raster.txt $k.py || echo FOUT $k; }; done

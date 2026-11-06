cp r2.txt raster.txt
for k in m_kleur k_kop3 k_oog4 k_onder3 k_fix3 k_warm k_vleugel5 k_spriet5 k_ruis k_r5 k_r6 k_ruis k_fix6 k_lijn k_na; do [ -f $k.py ] && { python3 schoon.py raster.txt $k.py || echo FOUT $k; }; done

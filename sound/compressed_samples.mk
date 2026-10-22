# Project Grounded: eigen muzieksamples die als DPCM (4 bit, ±halve grootte) in de ROM gaan.
# De HQ-mixer (src/m4a_hq_mixer.s) speelt ze af (MODE_COMP). Lijst = bestandsnamen zonder .wav in grounded/.
# Fully Ungrounded: alleen de samples van Keccles zijn nog over.
COMPRESSED_SAMPLES := \
	kc_bongo_hi kc_bongo_lo kc_claves kc_cowbell kc_cuatro kc_guiro_long \
	kc_guitar_57 kc_guitar_69 kc_timbale_hi kc_timbale_lo kc_trombone_55 kc_trombone_67

COMPRESSED_SAMPLE_BINS := $(patsubst %,sound/direct_sound_samples/grounded/%.bin,$(COMPRESSED_SAMPLES))
$(COMPRESSED_SAMPLE_BINS): sound/%.bin: sound/%.wav sound/compressed_samples.mk
	$(WAV2AGB) -b -c $< $@

# Project Grounded: eigen muzieksamples die als DPCM (4 bit, ±halve grootte) in de ROM gaan.
# De HQ-mixer (src/m4a_hq_mixer.s) speelt ze af (MODE_COMP). Lijst = bestandsnamen zonder .wav in grounded/.
COMPRESSED_SAMPLES :=

COMPRESSED_SAMPLE_BINS := $(patsubst %,sound/direct_sound_samples/grounded/%.bin,$(COMPRESSED_SAMPLES))
$(COMPRESSED_SAMPLE_BINS): sound/%.bin: sound/%.wav sound/compressed_samples.mk
	$(WAV2AGB) -b -c $< $@

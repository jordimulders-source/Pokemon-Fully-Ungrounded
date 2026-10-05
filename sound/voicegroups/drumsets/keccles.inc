@ Project Grounded: salsa-drumkit voor Battle! Keccles (keccles_theme.py): 36 kick, 37 clave, 38 cascara,
@ 39/40 timbales (hembra/macho), 41 campana, 42 conga slap, 43 tumbadora, 44 conga open, 45 crash, 46 rimshot,
@ 47/48 bongó (macho/hembra), 49/50 bongo-bel (mond/hiel), 51/52 güiro (lang/kort). kc_* = FluidR3 (gm_samples.py).
voice_group keccles_drumset, 36
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 0
	voice_directsound 60, 64, DirectSoundWaveData_kc_claves, 255, 0, 255, 100
	voice_directsound 79, 88, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 80
	voice_directsound 60, 54, DirectSoundWaveData_kc_timbale_lo, 255, 0, 255, 140
	voice_directsound 60, 82, DirectSoundWaveData_kc_timbale_hi, 255, 0, 255, 140
	voice_directsound_no_resample 64, 72, DirectSoundWaveData_sd90_cowbell, 255, 0, 255, 120
	voice_directsound_no_resample 64, 54, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 60
	voice_directsound 60, 46, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 60
	voice_directsound 66, 58, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 60
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165
	voice_directsound 72, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 100
	voice_directsound 60, 90, DirectSoundWaveData_kc_bongo_hi, 255, 0, 255, 80
	voice_directsound 60, 84, DirectSoundWaveData_kc_bongo_lo, 255, 0, 255, 80
	voice_directsound 54, 88, DirectSoundWaveData_kc_cowbell, 255, 0, 255, 120
	voice_directsound 57, 88, DirectSoundWaveData_kc_cowbell, 255, 0, 255, 100
	voice_directsound 60, 40, DirectSoundWaveData_kc_guiro_long, 255, 0, 255, 160
	voice_directsound 62, 40, DirectSoundWaveData_kc_guiro_long, 255, 0, 255, 60


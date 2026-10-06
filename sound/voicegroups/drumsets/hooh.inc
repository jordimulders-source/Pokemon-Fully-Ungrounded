@ Project Grounded: drumkit voor Battle! Ho-Oh v2 (hooh_theme.py): 36 kick, 37 snare, 38 odaiko, 39/40 nagado
@ (hoog/laag), 41 shime-daiko, 42 ka (rand), 43 kiai, 44 hyoshigi, 45 kotsuzumi, 46 ohtsuzumi, 47 bekken,
@ 48/49 toms, 50 orkestsnare (roffels). hooh_* = eigen samples (hooh_samples.py).
voice_group hooh_drumset, 36
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 150
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 180
	voice_directsound 60, 64, DirectSoundWaveData_hooh_odaiko, 255, 0, 255, 200
	voice_directsound 60, 58, DirectSoundWaveData_hooh_nagado, 255, 0, 255, 180
	voice_directsound 55, 70, DirectSoundWaveData_hooh_nagado, 255, 0, 255, 180
	voice_directsound 60, 76, DirectSoundWaveData_hooh_shime, 255, 0, 255, 90
	voice_directsound 60, 50, DirectSoundWaveData_hooh_ka, 255, 0, 255, 80
	voice_directsound 57, 64, DirectSoundWaveData_hooh_kiai, 255, 0, 255, 160
	voice_directsound 60, 40, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 90
	voice_directsound 60, 48, DirectSoundWaveData_ethnic_flavours_kotsuzumi, 255, 0, 255, 110
	voice_directsound 60, 80, DirectSoundWaveData_ethnic_flavours_ohtsuzumi, 255, 0, 255, 110
	voice_directsound_no_resample 60, 54, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 170
	voice_directsound 55, 44, DirectSoundWaveData_unused_sc55_tom, 255, 216, 77, 170
	voice_directsound 46, 84, DirectSoundWaveData_unused_sc55_tom, 255, 216, 77, 170
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 150


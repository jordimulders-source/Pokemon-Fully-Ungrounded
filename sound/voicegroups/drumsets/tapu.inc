@ Project Grounded: drumkit voor Battle! Tapu v2 (tapu_theme.py): 36/37 taiko (hoog/laag), 38 odaiko, 43 ka,
@ 45 bekken (eigen samples, tapu_samples.py); 39 Indiase trom, 40 tom, 41/42 conga, 44 kotsuzumi, 46 tamboerijn,
@ 47 hyoushigi, 48 kick (stock).
voice_group tapu_drumset, 36
	voice_directsound 60, 0, DirectSoundWaveData_tapu_taiko, 255, 0, 255, 190
	voice_directsound 56, 0, DirectSoundWaveData_tapu_taiko, 255, 0, 255, 190
	voice_directsound 60, 0, DirectSoundWaveData_tapu_odaiko, 255, 0, 255, 205
	voice_directsound 60, 0, DirectSoundWaveData_unused_heart_of_asia_indian_drum, 255, 0, 255, 140
	voice_directsound 60, 0, DirectSoundWaveData_unused_sc55_tom, 255, 0, 255, 150
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 80
	voice_directsound_no_resample 64, 0, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 60
	voice_directsound 60, 0, DirectSoundWaveData_tapu_ka, 255, 0, 255, 150
	voice_directsound 60, 0, DirectSoundWaveData_ethnic_flavours_kotsuzumi, 255, 0, 255, 110
	voice_directsound 60, 0, DirectSoundWaveData_tapu_crash, 255, 0, 255, 225
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_tambourine, 255, 0, 255, 90
	voice_directsound 60, 0, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 90
	voice_directsound 60, 0, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 120


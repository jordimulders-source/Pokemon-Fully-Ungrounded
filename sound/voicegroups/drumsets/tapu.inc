@ Project Grounded: drumkit voor Battle! Tapu (tapu_theme.py), alleen stock-samples: 36/37 taiko (hoog/laag),
@ 38 grote trom (ambient tom), 39 Indiase trom, 40 tom, 41/42 conga, 43 ohtsuzumi, 44 kotsuzumi, 45 orkestbekken,
@ 46 tamboerijn, 47 hyoushigi, 48 kick.
voice_group tapu_drumset, 36
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 140
	voice_directsound 53, 0, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 140
	voice_directsound 60, 0, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 150
	voice_directsound 60, 0, DirectSoundWaveData_unused_heart_of_asia_indian_drum, 255, 0, 255, 120
	voice_directsound 60, 0, DirectSoundWaveData_unused_sc55_tom, 255, 0, 255, 130
	voice_directsound 60, 44, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 80
	voice_directsound_no_resample 64, 84, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 60
	voice_directsound 60, 80, DirectSoundWaveData_ethnic_flavours_ohtsuzumi, 255, 0, 255, 110
	voice_directsound 60, 48, DirectSoundWaveData_ethnic_flavours_kotsuzumi, 255, 0, 255, 110
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216
	voice_directsound 60, 80, DirectSoundWaveData_sc88pro_tambourine, 255, 0, 255, 90
	voice_directsound 60, 40, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 90
	voice_directsound 60, 0, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 120


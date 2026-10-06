@ Project Grounded: drumkit voor Battle! Ho-Oh (hooh_theme.py), alleen stock-samples: 36 kick, 37 snare,
@ 38/39 taiko (hoog/laag), 40 grote trom (odaiko), 41-43 toms, 44 hyoshigi, 45 atarigane, 46 kotsuzumi,
@ 47 ohtsuzumi, 48/49 bekkens, 50 orkestsnare (roffels).
voice_group hooh_drumset, 36
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 150
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 180
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 160
	voice_directsound 53, 58, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 160
	voice_directsound 60, 64, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 170
	voice_directsound 60, 44, DirectSoundWaveData_unused_sc55_tom, 255, 216, 77, 170
	voice_directsound 55, 64, DirectSoundWaveData_unused_sc55_tom, 255, 216, 77, 170
	voice_directsound 50, 84, DirectSoundWaveData_unused_sc55_tom, 255, 216, 77, 170
	voice_directsound 60, 40, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 90
	voice_directsound 60, 88, DirectSoundWaveData_ethnic_flavours_atarigane, 255, 0, 255, 140
	voice_directsound 60, 48, DirectSoundWaveData_ethnic_flavours_kotsuzumi, 255, 0, 255, 110
	voice_directsound 60, 80, DirectSoundWaveData_ethnic_flavours_ohtsuzumi, 255, 0, 255, 110
	voice_directsound_no_resample 60, 54, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 200
	voice_directsound_no_resample 60, 76, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 150


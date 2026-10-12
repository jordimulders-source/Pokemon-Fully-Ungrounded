@ Project Grounded: drumkit voor Battle! Lugia (lugia_theme.py): 36 kick, 37 orkestsnare, 38 taiko,
@ 39/40 toms, 41 orkestbekken, 42 donder (trinity crash). Alleen stock-samples, geen PSG.
voice_group lugia_drumset, 36
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 200
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 200
	voice_directsound 54, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180
	voice_directsound 45, 58, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204
	voice_directsound 52, 70, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204
	voice_directsound_no_resample 30, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165


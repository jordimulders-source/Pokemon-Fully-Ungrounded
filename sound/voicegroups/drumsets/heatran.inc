@ Project Grounded: drumkit voor Battle! Heatran v5 (heatran_theme.py): de Gen 3-drums uit rs_drumset zonder
@ PSG-noten: 36 kick, 37 snare (dof), 38 hihat, 39 open hihat, 40 crash, 41-43 toms laag/midden/hoog,
@ 44 trinity-crash (blikkerig).
voice_group heatran_drumset, 36
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 242
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 242
	voice_directsound_no_resample 60, 79, DirectSoundWaveData_unknown_close_hihat, 255, 127, 0, 188
	voice_directsound_no_resample 60, 79, DirectSoundWaveData_unknown_open_hihat, 255, 242, 141, 0
	voice_directsound_no_resample 30, 54, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216
	voice_directsound 48, 44, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204
	voice_directsound 54, 64, DirectSoundWaveData_unused_sc55_tom, 255, 216, 77, 204
	voice_directsound 60, 79, DirectSoundWaveData_unused_sc55_tom, 255, 204, 77, 204
	voice_directsound_no_resample 60, 14, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165


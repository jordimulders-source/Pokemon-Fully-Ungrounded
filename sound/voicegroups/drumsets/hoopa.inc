@ Project Grounded: drumkit voor Battle! Hoopa (hoopa_theme.py): 36 darbuka dum, 37 tek, 38 ka, 39 lijsttrom
@ (bendir), 40 vingerbekken, 41 crash, 42 taiko, 43 tamboerijn, 44 orkestsnare (roffels), 45 lage dum.
@ hoopa_* = eigen samples (hoopa_samples.py).
voice_group hoopa_drumset, 36
	voice_directsound 60, 64, DirectSoundWaveData_hoopa_dum, 255, 0, 255, 160
	voice_directsound 60, 64, DirectSoundWaveData_hoopa_tek, 255, 0, 255, 100
	voice_directsound 56, 64, DirectSoundWaveData_hoopa_tek, 255, 0, 255, 100
	voice_directsound 60, 64, DirectSoundWaveData_hoopa_bendir, 255, 0, 255, 180
	voice_directsound 60, 64, DirectSoundWaveData_hoopa_zill, 255, 0, 255, 180
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 170
	voice_directsound 57, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_tambourine, 255, 0, 255, 120
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 150
	voice_directsound 54, 64, DirectSoundWaveData_hoopa_dum, 255, 0, 255, 170


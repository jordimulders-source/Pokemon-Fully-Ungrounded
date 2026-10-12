@ Project Grounded: drumkit voor legends3_theme.py (Zacian / Xerneas / meren). Alleen stock-samples, geen PSG.
@ 36 kick, 37 orkestsnare, 38 snare, 39 tom laag, 40 tom midden, 41 tom hoog, 42 orkestbekken, 43 crash, 44 hihat dicht, 45 tamboerijn, 46 taiko, 47 hihat open.
@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.
voice_group legends3_drumset, 36
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 200
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 200
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 200
	voice_directsound 45, 52, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204
	voice_directsound 51, 64, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204
	voice_directsound 57, 76, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216
	voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165
	voice_directsound 60, 64, DirectSoundWaveData_unknown_close_hihat, 255, 127, 0, 188
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_tambourine, 255, 127, 77, 204
	voice_directsound 57, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180
	voice_directsound 60, 64, DirectSoundWaveData_unknown_open_hihat, 255, 242, 141, 0

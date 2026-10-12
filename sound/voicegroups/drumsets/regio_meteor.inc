@ Project Grounded: drumkit voor regio_theme2.py (Meteor Falls). Alleen stock-samples, geen PSG.
@ 36 kick, 37 snare, 38 hyoushigi, 39 tom laag, 40 tom midden, 41 tom hoog, 42 crash, 43 taiko diep, 44 pauk.
@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.
voice_group regio_meteor_drumset, 36
	voice_directsound 62, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180
	voice_directsound 56, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 170
	voice_directsound 58, 72, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 120
	voice_directsound 45, 52, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180
	voice_directsound 51, 64, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180
	voice_directsound 57, 76, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180
	voice_directsound 56, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 235, 0, 165
	voice_directsound 48, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180
	voice_directsound 43, 64, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 200

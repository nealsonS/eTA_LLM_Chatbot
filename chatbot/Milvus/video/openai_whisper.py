import stable_whisper


model = stable_whisper.load_model('base')

#model = stable_whisper.load_faster_whisper('base') #faster version, but need to find the package first...

#model = stable_whisper.load_hf_whisper('base') #HuggingFace is supposed to be 9x faster, but I found it to be not as accurate or fast for some reason

result = model.transcribe('audio.mp3') #can also do .wav, no need to convert to mp3
result.to_srt_vtt('audio_fw.srt', segment_level=True, word_level=False) #SRT

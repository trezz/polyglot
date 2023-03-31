# Polyglot

Automatic translator for human language.

## Dev notes

### v0

Taking as input an audio file of a few seconds and a target language:
- Transcribe it to text
- Translate it to the target language
- Speak the translated text using a text to speech lib.

The quality of the final voice is not important.

The time it takes to do all those steps should be low. Ideally below the second.


#### Dev steps

I recordered a small audio file using Voice Memo Apple application in
`res/pres_vincent.m4a`. It's going to be the main input for my developments.

I followed:
https://github.com/openai/whisper#setup

```
python3 -m pip install whisper-openai
brew install ffmpeg
```

First tests:

```
$ whisper res/pres_vincent.m4a
/opt/homebrew/lib/python3.10/site-packages/whisper/transcribe.py:114: UserWarning: FP16 is not supported on CPU; using FP32 instead
  warnings.warn("FP16 is not supported on CPU; using FP32 instead")
Detecting language using up to the first 30 seconds. Use `--language` to specify the language
Detected language: French
[00:00.000 --> 00:04.680]  Bonjour, je m'appelle Vincent et j'ai 35 ans.
```

```
whisper res/pres_vincent.m4a --language French --fp16 False
[00:00.000 --> 00:04.680]  Bonjour, je m'appelle Vincent et j'ai 35 ans.
```

This command failed on macOS:
```
pip3 install -U libretranslate
Building wheel for LTpycld2 (setup.py) ... error
  error: subprocess-exited-with-error

  × python setup.py bdist_wheel did not run successfully.
  │ exit code: 1
  ╰─> [159 lines of output]
...
```

Second try with Docker:

```
cd vendor/LibreTranslate
docker build -f docker/Dockerfile --build-arg with_models=true -t libretranslate .
docker run -it -p 8080:8080 libretranslate --port 8080
```

```
 python3 ./polyglot ./res/pres_vincent.m4a
./res/pres_vincent.m4a
        input text:   Bonjour, je m'appelle Vincent et j'ai 35 ans.
        input lang:  fr
        translated:  Hello, my name is Vincent and I'm 35 years old.
```


### v1

Taking as input an audio stream from a bluetooth microphone, split the stream
into audio files of a few sentenses, and feed the v0 with those files.

It means:
- Reading audio from different types of microphones on linux
- Detection of the sentenses (optional, could be an enhancement).

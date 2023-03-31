import argparse
import json
import whisper
from urllib import request, parse


def cli():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("audio", nargs="+", type=str,
                        help="audio file(s) to transcribe")
    parser.add_argument("--model", default="small",
                        help="name of the Whisper model to use")
    parser.add_argument("--target-language", default="en",
                        help="language code to translate to")

    args = parser.parse_args()

    model = whisper.load_model(args.model)

    transcribed_texts = {}
    translated_texts = {}

    for f in args.audio:
        result = model.transcribe(f, fp16=False)
        transcribed_texts[f] = result

    for f, res in transcribed_texts.items():
        data = {
            "q": res["text"],
            "source": res["language"],
            "target": args.target_language,
        }

        body = parse.urlencode(data).encode()
        req = request.Request("http://0.0.0.0:8080/translate", data=body)
        resp = request.urlopen(req)
        raw_resp_body = resp.read()
        resp_body = json.loads(raw_resp_body)

        translated_texts[f] = resp_body["translatedText"]

    for f in args.audio:
        print(f)
        print('\tinput text: ', transcribed_texts[f]['text'])
        print('\tinput lang: ', transcribed_texts[f]['language'])
        print('\ttranslated: ', translated_texts[f])


cli()

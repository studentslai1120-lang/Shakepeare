#!/usr/bin/env python3
"""用 Google 文字轉語音（gTTS，英式口音）替每個單字與金句產生 mp3，存到 audio/words、audio/quotes。
需要網路：  pip install gTTS
用法：
  python3 make_audio.py            只處理「還是占位檔（小於 3 KB）」的項目，不會覆蓋你自己錄的音檔
  python3 make_audio.py --force    全部重做（會覆蓋）
  python3 make_audio.py A K Z      只處理指定字母
想用自己的聲音：直接用同樣的檔名放進 audio/ 覆蓋即可，不需要這個工具。"""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
try:
    from gtts import gTTS
except ImportError:
    sys.exit('請先安裝：pip install gTTS')
raw = open(os.path.join(ROOT, 'js', 'data.js'), encoding='utf-8').read()
data = json.loads(raw.split('=', 1)[1].strip().rstrip(';'))
force = '--force' in sys.argv
only = [a.upper() for a in sys.argv[1:] if not a.startswith('--')]
def clean(q): return q.replace('\n', ' ').replace('…', '').replace('“', '').replace('”', '')
for e in data:
    if only and e['letter'] not in only: continue
    name = f"{e['letter']}_{e['word'].lower()}.mp3"
    for kind, text in (('words', e['word']), ('quotes', clean(e['quote']))):
        path = os.path.join(ROOT, 'audio', kind, name)
        if not force and os.path.exists(path) and os.path.getsize(path) >= 3000:
            print('略過（已有錄音）', path); continue
        gTTS(text=text, lang='en', tld='co.uk', slow=False).save(path)
        print('完成', path); time.sleep(0.6)

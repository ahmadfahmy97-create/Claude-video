import json, os, subprocess, time
import numpy as np
from faster_whisper import WhisperModel
M='/home/user/mezz'; O='/home/user/work/tr'; os.makedirs(O,exist_ok=True)
model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=3)
def done_fetch(): return 'DONE' in open('/home/user/work/fetch.log').read()
while True:
    fin=done_fetch()
    todo=[c for c in sorted(os.listdir(M)) if c.endswith('.mp4') and '.tmp' not in c and not os.path.exists(f"{O}/{c[:-4]}.json")]
    if not todo and fin: break
    if not todo: time.sleep(20); continue
    for c in todo:
        a=subprocess.run(["ffmpeg","-v","error","-i",f"{M}/{c}","-vn","-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
        audio=np.frombuffer(a,np.int16).astype(np.float32)/32768.0
        out=[]
        if len(audio)>16000:
            segs,info=model.transcribe(audio,language="ms",word_timestamps=True,vad_filter=True,
                vad_parameters={"min_silence_duration_ms":400,"speech_pad_ms":200,"threshold":0.45},
                beam_size=3,condition_on_previous_text=False,
                initial_prompt="Ucapan rasmi Pengerusi FAMA, Lembaga Pemasaran Pertanian Persekutuan. Petani, usahawan, pertanian, MAHA.")
            for s in segs:
                out.append({"start":round(s.start,2),"end":round(s.end,2),"text":s.text.strip(),"nsp":round(s.no_speech_prob,2),"lp":round(s.avg_logprob,2),
                    "words":[{"w":w.word.strip(),"s":round(w.start,2),"e":round(w.end,2),"p":round(w.probability,2)} for w in (s.words or [])]})
        json.dump({"clip":c,"dur":len(audio)/16000,"segments":out},open(f"{O}/{c[:-4]}.json","w"),ensure_ascii=False)
        print("tr",c,len(out),flush=True)
print("TRDONE",flush=True)

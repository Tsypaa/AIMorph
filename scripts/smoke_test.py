import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
URL="http://127.0.0.1:8188"
LOG=ROOT/"logs"/"smoke_test.log"

def emit(message):
    line=f"[{datetime.now().isoformat(timespec='seconds')}] {message}"
    print(line,flush=True)
    with LOG.open("a",encoding="utf-8") as handle:
        handle.write(line+"\n")

def api(path,payload=None):
    data=None if payload is None else json.dumps(payload).encode("utf-8")
    request=urllib.request.Request(URL+path,data=data,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(request,timeout=30) as response:
        return json.load(response)

def gpu():
    try:
        return subprocess.check_output(["nvidia-smi","--query-gpu=temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw","--format=csv,noheader,nounits"],text=True,timeout=10).strip()
    except Exception as error:
        return str(error)

def mp4s(value):
    if isinstance(value,dict):
        for nested in value.values():
            yield from mp4s(nested)
    elif isinstance(value,list):
        for nested in value:
            yield from mp4s(nested)
    elif isinstance(value,str) and value.lower().endswith(".mp4"):
        yield value

def main():
    LOG.parent.mkdir(exist_ok=True)
    emit("Starting Wan2.2 5B I2V smoke test")
    stats=api("/system_stats")
    emit(f"Backend: ComfyUI {stats['system']['comfyui_version']}, {stats['devices'][0]['name']}")
    prompt=json.loads((ROOT/"workflows"/"gtx1080_video_test_api.json").read_text(encoding="utf-8"))
    try:
        response=api("/prompt",{"prompt":prompt,"client_id":"gtx1080-smoke"})
    except urllib.error.HTTPError as error:
        emit("Validation failed: "+error.read().decode("utf-8",errors="replace"))
        return 2
    prompt_id=response["prompt_id"]
    emit("Queued "+prompt_id)
    started=time.monotonic()
    last=-999.0
    while True:
        elapsed=time.monotonic()-started
        if elapsed-last>=20:
            emit(f"elapsed={elapsed:.0f}s GPU(temp,util,usedMiB,totalMiB,powerW)={gpu()}")
            last=elapsed
        history=api("/history/"+prompt_id)
        if prompt_id in history:
            entry=history[prompt_id]
            status=entry.get("status",{})
            emit(f"Completed {elapsed:.1f}s: {json.dumps(status,ensure_ascii=False)}")
            files=sorted(set(mp4s(entry.get("outputs",{}))))
            for filename in files:
                emit("Output: "+filename)
            return 0 if status.get("status_str")=="success" and status.get("completed") and files else 3
        time.sleep(5)

if __name__=="__main__":
    sys.stdout.reconfigure(encoding="utf-8",errors="replace")
    sys.stderr.reconfigure(encoding="utf-8",errors="replace")
    raise SystemExit(main())

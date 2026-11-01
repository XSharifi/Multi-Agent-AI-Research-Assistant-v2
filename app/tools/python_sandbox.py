import json, subprocess, tempfile
from pathlib import Path
from langchain_core.tools import tool

@tool
def execute_python_sandboxed(code: str) -> str:
    """Run generated Python inside a restricted Docker sandbox."""
    if len(code) > 30000:
        return "Rejected: code exceeds 30,000 characters."
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "main.py"
        p.write_text(code, encoding="utf-8")
        cmd = ["docker","run","--rm","--network","none","--cpus","1.0",
               "--memory","512m","--pids-limit","64","--read-only",
               "--tmpfs","/tmp:rw,noexec,nosuid,size=64m",
               "-v",f"{Path(tmp).resolve()}:/workspace:ro",
               "research-python-sandbox:latest","python","/workspace/main.py"]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            return json.dumps({"error":"timeout"})
        except FileNotFoundError:
            return json.dumps({"error":"Docker not found"})
        return json.dumps({"returncode":r.returncode,"stdout":r.stdout[-12000:],"stderr":r.stderr[-12000:]})

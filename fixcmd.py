
#!/usr/bin/env python3
import sys
import subprocess
import re
import shutil
from pathlib import Path

def diagnose(command, output, code):
    print("\n========== FIXCMD REPORT ==========")
    print("Command:", command)
    print("Exit code:", code)

    patterns = [
        (r"command not found", "Command install nahi hai ya naam galat hai."),
        (r"permission denied", "Permission ki dikkat hai."),
        (r"no such file or directory", "File ya path nahi mila."),
        (r"syntax error|unexpected token", "Script mein syntax error hai."),
        (r"ModuleNotFoundError|No module named", "Python module missing hai."),
        (r"IndentationError", "Python indentation galat hai."),
        (r"Connection refused|timed out", "Server ya network connection fail hai."),
        (r"No space left on device", "Storage bhar gayi hai."),
        (r"could not resolve|Name or service not known",
         "Internet ya DNS ki dikkat hai."),
    ]

    found = False
    for pattern, reason in patterns:
        if re.search(pattern, output, re.I):
            print("\nPossible reason:", reason)
            found = True

    if not found:
        print("\nExact reason local rules se identify nahi hui.")

    print("\nOriginal error output:")
    print(output or "(Koi output nahi mila)")

    print("\nTip: Python file ke liye python -m py_compile file.py")
    print("Tip: Bash file ke liye bash -n file.sh")
    print("===================================\n")

def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: fixcmd -- command [arguments]")
        print("Example: fixcmd -- python script.py")
        print("File check: fixcmd --check script.py")
        return

    if args[0] == "--check":
        if len(args) != 2:
            print("Usage: fixcmd --check file.py")
            return
        file = Path(args[1])
        if not file.is_file():
            print("File nahi mili:", file)
            return
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(file)],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("Python syntax theek hai:", file)
        else:
            print(result.stderr)
            diagnose("Python syntax check", result.stderr, result.returncode)
        return

    if args[0] != "--" or len(args) < 2:
        print("Usage: fixcmd -- command [arguments]")
        return

    command = args[1:]
    print("Running:", " ".join(command))

    try:
        result = subprocess.run(command, text=True, capture_output=True)
    except FileNotFoundError:
        diagnose(" ".join(command), "command not found", 127)
        return
    except KeyboardInterrupt:
        print("\nStopped by user.")
        return

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    if result.returncode == 0:
        print("\n[FIXCMD] Command successful.")
    else:
        diagnose(" ".join(command),
                 result.stdout + "\n" + result.stderr,
                 result.returncode)

if __name__ == "__main__":
    main()

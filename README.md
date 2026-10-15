# Termux fixcmd — command error diagnosis

`fixcmd` runs a command, preserves its output/exit code, identifies common error patterns, and optionally asks an AI model for a diagnosis. It can also propose a repair to a text/code file and only applies it after you type `YES`, creating a backup first.

## Important behavior

- It does **not** silently intercept every command you type in Termux. Run commands through `fixcmd -- ...` to diagnose failures.
- Local diagnostics work without an API key.
- AI diagnosis and `--repair` require an OpenAI API key and may incur API charges.
- AI-proposed changes can be wrong. Review the diff and test the file.
- Never paste API keys into GitHub or commit them to this repository.

## Install on Termux

1. Install requirements:

   ```bash
   pkg update
   pkg install python curl git
   ```

2. Create a GitHub repository named `termux-fixcmd` and upload `fixcmd.py` and `install.sh`.
3. In `install.sh`, replace `YOUR_GITHUB_USERNAME` with your GitHub username.
4. In Termux, run:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/termux-fixcmd/main/install.sh -o install.sh
   bash install.sh
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

   Replace `YOUR_GITHUB_USERNAME` in the URL with your real username.

## Usage

Diagnose a failing command:

```bash
fixcmd -- python broken_script.py
fixcmd -- bash script.sh
fixcmd -- pkg install package-name
fixcmd -- git clone https://example.com/repo.git
```

Ask AI to propose a repair to a file:

```bash
export OPENAI_API_KEY="YOUR_API_KEY"
fixcmd --repair broken_script.py
```

The tool shows a diff, asks for the exact word `YES`, and saves `broken_script.py.fixcmd.bak` before applying changes. Do not use a key you cannot afford to expose to the local device; unset it when not needed:

```bash
unset OPENAI_API_KEY
```

Optional model override:

```bash
export FIXCMD_MODEL="gpt-4.1-mini"
```

## Limitations

- Shell commands can behave differently when run through a wrapper. This implementation uses a shell for the command string; only pass commands you understand.
- It cannot guarantee a fix for every error, and it does not automatically repair installed packages, remote services, permissions, or network issues.
- The AI endpoint/model availability may change; see the current OpenAI API documentation.
- Keep backups and inspect changes before executing repaired code.

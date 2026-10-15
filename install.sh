#!/data/data/com.termux/files/usr/bin/bash
set -eu

ROOT="$HOME/.local/bin"
mkdir -p "$ROOT"

SCRIPT_URL="https://raw.githubusercontent.com/rohitdevika/termux-fixcmd/main/fixcmd.py"

if ! command -v python >/dev/null 2>&1; then
echo "Python install karein: pkg install python"
exit 1
fi

curl -fsSL "$SCRIPT_URL" -o "$ROOT/fixcmd.py"
chmod 700 "$ROOT/fixcmd.py"

cat > "$ROOT/fixcmd" <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
exec python "$HOME/.local/bin/fixcmd.py" "$@"
EOF

chmod 700 "$ROOT/fixcmd"

echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"

echo "Installation complete!"
echo "Ab Termux ko restart karein."

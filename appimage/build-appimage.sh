#!/usr/bin/env bash
# Build the Lollipop Chainsaw x86_64 AppImage (Re-Cherry Launcher + game set).
# Layout mirrors the shipped house AppImages: launcher, game exe and the
# matched runtime libs together in usr/bin (the launcher's program-set
# search finds them next to itself). No game data is bundled.
# The staged runtime is the exact set from LollipopChainsaw/run - the
# binary and its libs are a matched set; do not mix builds.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GAME_RUN="/mnt/sdb1/Games/LollipopChainsaw/run"
LAUNCHER_BIN="/mnt/sdb1/Games/LollipopChainsaw/project/tp-launcher/build-lollipop/ReCherryLauncher"
APPDIR="$HERE/AppDir"
OUTPUT="$HERE/ReCherry-x86_64.AppImage"
TOOLS="/home/muse/tools"

for f in "$LAUNCHER_BIN" "$GAME_RUN/re_cherry" "$GAME_RUN/librexruntime.so" \
         "$GAME_RUN/librexgpu-xenos.so" "$GAME_RUN/libTracyClient.so"; do
  [[ -f "$f" ]] || { echo "Missing input: $f" >&2; exit 1; }
done

rm -rf "$APPDIR"
install -d "$APPDIR/usr/bin"
install -m755 "$LAUNCHER_BIN" "$APPDIR/usr/bin/ReCherryLauncher"
install -m755 "$GAME_RUN/re_cherry" "$APPDIR/usr/bin/re_cherry"
install -m755 "$GAME_RUN/librexruntime.so" "$APPDIR/usr/bin/librexruntime.so"
install -m755 "$GAME_RUN/librexgpu-xenos.so" "$APPDIR/usr/bin/librexgpu-xenos.so"
install -m755 "$GAME_RUN/libTracyClient.so" "$APPDIR/usr/bin/libTracyClient.so"

# Attribution pack ships inside the AppImage.
install -d "$APPDIR/usr/share/licenses/recherry"
install -m644 "$HERE/LICENSE" "$HERE/CREDITS.md" \
  "$APPDIR/usr/share/licenses/recherry/"
cp -r "$HERE/licenses" "$APPDIR/usr/share/licenses/recherry/"

cat > "$HERE/recherry.desktop" <<'DESK'
[Desktop Entry]
Type=Application
Name=Re-Cherry Launcher
Comment=Launcher for the Lollipop Chainsaw Linux recompilation
Exec=ReCherryLauncher
Icon=recherry
Categories=Game;
Terminal=false
DESK
cp "$HERE/recherry-512.png" "$HERE/recherry.png"

export QMAKE="$(command -v qmake6 || command -v qmake)"
export PATH="$TOOLS:$PATH"

"$TOOLS/linuxdeploy" \
  --appdir "$APPDIR" \
  --executable "$APPDIR/usr/bin/ReCherryLauncher" \
  --executable "$APPDIR/usr/bin/re_cherry" \
  --desktop-file "$HERE/recherry.desktop" \
  --icon-file "$HERE/recherry.png" \
  --plugin qt

ARCH=x86_64 "$TOOLS/appimagetool" "$APPDIR" "$OUTPUT"
chmod 777 "$OUTPUT"
echo "Created: $OUTPUT"

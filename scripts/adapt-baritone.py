#!/usr/bin/env python3
"""Adapt the known Baritone 1.1.38 unload hook to Starling's current Streaming API.

Starling's game source replaced Streaming::forget(x, z) with
Streaming::forget_columns(world, gone). The new hook runs before removal and stashes
each unloaded chunk, preserving Baritone's ChunkEvent.UNLOAD behavior.
"""
from pathlib import Path
import sys

OLD_TARGET = 'target = "horizon_client_render::streaming::Streaming::forget"'
NEW_BLOCK = '''[[injection]]
id = "unload"
kind = "HEAD"
target = "horizon_client_render::streaming::Streaming::forget_columns"
helper = "hooks/unload.rs"
bindings = [
  { name = "world", ty = "&World", value = "&*world" },
  { name = "gone", ty = "&FxHashSet<(i32, i32)>", value = "gone" },
]'''

NEW_HELPER = '''fn baritone_unload(world: &World, gone: &FxHashSet<(i32, i32)>) {
    for &(x, z) in gone {
        if let Some(chunk) = world.chunks.get(&(x, z)) {
            baritone_unload::push(x, z, chunk.clone());
        }
    }
}
'''

def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: adapt-baritone.py MODS_DIR")

    root = Path(sys.argv[1])
    if not root.is_dir():
        raise SystemExit(f"mods directory not found: {root}")

    manifest = root / "baritone" / "horizon-mixin.toml"
    if not manifest.is_file():
        return

    text = manifest.read_text(encoding="utf-8")
    if OLD_TARGET not in text:
        return  # Newer Baritone already targets forget_columns.

    start = text.find('[[injection]]', text.find('id = "mod_unload_stash"'))
    if start < 0:
        raise SystemExit("Baritone has the old unload target but no unload injection block.")
    end_candidates = [p for p in (text.find('[[module]]', start + 1),
                                  text.find('[[injection]]', start + 1)) if p >= 0]
    end = min(end_candidates) if end_candidates else len(text)
    block = text[start:end]
    if OLD_TARGET not in block or 'id = "unload"' not in block:
        raise SystemExit("Baritone unload injection layout changed; refusing an unsafe patch.")

    text = text[:start] + NEW_BLOCK + "\n\n" + text[end:]
    helper = manifest.parent / "hooks" / "unload.rs"
    if not helper.is_file():
        raise SystemExit("Baritone unload helper is missing; refusing a partial patch.")
    helper.write_text(NEW_HELPER, encoding="utf-8")
    manifest.write_text(text, encoding="utf-8")
    print("adapt-baritone: mapped Streaming::forget to Streaming::forget_columns")

if __name__ == "__main__":
    main()

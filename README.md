# Alias Mod Builds

Private infrastructure project for compiling Starling native mods (.hnmod) with GitHub Actions and a Cloudflare Worker API.

## Components
- `.github/workflows/build.yml`: isolated build and publish jobs.
- `worker/`: Starling-compatible HTTPS build API.
- `scripts/`: request decryption, preparation, result publication and cleanup.
- `versions.json`: Starling version-to-source-commit map.

## Important security notes
Native mod build scripts/macros execute code during compilation. The build job therefore has read-only repository permissions, does not receive the API token, does not persist checkout credentials, and publishes only through a separate job that never executes mod code. Only use native mods from sources you trust.

## Setup
See [SETUP.md](SETUP.md) before deploying. The Worker requires a repository-scoped GitHub token with Actions and Contents read/write access, plus the two GitHub releases described there.

# Setup — Alias Mod Builds

## 1. GitHub repository
Keep this repository public if you want the Worker to download release assets without authentication. Do not commit tokens or private keys.

Create two GitHub Releases (no source code needed):
- tag: `requests`, title: `Build requests`
- tag: `results`, title: `Build results`

The API stores encrypted incoming mod bundles in `requests` and compiled libraries/status files in `results`.

## 2. Actions permissions
In Settings → Actions → General:
- Workflow permissions: Read and write permissions.
- Allow GitHub Actions to create and approve pull requests: leave disabled.

The workflow itself grants write permission only to the publish job.

## 3. GitHub token for the Worker
Create a fine-grained personal access token restricted to this repository only:
- Contents: Read and write
- Actions: Read and write
- Metadata: Read-only

Add it to the Cloudflare Worker as the secret `GITHUB_TOKEN`. Never put it in this repository or in the Android app.

## 4. Deploy the API
From the `worker` directory, install dependencies and deploy with Wrangler:
```sh
npm install
npx wrangler login
npx wrangler deploy
npx wrangler secret put GITHUB_TOKEN
```
Paste the token only into Wrangler's hidden secret prompt. The deploy command prints the Worker HTTPS URL.

## 5. Connect Starling
The Starling build-server setting expects the API base URL in the format documented by the Starling client. Confirm the URL is accepted by your installed Starling version before relying on it. Do not point the client at an untrusted server.

## 6. Supported version
The initial `versions.json` entry is Starling 0.8.0 and uses the upstream source commit pinned by Starling's official mod-builds project. Update the version map only after checking the corresponding Starling source revision and build scripts.

## 7. Test
Use a harmless mod you wrote or fully trust. Check Actions → build, then confirm the API returns a completed job and the library asset appears in the `results` release.

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Communication

**Répondre en français.** L'auteur (Hugo / Lightshadow02, repo `Oracios/UtopiaLauncher`) n'est pas développeur senior : préférer des étapes numérotées et des tableaux, expliquer le contexte plutôt que le jargon, et utiliser des liens cliquables `[fichier.ext:ligne](path#Lligne)`.

## What this is

The **Utopia Launcher** — a custom launcher for the Utopia modded Minecraft server, forked from [HeliosLauncher](https://github.com/dscalzi/HeliosLauncher). It reuses the customizations originally built for Hugo's earlier Nerysia launcher (branding, day/night background theme, distribution tooling). The current repo is a **modern Helios base** (Electron 39, helios-core ~2.3.0).

It downloads a remote distribution index describing servers and their mods, validates/downloads game assets and a compatible Java runtime, then builds and spawns the Minecraft JVM process. Most of the heavy lifting (distribution parsing, asset/Java validation, Mojang/Microsoft auth, logging) lives in the external `helios-core` dependency; this repo is primarily the launcher UI and process-launch glue.

The original Nerysia launcher is kept under `IMPORT/Nerysia-LAUCHER/` as **read-only reference** — port *from* it, never modify it (it is git-ignored).

## Commands

```bash
npm start            # Launch the app in dev (electron .)
npm run lint         # ESLint over the whole repo
npm run dist         # Build installer for the current platform
npm run dist:win     # Build Windows x64 installer
npm run dist:mac     # Build macOS installer
npm run dist:linux   # Build Linux x64 installer
```

There is no test suite. Requires Node.js v22. Verify changes by running `npm start` and using the launcher.

## Architecture

Electron app with the standard main/renderer split, but with `nodeIntegration: true` and `contextIsolation: false` (see `index.js` `createWindow`) — renderer scripts `require()` Node modules directly rather than going through a contextBridge.

**Main process — [index.js](index.js)**
- Creates the frameless `BrowserWindow`, loads `app/app.ejs`.
- `pickBackground()` chooses the launcher background by time of day: `clair` (light) between 7h–19h, otherwise `sombre` (dark). It returns a relative `theme/file` path used verbatim by [uibinder.js](app/assets/js/scripts/uibinder.js) (which is why uibinder no longer appends `.jpg`). Background images live in `app/assets/images/backgrounds/clair/` and `sombre/`.
- Hosts the `electron-updater` auto-update flow, driven by `autoUpdateAction` IPC messages.
- Owns the Microsoft OAuth login/logout flow: opens a separate `BrowserWindow` to `login.microsoftonline.com`, watches `did-navigate` for the redirect URI, and replies to the renderer via the `MSFT_OPCODE` channels. Opcodes/error types live in [app/assets/js/ipcconstants.js](app/assets/js/ipcconstants.js).

**Preloader — [app/assets/js/preloader.js](app/assets/js/preloader.js)**
- Runs before the renderer. Loads `ConfigManager`, injects `commonDir`/`instanceDir` into `DistroAPI` (the `DistributionAPI` constructor leaves these null on purpose — see [distromanager.js](app/assets/js/distromanager.js)), downloads/caches the distribution index, resolves the default selected server, then signals readiness with `distributionIndexDone`.

**Renderer UI — `app/*.ejs` + `app/assets/js/scripts/*.js`**
- The whole UI is a single page (`app.ejs`) of overlapping view containers shown/hidden by jQuery fades. View switching is centralized in [uibinder.js](app/assets/js/scripts/uibinder.js) (`VIEWS` map, `switchView`, `showMainUI`).
- Each script file maps to a view: `landing.js`, `login.js`, `loginOptions.js`, `settings.js`, `welcome.js`, plus `uicore.js` (core UI/frame setup) and `overlay.js` (modal overlays). These run in the renderer's global scope and freely share globals — which is why `app/assets/js/scripts/*.js` has `no-unused-vars`/`no-undef` disabled in [eslint.config.mjs](eslint.config.mjs).
- `uibinder.js` also reconciles the user's saved mod selections against the distribution index on every load via `syncModConfigurations`/`mergeModConfiguration` (recursive merge of optional sub-modules) and `ensureJavaSettings`.

**Supporting modules — `app/assets/js/*.js`** (used by both preloader and renderer)
- `configmanager.js` — single source of truth for persisted config. Reads/writes `config.json` in Electron's `userData` dir (game data default path `~/.utopialauncher`). All settings/account/mod/Java state goes through its getters/setters; callers must explicitly call `ConfigManager.save()`. Holds RAM heuristics and the `DEFAULT_CONFIG` shape.
- `processbuilder.js` — builds and `child_process.spawn`s the Minecraft JVM. Handles Forge (pre- and post-1.13), Fabric, and LiteLoader differences; constructs classpath, JVM/game args, and mod lists. This is the most intricate module — comments flag it as a candidate for rewrite. **Utopia patch:** NeoForge (and Forge 1.20.3+) removed `--fml.modLists`, so stock Helios can't inject mods that way. `setupNeoForgeMods()` instead copies enabled distribution mods into the instance `mods/` folder (tracked via `.utopia-managed-mods.json`); it triggers when the loader module is under the `net.neoforged` group (`usingNeoForge`).
- `authmanager.js` — wraps `helios-core` auth for Mojang (Yggdrasil) and Microsoft accounts; account state is persisted through `configmanager`.
- `distromanager.js` — defines `REMOTE_DISTRO_URL` and the shared `DistroAPI` singleton.
- `discordwrapper.js` (Rich Presence), `dropinmodutil.js` (drop-in mods/shaderpacks in the instance dir), `serverstatus.js`, `isdev.js`.

**i18n — [langloader.js](app/assets/js/langloader.js)**
- Strings live in TOML under `app/assets/lang/`. `en_US.toml` is the base; `_custom.toml` overrides it (for launcher customization). Look up strings with `LangLoader.queryJS('...')` / `Lang.queryJS('...')` (`js.*` keys) in scripts and `queryEJS` (`ejs.*` keys) in templates. Add any new user-facing string to the TOML rather than hardcoding it.

## Conventions

- ESLint stylistic rules are enforced and unusual: **no semicolons**, single quotes, 4-space indent, and **Windows (CRLF) line endings**. Run `npm run lint` before finishing; match the existing style exactly.
- `no-var` is on (use `const`/`let`). Unused args are allowed when prefixed `_` or named `reject`.

## Distribution tooling — `tools/` (NeoForge 1.21.1)

Utopia runs **NeoForge 1.21.1** (not Fabric like Nerysia). See [tools/README-UTOPIA.md](tools/README-UTOPIA.md) for the full workflow. Two-step pipeline:

1. `generate-neoforge-core.ps1` — drives the official NeoForge installer to build the **loader core block** (a `ForgeHosted` module + `VersionManifest` submodule + 47 `Library` submodules, with real MD5s). Library URLs point at public maven, so the only file to self-host is the `version.json` (written to `tools/neoforge-upload/`, git-ignored). Output `tools/neoforge-core.json` is committed. Re-run only on NeoForge version change.
2. `generate-distribution.ps1` — scans the modpack folder (`forgemods/{required,optionaloff,optionalon}` + `files/`), emits mods as `ForgeMod`, injects `neoforge-core.json`, and writes `docs/distribution.json`.

`generate-distribution-from-ftp.py` is the old Fabric FTP variant — **not yet adapted to NeoForge** (marked at its top); use the `.ps1`. Distribution is hosted on `apk.nerysia.fr/utopia-laucher/`; server `node.hloureiro.fr:45536`.

The generated structure was validated by parsing it through helios-core's `HeliosDistribution`, but a real modded game launch has **not** been verified — that must be tested on the deploy machine.

## Branding & placeholders to fill

Utopia-specific values already set: `package.json`, `electron-builder.yml` (`appId: fr.utopia.launcher`, publish `Oracios/UtopiaLauncher`), `dev-app-update.yml`, `_custom.toml`, update URLs in `settings.js`/`uicore.js`. Images: `Logo.png → SealCircle.png/.ico`, `GRAND_Utopia.png → UtopiaTitle.png` (shown on the landing page).

**Still placeholders (search `TODO UTOPIA`):**
- `REMOTE_DISTRO_URL` in [distromanager.js](app/assets/js/distromanager.js) → `apk.utopia.fr` (hosting not live yet).
- Social/website links in [_custom.toml](app/assets/lang/_custom.toml) (Discord, site).
- `AZURE_CLIENT_ID` in [ipcconstants.js](app/assets/js/ipcconstants.js) is still the shared Helios client id — see [docs/MicrosoftAuth.md](docs/MicrosoftAuth.md). Distribution format: [docs/distro.md](docs/distro.md).

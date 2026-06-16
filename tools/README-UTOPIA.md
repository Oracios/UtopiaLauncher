# Outils Utopia — génération de la distribution (NeoForge 1.21.1)

Le serveur Utopia tourne en **NeoForge 1.21.1**. Le launcher a été **patché** pour
charger les mods façon NeoForge (voir plus bas). Voici comment produire et publier
le `distribution.json`.

## Vue d'ensemble

| Élément | Rôle |
|---|---|
| `generate-neoforge-core.ps1` | Génère le **cœur NeoForge** (le loader + ses 47 bibliothèques). À relancer **seulement** quand tu changes de version NeoForge. |
| `neoforge-core.json` | Le bloc cœur généré (injecté automatiquement). **Committé.** |
| `neoforge-upload/` | Le(s) fichier(s) à **héberger sur ton FTP**. Pas committé. |
| `generate-distribution.ps1` | Scanne ton modpack (mods + fichiers) et assemble le `distribution.json` final, en injectant le cœur NeoForge. |
| `get-mod-info.ps1` | Petit helper (infos d'un mod). Optionnel. |
| `generate-distribution-from-ftp.py` | ⚠️ Variante FTP **encore en Fabric, non adaptée NeoForge**. Ne pas utiliser tel quel. |

## Étape 1 — Générer le cœur NeoForge (rare)

À faire une fois, et seulement si tu changes la version de NeoForge.

```powershell
& "tools/generate-neoforge-core.ps1"            # version 21.1.233 par défaut
# ou : & "tools/generate-neoforge-core.ps1" -Version 21.1.240
```

Ça produit :
1. `tools/neoforge-core.json` — le bloc cœur (utilisé automatiquement à l'étape 2).
2. `tools/neoforge-upload/versions/neoforge-<ver>/neoforge-<ver>.json` — **à uploader**
   sur ton FTP à la racine du repo, c.-à-d. vers
   `apk.nerysia.fr/utopia-laucher/versions/neoforge-<ver>/neoforge-<ver>.json`.

Les 47 bibliothèques NeoForge pointent directement vers les dépôts maven publics
(maven.neoforged.net / Mojang) : **rien d'autre à héberger**.

## Étape 2 — Générer le distribution.json (à chaque MAJ du modpack)

Range tes mods et fichiers sous `servers/Utopia-1.21.1/` (sur `Y:\apk\...`) :

```
servers/Utopia-1.21.1/
  forgemods/required/      <- mods obligatoires (.jar)
  forgemods/optionaloff/   <- mods optionnels désactivés par défaut
  forgemods/optionalon/    <- mods optionnels activés par défaut
  files/                   <- configs, resourcepacks, shaders...
```

Puis :

```powershell
& "tools/generate-distribution.ps1"              # sans bump
& "tools/generate-distribution.ps1" -Bump patch  # 1.0.0 -> 1.0.1
& "tools/generate-distribution.ps1" -Bump minor   # ajout d'un mod
```

Le script injecte le cœur NeoForge (`neoforge-core.json`), scanne les mods en
`ForgeMod` + les fichiers, et écrit `docs/distribution.json` (puis l'upload sur `Y:` si monté).

## Comment le launcher charge les mods NeoForge

NeoForge (et Forge 1.20.3+) a supprimé l'argument `--fml.modLists` qu'utilisait
Helios. Le launcher a donc été patché ([processbuilder.js](../app/assets/js/processbuilder.js),
méthode `setupNeoForgeMods`) : quand le loader est NeoForge, il **copie les mods
activés dans le dossier `mods/` de l'instance** (et les suit via
`.utopia-managed-mods.json` pour ne pas écraser tes mods ajoutés à la main).

## ⚠️ À tester sur ta machine

Toute la **structure** a été validée (parsing par helios-core OK), mais le
**lancement réel du jeu modé n'a pas pu être testé** ici. À vérifier chez toi :
1. Le launcher télécharge bien NeoForge + les 47 libs sans erreur.
2. Les mods apparaissent dans `instances/Utopia-1.21.1/mods/`.
3. Le jeu démarre en NeoForge avec le modpack chargé.

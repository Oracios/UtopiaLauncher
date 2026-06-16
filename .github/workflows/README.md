# ⚙️ Workflows GitHub Actions — Utopia Launcher

Ce dossier contient les automatisations GitHub du launcher. Voici à quoi elles servent
et comment les utiliser.

## 📋 Les 3 workflows

| Workflow | Fichier | Déclencheur | Ce qu'il fait |
|---|---|---|---|
| **Build & Release** | `release.yml` | Push d'un tag `v*` | Compile le launcher (Windows + Linux) et publie une **Release GitHub** |
| **Deploy News** | `deploy-news.yml` | Modif de `docs/feed.xml` (ou bouton) | Envoie les **actualités** (`feed.xml`) sur le FTP |
| **Update Modpack** | `update-modpack.yml` | Bouton **Run workflow** | Régénère le **`distribution.json`** depuis le FTP et le ré-uploade |

---

## 🔐 Secrets à configurer (une seule fois)

Deux workflows ont besoin d'accéder au FTP OVH. Va dans :

**Settings → Secrets and variables → Actions → New repository secret**

Et ajoute ces 3 secrets :

| Nom du secret | Valeur |
|---|---|
| `FTP_HOST` | l'adresse du serveur FTP OVH (ex. `ftp.cluster0xx.hosting.ovh.net`) |
| `FTP_USERNAME` | ton identifiant FTP |
| `FTP_PASSWORD` | ton mot de passe FTP |

> 🔒 Ne mets **jamais** ces valeurs en clair dans le code. Les secrets sont chiffrés par GitHub.
> Le secret `GITHUB_TOKEN` (utilisé par la Release) est fourni **automatiquement**, rien à faire.

---

## 🚀 Comment publier une nouvelle version du launcher

1. Mets à jour le numéro de version dans `package.json` (ex. `"version": "1.0.1"`).
2. Commit + push sur `master`.
3. Crée et pousse un tag correspondant :
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```
4. Le workflow **Build & Release** se lance tout seul et publie l'installeur dans
   **Releases** (Windows `.exe` + Linux `.AppImage`). Les utilisateurs reçoivent la MAJ automatiquement.

---

## 📰 Comment publier une actualité

1. Édite **`docs/feed.xml`** (ajoute un `<item>` en haut — voir [docs/news/README.md](../../docs/news/README.md)).
2. Commit + push sur `master`.
3. Le workflow **Deploy News** envoie le fichier sur le FTP → l'actu apparaît dans le launcher.

> Tu peux aussi le relancer à la main : onglet **Actions → Deploy News → Run workflow**.

---

## 🧩 Comment mettre à jour le modpack (sans le PC)

1. Mets tes mods/fichiers à jour sur le FTP (dossiers `forgemods/` et `files/`).
2. Va dans **Actions → Update Modpack → Run workflow**.
3. Choisis le type de bump :
   | Bump | Quand |
   |---|---|
   | `patch` | petit fix (config, MAJ d'un mod) — 1.0.0 → 1.0.1 |
   | `minor` | ajout d'un mod / système — 1.0.0 → 1.1.0 |
   | `major` | gros changement (version MC/NeoForge) — 1.0.0 → 2.0.0 |
   | `none` | régénère sans changer la version |
4. Le `distribution.json` est régénéré et ré-uploadé sur le FTP automatiquement.

> 💡 Sur ton PC, tu peux faire la même chose en local avec `tools/generate-distribution.ps1`
> (drive `Y:` monté). Voir [tools/README-UTOPIA.md](../../tools/README-UTOPIA.md).

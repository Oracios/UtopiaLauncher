# Installer le launcher Utopia sur Linux

Guide pas à pas pour installer le launcher Utopia sur Linux.
Le launcher est distribué en **AppImage** : un fichier unique, sans installation système, qui fonctionne sur la plupart des distributions.

---

## 1. Télécharger

👉 **Page de téléchargement :** https://github.com/Oracios/UtopiaLauncher/releases/latest

Récupère le fichier :

```
Utopia-Launcher-setup-X.X.X.AppImage
```

> ℹ️ Uniquement en **x86_64 (64 bits)**. Il n'y a pas de version ARM (Raspberry Pi, etc.).

---

## 2. Rendre le fichier exécutable

Un AppImage fraîchement téléchargé n'a pas le droit de s'exécuter. Il faut le lui donner — **une seule fois**.

**En ligne de commande :**

```bash
chmod +x Utopia-Launcher-setup-*.AppImage
```

**Ou avec la souris :** clic droit sur le fichier → **Propriétés** → onglet **Permissions** → coche
*« Autoriser l'exécution du fichier comme un programme »*.

Ensuite, double-clique dessus (ou lance-le depuis le terminal) :

```bash
./Utopia-Launcher-setup-*.AppImage
```

> 💡 Range le fichier dans un dossier stable (par exemple `~/Applications/`) : c'est lui, l'application.
> Si tu le supprimes ou le déplaces, le launcher n'est plus accessible.

---

## 3. Si l'AppImage refuse de démarrer

Deux cas très courants sur les distributions récentes.

### a) Erreur « libfuse.so.2 » / « dlopen(): error loading libfuse.so.2 »

Les AppImages ont besoin de **FUSE 2**, qui n'est plus installé par défaut sur les distributions récentes.

| Distribution | Commande |
| --- | --- |
| Ubuntu 24.04 et plus | `sudo apt install libfuse2t64` |
| Ubuntu 22.04 / Debian | `sudo apt install libfuse2` |
| Fedora | `sudo dnf install fuse-libs` |
| Arch / Manjaro | `sudo pacman -S fuse2` |

Relance ensuite l'AppImage.

### b) Erreur de « sandbox » ou fenêtre qui ne s'ouvre pas (Ubuntu 24.04+)

Les versions récentes d'Ubuntu restreignent un mécanisme utilisé par les applications Electron.
Symptômes : message contenant `SUID sandbox`, `namespace`, ou rien qui ne s'affiche du tout.

Lance alors le launcher ainsi :

```bash
./Utopia-Launcher-setup-*.AppImage --no-sandbox
```

> ℹ️ Cette option désactive une couche d'isolation interne du moteur graphique. C'est le contournement
> habituel pour les applications Electron sur Ubuntu 24.04, sans conséquence pour un launcher de jeu.

---

## 4. Premier lancement

Au premier démarrage, le launcher va :

1. Te demander de te connecter avec ton **compte Microsoft** (celui de Minecraft)
2. Télécharger automatiquement **Java** — rien à installer toi-même
3. Télécharger le **modpack** (plusieurs Go, prévois du temps selon ta connexion)

Ensuite le bouton **JOUER** se débloque et Minecraft se lance avec tous les mods.

Aux lancements suivants, le launcher vérifie tout seul si le modpack a changé et ne retélécharge que ce qui est nouveau.

---

## 5. Les mises à jour

**Elles sont automatiques sur Linux.** Quand une nouvelle version du launcher sort :

1. Elle se télécharge en arrière-plan
2. Une pastille apparaît sur le logo Utopia, en haut à gauche
3. Clique dessus → onglet **Updates** (l'interface du launcher est en anglais) → bouton **Install Now**
4. Le launcher redémarre à jour

Pour que la mise à jour automatique fonctionne, le fichier AppImage doit se trouver dans un dossier
où ton utilisateur a le **droit d'écrire** (ton dossier personnel, par exemple) — pas dans `/opt` ou `/usr/local`.

Les mises à jour **du modpack** (les mods) se font aussi toutes seules au lancement.

---

## 6. Ajouter le launcher au menu des applications (optionnel)

Un AppImage n'apparaît pas dans le menu de ton bureau par défaut. Le plus simple est d'installer
**AppImageLauncher**, qui propose de l'intégrer automatiquement au premier lancement :

```bash
# Ubuntu / Debian
sudo apt install appimagelauncher
```

Sinon, tu peux simplement garder un raccourci vers le fichier sur ton bureau.

---

## 7. En cas de problème

### Le téléchargement du modpack reste bloqué

Ferme complètement le launcher et rouvre-le : il reprend là où il s'était arrêté.
Si ça bloque encore, c'est souvent une coupure temporaire des serveurs de Mojang — réessaie plus tard.

### Voir les messages d'erreur détaillés

Lance le launcher depuis un terminal : les erreurs s'affichent directement dans la fenêtre.

```bash
./Utopia-Launcher-setup-*.AppImage
```

C'est le plus utile à copier si tu demandes de l'aide.

### Repartir de zéro proprement

```bash
rm -rf ~/.utopialauncher
```

> ⚠️ Cela supprime aussi tes mondes solo et tes réglages de jeu.
> Le dossier `~/.config/Utopia Launcher` contient ta connexion : le supprimer te déconnectera, sans plus de dégâts.

### Autre souci

Demande de l'aide sur le **Discord d'Utopia** en précisant :
- ta distribution et sa version (ex. Ubuntu 24.04, Fedora 41…),
- la version du launcher (réglages ⚙️ → onglet **About**),
- le message d'erreur affiché dans le terminal.

---

## Questions fréquentes

**Faut-il installer Java ou NeoForge soi-même ?**
Non. Le launcher télécharge et gère Java, NeoForge et tous les mods automatiquement.

**Où sont installés les fichiers du jeu ?**
Dans `~/.utopialauncher` (mods, configs, mondes solo). Le launcher gère tout seul son contenu.

**Le jeu fonctionne-t-il sous Wayland ?**
Oui dans la grande majorité des cas. En cas d'affichage bizarre, essaie de démarrer ta session en **Xorg**
depuis l'écran de connexion.

**Ai-je besoin des pilotes graphiques propriétaires ?**
Minecraft moderne avec des shaders demande une bonne accélération 3D. Sur carte NVIDIA, les pilotes
propriétaires sont fortement recommandés.

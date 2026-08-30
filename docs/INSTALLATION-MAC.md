# Installer le launcher Utopia sur Mac

Guide pas à pas pour installer le launcher Utopia sur macOS.
**Compte 5 minutes.** L'étape 3 est un peu inhabituelle mais elle ne se fait qu'une seule fois.

---

## 1. Choisir le bon fichier

Il existe deux versions du launcher : une pour les Mac **Apple Silicon** et une pour les Mac **Intel**.

**Pour savoir lequel tu as :**
clique sur le menu  (en haut à gauche) → **À propos de ce Mac**.

| Ce que tu lis | Le fichier à télécharger |
|---|---|
| « Puce **Apple** M1 / M2 / M3 / M4 » | `Utopia-Launcher-setup-X.X.X-**arm64**.dmg` |
| « Processeur **Intel** » | `Utopia-Launcher-setup-X.X.X-**x64**.dmg` |

👉 **Télécharge ici :** https://github.com/Oracios/UtopiaLauncher/releases/latest

> Si tu te trompes de version, le launcher refusera de s'ouvrir ou sera très lent : reprends simplement l'autre fichier.

---

## 2. Installer

1. Double-clique sur le fichier `.dmg` que tu viens de télécharger
2. Une fenêtre s'ouvre : **glisse l'icône Utopia Launcher sur le dossier Applications**
3. Ferme la fenêtre, tu peux éjecter le disque `Utopia Launcher` dans le Finder

---

## 3. Autoriser le launcher (important, une seule fois)

Le launcher n'est pas « signé » auprès d'Apple (cela coûte un abonnement annuel de développeur).
macOS le bloque donc au premier lancement. **Ce n'est pas un virus, c'est juste la sécurité d'Apple qui ne connaît pas encore l'application.**

Voici comment l'autoriser :

1. Ouvre le dossier **Applications** et double-clique sur **Utopia Launcher**
2. Un message apparaît : *« Utopia Launcher n'a pas pu être ouvert car Apple n'a pas pu vérifier qu'il ne contient pas de logiciel malveillant »* → clique sur **OK** (ou **Terminer**)
3. Ouvre les **Réglages Système** (menu  → Réglages Système)
4. Va dans **Confidentialité et sécurité**
5. Descends tout en bas de la page : tu verras une ligne
   *« Utopia Launcher a été bloqué car il ne provient pas d'un développeur identifié »*
6. Clique sur le bouton **Ouvrir quand même**
7. Confirme avec ton mot de passe Mac ou Touch ID
8. Une dernière fenêtre s'affiche → clique sur **Ouvrir**

✅ C'est fini. Les fois suivantes, le launcher s'ouvrira normalement d'un simple double-clic.

> **Sur les anciennes versions de macOS** (Monterey, Ventura, Sonoma), tu peux aussi faire un
> **clic droit sur l'application → Ouvrir** puis confirmer **Ouvrir**. Sur macOS Sequoia (15) et plus
> récent, cette astuce ne fonctionne plus : il faut passer par les Réglages Système comme ci-dessus.

---

## 4. Premier lancement

Au premier démarrage, le launcher va :

1. Te demander de te connecter avec ton **compte Microsoft** (celui de Minecraft)
2. Télécharger automatiquement **Java** (tu n'as rien à installer toi-même)
3. Télécharger le **modpack** (plusieurs Go — compte un bon moment selon ta connexion)

Ensuite, le bouton **JOUER** se débloque et Minecraft se lance avec tous les mods.

Les fois suivantes, le launcher vérifie tout seul si le modpack a changé et télécharge uniquement ce qui est nouveau.

---

## 5. Les mises à jour du launcher sur Mac

Sur Windows, le launcher se met à jour tout seul. **Sur Mac, comme l'application n'est pas signée, la mise à jour automatique n'est pas possible.**

Quand une nouvelle version du launcher sort, voici ce qui se passe :

1. Une **pastille de notification** apparaît sur le logo Utopia, en haut à gauche du launcher
2. Clique dessus : le launcher t'emmène dans l'onglet **Updates** (l'interface est en anglais)
3. Clique sur le bouton **Download from GitHub** : le téléchargement du nouveau `.dmg` s'ouvre dans ton navigateur
4. Ferme le launcher, ouvre le `.dmg` et glisse-le dans **Applications** en remplaçant l'ancien
5. Relance le launcher

⚠️ Tu n'auras **pas** à refaire l'étape 3 (l'autorisation) : elle n'est demandée qu'à la toute première installation.

> ℹ️ Ceci ne concerne que les mises à jour **du launcher**. Les mises à jour **du modpack** (les mods), elles, se font toujours automatiquement.

---

## 6. En cas de problème

### « L'application est endommagée et ne peut pas être ouverte »

Ce message apparaît parfois sur les Mac Apple Silicon. Il ne veut pas dire que le fichier est corrompu :
macOS a simplement mis l'application en quarantaine. Pour la libérer :

1. Ouvre l'application **Terminal** (Applications → Utilitaires → Terminal)
2. Copie-colle exactement cette ligne, puis appuie sur **Entrée** :

```bash
xattr -cr "/Applications/Utopia Launcher.app"
```

3. Relance le launcher

### Le launcher ne s'ouvre pas du tout / se ferme aussitôt

Tu as probablement téléchargé la mauvaise version (Intel au lieu d'Apple Silicon, ou l'inverse).
Reprends l'**étape 1** pour vérifier, et télécharge l'autre fichier.

### Le téléchargement du modpack reste bloqué

Ferme complètement le launcher et rouvre-le : il reprend là où il s'était arrêté.
Si le blocage persiste, c'est souvent une coupure temporaire des serveurs de Mojang — réessaie un peu plus tard.

### Autre souci

Demande de l'aide sur le **Discord d'Utopia**, en précisant :
- ton modèle de Mac (Apple Silicon ou Intel) et ta version de macOS,
- la version du launcher (réglages ⚙️ → onglet **About**),
- une capture d'écran du message d'erreur.

---

## Questions fréquentes

**Est-ce dangereux d'installer une app non signée ?**
Le blocage d'Apple signifie seulement que l'application n'a pas été soumise à Apple (une démarche payante pour le développeur), pas qu'elle est malveillante. Ne télécharge le launcher **que** depuis la page officielle des versions :
https://github.com/Oracios/UtopiaLauncher/releases

**Où sont installés les fichiers du jeu ?**
Dans `~/Library/Application Support/.utopialauncher` (dossier caché). Le launcher gère tout seul son contenu.
Pour y accéder : dans le Finder, menu **Aller** → **Aller au dossier…** et colle ce chemin.

**Puis-je supprimer le `.dmg` après installation ?**
Oui, une fois l'application copiée dans Applications, le `.dmg` ne sert plus à rien.

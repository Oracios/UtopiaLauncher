# Installer le launcher Utopia sur Windows

Guide pas à pas pour installer le launcher Utopia sur Windows.
**Compte 3 minutes.** L'étape 2 affiche un avertissement de sécurité : c'est normal, tout est expliqué.

---

## 1. Télécharger

👉 **Page de téléchargement :** https://github.com/Oracios/UtopiaLauncher/releases/latest

Récupère le fichier :

```
Utopia-Launcher-setup-X.X.X.exe
```

> ℹ️ Le launcher existe uniquement en **64 bits**, ce qui couvre tous les PC Windows modernes.
> Windows 10 ou Windows 11 sont recommandés.

---

## 2. Le message « Windows a protégé votre ordinateur »

Le launcher n'est pas signé avec un certificat payant. Windows affiche donc un écran bleu d'avertissement au moment de lancer l'installeur. **Ce n'est pas un virus** : Windows signale simplement qu'il ne connaît pas encore ce programme.

Pour continuer :

1. Double-clique sur le fichier `.exe` téléchargé
2. Une fenêtre bleue apparaît : *« Windows a protégé votre ordinateur »*
3. Clique sur **Informations complémentaires** (le petit texte, souvent souligné)
4. Un bouton **Exécuter quand même** apparaît en bas → clique dessus

L'installation démarre normalement.

> 🛡️ **Si ton antivirus bloque le fichier** (Avast, Norton, McAfee…), c'est le même phénomène :
> un programme récent et non signé est parfois signalé à tort. Tu peux l'autoriser, ou l'ajouter aux
> exceptions. **Ne télécharge le launcher que depuis la page officielle ci-dessus.**

---

## 3. Installer

L'installeur te guide en quelques écrans :

1. Choisis si tu installes **pour toi uniquement** (recommandé, aucun droit administrateur nécessaire) ou pour tous les utilisateurs
2. Tu peux **changer le dossier d'installation** si tu veux, sinon laisse celui proposé
3. Clique sur **Installer**, puis **Terminer**

Un raccourci **Utopia Launcher** est créé dans le menu Démarrer (et sur le bureau).

---

## 4. Premier lancement

Au premier démarrage, le launcher va :

1. Te demander de te connecter avec ton **compte Microsoft** (celui de Minecraft)
2. Télécharger automatiquement **Java** — tu n'as rien à installer toi-même
3. Télécharger le **modpack** (plusieurs Go, compte un bon moment selon ta connexion)

Ensuite le bouton **JOUER** se débloque et Minecraft se lance avec tous les mods.

Aux lancements suivants, le launcher vérifie tout seul si le modpack a changé et ne retélécharge que ce qui est nouveau.

---

## 5. Les mises à jour

**Tout est automatique sur Windows.** Quand une nouvelle version du launcher sort :

1. Elle se télécharge en arrière-plan
2. Une pastille apparaît sur le logo Utopia en haut à gauche
3. Clique dessus → onglet **Updates** (l'interface du launcher est en anglais) → bouton **Install Now**
4. Le launcher redémarre à jour

Les mises à jour **du modpack** (les mods) se font également toutes seules au lancement.

---

## 6. En cas de problème

### Le launcher ne se lance pas / se ferme aussitôt

1. Redémarre le PC (souvent suffisant après une installation)
2. Vérifie que ton antivirus n'a pas mis le launcher en quarantaine
3. Réinstalle par-dessus avec le dernier `.exe` de la page officielle

### Le téléchargement du modpack reste bloqué

Ferme complètement le launcher et rouvre-le : il reprend là où il s'était arrêté.
Si ça bloque encore, c'est souvent une coupure temporaire des serveurs de Mojang — réessaie plus tard.

### « Java » ou une erreur au lancement du jeu

Le launcher installe sa propre version de Java, tu n'as pas à en installer une.
Si le message persiste, ouvre les réglages (icône ⚙️) → onglet **Java** et laisse le launcher réinstaller Java.

### Repartir de zéro proprement

Tu peux supprimer le dossier de jeu pour forcer un retéléchargement complet :

1. Appuie sur **Windows + R**
2. Colle `%APPDATA%` puis **Entrée**
3. Supprime le dossier **`.utopialauncher`**

> ⚠️ Cela supprime aussi tes mondes solo et tes réglages de jeu. Le dossier `Utopia Launcher`
> (à côté) contient ta connexion : le supprimer te déconnectera, sans plus de dégâts.

### Autre souci

Demande de l'aide sur le **Discord d'Utopia** en précisant :
- ta version de Windows,
- la version du launcher (réglages ⚙️ → onglet **About**),
- une capture d'écran du message d'erreur.

---

## Questions fréquentes

**Faut-il installer Java ou NeoForge soi-même ?**
Non. Le launcher télécharge et gère Java, NeoForge et tous les mods automatiquement.

**Où sont installés les fichiers du jeu ?**
Dans `%APPDATA%\.utopialauncher` (mods, configs, mondes solo).

**Puis-je supprimer le `.exe` après installation ?**
Oui, une fois l'installation terminée il ne sert plus à rien.

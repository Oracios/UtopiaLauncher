# 📰 Les actualités du launcher Utopia

Les news qui s'affichent dans le launcher viennent du fichier **`docs/feed.xml`**
(format RSS). Quand tu le modifies et que tu push, le workflow **Deploy News** l'envoie
sur le FTP, et l'actu apparaît dans le launcher des joueurs.

> 📍 Fichier à éditer : **[`docs/feed.xml`](../feed.xml)**
> 🌐 En ligne sur : `https://apk.nerysia.fr/utopia-laucher/feed.xml`

---

## ✍️ Publier une actu (3 étapes)

1. Génère ton bloc `<item>` (à la main, ou avec une IA — voir plus bas 👇).
2. Colle-le dans **`docs/feed.xml`**, **juste après `<channel>`** (le plus récent doit être **tout en haut**).
3. Commit + push sur `master` → le workflow Deploy News publie automatiquement.

> 💡 Tu peux aussi lancer la publication à la main : onglet **Actions → Deploy News → Run workflow**.

---

## 🤖 Faire écrire l'actu par une IA (recommandé)

Copie-colle **tout le bloc de prompt ci-dessous** dans n'importe quelle IA (ChatGPT, Claude,
Gemini, Le Chat, Copilot…). Remplace seulement la partie **« CE QUE JE VEUX ANNONCER »** par
ton texte (même écrit en vrac), et l'IA te rendra un bloc `<item>` **propre et bien mis en
page**, prêt à coller dans `docs/feed.xml`.

> ⬇️ **PROMPT À COPIER (tout, du début à la fin)** ⬇️

````text
Tu génères une actualité pour le launcher du serveur Minecraft "Utopia", au format RSS.

Rends-moi UNIQUEMENT un bloc <item>...</item> (aucune explication, aucun texte autour).
IMPORTANT : n'entoure PAS ta réponse de barrières de code markdown (pas de ```xml, pas de ```).
Donne le bloc <item> brut, directement.

Respecte EXACTEMENT cette structure :

    <item>
      <title>Titre court et accrocheur</title>
      <link>https://apk.nerysia.fr</link>
      <pubDate>METS_LA_DATE_ICI</pubDate>
      <dc:creator>Oracios</dc:creator>
      <slash:comments>0</slash:comments>
      <content:encoded><![CDATA[
        ... le contenu HTML ici ...
      ]]></content:encoded>
    </item>

RÈGLES DE MISE EN PAGE (très important, c'est ça qui rend l'actu belle) :
- Commence par un grand titre <h2> avec un emoji au début. Ex : <h2>🎉 Grosse mise à jour !</h2>
- Ensuite un court paragraphe <p> d'introduction (1-2 phrases).
- Découpe le reste en sections : chaque section = un <h3> avec un emoji, suivi d'une liste <ul><li>...</li></ul>.
- Mets en <strong>gras</strong> les mots-clés importants (noms d'objets, chiffres, commandes, nouveautés).
- Pour les commandes ou termes techniques, utilise <code>/macommande</code>.
- Termine par un petit <p><em>une phrase de fin sympa</em> avec un emoji</p>.
- Utilise des emojis pertinents (🎉 ⚔️ 🌴 💰 🔧 🐛 🎮 🛡️ ✨ 📌 …).
- Écris en FRANÇAIS.
- Balises AUTORISÉES UNIQUEMENT : <h2> <h3> <p> <ul> <li> <ol> <strong> <em> <code> <a href="...">. Aucune autre balise.
- pubDate doit être au format EXACT : "Jjj, JJ Mmm AAAA HH:MM:SS +0200", avec le jour et le mois
  en ANGLAIS abrégés. Jours : Mon Tue Wed Thu Fri Sat Sun. Mois : Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec.
  Exemple : Tue, 17 Jun 2026 19:00:00 +0200. Mets la date et l'heure d'aujourd'hui.

EXEMPLE de rendu attendu (inspire-toi de ce style, ne le recopie pas tel quel) :

    <item>
      <title>Mise à jour majeure — Économie & nouveaux décors</title>
      <link>https://apk.nerysia.fr</link>
      <pubDate>Tue, 17 Jun 2026 19:00:00 +0200</pubDate>
      <dc:creator>Oracios</dc:creator>
      <slash:comments>0</slash:comments>
      <content:encoded><![CDATA[
        <h2>🎉 Une grosse mise à jour vient d'arriver !</h2>
        <p>Relance simplement le launcher pour tout télécharger automatiquement. Voici ce qui change.</p>

        <h3>💰 Économie</h3>
        <ul>
          <li>Les <strong>Utopièces</strong> rapportent désormais plus en vendant tes productions</li>
          <li>Nouvelle commande <code>/shop</code> pour ouvrir ta boutique</li>
        </ul>

        <h3>🌴 Nouveautés sur l'île</h3>
        <ul>
          <li><strong>+40 nouveaux meubles</strong> et décorations</li>
          <li>Une nouvelle zone d'événements au centre de l'île</li>
        </ul>

        <h3>🐛 Corrections</h3>
        <ul>
          <li>Correction d'un bug de duplication</li>
          <li>Meilleures performances</li>
        </ul>

        <p><em>Bon jeu sur Utopia ! 🌴</em></p>
      ]]></content:encoded>
    </item>

CE QUE JE VEUX ANNONCER (récris-le proprement, c'est juste mes notes en vrac) :
"""
👉 écris ici ce que tu veux annoncer
"""
````

Une fois la réponse de l'IA obtenue, **colle son bloc `<item>` en haut de [`docs/feed.xml`](../feed.xml)**
(juste après `<channel>`), puis commit + push. C'est tout. ✅

---

## 🧱 Rappel : balises utilisables dans le texte

| Balise | Effet |
|---|---|
| `<h2>` `<h3>` | Titres / sous-titres |
| `<p>` | Paragraphe |
| `<ul><li>` | Liste à puces |
| `<ol><li>` | Liste numérotée |
| `<strong>` | **Gras** |
| `<em>` | *Italique* |
| `<code>` | `texte en code` |
| `<a href="...">` | Lien cliquable |

Les emojis (🎉 🌴 ⚔️) fonctionnent directement.

---

## ⚠️ Règles importantes (à vérifier après l'IA)

- **Le plus récent en haut** : le launcher affiche les `<item>` dans l'ordre du fichier.
- **La date** suit ce format exact : `Jjj, JJ Mmm AAAA HH:MM:SS +0200`
  (ex. `Tue, 17 Jun 2026 19:00:00 +0200`). Jour et mois en anglais.
- **Ne casse pas le XML** : chaque `<item>` doit être bien fermé (`</item>`), et le contenu HTML
  doit rester **à l'intérieur** du `<![CDATA[ ... ]]>`.
- Garde toujours la structure `<rss> … <channel> … </channel> </rss>` intacte.
- Un modèle simple sans IA est aussi dispo dans **[`exemple-article.xml`](exemple-article.xml)**.

> 🧪 En cas de doute, compare avec [`docs/feed.xml`](../feed.xml) qui contient déjà des articles d'exemple.

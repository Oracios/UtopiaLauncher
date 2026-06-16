# 📰 Les actualités du launcher Utopia

Les news qui s'affichent dans le launcher viennent d'un fichier **`docs/feed.xml`**
(format RSS). Quand tu le modifies et que tu push, le workflow **Deploy News** l'envoie
sur le FTP, et l'actu apparaît dans le launcher des joueurs.

> 📍 Fichier à éditer : **[`docs/feed.xml`](../feed.xml)**
> 🌐 En ligne sur : `https://apk.nerysia.fr/utopia-laucher/feed.xml`

---

## ✍️ Ajouter une actualité (3 étapes)

1. Ouvre **`docs/feed.xml`**.
2. Copie le **modèle ci-dessous** et colle-le **juste après `<channel>`** (le plus
   récent doit être **tout en haut**, avant les autres `<item>`).
3. Commit + push sur `master` → le workflow Deploy News publie automatiquement.

> 💡 Tu peux aussi lancer la publication à la main : onglet **Actions → Deploy News → Run workflow**.

---

## 📋 Modèle d'article (à copier-coller)

Un exemple complet et prêt à copier est dans **[`exemple-article.xml`](exemple-article.xml)**.

```xml
    <item>
      <title>Titre de ton actu</title>
      <link>https://apk.nerysia.fr</link>
      <pubDate>Mon, 16 Jun 2026 20:00:00 +0200</pubDate>
      <dc:creator>Oracios</dc:creator>
      <slash:comments>0</slash:comments>
      <content:encoded><![CDATA[
        <h2>🎉 Un grand titre</h2>
        <p>Ton texte d'introduction.</p>

        <h3>🔧 Une section</h3>
        <ul>
          <li>Un point <strong>important</strong></li>
          <li>Un autre point</li>
        </ul>

        <p><em>Un mot de fin.</em></p>
      ]]></content:encoded>
    </item>
```

---

## 🧱 Ce que tu peux mettre dans le texte

Le contenu (entre `<![CDATA[ ... ]]>`) accepte du **HTML simple** :

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

## ⚠️ Règles importantes

- **Le plus récent en haut** : le launcher affiche les `<item>` dans l'ordre du fichier.
- **La date** suit ce format exact : `Jour, JJ Mois AAAA HH:MM:SS +0200`
  (ex. `Mon, 16 Jun 2026 20:00:00 +0200`). Mois en anglais : `Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec`.
- **Ne casse pas le XML** : chaque `<item>` doit être bien fermé (`</item>`), et le
  contenu HTML doit rester **à l'intérieur** du `<![CDATA[ ... ]]>`.
- Garde toujours la structure `<rss> … <channel> … </channel> </rss>` intacte.

> 🧪 En cas de doute, compare avec [`docs/feed.xml`](../feed.xml) qui contient déjà 2 articles d'exemple.

# TubeDZ 🇩🇿 — YouTube Sans Publicité avec Identité Algérienne

**TubeDZ** est une version personnalisée et optimisée de l'application YouTube pour Android, conçue pour offrir une expérience de visionnage fluide, sans aucune interruption publicitaire, avec un thème sombre élégant et une identité visuelle algérienne unique.

---

## ✨ Fonctionnalités Principales
- 🚫 **Bloqueur Intégral de Publicités :** Suppression totale de toutes les publicités vidéo (au début et au milieu), des bannières promotionnelles et des annonces dans les Shorts.
- 🎧 **Lecture en Arrière-Plan & Mode PiP :** Continuez à écouter de la musique ou des podcasts avec l'écran verrouillé pour économiser la batterie, ou profitez du lecteur flottant pendant l'utilisation d'autres applications.
- ⚡ **Installation Indépendante (Clone) :** Nom de package dédié (`anddea.youtube`), permettant d'installer TubeDZ côte à côte avec l'application YouTube officielle sans conflit ni écrasement.
- 🔐 **Connexion Compte Google Sécurisée :** Prise en charge complète de MicroG (GmsCore) pour synchroniser vos abonnements, playlists et historique en toute sécurité.
- ⏩ **Passer les Segments Sponsorisés (SponsorBlock) :** Saut automatique des intros, des segments de sponsoring et des appels aux dons intégrés aux vidéos.
- 🌙 **Thème Sombre Pur (AMOLED Black) :** Interface noire profonde (#000000) idéale pour les écrans OLED, réduisant la fatigue oculaire et la consommation de batterie.
- 🇩🇿 **Identité Nationale Algérienne :** Logo officiel et icônes haute résolution inspirés du drapeau algérien et du monument des Martyrs (Maqam Echahid).

---

## 📁 Structure du Projet
- [`index.html`](index.html) : Site web officiel bilingue (Français & Arabe) avec téléchargement direct et guide complet.
- [`logo.png`](logo.png) : Logo officiel haute résolution de TubeDZ.
- [`server.py`](server.py) : Serveur HTTP local ultra-rapide (ports `8080` et `3000`).
- [`build_tubedz.py`](build_tubedz.py) : Script Python d'automatisation de la construction, du patch et de la signature.
- [`tubedz.keystore`](tubedz.keystore) : Clé de signature officielle (RSA-2048, schémas V1/V2/V3).
- [`AndroidManifest.xml`](AndroidManifest.xml) : Manifeste Android configuré avec le nom indépendant TubeDZ.

---

## 🚀 Lancer le Serveur Web Local
```bash
python3 server.py
```
Accédez au site via :
`http://localhost:8080` ou `http://localhost:3000`

---

## 📦 Téléchargements (Releases GitHub)
Retrouvez les fichiers signés dans la section **Releases** de ce dépôt privé :
1. **TubeDZ.apk (145 Mo) :** Application principale signée et prête à installer.
   - SHA-256 : `a8fbb24f777527c69d4f42cc9aace7993c6bb2e36ad54a32274b2f23e1eba680`
2. **MicroG.apk (101 Mo) :** Package de connexion Google pour synchroniser vos données.
   - SHA-256 : `62119f040d629a9cd3225f280649a464936730c6466cafb5b9dd5ded14269a65`

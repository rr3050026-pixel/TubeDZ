# TubeDZ 🇩🇿 — YouTube Sans Publicité avec Identité Algérienne

<p align="center">
  <img src="logo.png" alt="TubeDZ Logo" width="120" style="border-radius: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.5);" />
</p>

<p align="center">
  <strong>Lecteur Web interactif et Application Android YouTube personnalisée, ultra-rapide et sans interruption publicitaire.</strong>
</p>

<p align="center">
  <a href="https://tubedz.onrender.com"><strong>🌐 Accéder au Site Web (tubedz.onrender.com)</strong></a> •
  <a href="#-téléchargements-releases-github">Téléchargements</a> •
  <a href="#-fonctionnalités-principales">Fonctionnalités</a> •
  <a href="README_AR.md">🇩🇿 النسخة العربية</a>
</p>

---

## 🌐 Site Web Officiel en Ligne
Le lecteur web sans publicité est accessible 24h/24 et 7j/7 sur :  
👉 **[https://tubedz.onrender.com](https://tubedz.onrender.com)**  
*(Miroir secondaire : [https://rr3050026-pixel.github.io/TubeDZ/](https://rr3050026-pixel.github.io/TubeDZ/))*

Vous pouvez y rechercher et regarder n'importe quelle vidéo YouTube sans publicité directement depuis votre navigateur, sur mobile ou ordinateur.

---

## ✨ Fonctionnalités Principales
- 🚫 **Bloqueur Intégral de Publicités :** Élimination totale de toutes les pubs vidéo (pré-roll, mid-roll), bannières promotionnelles et annonces dans les Shorts.
- 🎧 **Lecture Audio en Arrière-Plan & Mode PiP :** Écoutez vos vidéos même avec l'écran verrouillé pour économiser la batterie, ou profitez du lecteur flottant (Picture-in-Picture).
- ⚡ **Installation Indépendante (Clone) :** Nom de package dédié (`anddea.youtube`), permettant d'installer TubeDZ aux côtés de YouTube officiel sans aucun conflit.
- 🔐 **Connexion Compte Google Sécurisée :** Prise en charge intégrale du module MicroG (GmsCore) pour synchroniser abonnements, favoris et historique.
- ⏩ **SponsorBlock Automatique :** Saut intelligent des intros, segments sponsorisés intégrés par les créateurs et appels aux dons.
- 🌙 **Thème Sombre Pur (AMOLED Black) :** Interface noire absolue (#000000) conçue pour soulager les yeux et économiser la batterie sur écrans OLED.
- 🇩🇿 **Identité Visuelle Algérienne :** Icône et logo officiels inspirés des couleurs nationales et de Maqam Echahid.
- 🎧 **Mode YouTube Music (YT Music Mode) :** Un lecteur audio dédié inspiré de YouTube Music, avec disque vinyle rotatif, visualiseur d'ondes sonores (Audio Visualizer), bibliothèque musicale algérienne et internationale, et mini-lecteur flottant pour écouter en arrière-plan pendant la navigation.

---

## 📦 Téléchargements (Releases GitHub)
Les fichiers officiels sont disponibles directement dans la section **Releases** de ce dépôt :

| Fichier | Description | Taille | SHA-256 |
|---|---|---|---|
| **[TubeDZ.apk](https://github.com/rr3050026-pixel/TubeDZ/releases/download/v1.1.0/TubeDZ.apk)** | Application officielle signée | `145 Mo` | `a8fbb24f777527c69d4f42cc9aace7993c6bb2e36ad54a32274b2f23e1eba680` |
| **[microg.apk](https://github.com/rr3050026-pixel/TubeDZ/releases/download/v1.1.0/microg.apk)** | Module de connexion Google | `101 Mo` | `62119f040d629a9cd3225f280649a464936730c6466cafb5b9dd5ded14269a65` |

---

## 📋 Guide d'Installation Rapide
1. **Téléchargez `TubeDZ.apk`** depuis les liens ci-dessus.
2. Ouvrez le fichier et cochez **« Autoriser cette source »** dans les paramètres Android si demandé.
3. *(Optionnel pour connecter votre compte Google)* Téléchargez et installez **`microg.apk`**.
4. Lancez **TubeDZ** et profitez d'une expérience de visionnage pure !

---

## 📁 Structure du Projet
- [`index.html`](index.html) : Lecteur web interactif bilingue (Français par défaut avec commutateur Arabe dynamique).
- [`logo.png`](logo.png) : Logo officiel haute résolution de TubeDZ.
- [`server.py`](server.py) : Serveur HTTP local ultra-léger (ports `8080` et `3000`).
- [`build_tubedz.py`](build_tubedz.py) : Script Python d'automatisation de compilation, patch et signature.
- [`tubedz.keystore`](tubedz.keystore) : Clé de signature cryptographique (RSA-2048, schémas V1/V2/V3).
- [`AndroidManifest.xml`](AndroidManifest.xml) : Manifeste Android configuré avec le nom TubeDZ.

---

## 🚀 Démarrer le Serveur Web Local
```bash
python3 server.py
```
Puis ouvrez votre navigateur ou la vue web sur :
`http://localhost:8080` ou `http://localhost:3000`

---

## 🛡️ Sécurité & Intégrité
Toutes les versions publiées sont signées avec la clé officielle de signature de TubeDZ. Vous pouvez vérifier l'empreinte SHA-256 avec la commande :
```bash
sha256sum TubeDZ.apk
```

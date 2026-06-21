# INGEN SYSTEMS — Image Forensics Workstation v2.0
## Guide de Développement d'Effets

> **Classification :** Documentation Technique — Niveau Développeur  
> **Version :** 4.0 FORENSIC & HERITAGE UNIFIED  
> **Langage :** Python 3.x (PIL/Pillow + NumPy)

---

## Table des Matières

1. [Architecture du Système d'Effets](#1-architecture-du-système-deffets)
2. [Structure d'un Effet](#2-structure-dun-effet)
3. [API Interne Disponible](#3-api-interne-disponible)
4. [Catégories d'Effets](#4-catégories-deffets)
5. [Guide de Développement Pas à Pas](#5-guide-de-développement-pas-à-pas)
6. [Techniques Avancées](#6-techniques-avancées)
7. [Optimisation des Performances](#7-optimisation-des-performances)
8. [Débogage et Tests](#8-débogage-et-tests)
9. [Référence des Effets Intégrés](#9-référence-des-effets-intégrés)
10. [Bonnes Pratiques](#10-bonnes-pratiques)

---

## 1. Architecture du Système d'Effets

### 1.1 Vue d'Ensemble

Le système d'effets repose sur une architecture **déclarative + impérative** :

```
┌─────────────────────────────────────────────────────────────┐
│                    effects.json (Déclaratif)                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Métadonnées │  │  Paramètres │  │  Code Python (str)  │  │
│  │  (id, name)  │  │  (dict)     │  │  (exécuté via exec) │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              ImageAnalyzerApp._apply_effect_and_adjustments() │
│                    (Moteur d'exécution)                       │
│  1. Charge l'effet depuis effects.json                      │
│  2. Exécute le code via `apply_effect()`                    │
│  3. Applique les ajustements (brightness, contrast...)      │
│  4. Rafraîchit l'affichage                                  │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Flux d'Exécution

```python
# 1. Sélection de l'effet dans la ComboBox
self.current_effect_id = "mon_effet"

# 2. Déclenchement de _apply_effect_and_adjustments()
#    → Charge l'image originale (RGB)
#    → Exécute apply_effect(img, effect)
#    → Applique les ajustements utilisateur
#    → Met à jour l'affichage

# 3. Fonction apply_effect() (dans image_analyzer.py)
def apply_effect(img: Image.Image, effect: dict) -> Image.Image:
    params = effect.get("params", {})
    code = effect.get("code", "return img.copy()")
    local_ns = {"img": img, "params": params}

    # Le code est wrappé dans une fonction
    wrapped = "def _effect(img, params):\n"
    for line in code.splitlines():
        wrapped += "    " + line + "\n"

    exec(wrapped, local_ns)
    return local_ns["_effect"](img, params)
```

### 1.3 Sécurité d'Exécution

> ⚠️ **Important :** Le code des effets est exécuté via `exec()`. Cela offre une grande flexibilité mais implique que :
> - Tout module Python disponible dans l'environnement peut être importé
> - Les erreurs de syntaxe/runtime sont capturées et affichées dans une boîte de dialogue
> - Le code s'exécute dans le namespace local de `apply_effect()`

---

## 2. Structure d'un Effet

### 2.1 Schéma JSON Minimal

```json
{
  "id": "mon_effet_unique",
  "name": "Mon Effet Pro",
  "category": "custom",
  "description": "Description courte et claire de ce que fait l'effet",
  "params": {
    "param1": 42,
    "param2": "#ff0000",
    "param3": true
  },
  "code": "import numpy as np\nfrom PIL import Image\n# Votre code ici\nreturn img.copy()"
}
```

### 2.2 Champs Obligatoires

| Champ | Type | Description |
|-------|------|-------------|
| `id` | `str` | Identifiant unique, **snake_case**, sans espaces |
| `name` | `str` | Nom affiché dans l'interface (préfixer `[CUSTOM]` pour les effets personnalisés) |
| `category` | `str` | Catégorie fonctionnelle (voir §4) |
| `description` | `str` | Description affichée sous le sélecteur d'effets |
| `params` | `dict` | Paramètres par défaut (peut être vide `{}`) |
| `code` | `str` | Code Python exécutable (doit retourner un `PIL.Image.Image`) |

### 2.3 Conventions de Nommage

```
# IDs des effets intégrés
base_*, color_*, forensic_*, enhancement_*, artistic_*, 
distortion_*, blur_*, stylize_*, lighting_*, 
paleo_*, epi_*, stego_*, custom_*

# IDs des effets custom (créés par l'utilisateur)
# → Préfixer le name avec [CUSTOM] automatiquement
# → L'ID est fourni par l'utilisateur dans l'éditeur
```

---

## 3. API Interne Disponible

### 3.1 Variables Injectées

Lors de l'exécution du code d'un effet, deux variables sont **automatiquement injectées** :

| Variable | Type | Description |
|----------|------|-------------|
| `img` | `PIL.Image.Image` | Image d'entrée (toujours en mode compatible, souvent RGB) |
| `params` | `dict` | Dictionnaire des paramètres avec leurs valeurs actuelles |

### 3.2 Modules Disponibles

Le code d'effet peut importer **tout module** installé dans l'environnement Python :

```python
# Modules garantis (dépendances de l'application)
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageChops
import numpy as np
import math
import colorsys
import io
import json

# Modules optionnels (si installés)
import cv2          # OpenCV — pour les opérations avancées
from scipy import ndimage, signal  # SciPy — pour le traitement signal
from scipy.interpolate import interp1d
```

### 3.3 Fonctions Utilitaires de l'Application

Bien que non directement accessibles depuis le code d'effet, les fonctions suivantes du fichier `image_analyzer.py` peuvent être reproduites :

```python
# Conversion HEX → RGB
def hex_to_rgb(hex_str):
    h = hex_str.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# Conversion RGB → HSV (vecteurisé)
# → Utiliser colorsys.rgb_to_hsv() ou numpy
```

---

## 4. Catégories d'Effets

### 4.1 Taxonomie Complète

| Catégorie | Préfixe ID | Usage |
|-----------|-----------|-------|
| `base` | `base_`, `auto_`, `flip_` | Opérations de base (rotation, recadrage...) |
| `color` | `color_`, `sepia`, `duotone` | Manipulation des canaux couleur |
| `forensic` | `forensic_`, `ela`, `noise_` | Analyse forensique et détection de falsification |
| `enhancement` | `enhance_`, `sharpen_`, `hdr_` | Amélioration de la qualité image |
| `artistic` | `emboss`, `pixelate`, `glitch` | Effets artistiques et rétro |
| `distortion` | `fisheye`, `swirl`, `ripple` | Distorsions géométriques |
| `blur` | `motion_blur`, `bokeh`, `zoom_blur` | Effets de flou |
| `stylize` | `comic_book`, `neon_glow`, `cyberpunk` | Styles visuels prédéfinis |
| `lighting` | `lens_flare`, `god_rays`, `bloom` | Effets d'éclairage |
| `paleography` | `paleo_` | Traitement de manuscrits, parchemins, palimpsestes |
| `epigraphy` | `epi_` | Traitement d'inscriptions sur pierre/métal |
| `steganography` | `stego_` | Détection et extraction de données cachées |
| `custom` | `custom_` | Effets créés par l'utilisateur |

### 4.2 Ordre d'Affichage dans l'Interface

Les effets sont affichés dans l'ordre du fichier `effects.json`. L'ordre est :
1. `none` (toujours en premier)
2. Catégories dans l'ordre d'apparition
3. Effets custom à la fin

---

## 5. Guide de Développement Pas à Pas

### 5.1 Créer un Effet Simple (Niveau Débutant)

**Objectif :** Créer un effet "Teinte Rouge" qui accentue le canal rouge.

#### Étape 1 : Définir les métadonnées

```json
{
  "id": "custom_red_boost",
  "name": "[CUSTOM] Boost Rouge",
  "category": "custom",
  "description": "Accentue le canal rouge de l'image",
  "params": {
    "intensity": 1.5
  },
  "code": "..."
}
```

#### Étape 2 : Écrire le code

```python
import numpy as np
from PIL import Image

# Récupérer le paramètre
intensity = params.get('intensity', 1.5)

# Convertir en array NumPy
arr = np.array(img.convert('RGB'), dtype=np.float32)

# Appliquer l'effet : multiplier le canal rouge
arr[:,:,0] = np.clip(arr[:,:,0] * intensity, 0, 255)

# Retourner un PIL.Image
return Image.fromarray(arr.astype(np.uint8))
```

#### Étape 3 : Assembler dans effects.json

```json
{
  "id": "custom_red_boost",
  "name": "[CUSTOM] Boost Rouge",
  "category": "custom",
  "description": "Accentue le canal rouge de l'image",
  "params": {
    "intensity": 1.5
  },
  "code": "import numpy as np\nfrom PIL import Image\nintensity = params.get('intensity', 1.5)\narr = np.array(img.convert('RGB'), dtype=np.float32)\narr[:,:,0] = np.clip(arr[:,:,0] * intensity, 0, 255)\nreturn Image.fromarray(arr.astype(np.uint8))"
}
```

> 💡 **Astuce :** Utilisez l'**Éditeur d'Effet Custom** intégré à l'application (bouton "✎ AJOUTER EFFET CUSTOM") pour éviter d'écrire le JSON manuellement.

### 5.2 Créer un Effet avec Paramètres Complexes

**Objectif :** Effet "Vignette Radiale" avec couleur personnalisable.

```python
import numpy as np
from PIL import Image

# Paramètres
color_str = params.get('color', '#000000')
strength = params.get('strength', 2.5)

# Convertir HEX → RGB
hex_val = color_str.lstrip('#')
r, g, b = tuple(int(hex_val[i:i+2], 16) for i in (0, 2, 4))

# Image en array
arr = np.array(img.convert('RGB'), dtype=np.float32)
h, w = arr.shape[:2]

# Calcul de la distance au centre
Y, X = np.ogrid[:h, :w]
cx, cy = w/2, h/2
dist = np.sqrt(((X-cx)/cx)**2 + ((Y-cy)/cy)**2)

# Masque de vignette (1 au centre, 0 aux bords)
mask = 1 - np.clip(dist * strength * 0.5, 0, 1)

# Application : interpolation entre l'image et la couleur
for c, val in enumerate([r, g, b]):
    arr[:,:,c] = arr[:,:,c] * mask + val * (1 - mask)

return Image.fromarray(arr.clip(0,255).astype(np.uint8))
```

### 5.3 Créer un Effet Forensique (Niveau Avancé)

**Objectif :** Détection de zones retouchées par analyse du bruit.

```python
import numpy as np
from PIL import Image, ImageFilter

# Paramètres
sigma = params.get('sigma', 1.5)

# Image originale en float
arr = np.array(img.convert('RGB'), dtype=np.float32)

# Version lissée (supprime le bruit naturel)
smooth = np.array(
    img.filter(ImageFilter.GaussianBlur(radius=sigma)).convert('RGB'), 
    dtype=np.float32
)

# Bruit résiduel = différence amplifiée
noise = np.abs(arr - smooth) * 4
noise = np.clip(noise, 0, 255)

# Le bruit non uniforme indique une retouche
return Image.fromarray(noise.astype(np.uint8))
```

---

## 6. Techniques Avancées

### 6.1 Traitement Vectorisé avec NumPy

**❌ À ÉVITER (lent) :**
```python
# Boucles Python sur les pixels — TRÈS LENT
for i in range(arr.shape[0]):
    for j in range(arr.shape[1]):
        r, g, b = arr[i,j]
        arr[i,j] = [r*2, g, b]
```

**✅ RECOMMANDÉ (rapide) :**
```python
# Vectorisation NumPy — RAPIDE
arr[:,:,0] = np.clip(arr[:,:,0] * 2, 0, 255)
```

### 6.2 Utilisation de Masques Booléens

```python
# Créer un masque conditionnel
bright_mask = arr.mean(axis=2) > 200

# Appliquer selectivement
result = arr.copy()
result[bright_mask] = result[bright_mask] * 1.2
```

### 6.3 Convolution et Filtres Personnalisés

```python
from PIL import ImageFilter

# Kernel personnalisé (ex: sharpen)
kernel = ImageFilter.Kernel(
    size=(3, 3),
    kernel=[0, -1, 0, -1, 5, -1, 0, -1, 0],
    scale=1,
    offset=0
)
return img.filter(kernel).convert('RGB')
```

### 6.4 Manipulation des Canaux par Séparation

```python
# Séparer les canaux
r, g, b = img.split()

# Traiter individuellement
r = r.point(lambda x: min(255, int(x * 1.2)))

# Recombiner
return Image.merge('RGB', (r, g, b))
```

### 6.5 Utilisation de SciPy (si disponible)

```python
from scipy import ndimage

# Filtre morphologique
binary = gray > 128
dilated = ndimage.binary_dilation(binary, iterations=2)

# Mesures de régions
labels, num = ndimage.label(binary)
sizes = ndimage.sum(binary, labels, range(1, num+1))
```

### 6.6 Détection de Contours Avancée

```python
from PIL import ImageFilter
import numpy as np

# Gradient Sobel approximé
def sobel_edge(gray_img):
    arr = np.array(gray_img, dtype=np.float32)

    # Kernels Sobel
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    ky = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    gx = ndimage.convolve(arr, kx)
    gy = ndimage.convolve(arr, ky)

    magnitude = np.sqrt(gx**2 + gy**2)
    return Image.fromarray(np.clip(magnitude, 0, 255).astype(np.uint8))
```

---

## 7. Optimisation des Performances

### 7.1 Règles d'Or

| Règle | Impact | Exemple |
|-------|--------|---------|
| **Vectoriser avec NumPy** | ×10 à ×100 | Remplacer les boucles par des opérations array |
| **Éviter les conversions inutiles** | ×2 | Minimiser `Image ↔ array` |
| **Utiliser des tailles réduites pour les tests** | Instantané | Tester sur 64×64 avant l'image complète |
| **Préférer PIL pour les opérations simples** | ×2-5 | `ImageEnhance` vs NumPy pour brightness |
| **Éviter les imports conditionnels dans la boucle** | Mineur | Importer en début de code |

### 7.2 Anti-Patterns à Éviter

```python
# ❌ Mauvais : import dans le code
if some_condition:
    import cv2  # Lent si répété

# ✅ Bon : import en haut du code
try:
    import cv2
except ImportError:
    cv2 = None

# ❌ Mauvais : création d'image intermédiaire inutile
arr = np.array(img.convert('RGB'))
result = Image.fromarray(arr)
arr2 = np.array(result.convert('RGB'))  # Inutile !

# ✅ Bon : garder l'array
arr = np.array(img.convert('RGB'), dtype=np.float32)
# ... traitements ...
return Image.fromarray(arr.astype(np.uint8))
```

### 7.3 Gestion de la Mémoire

```python
# Libérer explicitement les grands arrays intermédiaires
import gc

large_temp = np.zeros((4000, 6000, 3), dtype=np.float32)
# ... traitements ...
del large_temp
gc.collect()
```

---

## 8. Débogage et Tests

### 8.1 Utiliser l'Éditeur Intégré

L'application dispose d'un **testeur d'effet** intégré :

1. Cliquez sur **"✎ AJOUTER EFFET CUSTOM"**
2. Remplissez les champs
3. Cliquez sur **"[ TESTER ]"**
4. Le test s'exécute sur une image 64×64 de test

### 8.2 Messages d'Erreur Courants

| Erreur | Cause | Solution |
|--------|-------|----------|
| `NameError: name 'Image' is not defined` | Import manquant | Ajouter `from PIL import Image` |
| `ValueError: cannot convert float NaN to integer` | Valeurs NaN/Inf dans l'array | Utiliser `np.nan_to_num()` ou `np.clip()` |
| `TypeError: 'NoneType' object is not subscriptable` | `params.get()` retourne None | Fournir une valeur par défaut : `params.get('key', default)` |
| `MemoryError` | Image trop grande | Réduire la résolution ou optimiser |
| `ModuleNotFoundError: No module named 'cv2'` | OpenCV non installé | Utiliser `try/except` avec fallback |

### 8.3 Technique de Débogage

```python
# Ajouter des prints (visibles dans la console Python)
print(f"DEBUG: img.size = {img.size}")
print(f"DEBUG: params = {params}")

# Vérifier les valeurs min/max
arr = np.array(img.convert('RGB'), dtype=np.float32)
print(f"DEBUG: min={arr.min()}, max={arr.max()}, mean={arr.mean()}")

# Sauvegarder une image intermédiaire (pour inspection)
# temp = Image.fromarray(arr.astype(np.uint8))
# temp.save('/tmp/debug_step1.png')
```

### 8.4 Tests Unitaires Manuels

```python
# Script de test indépendant
from PIL import Image
import json

# Charger l'effet
with open('effects.json') as f:
    data = json.load(f)

effect = next(e for e in data['effects'] if e['id'] == 'mon_effet')

# Créer une image de test
test_img = Image.new('RGB', (256, 256), (128, 64, 200))

# Exécuter (copier la logique de apply_effect)
params = effect.get("params", {})
code = effect.get("code", "return img.copy()")
local_ns = {"img": test_img, "params": params}
wrapped = "def _effect(img, params):\n"
for line in code.splitlines():
    wrapped += "    " + line + "\n"
exec(wrapped, local_ns)
result = local_ns["_effect"](test_img, params)

# Vérifier
assert isinstance(result, Image.Image)
assert result.size == (256, 256)
print("✓ Test passed")
```

---

## 9. Référence des Effets Intégrés

### 9.1 Effets de Base (`base`)

| ID | Nom | Description |
|----|-----|-------------|
| `none` | Aucun effet | Passe-through |
| `auto_crop` | Recadrage Auto | Supprime les bords vides |
| `auto_rotate` | Rotation Auto | Applique l'orientation EXIF |
| `flip_mirror` | Miroir Horizontal | Retournement horizontal |

### 9.2 Effets de Couleur (`color`)

| ID | Paramètres Clés | Technique |
|----|-----------------|-----------|
| `grayscale` | — | `ImageOps.grayscale()` |
| `invert` | — | `ImageOps.invert()` |
| `sepia` | — | Matrice de transformation RGB |
| `duotone` | `color1`, `color2` | Interpolation linéaire entre deux couleurs |
| `color_temperature` | `temp` | Ajustement chaud/froid |
| `vibrance` | `amount` | Saturation intelligente |
| `colorize` | `hue`, `saturation` | Colorisation monochrome |
| `cross_process` | — | Courbes de tonalité croisées |
| `black_white_split` | `black_point`, `white_point` | Expansion des tons |
| `split_toning` | `shadow_hue`, `highlight_hue` | Tons partagés ombres/lumières |

### 9.3 Effets Forensiques (`forensic`)

| ID | Paramètres | Usage |
|----|-----------|-------|
| `thermal` | — | Pseudo-colorisation thermique FLIR |
| `night_vision` | — | NVG militaire (vert phosphore) |
| `edge_detection` | — | Filtre FIND_EDGES + boost |
| `histogram_equalize` | — | Égalisation d'histogramme |
| `clahe` | — | CLAHE (requiert OpenCV) |
| `forensic_enhance` | — | Pipeline NCIS (sharpen + contraste + égalisation) |
| `ela` | `quality`, `amplify` | Error Level Analysis |
| `noise_analysis` | `sigma` | Visualisation du bruit résiduel |
| `shadow_recovery` | `lift` | Extraction des détails dans les ombres |
| `highlight_recovery` | `compress` | Récupération des hautes lumières |
| `frequency_separation` | `mode` | Séparation haute/basse fréquence |
| `difference_blend` | — | Mode différence |
| `grain_analysis` | — | Analyse du grain de compression |
| `channel_isolation` | `channel` | Isolation RGB individuelle |
| `local_contrast` | `amount`, `radius` | Unsharp Mask avancé |

### 9.4 Effets de Stéganographie (`steganography`)

| ID | Paramètres | Principe |
|----|-----------|----------|
| `stego_lsb_extract` | `bit_mask`, `channel` | Extraction des bits de poids faible |
| `stego_entropy_map` | `radius` | Cartographie d'entropie locale |
| `forensic_bit_plane_slicing` | `plane` | Décomposition en plans de bits (0-7) |
| `forensic_laplacian_noise` | `gain` | Extraction du bruit de capteur |

### 9.5 Effets Paléographiques (`paleography`)

| ID | Paramètres | Application |
|----|-----------|-------------|
| `paleo_ink_enhance` | `ink_channel`, `sensitivity` | Extraction encre délavée |
| `paleo_fade_recovery` | `recovery_boost` | Récupération encre effacée |
| `paleo_ghost_text` | `layer_depth` | Texte palimpseste |
| `paleo_raking_light` | `angle`, `elevation` | Lumière rasante RTI |
| `paleo_multispectral` | `band` | Fausses couleurs multispectral |
| `paleo_stain_remove` | `stain_threshold` | Suppression taches |
| `paleo_line_thinning` | `thin_factor` | Amincissement traits |
| `paleo_letter_separation` | `separation_strength` | Séparation ligatures |
| `paleo_ink_corrosion` | `corrosion_threshold` | Inversion corrosion |
| `paleo_parchment_flatten` | `smoothness` | Aplatissement parchemin |
| `paleo_ductus_reveal` | `sensitivity` | Révélation ductus |
| `paleo_illumination_enhance` | `saturation_threshold` | Extraction enluminures |
| `paleo_ir_simulation` | `penetration_depth` | Réflectographie IR |
| `paleo_watermark_reveal` | `sensitivity` | Filigranes papier |
| `paleo_text_stabilize` | `line_smooth` | Stabilisation texte |
| `paleo_ink_dating` | `analysis_mode` | Datation spectrale indicative |

### 9.6 Effets Épigraphiques (`epigraphy`)

| ID | Paramètres | Application |
|----|-----------|-------------|
| `epi_erosion_compensate` | `erosion_type` | Reconstruction érosion |
| `epi_lichen_remove` | `green_suppress` | Suppression lichens |
| `epi_raking_enhance` | `light_angle` | Lumière rasante mur |
| `epi_depth_map` | `scale` | Carte de profondeur |
| `epi_moss_remove` | `moisture_threshold` | Suppression mousse |
| `epi_patina_remove` | `patina_type` | Suppression patine |
| `epi_crack_repair` | `crack_width` | Réparation fissures |
| `epi_3d_relief` | `relief_height` | Reconstruction 3D |
| `epi_sandblast_restore` | `wind_direction` | Restauration sablage |
| `epi_multiview_stereo` | `n_lights` | Stéréo-photométrie |
| `epi_weathering_reverse` | `weathering_type` | Inversion altération |
| `epi_ink_trace` | `red_threshold` | Traces encre rouge |
| `epi_surface_clean` | `clean_strength` | Nettoyage surface |
| `epi_pigment_analysis` | `pigment` | Analyse pigments |
| `epi_rti_simple` | `n_angles` | RTI simplifié |
| `epi_inscription_extract` | `method` | Extraction inscription |
| `epi_stroke_enhance` | `line_width` | Renforcement traits |

---

## 10. Bonnes Pratiques

### 10.1 Checklist de Validation

Avant de sauvegarder un effet, vérifiez :

- [ ] Le code retourne **toujours** un objet `PIL.Image.Image`
- [ ] Les paramètres ont des **valeurs par défaut** sensibles
- [ ] Les valeurs sont **clippées** entre 0 et 255 avant conversion `uint8`
- [ ] Les imports optionnels (cv2, scipy) sont dans un **try/except**
- [ ] L'ID est unique et en **snake_case**
- [ ] Le nom est descriptif et préfixé par `[CUSTOM]` si applicable
- [ ] Le code fonctionne sur une image **64×64** (test intégré)
- [ ] Le code fonctionne sur une image **grande résolution** (pas de MemoryError)

### 10.2 Style de Code

```python
# ✅ Style recommandé
import numpy as np
from PIL import Image

# 1. Extraire les paramètres avec valeurs par défaut
strength = params.get('strength', 1.0)
color = params.get('color', '#ffffff')

# 2. Convertir l'image
arr = np.array(img.convert('RGB'), dtype=np.float32)

# 3. Traitement (vectorisé)
result = arr * strength

# 4. Clip et conversion
result = np.clip(result, 0, 255)

# 5. Retour
return Image.fromarray(result.astype(np.uint8))
```

### 10.3 Gestion des Erreurs

```python
# Fallback gracieux
try:
    import cv2
    # Code utilisant OpenCV
    result = cv2.some_operation(...)
except ImportError:
    # Fallback avec PIL
    from PIL import ImageFilter
    result = img.filter(ImageFilter.GaussianBlur(radius=2))

# Toujours retourner un Image
return result.convert('RGB')
```

### 10.4 Documentation Inline

```python
# Description de l'algorithme
# Algorithme : Unsharp Mask avec masque de luminance
# Référence : Pratt, W.K. "Digital Image Processing"
# Paramètres : amount (1.0-3.0), radius (1-10)

import numpy as np
from PIL import Image, ImageFilter

amount = params.get('amount', 1.5)
rad = params.get('radius', 5)

arr = np.array(img.convert('RGB'), dtype=np.float32)
blur = np.array(img.filter(ImageFilter.GaussianBlur(radius=rad)).convert('RGB'), dtype=np.float32)

# Masque = image originale - image floue
mask = arr - blur

# Application du masque amplifié
result = arr + mask * amount

return Image.fromarray(result.clip(0,255).astype(np.uint8))
```

---

## Annexe A : Table de Conversion des Types

| Source | Conversion | Destination |
|--------|-----------|-------------|
| `PIL.Image` | `np.array(img)` | `ndarray uint8` |
| `ndarray uint8` | `arr.astype(np.float32)` | `ndarray float32` |
| `ndarray float32` | `np.clip(arr, 0, 255)` | `ndarray float32 (safe)` |
| `ndarray float32` | `arr.astype(np.uint8)` | `ndarray uint8` |
| `ndarray uint8` | `Image.fromarray(arr)` | `PIL.Image` |
| `ndarray uint8 (H,W)` | `Image.fromarray(arr).convert('RGB')` | `PIL.Image RGB` |

---

## Annexe B : Constantes de Couleur du Thème

```python
# Palette phosphore INGEN Systems (pour référence)
C_BG        = "#050a05"   # Fond principal
C_BG2       = "#0a0f0a"   # Fond secondaire
C_BG3       = "#0f150f"   # Fond tertiaire
C_PANEL     = "#0d1a0d"   # Panneaux
C_BORDER    = "#1a3a1a"   # Bordures
C_GREEN     = "#00ff41"   # Vert phosphore (principal)
C_GREEN2    = "#00cc33"   # Vert secondaire
C_GREEN3    = "#008822"   # Vert foncé
C_AMBER     = "#ffb000"   # Ambre (alertes)
C_RED       = "#ff2222"   # Rouge (erreurs)
C_CYAN      = "#00e5ff"   # Cyan (liens)
C_WHITE     = "#e8ffe8"   # Blanc cassé
C_DIM       = "#3a5a3a"   # Vert tamisé
```

---

## Annexe C : Exemple Complet — Effet "Détection de Texte Caché"

```json
{
  "id": "custom_hidden_text",
  "name": "[CUSTOM] Texte Caché — Détection",
  "category": "custom",
  "description": "Détecte le texte caché sous une couche de peinture ou d'encre par analyse de la réponse spectrale différentielle",
  "params": {
    "layer_depth": 0.6,
    "contrast_boost": 2.5,
    "blue_sensitivity": 1.8
  },
  "code": "import numpy as np\nfrom PIL import Image, ImageFilter\n\n# Paramètres\ndepth = params.get('layer_depth', 0.6)\nboost = params.get('contrast_boost', 2.5)\nblue_sens = params.get('blue_sensitivity', 1.8)\n\n# Chargement\narr = np.array(img.convert('RGB'), dtype=np.float32)\n\n# Séparation surface / profondeur\nsurface = np.array(img.filter(ImageFilter.GaussianBlur(radius=20)).convert('RGB'), dtype=np.float32)\ndeep = arr - surface * depth\n\n# Analyse spectrale : l'encre profonde réagit différemment au bleu\n# (principe de la réflectographie multispectral simplifié)\nblue_response = deep[:,:,2] * blue_sens - deep[:,:,0] * 0.3\n\n# Normalisation\nblue_response = (blue_response - blue_response.min()) / (blue_response.max() - blue_response.min() + 1e-6) * 255\n\n# Boost de contraste\nblue_response = np.clip((blue_response - 128) * boost + 128, 0, 255)\n\n# Visualisation en fausses couleurs\nresult = np.zeros((arr.shape[0], arr.shape[1], 3), dtype=np.float32)\nresult[:,:,0] = blue_response * 0.2  # Rouge faible\nresult[:,:,1] = blue_response * 0.5  # Vert moyen\nresult[:,:,2] = blue_response        # Bleu fort\n\n# Superposition avec l'original pour le contexte\nresult = result * 0.7 + arr * 0.3\n\nreturn Image.fromarray(result.clip(0,255).astype(np.uint8))"
}
```

---

> **INGEN SYSTEMS** — *Classified Analysis Tool — Authorized Personnel Only*  
> Documentation générée pour la version 4.0 FORENSIC & HERITAGE UNIFIED

***

# 📚 Catalogue des Effets d'Image - INGEN Systems

## 🛠️ Opérations de Base (`base`)
*Outils fondamentaux de manipulation et de préparation d'image.*
* **--- Aucun effet ---** (`none`) : Image originale sans traitement.
* **Recadrage Auto** (`auto_crop`) : Recadrage automatique des bords vides ou blancs.
* **Rotation Auto (EXIF)** (`auto_rotate`) : Rotation automatique basée sur les métadonnées EXIF.
* **Miroir Horizontal** (`flip_mirror`) : Retournement horizontal de l'image.

## 🎨 Couleur et Tonalité (`color`)
*Gestion des couleurs, courbes et ambiances chromatiques.*
* **Niveaux de gris** (`grayscale`) : Conversion en niveaux de gris.
* **Négatif** (`invert`) : Inversion des couleurs (négatif photographique).
* **Sépia** (`sepia`) : Effet sépia vintage.
* **Duotone Pro** (`duotone`) : Duotone avec couleurs personnalisables.
* **Température de couleur** (`color_temperature`) : Ajustement chaud/froid de la température de couleur.
* **Vibrance** (`vibrance`) : Saturation intelligente (préserve les tons chair).
* **Colorisation** (`colorize`) : Colorisation monochrome avec teinte personnalisable.
* **Traversé Photo** (`cross_process`) : Simulation de traitement croisé C41/E6.
* **Séparation Tons** (`black_white_split`) : Séparation des tons noirs et blancs avec contrôle.
* **Tons partagés** (`split_toning`) : Tons partagés ombres/lumières (style cinéma).

## 🔍 Analyse Forensique et Stéganographie (`forensic`)
*Outils d'investigation, détection de falsification et analyse de bruit.*
* **Vision Thermique** (`thermal`) : Pseudo-colorisation thermique (style FLIR).
* **Vision Nocturne** (`night_vision`) : Effet vision nocturne NVG militaire (vert phosphore).
* **Détection de Contours** (`edge_detection`) : Détection des contours (filtre Canny/Sobel).
* **Égalisation Histogramme** (`histogram_equalize`) : Égalisation de l'histogramme — révèle les détails cachés.
* **CLAHE (Contraste Adaptatif)** (`clahe`) : Contrast Limited Adaptive Histogram Equalization — technique forensique avancée.
* **Forensique Avancé** (`forensic_enhance`) : Pipeline complet: sharpen + contraste + égalisation (style NCIS).
* **ELA — Détection Falsification** (`ela`) : Error Level Analysis — détecte les zones potentiellement retouchées.
* **Analyse de Bruit** (`noise_analysis`) : Visualisation du bruit résiduel pour détecter les manipulations.
* **Récupération Ombres** (`shadow_recovery`) : Extraction et amplification des détails dans les ombres.
* **Récupération Hautes Lumières** (`highlight_recovery`) : Récupération des détails dans les zones surexposées.
* **Séparation Fréquentielle** (`frequency_separation`) : Séparation haute/basse fréquence pour analyse de texture.
* **Mode Différence** (`difference_blend`) : Mode de fusion différence pour comparaison d'images.
* **Analyse de Grain** (`grain_analysis`) : Analyse du grain pour détecter les incohérences de compression.
* **Isolation Canaux** (`channel_isolation`) : Isolation individuelle des canaux RGB pour analyse.
* **Stéganographie — LSB Extractor** (`stego_lsb_extract`) : Extrait les bits de poids faible (LSB) pour révéler les données cachées.
* **Stéganographie — Cartographie d'Entropie** (`stego_entropy_map`) : Calcule l'entropie locale pour détecter les anomalies statistiques (injection de données).
* **Forensic — Décomposition en Plans de Bits** (`forensic_bit_plane_slicing`) : Isole un plan de bits spécifique (0 à 7) pour analyser la structure fine du bruit.
* **Forensic — Bruit de Capteur (Laplacien)** (`forensic_laplacian_noise`) : Extrait le bruit haute fréquence pour inspecter l'homogénéité du grain et détecter les collages.
* **Forensic — Détection Copier-Coller** (`forensic_copy_move_detect`) : Détecte les régions dupliquées par appariement de blocs (clonage).
* **Forensic — JPEG Ghost** (`forensic_jpeg_ghost`) : Identifie les niveaux de compression JPEG par zone pour trahir les montages.
* **Forensic — Empreinte Capteur (PRNU Proxy)** (`forensic_prnu_proxy`) : Extrait une approximation du bruit résiduel de motif fixe (PRNU).
* **Forensic — Cartographie des Reflets Spéculaires** (`forensic_specular_highlight_map`) : Isole les reflets pour vérifier la cohérence des sources lumineuses.
* **Forensic — Détection de Rééchantillonnage** (`forensic_resampling_detect`) : Met en évidence les motifs périodiques créés par redimensionnement/rotation.
* **LSB Steganography Reveal** (`lsb_stego`) : Extrait les bits de poids faible pour révéler messages cachés.
* **Artefacts JPEG DCT** (`dct_artifact`) : Visualise les artefacts de compression pour détecter montages.
* **PRNU Sensor Fingerprint** (`prnu_noise`) : Signature approximative du capteur photo.
* **Glitch Forensique** (`glitch_forensic`) : Visualise corruptions ou interpolations suspectes.

## ✨ Amélioration et Restauration (`enhancement`)
*Correction, netteté et optimisation de la qualité visuelle.*
* **Super Netteté** (`sharpen_extreme`) : Accentuation extrême de la netteté (style CSI zoom enhance).
* **Éclaircir l'image** (`enhance_brightness`) : Augmentation de la luminosité pour révéler les zones sombres.
* **Correction Gamma** (`gamma_correction`) : Correction gamma pour révéler les détails.
* **Réduction de Bruit** (`noise_reduction`) : Lissage gaussien pour réduire le bruit.
* **HDR Simulé** (`hdr_fake`) : Simulation d'effet HDR par fusion multi-exposition.
* **Masque Flou** (`unsharp_mask`) : Unsharp Mask standard pour la netteté.
* **Netteté Intelligente** (`smart_sharpen`) : Netteté adaptative selon le contenu de l'image.
* **Amélioration Détail** (`detail_enhance`) : Amélioration des micro-détails par filtrage bilatéral.
* **Débrumage** (`dehaze`) : Réduction de la brume/atmosphère (Dark Channel Prior).
* **Contraste Adaptatif** (`contrast_adaptive`) : Contraste adaptatif local (style Retinex).
* **Balance des Blancs** (`white_balance`) : Balance des blancs automatique (Gray World).
* **Fusion Exposition** (`exposure_fusion`) : Fusion de plusieurs expositions simulées.
* **Dénuisage Wavelet Avancé** (`wavelet_denoise`) : Dénuisage par ondelettes (préserve mieux les détails).

## 📜 Paléographie et Manuscrits (`paleography`)
*Traitement spécialisé pour parchemins, manuscrits, encres historiques et palimpsestes.*
* **Contraste Local Adaptatif** (`local_contrast`) : Améliore lisibilité des zones textuelles dégradées.
* **Encre Manuscrit — Extraction** (`paleo_ink_enhance`) : Extraction et renforcement de l'encre délavée (séparation encre/support).
* **Récupération Encre Effacée** (`paleo_fade_recovery`) : Récupération de l'encre effacée par oxydation/humidité.
* **Texte Fantôme — Palimpseste** (`paleo_ghost_text`) : Révélation de texte sous-jacent (palimpsestes).
* **Lumière Rasant — Relief** (`paleo_raking_light`) : Simulation de lumière rasante pour révéler empreintes de calame/incisions.
* **Multispectral — Fausses Couleurs** (`paleo_multispectral`) : Simulation d'imagerie multispectral (UV/IR) pour distinguer l'encre du support.
* **Suppression Taches** (`paleo_stain_remove`) : Suppression des taches d'humidité/moisissure en préservant l'encre.
* **Amincissement Traits** (`paleo_line_thinning`) : Amincissement des traits d'encre épais (skeletonization).
* **Séparation Lettres** (`paleo_letter_separation`) : Séparation des lettres enchevêtrées ou ligaturées.
* **Corrosion Encre — Inversion** (`paleo_ink_corrosion`) : Compensation de la corrosion de l'encre (attaque chimique du support).
* **Aplatissement Parchemin** (`paleo_parchment_flatten`) : Correction de l'éclairage inégal (ondulations, plis).
* **Ductus Révélation** (`paleo_ductus_reveal`) : Révélation du ductus (direction des traits de plume).
* **Enluminures — Extraction** (`paleo_illumination_enhance`) : Extraction et mise en valeur des enluminures et lettrines.
* **IR Reflectography** (`paleo_ir_simulation`) : Simulation de réflectographie IR pour sous-dessins et repentirs.
* **Filigrane — Révélation** (`paleo_watermark_reveal`) : Révélation des filigranes de papier par transparence.
* **Stabilisation Texte** (`paleo_text_stabilize`) : Alignement des lignes de base et redressement des caractères.
* **Datation Encre — Spectre** (`paleo_ink_dating`) : Analyse spectrale indicative (carbone, ferro-gallique).
* **Fluorescence UV — Simulation** (`paleo_uv_fluorescence_sim`) : Simulation de fluorescence induite par UV (365nm).
* **Carte des Lacunes** (`paleo_lacuna_map`) : Cartographie thermique des zones illisibles ou dégradées.
* **Grille de Réglures** (`paleo_baseline_grid`) : Détection des lignes de base et superposition d'une grille.
* **Lignes de Chaînette — Papier** (`paleo_chain_lines`) : Révélation des lignes de chaînette (FFT) pour datation/identification.
* **Carte de Densité d'Encre** (`paleo_ink_density_map`) : Cartographie thermique pour repérer changements de main ou ré-encrage.
* **Palimpseste — Séparation Couches** (`paleo_palimpsest_separate`) : Séparation de deux couches d'écriture superposées.
* **Empilement Multi-Échelle** (`paleo_focus_stack`) : Combine plusieurs niveaux de rehaussement (focus-stacking).
* **Isolation Marginalia** (`paleo_marginalia_isolate`) : Isolation des annotations marginales (gloses, notes).
* **Simulation Multispectrale** (`multispectral_sim`) : Simule UV/IR pour révéler encres effacées.
* **Séparation d’Encre Historique** (`ink_separation`) : Sépare encres ferro-gallique / carbone.
* **Boost Transcription Paléographique** (`transcription_boost`) : Contraste local + netteté pour lecture de manuscrits.
* **Révélation Palimpseste** (`palimpsest_reveal`) : Technique inspirée ICA/PCA pour textes sous-jacents.
* **Fluorescence UV Simulée** (`uv_fluorescence`) : Simule fluorescence des encres sous UV.
* **Réflectance IR** (`ir_reflectance`) : Simulation infrarouge pour visibilité des encres carbone.
* **Boost Contours Écriture** (`script_edge_boost`) : Renforce les traits d’écriture tout en réduisant le bruit de parchemin.
* **Suppression Texture Parchemin** (`parchment_remove`) : Réduit le bruit de fibre du support pour isoler l’encre.

## 🏛️ Épigraphie et Inscriptions (`epigraphy`)
*Outils pour pierres gravées, inscriptions murales, érosion et polychromie.*
* **Compensation Érosion** (`epi_erosion_compensate`) : Reconstruction des parties manquantes par interpolation des contours.
* **Suppression Lichens** (`epi_lichen_remove`) : Suppression des lichens et végétation recouvrant les inscriptions.
* **Lumière Rasant Mur**
Voici le catalogue structuré de votre bibliothèque d'effets **INGEN Systems**, organisé par catégorie et formaté en Markdown. J'ai inclus l'identifiant (`id`) de chaque effet pour faciliter la correspondance avec votre code.

***

# 📚 Catalogue des Effets d'Image - INGEN Systems

## 🛠️ Opérations de Base (`base`)
*Outils fondamentaux de manipulation et de préparation d'image.*
* **--- Aucun effet ---** (`none`) : Image originale sans traitement.
* **Recadrage Auto** (`auto_crop`) : Recadrage automatique des bords vides ou blancs.
* **Rotation Auto (EXIF)** (`auto_rotate`) : Rotation automatique basée sur les métadonnées EXIF.
* **Miroir Horizontal** (`flip_mirror`) : Retournement horizontal de l'image.

## 🎨 Couleur et Tonalité (`color`)
*Gestion des couleurs, courbes et ambiances chromatiques.*
* **Niveaux de gris** (`grayscale`) : Conversion en niveaux de gris.
* **Négatif** (`invert`) : Inversion des couleurs (négatif photographique).
* **Sépia** (`sepia`) : Effet sépia vintage.
* **Duotone Pro** (`duotone`) : Duotone avec couleurs personnalisables.
* **Température de couleur** (`color_temperature`) : Ajustement chaud/froid de la température de couleur.
* **Vibrance** (`vibrance`) : Saturation intelligente (préserve les tons chair).
* **Colorisation** (`colorize`) : Colorisation monochrome avec teinte personnalisable.
* **Traversé Photo** (`cross_process`) : Simulation de traitement croisé C41/E6.
* **Séparation Tons** (`black_white_split`) : Séparation des tons noirs et blancs avec contrôle.
* **Tons partagés** (`split_toning`) : Tons partagés ombres/lumières (style cinéma).

## 🔍 Analyse Forensique et Stéganographie (`forensic`)
*Outils d'investigation, détection de falsification et analyse de bruit.*
* **Vision Thermique** (`thermal`) : Pseudo-colorisation thermique (style FLIR).
* **Vision Nocturne** (`night_vision`) : Effet vision nocturne NVG militaire (vert phosphore).
* **Détection de Contours** (`edge_detection`) : Détection des contours (filtre Canny/Sobel).
* **Égalisation Histogramme** (`histogram_equalize`) : Égalisation de l'histogramme — révèle les détails cachés.
* **CLAHE (Contraste Adaptatif)** (`clahe`) : Contrast Limited Adaptive Histogram Equalization — technique forensique avancée.
* **Forensique Avancé** (`forensic_enhance`) : Pipeline complet: sharpen + contraste + égalisation (style NCIS).
* **ELA — Détection Falsification** (`ela`) : Error Level Analysis — détecte les zones potentiellement retouchées.
* **Analyse de Bruit** (`noise_analysis`) : Visualisation du bruit résiduel pour détecter les manipulations.
* **Récupération Ombres** (`shadow_recovery`) : Extraction et amplification des détails dans les ombres.
* **Récupération Hautes Lumières** (`highlight_recovery`) : Récupération des détails dans les zones surexposées.
* **Séparation Fréquentielle** (`frequency_separation`) : Séparation haute/basse fréquence pour analyse de texture.
* **Mode Différence** (`difference_blend`) : Mode de fusion différence pour comparaison d'images.
* **Analyse de Grain** (`grain_analysis`) : Analyse du grain pour détecter les incohérences de compression.
* **Isolation Canaux** (`channel_isolation`) : Isolation individuelle des canaux RGB pour analyse.
* **Stéganographie — LSB Extractor** (`stego_lsb_extract`) : Extrait les bits de poids faible (LSB) pour révéler les données cachées.
* **Stéganographie — Cartographie d'Entropie** (`stego_entropy_map`) : Calcule l'entropie locale pour détecter les anomalies statistiques (injection de données).
* **Forensic — Décomposition en Plans de Bits** (`forensic_bit_plane_slicing`) : Isole un plan de bits spécifique (0 à 7) pour analyser la structure fine du bruit.
* **Forensic — Bruit de Capteur (Laplacien)** (`forensic_laplacian_noise`) : Extrait le bruit haute fréquence pour inspecter l'homogénéité du grain et détecter les collages.
* **Forensic — Détection Copier-Coller** (`forensic_copy_move_detect`) : Détecte les régions dupliquées par appariement de blocs (clonage).
* **Forensic — JPEG Ghost** (`forensic_jpeg_ghost`) : Identifie les niveaux de compression JPEG par zone pour trahir les montages.
* **Forensic — Empreinte Capteur (PRNU Proxy)** (`forensic_prnu_proxy`) : Extrait une approximation du bruit résiduel de motif fixe (PRNU).
* **Forensic — Cartographie des Reflets Spéculaires** (`forensic_specular_highlight_map`) : Isole les reflets pour vérifier la cohérence des sources lumineuses.
* **Forensic — Détection de Rééchantillonnage** (`forensic_resampling_detect`) : Met en évidence les motifs périodiques créés par redimensionnement/rotation.
* **LSB Steganography Reveal** (`lsb_stego`) : Extrait les bits de poids faible pour révéler messages cachés.
* **Artefacts JPEG DCT** (`dct_artifact`) : Visualise les artefacts de compression pour détecter montages.
* **PRNU Sensor Fingerprint** (`prnu_noise`) : Signature approximative du capteur photo.
* **Glitch Forensique** (`glitch_forensic`) : Visualise corruptions ou interpolations suspectes.

## ✨ Amélioration et Restauration (`enhancement`)
*Correction, netteté et optimisation de la qualité visuelle.*
* **Super Netteté** (`sharpen_extreme`) : Accentuation extrême de la netteté (style CSI zoom enhance).
* **Éclaircir l'image** (`enhance_brightness`) : Augmentation de la luminosité pour révéler les zones sombres.
* **Correction Gamma** (`gamma_correction`) : Correction gamma pour révéler les détails.
* **Réduction de Bruit** (`noise_reduction`) : Lissage gaussien pour réduire le bruit.
* **HDR Simulé** (`hdr_fake`) : Simulation d'effet HDR par fusion multi-exposition.
* **Masque Flou** (`unsharp_mask`) : Unsharp Mask standard pour la netteté.
* **Netteté Intelligente** (`smart_sharpen`) : Netteté adaptative selon le contenu de l'image.
* **Amélioration Détail** (`detail_enhance`) : Amélioration des micro-détails par filtrage bilatéral.
* **Débrumage** (`dehaze`) : Réduction de la brume/atmosphère (Dark Channel Prior).
* **Contraste Adaptatif** (`contrast_adaptive`) : Contraste adaptatif local (style Retinex).
* **Balance des Blancs** (`white_balance`) : Balance des blancs automatique (Gray World).
* **Fusion Exposition** (`exposure_fusion`) : Fusion de plusieurs expositions simulées.
* **Dénuisage Wavelet Avancé** (`wavelet_denoise`) : Dénuisage par ondelettes (préserve mieux les détails).

## 📜 Paléographie et Manuscrits (`paleography`)
*Traitement spécialisé pour parchemins, manuscrits, encres historiques et palimpsestes.*
* **Contraste Local Adaptatif** (`local_contrast`) : Améliore lisibilité des zones textuelles dégradées.
* **Encre Manuscrit — Extraction** (`paleo_ink_enhance`) : Extraction et renforcement de l'encre délavée (séparation encre/support).
* **Récupération Encre Effacée** (`paleo_fade_recovery`) : Récupération de l'encre effacée par oxydation/humidité.
* **Texte Fantôme — Palimpseste** (`paleo_ghost_text`) : Révélation de texte sous-jacent (palimpsestes).
* **Lumière Rasant — Relief** (`paleo_raking_light`) : Simulation de lumière rasante pour révéler empreintes de calame/incisions.
* **Multispectral — Fausses Couleurs** (`paleo_multispectral`) : Simulation d'imagerie multispectral (UV/IR) pour distinguer l'encre du support.
* **Suppression Taches** (`paleo_stain_remove`) : Suppression des taches d'humidité/moisissure en préservant l'encre.
* **Amincissement Traits** (`paleo_line_thinning`) : Amincissement des traits d'encre épais (skeletonization).
* **Séparation Lettres** (`paleo_letter_separation`) : Séparation des lettres enchevêtrées ou ligaturées.
* **Corrosion Encre — Inversion** (`paleo_ink_corrosion`) : Compensation de la corrosion de l'encre (attaque chimique du support).
* **Aplatissement Parchemin** (`paleo_parchment_flatten`) : Correction de l'éclairage inégal (ondulations, plis).
* **Ductus Révélation** (`paleo_ductus_reveal`) : Révélation du ductus (direction des traits de plume).
* **Enluminures — Extraction** (`paleo_illumination_enhance`) : Extraction et mise en valeur des enluminures et lettrines.
* **IR Reflectography** (`paleo_ir_simulation`) : Simulation de réflectographie IR pour sous-dessins et repentirs.
* **Filigrane — Révélation** (`paleo_watermark_reveal`) : Révélation des filigranes de papier par transparence.
* **Stabilisation Texte** (`paleo_text_stabilize`) : Alignement des lignes de base et redressement des caractères.
* **Datation Encre — Spectre** (`paleo_ink_dating`) : Analyse spectrale indicative (carbone, ferro-gallique).
* **Fluorescence UV — Simulation** (`paleo_uv_fluorescence_sim`) : Simulation de fluorescence induite par UV (365nm).
* **Carte des Lacunes** (`paleo_lacuna_map`) : Cartographie thermique des zones illisibles ou dégradées.
* **Grille de Réglures** (`paleo_baseline_grid`) : Détection des lignes de base et superposition d'une grille.
* **Lignes de Chaînette — Papier** (`paleo_chain_lines`) : Révélation des lignes de chaînette (FFT) pour datation/identification.
* **Carte de Densité d'Encre** (`paleo_ink_density_map`) : Cartographie thermique pour repérer changements de main ou ré-encrage.
* **Palimpseste — Séparation Couches** (`paleo_palimpsest_separate`) : Séparation de deux couches d'écriture superposées.
* **Empilement Multi-Échelle** (`paleo_focus_stack`) : Combine plusieurs niveaux de rehaussement (focus-stacking).
* **Isolation Marginalia** (`paleo_marginalia_isolate`) : Isolation des annotations marginales (gloses, notes).
* **Simulation Multispectrale** (`multispectral_sim`) : Simule UV/IR pour révéler encres effacées.
* **Séparation d’Encre Historique** (`ink_separation`) : Sépare encres ferro-gallique / carbone.
* **Boost Transcription Paléographique** (`transcription_boost`) : Contraste local + netteté pour lecture de manuscrits.
* **Révélation Palimpseste** (`palimpsest_reveal`) : Technique inspirée ICA/PCA pour textes sous-jacents.
* **Fluorescence UV Simulée** (`uv_fluorescence`) : Simule fluorescence des encres sous UV.
* **Réflectance IR** (`ir_reflectance`) : Simulation infrarouge pour visibilité des encres carbone.
* **Boost Contours Écriture** (`script_edge_boost`) : Renforce les traits d’écriture tout en réduisant le bruit de parchemin.
* **Suppression Texture Parchemin** (`parchment_remove`) : Réduit le bruit de fibre du support pour isoler l’encre.

## 🏛️ Épigraphie et Inscriptions (`epigraphy`)
*Outils pour pierres gravées, inscriptions murales, érosion et polychromie.*
* **Compensation Érosion** (`epi_erosion_compensate`) : Reconstruction des parties manquantes par interpolation des contours.
* **Suppression Lichens** (`epi_lichen_remove`) : Suppression des lichens et végétation recouvrant les inscriptions.
* **Lumière Rasant Mur** (`epi_raking_enhance`) : Accentue les reliefs et incisions par éclairage latéral simulé.
* **Carte de Profondeur** (`epi_depth_map`) : Génération d'une carte de profondeur pour quantifier l'érosion.
* **Suppression Mousse/Algae** (`epi_moss_remove`) : Suppression de la mousse, algues et biofilm.
* **Suppression Patine** (`epi_patina_remove`) : Suppression de la patine noire/verte des métaux ou oxydation des pierres.
* **Réparation Fissures** (`epi_crack_repair`) : Interpolation linéaire des zones endommagées par les fissures.
* **Relief 3D Inscription** (`epi_3d_relief`) : Reconstruction visuelle du relief 3D des inscriptions gravées.
* **Restauration Sablage** (`epi_sandblast_restore`) : Reconstruction par direction de l'érosion dominante (vent/sable).
* **Stéréo Multi-Vue** (`epi_multiview_stereo`) : Simulation de stéréo-photométrie pour extraire la géométrie 3D.
* **Inversion Altération** (`epi_weathering_reverse`) : Inversion des effets d'altération météorologique (pluie, gel, soleil).
* **Trace Encre Rouge** (`epi_ink_trace`) : Extraction des traces d'encre rouge (ocre, cinabre) sur pierre.
* **Nettoyage Surface** (`epi_surface_clean`) : Suppression des salissures et dépôts superficiels.
* **Analyse Pigments** (`epi_pigment_analysis`) : Analyse indicative des pigments (ocre, cinabre, charbon).
* **RTI Simplifié** (`epi_rti_simple`) : Reflectance Transformation Imaging combinant plusieurs éclairages virtuels.
* **Extraction Inscription** (`epi_inscription_extract`) : Segmentation adaptative pour séparer le texte du support.
* **Renforcement Traits** (`epi_stroke_enhance`) : Amplification des structures linéaires cohérentes (traits fins).
* **Carte des Normales** (`epi_normal_map`) : Génère une normal-map (RVB) pour workflows RTI et 3D.
* **Tracé des Contours de Lettres** (`epi_letter_outline_trace`) : Détection et traçage fin des contours de lettres gravées.
* **Profil de Gravure** (`epi_groove_profile`) : Trace un profil de profondeur le long d'une ligne horizontale.
* **Statistiques Hauteur des Lettres** (`epi_letter_height_stats`) : Détecte les lettres et superpose leurs boîtes avec hauteur moyenne.
* **Résidus de Polychromie — UV** (`epi_paint_residue_uv`) : Simulation de détection des résidus de peinture dans les lettres incisées.
* **Séparation Inscriptions Superposées** (`epi_graffiti_layer_split`) : Sépare deux phases de graffitis (anciennes vs récentes).

## 🎭 Artistique et Créatif (`artistic`)
*Effets visuels, rendus traditionnels et altérations créatives.*
* **Relief (Emboss)** (`emboss`) : Effet relief 3D.
* **Pixelisation** (`pixelate`) : Effet pixelisation rétro.
* **Glitch RGB** (`glitch`) : Effet glitch cyberpunk par décalage des canaux RGB.
* **Lignes de Scan CRT** (`scanlines`) : Effet scanlines d'écran CRT vintage.
* **Postérisation** (`posterize`) : Réduction du nombre de niveaux de couleur.
* **Peinture à l'huile** (`oil_painting`) : Simulation de peinture à l'huile.
* **Croquis** (`sketch`) : Conversion en dessin au crayon.
* **Aquarelle** (`watercolor`) : Effet aquarelle par lissage et renforcement des contours.
* **Trame de demi-teintes** (`halftone`) : Simulation d'impression en trame de demi-teintes.
* **Vignettage** (`vignette`) : Assombrissement progressif des bords.
* **Tilt-Shift** (`tilt_shift`) : Effet tilt-shift (miniature).
* **Effet Lomo** (`lomo`) : Effet style appareil photo Lomo.
* **Double Exposition** (`double_exposure`) : Simulation de double exposition photographique.
* **Aberration Chromatique** (`chromatic_aberration`) : Simulation d'aberration chromatique (décalage RGB).
* **Projection Holographique** (`holographic`) : Effet visuel scientifique futuriste pour mise en valeur.

## 🌀 Distorsion et Géométrie (`distortion`)
*Altérations de la perspective et de la forme.*
* **Fisheye** (`fisheye`) : Distorsion fisheye (grand-angle extrême).
* **Tourbillon** (`swirl`) : Distorsion en tourbillon spiral.
* **Ondulation** (`ripple`) : Effet ondulation d'eau.
* **Distorsion Barrel** (`barrel`) : Correction/distorsion barrel standard (objectif grand-angle).
* **Distorsion Coussin** (`pincushion`) : Distorsion pincushion (téléobjectif).
* **Sphérisation** (`spherize`) : Effet de sphérisation 3D (bulle).

## 💧 Flou et Profondeur (`blur`)
*Simulations de profondeur de champ et flous directionnels.*
* **Flou de Mouvement** (`motion_blur`) : Flou directionnel simulant un mouvement de caméra.
* **Flou Radial** (`radial_blur`) : Flou radial émanant du centre de l'image.
* **Bokeh** (`bokeh`) : Flou de profondeur de champ style bokeh.
* **Flou de Zoom** (`zoom_blur`) : Flou de zoom radié depuis le centre.
* **Flou de Surface** (`surface_blur`) : Flou préservant les contours (filtre bilatéral approximé).
* **Flou Tilt-Shift** (`tilt_shift_blur`) : Flou sélectif simulant un objectif tilt-shift.

## 🖌️ Stylisation et Rendu (`stylize`)
*Transpositions stylistiques (cinéma, rétro, pop-culture).*
* **Crayon de Couleur** (`pencil_color`) : Effet crayon de couleur avec texture de papier.
* **Comic Book** (`comic_book`) : Style bande dessinée avec contours noirs et aplats.
* **Low Poly** (`low_poly`) : Approximation low-poly par quantification de couleur.
* **Néon Glow** (`neon_glow`) : Effet néon luminescent sur les contours.
* **Cyberpunk** (`cyberpunk`) : Look cyberpunk néon avec tons magenta/cyan.
* **Grain Pellicule** (`film_grain`) : Grain organique style pellicule argentique 35mm.
* **Fondu Vintage** (`vintage_fade`) : Fondu vintage avec teinte brunâtre et lift des ombres.
* **Effet VHS** (`vhs`) : Dégradation style cassette VHS.
* **Infrarouge** (`infrared`) : Simulation de photographie infrarouge (fausses couleurs).
* **Film Analogique** (`analog_film`) : Simulation de film analogique avec grain, vignette et courbes.

## 💡 Éclairage et Lumière (`lighting`)
*Ajout ou simulation de sources lumineuses et d'effets optiques.*
* **Flare Objectif** (`lens_flare`) : Simulation de flare d'objectif avec orbes lumineux.
* **Rayons de Lumière** (`god_rays`) : Rayons de lumière volumétriques (crepuscular rays).
* **Bloom** (`bloom`) : Effet bloom pour les zones surexposées.
* **Lumière Volumétrique** (`volumetric_light`) : Simulation de lumière volumétrique traversant la scène.
* **Lumière de Bord** (`rim_light`) : Lumière de bord pour faire ressortir les silhouettes.
* **Projecteur** (`spotlight`) : Effet de projecteur/faisceau lumineux directionnel.

## ⚙️ Effets Personnalisés (`custom`)
*Modules configurables et exemples d'implémentation avancée.*
* **[CUSTOM] Vignette** (`custom_example`) : Exemple d'effet custom — vignettage.
* **[CUSTOM] Courbe de Tonalité** (`custom_tone_curve`) : Courbe de tonalité personnalisable (5 points de contrôle).
* **[CUSTOM] LUT Cinéma** (`custom_lut`) : Application de LUT 3D pour grading cinéma (warm/teal).
* **[CUSTOM] Aberration Chromatique** (`custom_chromatic`) : Aberration chromatique contrôlée (radiale ou linéaire).
* **[CUSTOM] Flare Anamorphique** (`custom_anamorphic`) : Simulation de flare anamorphique (streaks horizontaux).
* **[CUSTOM] Tramage Ordered** (`custom_dither`) : Tramage ordonné (Bayer dithering) pour effet rétro pixel.

## 🌍 OSINT et Vérification d'Image (`osint`)
*Outils d'investigation en sources ouvertes (géolocalisation, vérification de contexte).*
* **OSINT — Compas des Ombres** (`osint_shadow_compass`) : Détecte la direction des ombres pour recoupement avec la position du soleil.
* **OSINT — Grille de Point de Fuite** (`osint_vanishing_grid`) : Estime un point de fuite approximatif pour comparer la géométrie d'un lieu.
* **OSINT — Sonde de Reflets** (`osint_reflection_probe`) : Amplifie le contraste dans les reflets (vitres, eau) pour révéler des détails cachés.
* **OSINT — Vérification d'Horizon** (`osint_horizon_level`) : Mesure l'inclinaison de la ligne d'horizon (contrôle cohérence caméra).
* **OSINT — Cohérence Chromatique** (`osint_color_consistency`) : Compare la température de couleur entre les quadrants pour détecter des photomontages.
* **OSINT — Lisibilité d'Enseignes** (`osint_signage_legibility`) : Pipeline d'amélioration pour texte de petite taille (panneaux, devantures).

## 🔬 Analyse Scientifique (`scientific`)
*Transformations mathématiques et spectrales.*
* **Analyse Texture Fourier** (`fourier_texture`) : Composantes fréquentielles pour détecter patterns périodiques.
* **Enhancement PCA-like** (`pca_enhance`) : Simulation d’analyse en composantes principales pour MSI.
* **Simulation Radiographie** (`xray_sim`) : Effet rayons X pour visualiser sous-couches et reliefs.

## 🤖 Détection IA et Artefacts (`ai_detection`)
*Outils spécifiques pour identifier les images générées par Intelligence Artificielle.*
* **FFT Spectrum - Anomalies IA** (`ai_fft_spectrum`) : Visualise le spectre de Fourier (pics/motifs périodiques anormaux).
* **High-Frequency Residual (IA)** (`ai_high_freq`) : Extrait les hautes fréquences (bruit structuré ou absent).
* **ELA Enhanced - AI Compression** (`ai_ela_enhanced`) : ELA optimisé pour détecter le lissage typique des générateurs IA.
* **Noise Pattern Analysis** (`ai_noise_pattern`) : Visualise le pattern de bruit (souvent uniforme ou corrélé sur l'IA).
* **Checkerboard / Upsampling Artifacts** (`ai_checkerboard`) : Met en évidence les motifs en damier (convolutions transposées).
* **Spectral Anomaly Boost** (`ai_spectral_anomaly`) : Amplifie les anomalies dans le domaine fréquentiel (pics des modèles de diffusion).
* **Smoothness / Plastic Map** (`ai_smoothness_map`) : Met en évidence les zones excessivement lisses (« plastic look »).
* **PRNU Absence (AI Signature)** (`ai_prnu_absence`) : Détecte l'absence de signature capteur PRNU (bruit résiduel très uniforme).
* **Edge Incoherence Detector** (`ai_edge_incoherence`) : Renforce les contours pour révéler des transitions de blending peu naturelles.
* **Combined AI Forensic View** (`ai_combined_forensic`) : Vue combinée (FFT + Noise + ELA) pour une analyse rapide.

***

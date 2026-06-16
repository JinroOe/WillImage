#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║  INGEN SYSTEMS — IMAGE FORENSICS WORKSTATION v2.0        ║
║  Classified Analysis Tool — Authorized Personnel Only    ║
╚══════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import json
import math
import struct
import hashlib
import colorsys
import io
import traceback
import threading
import time
from datetime import datetime
from collections import Counter
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps, ImageDraw
import numpy as np

# ── Palette phosphore ──────────────────────────────────────
C_BG        = "#050a05"
C_BG2       = "#0a0f0a"
C_BG3       = "#0f150f"
C_PANEL     = "#0d1a0d"
C_BORDER    = "#1a3a1a"
C_GREEN     = "#00ff41"
C_GREEN2    = "#00cc33"
C_GREEN3    = "#008822"
C_AMBER     = "#ffb000"
C_RED       = "#ff2222"
C_CYAN      = "#00e5ff"
C_WHITE     = "#e8ffe8"
C_DIM       = "#3a5a3a"
FONT_MONO   = ("Courier New", 10)
FONT_MONO_S = ("Courier New", 9)
FONT_MONO_L = ("Courier New", 12, "bold")
FONT_TITLE  = ("Courier New", 14, "bold")

EFFECTS_FILE = os.path.join(os.path.dirname(__file__), "effects.json")


# ══════════════════════════════════════════════════════════════
#  UTILITIES
# ══════════════════════════════════════════════════════════════

def load_effects():
    with open(EFFECTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["effects"]


def apply_effect(img: Image.Image, effect: dict) -> Image.Image:
    params = effect.get("params", {})
    code = effect.get("code", "return img.copy()")
    local_ns = {"img": img, "params": params}
    # Wrap code in a function to support `return`
    wrapped = "def _effect(img, params):\n"
    for line in code.splitlines():
        wrapped += "    " + line + "\n"
    exec(wrapped, local_ns)
    result = local_ns["_effect"](img, params)
    return result


def file_hash(path, algo="md5"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_exif(img: Image.Image) -> dict:
    try:
        from PIL.ExifTags import TAGS, GPSTAGS
        exif_raw = img._getexif()
        if not exif_raw:
            return {}
        decoded = {}
        for tag_id, value in exif_raw.items():
            tag = TAGS.get(tag_id, str(tag_id))
            if tag == "GPSInfo":
                gps = {}
                for gps_id, gps_val in value.items():
                    gps_tag = GPSTAGS.get(gps_id, str(gps_id))
                    gps[gps_tag] = gps_val
                decoded["GPS_RAW"] = gps
            else:
                try:
                    if isinstance(value, bytes):
                        value = value.decode("utf-8", errors="replace")
                    decoded[tag] = str(value)[:200]
                except Exception:
                    pass
        return decoded
    except Exception:
        return {}


def gps_to_decimal(gps_raw: dict):
    try:
        lat_ref = gps_raw.get("GPSLatitudeRef", "N")
        lon_ref = gps_raw.get("GPSLongitudeRef", "E")
        lat_vals = gps_raw.get("GPSLatitude", None)
        lon_vals = gps_raw.get("GPSLongitude", None)
        if not lat_vals or not lon_vals:
            return None, None

        def to_deg(vals):
            d, m, s = vals
            # Handle IFDRational or tuples
            def to_float(v):
                if hasattr(v, 'numerator'):
                    return v.numerator / v.denominator if v.denominator else 0
                if isinstance(v, tuple):
                    return v[0] / v[1] if v[1] else 0
                return float(v)
            return to_float(d) + to_float(m) / 60 + to_float(s) / 3600

        lat = to_deg(lat_vals)
        lon = to_deg(lon_vals)
        if lat_ref == "S":
            lat = -lat
        if lon_ref == "W":
            lon = -lon
        return lat, lon
    except Exception:
        return None, None


def dominant_colors(img: Image.Image, n=8):
    small = img.convert("RGB").resize((100, 100), Image.LANCZOS)
    pixels = list(small.getdata())
    quantized = small.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette()[:n*3]
    colors = []
    for i in range(n):
        r, g, b = palette[i*3], palette[i*3+1], palette[i*3+2]
        colors.append((r, g, b))
    return colors


def analyze_image_full(path: str, img: Image.Image) -> dict:
    result = {}

    # ── File properties ──
    stat = os.stat(path)
    result["file"] = {
        "path": path,
        "filename": os.path.basename(path),
        "size_bytes": stat.st_size,
        "size_human": f"{stat.st_size / 1024:.2f} KB" if stat.st_size < 1_048_576 else f"{stat.st_size / 1_048_576:.2f} MB",
        "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        "md5": file_hash(path, "md5"),
        "sha256": file_hash(path, "sha256"),
        "format": img.format or "N/A",
        "mime": f"image/{(img.format or 'unknown').lower()}",
    }

    # ── Image properties ──
    rgb = img.convert("RGB")
    arr = np.array(rgb, dtype=np.float32)
    w, h = img.size
    result["image"] = {
        "width": w,
        "height": h,
        "megapixels": f"{(w * h) / 1_000_000:.2f} MP",
        "aspect_ratio": f"{w/math.gcd(w,h)}:{h/math.gcd(w,h)}",
        "mode": img.mode,
        "channels": len(img.getbands()),
        "has_alpha": "A" in img.getbands(),
        "bit_depth": 8 * len(img.getbands()),
        "dpi": str(img.info.get("dpi", "N/A")),
        "compression": img.info.get("compression", "N/A"),
    }

    # ── Color analysis ──
    r_ch = arr[:,:,0].flatten()
    g_ch = arr[:,:,1].flatten()
    b_ch = arr[:,:,2].flatten()
    mean_r, mean_g, mean_b = r_ch.mean(), g_ch.mean(), b_ch.mean()
    gray = arr.mean(axis=2).flatten()

    result["colors"] = {
        "mean_rgb": f"({mean_r:.1f}, {mean_g:.1f}, {mean_b:.1f})",
        "mean_brightness": f"{gray.mean():.1f}/255",
        "brightness_pct": f"{gray.mean()/255*100:.1f}%",
        "std_dev": f"{gray.std():.2f}",
        "contrast_rms": f"{np.sqrt(np.mean((gray - gray.mean())**2)):.2f}",
        "dominant_channel": ["Rouge", "Vert", "Bleu"][np.argmax([mean_r, mean_g, mean_b])],
        "is_grayscale": bool(np.allclose(r_ch, g_ch, atol=5) and np.allclose(g_ch, b_ch, atol=5)),
        "entropy": f"{-np.sum(np.unique(gray.astype(int), return_counts=True)[1]/len(gray) * np.log2(np.unique(gray.astype(int), return_counts=True)[1]/len(gray) + 1e-10)):.3f} bits",
    }

    dom = dominant_colors(img, 8)
    result["colors"]["dominant_palette"] = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in dom]

    # ── EXIF / Metadata ──
    exif = parse_exif(img)
    gps_raw = exif.pop("GPS_RAW", {})
    result["exif"] = exif
    result["gps"] = {}
    if gps_raw:
        lat, lon = gps_to_decimal(gps_raw)
        result["gps"]["raw"] = {k: str(v)[:100] for k, v in gps_raw.items()}
        if lat is not None:
            result["gps"]["latitude"] = f"{lat:.6f}°"
            result["gps"]["longitude"] = f"{lon:.6f}°"
            result["gps"]["maps_url"] = f"https://www.google.com/maps?q={lat},{lon}"

    # ── PNG chunks ──
    result["png_chunks"] = {}
    if img.format == "PNG":
        for key, val in img.info.items():
            try:
                result["png_chunks"][key] = str(val)[:200]
            except Exception:
                pass

    return result


# ══════════════════════════════════════════════════════════════
#  EFFECT EDITOR DIALOG
# ══════════════════════════════════════════════════════════════

class EffectEditorDialog(tk.Toplevel):
    def __init__(self, parent, effect=None, on_save=None):
        super().__init__(parent)
        self.on_save = on_save
        self.edit_mode = effect is not None
        self.configure(bg=C_BG)
        self.title("◈ ÉDITEUR D'EFFET CUSTOM")
        self.geometry("720x600")
        self.resizable(True, True)

        title = "MODIFIER EFFET" if self.edit_mode else "NOUVEL EFFET CUSTOM"
        tk.Label(self, text=f"╔ {title} ╗", font=FONT_TITLE,
                 bg=C_BG, fg=C_GREEN).pack(pady=(16, 8))

        frm = tk.Frame(self, bg=C_BG)
        frm.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)

        def lbl(text, row, col=0):
            tk.Label(frm, text=text, font=FONT_MONO_S, bg=C_BG, fg=C_GREEN2,
                     anchor="w").grid(row=row, column=col, sticky="w", padx=4, pady=2)

        lbl("ID (unique, snake_case):", 0)
        self.id_var = tk.StringVar(value=effect.get("id", "") if effect else "")
        tk.Entry(frm, textvariable=self.id_var, font=FONT_MONO, bg=C_BG3,
                 fg=C_GREEN, insertbackground=C_GREEN, relief="flat",
                 highlightthickness=1, highlightcolor=C_GREEN3).grid(
                     row=0, column=1, sticky="ew", padx=4, pady=2)

        lbl("Nom affiché:", 1)
        self.name_var = tk.StringVar(value=effect.get("name", "") if effect else "")
        tk.Entry(frm, textvariable=self.name_var, font=FONT_MONO, bg=C_BG3,
                 fg=C_GREEN, insertbackground=C_GREEN, relief="flat",
                 highlightthickness=1, highlightcolor=C_GREEN3).grid(
                     row=1, column=1, sticky="ew", padx=4, pady=2)

        lbl("Description:", 2)
        self.desc_var = tk.StringVar(value=effect.get("description", "") if effect else "")
        tk.Entry(frm, textvariable=self.desc_var, font=FONT_MONO, bg=C_BG3,
                 fg=C_GREEN, insertbackground=C_GREEN, relief="flat",
                 highlightthickness=1, highlightcolor=C_GREEN3).grid(
                     row=2, column=1, sticky="ew", padx=4, pady=2)

        lbl("Paramètres JSON:", 3)
        self.params_var = tk.StringVar(value=json.dumps(effect.get("params", {})) if effect else "{}")
        tk.Entry(frm, textvariable=self.params_var, font=FONT_MONO, bg=C_BG3,
                 fg=C_AMBER, insertbackground=C_AMBER, relief="flat",
                 highlightthickness=1, highlightcolor=C_GREEN3).grid(
                     row=3, column=1, sticky="ew", padx=4, pady=2)

        frm.columnconfigure(1, weight=1)

        tk.Label(frm, text="Code Python (variable 'img': PIL.Image, 'params': dict → return PIL.Image):",
                 font=FONT_MONO_S, bg=C_BG, fg=C_GREEN2, anchor="w").grid(
                     row=4, column=0, columnspan=2, sticky="w", padx=4, pady=(8,2))

        default_code = effect.get("code", "# Exemple:\n# from PIL import ImageOps\n# return ImageOps.grayscale(img).convert('RGB')") if effect else \
                       "# Votre effet ici\n# 'img' = PIL.Image.Image\n# 'params' = dict des paramètres\n# Retournez un PIL.Image.Image\nresult = img.copy()\nreturn result"

        self.code_text = scrolledtext.ScrolledText(frm, font=("Courier New", 10),
                                                    bg="#000a00", fg=C_GREEN,
                                                    insertbackground=C_GREEN,
                                                    selectbackground=C_GREEN3,
                                                    relief="flat", height=14,
                                                    wrap=tk.NONE)
        self.code_text.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)
        self.code_text.insert("1.0", default_code)
        frm.rowconfigure(5, weight=1)

        btn_frm = tk.Frame(self, bg=C_BG)
        btn_frm.pack(pady=12)
        tk.Button(btn_frm, text="[ TESTER ]", font=FONT_MONO, bg=C_BG3,
                  fg=C_AMBER, activebackground=C_GREEN3, relief="flat",
                  padx=12, command=self.test_effect).pack(side=tk.LEFT, padx=8)
        tk.Button(btn_frm, text="[ SAUVEGARDER ]", font=FONT_MONO, bg=C_BG3,
                  fg=C_GREEN, activebackground=C_GREEN3, relief="flat",
                  padx=12, command=self.save_effect).pack(side=tk.LEFT, padx=8)
        tk.Button(btn_frm, text="[ ANNULER ]", font=FONT_MONO, bg=C_BG3,
                  fg=C_RED, activebackground=C_GREEN3, relief="flat",
                  padx=12, command=self.destroy).pack(side=tk.LEFT, padx=8)

    def test_effect(self):
        code = self.code_text.get("1.0", tk.END).strip()
        try:
            test_img = Image.new("RGB", (64, 64), (128, 64, 200))
            params = json.loads(self.params_var.get() or "{}")
            effect = {"code": code, "params": params}
            result = apply_effect(test_img, effect)
            messagebox.showinfo("TEST OK",
                                f"✓ Effet compilé avec succès.\nType retourné: {type(result).__name__}\nTaille: {result.size}")
        except Exception as e:
            messagebox.showerror("ERREUR", f"Erreur dans le code:\n\n{traceback.format_exc()}")

    def save_effect(self):
        eid = self.id_var.get().strip()
        name = self.name_var.get().strip()
        code = self.code_text.get("1.0", tk.END).strip()
        if not eid or not name or not code:
            messagebox.showerror("ERREUR", "ID, Nom et Code sont obligatoires.")
            return
        try:
            params = json.loads(self.params_var.get() or "{}")
        except json.JSONDecodeError:
            messagebox.showerror("ERREUR", "Paramètres JSON invalides.")
            return

        effect = {
            "id": eid,
            "name": f"[CUSTOM] {name}",
            "category": "custom",
            "description": self.desc_var.get().strip(),
            "params": params,
            "code": code,
        }

        # Save to JSON
        with open(EFFECTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        existing_ids = [e["id"] for e in data["effects"]]
        if eid in existing_ids:
            idx = existing_ids.index(eid)
            data["effects"][idx] = effect
        else:
            data["effects"].append(effect)

        with open(EFFECTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        if self.on_save:
            self.on_save()
        messagebox.showinfo("SAUVEGARDÉ", f"Effet '{name}' sauvegardé dans effects.json")
        self.destroy()


# ══════════════════════════════════════════════════════════════
#  HISTOGRAM CANVAS
# ══════════════════════════════════════════════════════════════

class HistogramCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=C_BG, highlightthickness=0, **kwargs)

    def draw(self, img: Image.Image):
        self.delete("all")
        w = self.winfo_width() or 280
        h = self.winfo_height() or 100
        if w < 10 or h < 10:
            return
        arr = np.array(img.convert("RGB"))
        colors_map = [("red", 0, C_RED), ("green", 1, C_GREEN), ("blue", 2, "#4488ff")]
        for color_name, ch_idx, color_hex in colors_map:
            channel = arr[:, :, ch_idx].flatten()
            hist, _ = np.histogram(channel, bins=64, range=(0, 255))
            hist = hist / (hist.max() + 1e-6)
            points = []
            for i, val in enumerate(hist):
                x = int(i * w / 64)
                y = int(h - val * (h - 4))
                points.extend([x, y])
            points.extend([w, h, 0, h])
            if len(points) >= 4:
                self.create_polygon(points, fill="", outline=color_hex, width=1)
        # Grid
        for i in range(0, w, w//8):
            self.create_line(i, 0, i, h, fill=C_BORDER, width=1)


# ══════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════════

class ImageAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INGEN SYSTEMS — IMAGE FORENSICS WORKSTATION v2.0")
        self.configure(bg=C_BG)
        self.geometry("1440x900")
        self.minsize(1100, 700)

        self.img_path: str = None
        self.img_original: Image.Image = None
        self.img_display: Image.Image = None
        self.img_photo: ImageTk.PhotoImage = None
        self.analysis_data: dict = {}
        self.effects_list: list = []
        self.current_effect_id = "none"
        self._scan_job = None
        self._clock_job = None

        self._build_style()
        self._build_ui()
        self._reload_effects()
        self._start_clock()
        self._animate_scanline()

    # ── Style ──────────────────────────────────────────────────
    def _build_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background=C_BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=C_BG2, foreground=C_DIM,
                        font=FONT_MONO_S, padding=[12, 4], borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", C_BG3)],
                  foreground=[("selected", C_GREEN)])
        style.configure("TScrollbar", background=C_BG2, troughcolor=C_BG,
                        borderwidth=0, arrowcolor=C_GREEN3)
        style.configure("Treeview", background=C_BG2, fieldbackground=C_BG2,
                        foreground=C_GREEN2, rowheight=20, font=FONT_MONO_S)
        style.configure("Treeview.Heading", background=C_BG3,
                        foreground=C_GREEN, font=FONT_MONO_S)
        style.map("Treeview", background=[("selected", C_GREEN3)],
                  foreground=[("selected", C_WHITE)])

    # ── UI Layout ──────────────────────────────────────────────
    def _build_ui(self):
        # ─── Header ───
        header = tk.Frame(self, bg=C_BG, height=48)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        tk.Label(header, text="◈ INGEN SYSTEMS", font=("Courier New", 16, "bold"),
                 bg=C_BG, fg=C_GREEN).pack(side=tk.LEFT, padx=16, pady=8)
        tk.Label(header, text="IMAGE FORENSICS WORKSTATION", font=("Courier New", 11),
                 bg=C_BG, fg=C_GREEN3).pack(side=tk.LEFT, padx=4, pady=8)

        self.clock_var = tk.StringVar(value="")
        tk.Label(header, textvariable=self.clock_var, font=FONT_MONO_S,
                 bg=C_BG, fg=C_DIM).pack(side=tk.RIGHT, padx=16)

        self.status_var = tk.StringVar(value="SYSTÈME PRÊT — Chargez une image pour commencer")
        tk.Label(header, textvariable=self.status_var, font=FONT_MONO_S,
                 bg=C_BG, fg=C_AMBER).pack(side=tk.RIGHT, padx=16)

        tk.Frame(self, bg=C_BORDER, height=1).pack(fill=tk.X)

        # ─── Main paned ───
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=C_BG,
                               sashwidth=4, sashrelief="flat", sashpad=0)
        paned.pack(fill=tk.BOTH, expand=True)

        # ─ Left panel ─
        left = tk.Frame(paned, bg=C_PANEL, width=290)
        left.pack_propagate(False)
        paned.add(left, minsize=240)
        self._build_left_panel(left)

        # ─ Center panel ─
        center = tk.Frame(paned, bg=C_BG)
        paned.add(center, minsize=500)
        self._build_center_panel(center)

        # ─ Right panel ─
        right = tk.Frame(paned, bg=C_PANEL, width=360)
        right.pack_propagate(False)
        paned.add(right, minsize=300)
        self._build_right_panel(right)

        # ─── Status bar ───
        tk.Frame(self, bg=C_BORDER, height=1).pack(fill=tk.X)
        sbar = tk.Frame(self, bg=C_BG, height=22)
        sbar.pack(fill=tk.X, side=tk.BOTTOM)
        sbar.pack_propagate(False)
        self.pixel_var = tk.StringVar(value="")
        tk.Label(sbar, textvariable=self.pixel_var, font=("Courier New", 8),
                 bg=C_BG, fg=C_DIM).pack(side=tk.LEFT, padx=8)

    # ── Left Panel ────────────────────────────────────────────
    def _build_left_panel(self, parent):
        tk.Label(parent, text="╔ CONTRÔLES ╗", font=FONT_MONO_S,
                 bg=C_PANEL, fg=C_GREEN).pack(pady=(12, 4), padx=8, anchor="w")

        # Load / Save buttons
        btn_cfg = dict(font=FONT_MONO_S, bg=C_BG, fg=C_GREEN,
                       activebackground=C_GREEN3, activeforeground=C_WHITE,
                       relief="flat", bd=0, padx=8, pady=4, cursor="hand2")

        tk.Button(parent, text="▶ CHARGER IMAGE", command=self._load_image,
                  **btn_cfg).pack(fill=tk.X, padx=12, pady=3)
        tk.Button(parent, text="▼ EXPORTER IMAGE TRAITÉE", command=self._export_image,
                  **btn_cfg).pack(fill=tk.X, padx=12, pady=3)
        tk.Button(parent, text="▼ EXPORTER RAPPORT", command=self._export_report,
                  **btn_cfg).pack(fill=tk.X, padx=12, pady=3)

        tk.Frame(parent, bg=C_BORDER, height=1).pack(fill=tk.X, padx=8, pady=8)

        # ─ Effects ─
        tk.Label(parent, text="╔ EFFETS IMAGE ╗", font=FONT_MONO_S,
                 bg=C_PANEL, fg=C_GREEN).pack(pady=(0, 4), padx=8, anchor="w")

        self.effect_var = tk.StringVar()
        self.effect_combo = ttk.Combobox(parent, textvariable=self.effect_var,
                                          font=FONT_MONO_S, state="readonly")
        self.effect_combo.pack(fill=tk.X, padx=12, pady=2)
        self.effect_combo.bind("<<ComboboxSelected>>", self._on_effect_change)

        self.effect_desc = tk.Label(parent, text="", font=("Courier New", 8),
                                    bg=C_PANEL, fg=C_DIM, wraplength=240,
                                    justify="left", anchor="nw")
        self.effect_desc.pack(fill=tk.X, padx=12, pady=(0, 4))

        btn_cfg2 = dict(**btn_cfg)
        btn_cfg2["fg"] = C_AMBER
        tk.Button(parent, text="✎ AJOUTER EFFET CUSTOM",
                  command=self._add_custom_effect, **btn_cfg2).pack(fill=tk.X, padx=12, pady=2)
        tk.Button(parent, text="✎ MODIFIER EFFET SÉLECTIONNÉ",
                  command=self._edit_selected_effect, **btn_cfg2).pack(fill=tk.X, padx=12, pady=2)

        tk.Frame(parent, bg=C_BORDER, height=1).pack(fill=tk.X, padx=8, pady=8)

        # ─ Adjustments ─
        tk.Label(parent, text="╔ AJUSTEMENTS ╗", font=FONT_MONO_S,
                 bg=C_PANEL, fg=C_GREEN).pack(pady=(0, 4), padx=8, anchor="w")

        sliders_cfg = [
            ("Luminosité", "brightness", 0.1, 3.0, 1.0),
            ("Contraste",  "contrast",   0.1, 3.0, 1.0),
            ("Saturation", "saturation", 0.0, 3.0, 1.0),
            ("Netteté",    "sharpness",  0.0, 3.0, 1.0),
        ]
        self.adj_vars = {}
        for label, key, lo, hi, default in sliders_cfg:
            frm = tk.Frame(parent, bg=C_PANEL)
            frm.pack(fill=tk.X, padx=12, pady=1)
            tk.Label(frm, text=f"{label}:", font=("Courier New", 8),
                     bg=C_PANEL, fg=C_DIM, width=10, anchor="w").pack(side=tk.LEFT)
            var = tk.DoubleVar(value=default)
            self.adj_vars[key] = var
            val_lbl = tk.Label(frm, text=f"{default:.1f}", font=("Courier New", 8),
                               bg=C_PANEL, fg=C_GREEN2, width=4)
            val_lbl.pack(side=tk.RIGHT)
            sl = tk.Scale(frm, variable=var, from_=lo, to=hi, resolution=0.05,
                          orient=tk.HORIZONTAL, bg=C_PANEL, fg=C_GREEN2,
                          troughcolor=C_BG, highlightthickness=0, showvalue=False,
                          command=lambda v, lbl=val_lbl, k=key: self._on_adj(v, lbl, k))
            sl.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Button(parent, text="↺ RESET AJUSTEMENTS",
                  command=self._reset_adjustments, **btn_cfg).pack(fill=tk.X, padx=12, pady=6)

        # ─ Histogram ─
        tk.Frame(parent, bg=C_BORDER, height=1).pack(fill=tk.X, padx=8, pady=4)
        tk.Label(parent, text="╔ HISTOGRAMME ╗", font=FONT_MONO_S,
                 bg=C_PANEL, fg=C_GREEN).pack(pady=(0, 2), padx=8, anchor="w")
        self.hist_canvas = HistogramCanvas(parent, height=90)
        self.hist_canvas.pack(fill=tk.X, padx=12, pady=4)
        self.hist_canvas.bind("<Configure>", lambda e: self._update_histogram())

        # ─ Dominant palette ─
        tk.Label(parent, text="PALETTE DOMINANTE:", font=("Courier New", 8),
                 bg=C_PANEL, fg=C_DIM).pack(anchor="w", padx=12, pady=(4, 0))
        self.palette_canvas = tk.Canvas(parent, height=28, bg=C_BG, highlightthickness=0)
        self.palette_canvas.pack(fill=tk.X, padx=12, pady=4)

    # ── Center Panel ──────────────────────────────────────────
    def _build_center_panel(self, parent):
        tk.Label(parent, text="╔ VISUALISATION ╗", font=FONT_MONO_S,
                 bg=C_BG, fg=C_GREEN).pack(anchor="w", padx=12, pady=(8, 0))

        # Toolbar
        toolbar = tk.Frame(parent, bg=C_BG)
        toolbar.pack(fill=tk.X, padx=12, pady=4)

        tb_cfg = dict(font=("Courier New", 8), bg=C_BG2, fg=C_GREEN2,
                      activebackground=C_GREEN3, relief="flat", padx=6, pady=2, cursor="hand2")

        self.zoom_var = tk.DoubleVar(value=1.0)
        tk.Button(toolbar, text="[-]", command=self._zoom_out, **tb_cfg).pack(side=tk.LEFT, padx=2)
        self.zoom_lbl = tk.Label(toolbar, text="100%", font=("Courier New", 8),
                                  bg=C_BG, fg=C_DIM, width=5)
        self.zoom_lbl.pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="[+]", command=self._zoom_in, **tb_cfg).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="[FIT]", command=self._zoom_fit, **tb_cfg).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="[1:1]", command=self._zoom_100, **tb_cfg).pack(side=tk.LEFT, padx=2)

        self.show_grid_var = tk.BooleanVar(value=False)
        tk.Checkbutton(toolbar, text="Grille", variable=self.show_grid_var,
                       bg=C_BG, fg=C_DIM, selectcolor=C_BG2, activebackground=C_BG,
                       font=("Courier New", 8), command=self._refresh_display).pack(side=tk.LEFT, padx=8)

        self.compare_var = tk.BooleanVar(value=False)
        tk.Checkbutton(toolbar, text="Comparer (avant/après)", variable=self.compare_var,
                       bg=C_BG, fg=C_DIM, selectcolor=C_BG2, activebackground=C_BG,
                       font=("Courier New", 8), command=self._refresh_display).pack(side=tk.LEFT, padx=4)

        # Image canvas with scrollbars
        canvas_frame = tk.Frame(parent, bg=C_BG)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        self.h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, bg=C_BG2)
        self.v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, bg=C_BG2)
        self.img_canvas = tk.Canvas(canvas_frame, bg="#000500", cursor="crosshair",
                                    highlightthickness=1, highlightbackground=C_BORDER,
                                    xscrollcommand=self.h_scroll.set,
                                    yscrollcommand=self.v_scroll.set)
        self.h_scroll.config(command=self.img_canvas.xview)
        self.v_scroll.config(command=self.img_canvas.yview)

        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.img_canvas.pack(fill=tk.BOTH, expand=True)

        self.img_canvas.bind("<Motion>", self._on_canvas_mouse)
        self.img_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.img_canvas.bind("<Configure>", lambda e: self._refresh_display())

        # Scanline overlay
        self._scanline_y = 0

        # Placeholder
        self._draw_placeholder()

    # ── Right Panel (Tabs) ────────────────────────────────────
    def _build_right_panel(self, parent):
        tk.Label(parent, text="╔ ANALYSE ╗", font=FONT_MONO_S,
                 bg=C_PANEL, fg=C_GREEN).pack(pady=(12, 0), padx=8, anchor="w")

        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        def make_tab(label):
            frm = tk.Frame(notebook, bg=C_BG2)
            notebook.add(frm, text=f" {label} ")
            return frm

        # Tab: Fichier
        tab_file = make_tab("FICHIER")
        self.tv_file = self._make_treeview(tab_file)

        # Tab: Image
        tab_img = make_tab("IMAGE")
        self.tv_image = self._make_treeview(tab_img)

        # Tab: Couleurs
        tab_col = make_tab("COULEURS")
        self.tv_colors = self._make_treeview(tab_col)

        # Tab: EXIF
        tab_exif = make_tab("EXIF")
        self.tv_exif = self._make_treeview(tab_exif)

        # Tab: GPS
        tab_gps = make_tab("GPS")
        self._build_gps_tab(tab_gps)

        # Tab: PNG
        tab_png = make_tab("CHUNKS")
        self.tv_png = self._make_treeview(tab_png)

        # Tab: Pixel Inspector
        tab_px = make_tab("PIXEL")
        self._build_pixel_tab(tab_px)

        # Tab: Forensique
        tab_forensic = make_tab("FORENSIQUE")
        self._build_forensic_tab(tab_forensic)

    def _make_treeview(self, parent):
        frm = tk.Frame(parent, bg=C_BG2)
        frm.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        sb = ttk.Scrollbar(frm)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        tv = ttk.Treeview(frm, columns=("val",), show="tree headings",
                          yscrollcommand=sb.set)
        tv.heading("#0", text="Propriété", anchor="w")
        tv.heading("val", text="Valeur", anchor="w")
        tv.column("#0", width=140, minwidth=100)
        tv.column("val", width=180, minwidth=100)
        sb.config(command=tv.yview)
        tv.pack(fill=tk.BOTH, expand=True)
        return tv

    def _build_gps_tab(self, parent):
        self.tv_gps = self._make_treeview(parent)
        self.gps_map_btn = tk.Button(parent, text="▶ OUVRIR DANS GOOGLE MAPS",
                                      font=FONT_MONO_S, bg=C_BG, fg=C_CYAN,
                                      activebackground=C_GREEN3, relief="flat",
                                      command=self._open_maps, state="disabled")
        self.gps_map_btn.pack(fill=tk.X, padx=8, pady=4)

    def _build_pixel_tab(self, parent):
        frm = tk.Frame(parent, bg=C_BG2)
        frm.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.px_info = tk.StringVar(value="Survolez l'image pour inspecter les pixels")
        tk.Label(frm, textvariable=self.px_info, font=FONT_MONO_S,
                 bg=C_BG2, fg=C_GREEN2, justify="left", wraplength=300,
                 anchor="nw").pack(fill=tk.X, pady=4)

        self.px_color_canvas = tk.Canvas(frm, height=60, bg=C_BG, highlightthickness=0)
        self.px_color_canvas.pack(fill=tk.X, pady=4)

        tk.Label(frm, text="Loupe (5×5 pixels):", font=("Courier New", 8),
                 bg=C_BG2, fg=C_DIM).pack(anchor="w", pady=(8, 2))
        self.loupe_canvas = tk.Canvas(frm, width=150, height=150,
                                       bg=C_BG, highlightthickness=1,
                                       highlightbackground=C_GREEN3)
        self.loupe_canvas.pack()

    def _build_forensic_tab(self, parent):
        frm = tk.Frame(parent, bg=C_BG2)
        frm.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        tk.Label(frm, text="ANALYSE FORENSIQUE AUTOMATIQUE", font=FONT_MONO_S,
                 bg=C_BG2, fg=C_GREEN).pack(anchor="w", pady=(0, 8))

        self.forensic_text = scrolledtext.ScrolledText(frm, font=("Courier New", 9),
                                                        bg="#000500", fg=C_GREEN2,
                                                        insertbackground=C_GREEN,
                                                        relief="flat", wrap=tk.WORD)
        self.forensic_text.pack(fill=tk.BOTH, expand=True)

        tk.Button(frm, text="▶ LANCER ANALYSE FORENSIQUE",
                  font=FONT_MONO_S, bg=C_BG, fg=C_AMBER,
                  activebackground=C_GREEN3, relief="flat",
                  command=self._run_forensic_analysis).pack(fill=tk.X, pady=(6, 0))

    # ──────────────────────────────────────────────────────────
    #  LOGIC
    # ──────────────────────────────────────────────────────────

    def _start_clock(self):
        def tick():
            self.clock_var.set(datetime.now().strftime("  [%Y-%m-%d %H:%M:%S]"))
            self._clock_job = self.after(1000, tick)
        tick()

    def _animate_scanline(self):
        """Subtle scanline animation on image canvas"""
        if self.img_canvas.winfo_exists():
            h = self.img_canvas.winfo_height()
            self.img_canvas.delete("scanline")
            if h > 0:
                y = self._scanline_y % (h + 20)
                self.img_canvas.create_line(0, y, 9999, y, fill="#0a1f0a",
                                             width=2, tags="scanline")
                self._scanline_y += 3
        self.after(60, self._animate_scanline)

    def _draw_placeholder(self):
        self.img_canvas.delete("all")
        w = self.img_canvas.winfo_width() or 600
        h = self.img_canvas.winfo_height() or 400
        cx, cy = w // 2, h // 2
        self.img_canvas.create_text(cx, cy - 20, text="◈ AUCUNE IMAGE CHARGÉE ◈",
                                     font=FONT_TITLE, fill=C_GREEN3)
        self.img_canvas.create_text(cx, cy + 20,
                                     text="Cliquez sur ▶ CHARGER IMAGE",
                                     font=FONT_MONO_S, fill=C_DIM)

    def _load_image(self):
        path = filedialog.askopenfilename(
            title="Charger une image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.tif *.webp *.ico"),
                       ("Tous fichiers", "*.*")])
        if not path:
            return
        try:
            self.img_path = path
            self.img_original = Image.open(path)
            self.img_original.load()
            self.status_var.set(f"CHARGÉ: {os.path.basename(path)}")
            self._reset_adjustments()
            self._run_analysis()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir l'image:\n{e}")

    def _run_analysis(self):
        if not self.img_original:
            return
        self.status_var.set("ANALYSE EN COURS...")
        self.update_idletasks()
        try:
            self.analysis_data = analyze_image_full(self.img_path, self.img_original)
            self._populate_tabs()
            self._apply_effect_and_adjustments()
            self.status_var.set(f"ANALYSE COMPLÈTE — {os.path.basename(self.img_path)}")
        except Exception as e:
            self.status_var.set(f"ERREUR: {e}")
            messagebox.showerror("Erreur analyse", traceback.format_exc())

    def _populate_tabs(self):
        d = self.analysis_data

        def fill_tv(tv, data: dict, prefix=""):
            tv.delete(*tv.get_children())
            for k, v in data.items():
                if isinstance(v, list):
                    v = ", ".join(str(x) for x in v)
                tv.insert("", tk.END, text=str(k), values=(str(v),))

        fill_tv(self.tv_file, d.get("file", {}))
        fill_tv(self.tv_image, d.get("image", {}))

        colors = d.get("colors", {})
        col_display = {k: v for k, v in colors.items() if k != "dominant_palette"}
        fill_tv(self.tv_colors, col_display)

        fill_tv(self.tv_exif, d.get("exif", {}))

        gps = d.get("gps", {})
        self.tv_gps.delete(*self.tv_gps.get_children())
        gps_flat = {}
        for k, v in gps.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    gps_flat[kk] = str(vv)
            else:
                gps_flat[k] = str(v)
        for k, v in gps_flat.items():
            self.tv_gps.insert("", tk.END, text=k, values=(v,))

        has_gps = "maps_url" in gps
        self.gps_map_btn.config(state="normal" if has_gps else "disabled")

        fill_tv(self.tv_png, d.get("png_chunks", {}))

        # Dominant palette
        self._draw_palette(colors.get("dominant_palette", []))
        self._update_histogram()

    def _draw_palette(self, colors):
        self.palette_canvas.delete("all")
        if not colors:
            return
        w = self.palette_canvas.winfo_width() or 260
        bw = max(1, w // len(colors))
        for i, hex_color in enumerate(colors):
            x0 = i * bw
            x1 = x0 + bw
            self.palette_canvas.create_rectangle(x0, 0, x1, 28, fill=hex_color, outline="")
            self.palette_canvas.create_text(x0 + bw//2, 14, text=hex_color,
                                             font=("Courier New", 6), fill="#000000")

    def _update_histogram(self):
        img = self.img_display or self.img_original
        if img:
            self.hist_canvas.draw(img)

    def _apply_effect_and_adjustments(self):
        if not self.img_original:
            return
        try:
            # Apply selected effect
            effect = next((e for e in self.effects_list
                           if e["id"] == self.current_effect_id), None)
            if effect and effect["id"] != "none":
                img = apply_effect(self.img_original.convert("RGB"), effect)
            else:
                img = self.img_original.convert("RGB")

            # Apply adjustments
            img = ImageEnhance.Brightness(img).enhance(self.adj_vars["brightness"].get())
            img = ImageEnhance.Contrast(img).enhance(self.adj_vars["contrast"].get())
            img = ImageEnhance.Color(img).enhance(self.adj_vars["saturation"].get())
            img = ImageEnhance.Sharpness(img).enhance(self.adj_vars["sharpness"].get())

            self.img_display = img
            self._refresh_display()
            self._update_histogram()
        except Exception as e:
            self.status_var.set(f"ERREUR EFFET: {e}")

    def _refresh_display(self):
        self.img_canvas.delete("all")
        if not self.img_display:
            self._draw_placeholder()
            return

        cw = self.img_canvas.winfo_width() or 600
        ch = self.img_canvas.winfo_height() or 400
        zoom = self.zoom_var.get()

        if self.compare_var.get() and self.img_original:
            # Side by side
            half = cw // 2
            left_img = self._resize_for_display(self.img_original.convert("RGB"),
                                                  half - 2, ch, zoom)
            right_img = self._resize_for_display(self.img_display, half - 2, ch, zoom)
            combined = Image.new("RGB", (cw, ch), (0, 0, 0))
            combined.paste(left_img, (0, (ch - left_img.height) // 2))
            combined.paste(right_img, (half + 2, (ch - right_img.height) // 2))
            draw = ImageDraw.Draw(combined)
            draw.line([(half, 0), (half, ch)], fill=(0, 100, 0), width=2)
            self.img_photo = ImageTk.PhotoImage(combined)
            self.img_canvas.create_image(0, 0, anchor="nw", image=self.img_photo)
            self.img_canvas.create_text(half // 2, 12, text="ORIGINAL",
                                         font=("Courier New", 8), fill=C_DIM)
            self.img_canvas.create_text(half + half // 2, 12, text="TRAITÉ",
                                         font=("Courier New", 8), fill=C_GREEN2)
        else:
            display = self._resize_for_display(self.img_display, cw, ch, zoom)
            x = (cw - display.width) // 2
            y = (ch - display.height) // 2
            self.img_photo = ImageTk.PhotoImage(display)
            self.img_canvas.create_image(x, y, anchor="nw", image=self.img_photo)
            self._img_offset = (x, y)
            self._img_scale = display.width / self.img_display.width

        if self.show_grid_var.get():
            for x in range(0, cw, 50):
                self.img_canvas.create_line(x, 0, x, ch, fill=C_BORDER, width=1)
            for y in range(0, ch, 50):
                self.img_canvas.create_line(0, y, cw, y, fill=C_BORDER, width=1)

    def _resize_for_display(self, img, max_w, max_h, zoom):
        w, h = img.size
        scale = min(max_w / max(w, 1), max_h / max(h, 1)) * zoom
        nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
        return img.resize((nw, nh), Image.LANCZOS if scale < 1 else Image.NEAREST)

    # ── Zoom ──────────────────────────────────────────────────
    def _zoom_in(self):
        self.zoom_var.set(min(8.0, self.zoom_var.get() * 1.25))
        self.zoom_lbl.config(text=f"{int(self.zoom_var.get()*100)}%")
        self._refresh_display()

    def _zoom_out(self):
        self.zoom_var.set(max(0.05, self.zoom_var.get() / 1.25))
        self.zoom_lbl.config(text=f"{int(self.zoom_var.get()*100)}%")
        self._refresh_display()

    def _zoom_fit(self):
        self.zoom_var.set(1.0)
        self.zoom_lbl.config(text="FIT")
        self._refresh_display()

    def _zoom_100(self):
        if self.img_display:
            cw = self.img_canvas.winfo_width() or 600
            ch = self.img_canvas.winfo_height() or 400
            w, h = self.img_display.size
            scale = min(cw / w, ch / h)
            self.zoom_var.set(1.0 / scale)
            self.zoom_lbl.config(text="1:1")
            self._refresh_display()

    def _on_mousewheel(self, event):
        if event.delta > 0:
            self._zoom_in()
        else:
            self._zoom_out()

    # ── Mouse / Pixel Inspector ────────────────────────────────
    def _on_canvas_mouse(self, event):
        if not self.img_display:
            return
        try:
            ox, oy = getattr(self, "_img_offset", (0, 0))
            scale = getattr(self, "_img_scale", 1.0)
            px = int((event.x - ox) / scale)
            py = int((event.y - oy) / scale)
            w, h = self.img_display.size
            if 0 <= px < w and 0 <= py < h:
                r, g, b = self.img_display.getpixel((px, py))[:3]
                hex_col = f"#{r:02x}{g:02x}{b:02x}"
                hue, sat, val = colorsys.rgb_to_hsv(r/255, g/255, b/255)
                self.px_info.set(
                    f"X:{px} Y:{py}\n"
                    f"RGB:  ({r}, {g}, {b})\n"
                    f"HEX:  {hex_col.upper()}\n"
                    f"HSV:  ({int(hue*360)}°, {int(sat*100)}%, {int(val*100)}%)\n"
                    f"L:    {int(0.299*r+0.587*g+0.114*b)}"
                )
                self.px_color_canvas.delete("all")
                self.px_color_canvas.create_rectangle(0, 0, 200, 60, fill=hex_col, outline=C_GREEN3)
                lum = 0.299*r+0.587*g+0.114*b
                txt_col = "#000000" if lum > 128 else "#ffffff"
                self.px_color_canvas.create_text(100, 30, text=hex_col.upper(),
                                                  font=FONT_MONO, fill=txt_col)
                self.pixel_var.set(f"  PIXEL ({px}, {py})  RGB({r},{g},{b})  {hex_col.upper()}")
                self._draw_loupe(px, py)
        except Exception:
            pass

    def _draw_loupe(self, px, py):
        if not self.img_display:
            return
        size = 5
        half = size // 2
        w, h = self.img_display.size
        lc = self.loupe_canvas
        lc.delete("all")
        cell = 30
        for dy in range(-half, half + 1):
            for dx in range(-half, half + 1):
                x = px + dx
                y = py + dy
                if 0 <= x < w and 0 <= y < h:
                    r, g, b = self.img_display.getpixel((x, y))[:3]
                    fill = f"#{r:02x}{g:02x}{b:02x}"
                else:
                    fill = C_BG
                cx0 = (dx + half) * cell
                cy0 = (dy + half) * cell
                lc.create_rectangle(cx0, cy0, cx0+cell, cy0+cell, fill=fill, outline="")
        # Cross cursor
        lc.create_line(half*cell, 0, half*cell, 150, fill=C_GREEN, width=1)
        lc.create_line(0, half*cell, 150, half*cell, fill=C_GREEN, width=1)

    # ── Effects ───────────────────────────────────────────────
    def _reload_effects(self):
        self.effects_list = load_effects()
        names = [e["name"] for e in self.effects_list]
        self.effect_combo["values"] = names
        # Restore selection
        cur = next((i for i, e in enumerate(self.effects_list)
                    if e["id"] == self.current_effect_id), 0)
        self.effect_combo.current(cur)
        self._update_effect_desc()

    def _update_effect_desc(self):
        idx = self.effect_combo.current()
        if 0 <= idx < len(self.effects_list):
            e = self.effects_list[idx]
            cat = e.get("category", "")
            self.effect_desc.config(
                text=f"[{cat.upper()}] {e.get('description', '')}")

    def _on_effect_change(self, event=None):
        idx = self.effect_combo.current()
        if 0 <= idx < len(self.effects_list):
            self.current_effect_id = self.effects_list[idx]["id"]
        self._update_effect_desc()
        self._apply_effect_and_adjustments()

    def _add_custom_effect(self):
        EffectEditorDialog(self, on_save=self._reload_effects)

    def _edit_selected_effect(self):
        idx = self.effect_combo.current()
        if 0 <= idx < len(self.effects_list):
            EffectEditorDialog(self, effect=self.effects_list[idx],
                                on_save=self._reload_effects)

    # ── Adjustments ───────────────────────────────────────────
    def _on_adj(self, value, lbl, key):
        lbl.config(text=f"{float(value):.1f}")
        if self._scan_job:
            self.after_cancel(self._scan_job)
        self._scan_job = self.after(120, self._apply_effect_and_adjustments)

    def _reset_adjustments(self):
        for key, var in self.adj_vars.items():
            var.set(1.0)
        self._apply_effect_and_adjustments()

    # ── Export ────────────────────────────────────────────────
    def _export_image(self):
        if not self.img_display:
            messagebox.showwarning("Attention", "Aucune image à exporter.")
            return
        path = filedialog.asksaveasfilename(
            title="Exporter image traitée",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp"), ("TIFF", "*.tiff")])
        if path:
            self.img_display.save(path)
            self.status_var.set(f"EXPORTÉ: {os.path.basename(path)}")

    def _export_report(self):
        if not self.analysis_data:
            messagebox.showwarning("Attention", "Aucune analyse à exporter.")
            return
        path = filedialog.asksaveasfilename(
            title="Exporter rapport",
            defaultextension=".txt",
            filetypes=[("Rapport texte", "*.txt"), ("JSON", "*.json")])
        if not path:
            return
        if path.endswith(".json"):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.analysis_data, f, indent=2, ensure_ascii=False, default=str)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write("╔══════════════════════════════════════╗\n")
                f.write("║  INGEN SYSTEMS — RAPPORT D'ANALYSE   ║\n")
                f.write(f"║  Généré: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ║\n")
                f.write("╚══════════════════════════════════════╝\n\n")
                for section, data in self.analysis_data.items():
                    f.write(f"\n═══ {section.upper()} ═══\n")
                    if isinstance(data, dict):
                        for k, v in data.items():
                            f.write(f"  {k:<25} {v}\n")
                    else:
                        f.write(f"  {data}\n")
        self.status_var.set(f"RAPPORT EXPORTÉ: {os.path.basename(path)}")

    # ── GPS ───────────────────────────────────────────────────
    def _open_maps(self):
        url = self.analysis_data.get("gps", {}).get("maps_url")
        if url:
            import webbrowser
            webbrowser.open(url)

    # ── Forensic Analysis ─────────────────────────────────────
    def _run_forensic_analysis(self):
        if not self.img_original:
            messagebox.showwarning("Attention", "Chargez une image d'abord.")
            return
        self.forensic_text.delete("1.0", tk.END)
        self.forensic_text.insert(tk.END, "ANALYSE FORENSIQUE EN COURS...\n\n")
        self.update_idletasks()

        report = []
        img = self.img_original.convert("RGB")
        arr = np.array(img, dtype=np.float32)
        d = self.analysis_data

        # EXIF présence
        exif = d.get("exif", {})
        report.append("═ SIGNATURES EXIF ═")
        if exif:
            report.append(f"  [✓] {len(exif)} champs EXIF présents")
            if "Make" in exif:     report.append(f"  Appareil: {exif.get('Make')} {exif.get('Model','')}")
            if "Software" in exif: report.append(f"  Logiciel: {exif.get('Software')}")
            if "DateTime" in exif: report.append(f"  Prise de vue: {exif.get('DateTime')}")
            if "DateTimeOriginal" in exif and "DateTime" in exif:
                if exif["DateTimeOriginal"] != exif["DateTime"]:
                    report.append("  [⚠] ALERTE: Date originale ≠ Date de modification → Retouche possible")
        else:
            report.append("  [⚠] Aucune métadonnée EXIF — supprimées ou image générée")

        # ELA rapide
        report.append("\n═ ELA (ERROR LEVEL ANALYSIS) ═")
        try:
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=90)
            buf.seek(0)
            jpeg = Image.open(buf).convert("RGB")
            diff = np.abs(arr - np.array(jpeg, dtype=np.float32))
            ela_mean = diff.mean()
            ela_max = diff.max()
            report.append(f"  Erreur moyenne: {ela_mean:.3f}")
            report.append(f"  Erreur max:     {ela_max:.1f}")
            if ela_mean > 8.0:
                report.append("  [⚠] ALERTE: Niveau d'erreur élevé → Zones potentiellement retouchées")
            else:
                report.append("  [✓] Niveaux d'erreur normaux")
        except Exception as e:
            report.append(f"  Erreur ELA: {e}")

        # Noise analysis
        report.append("\n═ ANALYSE DU BRUIT ═")
        gray = arr.mean(axis=2)
        local_std = []
        for y in range(0, gray.shape[0]-8, 8):
            for x in range(0, gray.shape[1]-8, 8):
                block = gray[y:y+8, x:x+8]
                local_std.append(block.std())
        if local_std:
            noise_uniform = np.std(local_std)
            report.append(f"  Variance locale du bruit: {noise_uniform:.2f}")
            if noise_uniform > 15:
                report.append("  [⚠] Bruit non uniforme → Possible montage de zones")
            else:
                report.append("  [✓] Bruit uniforme — cohérent")

        # Color channels balance
        report.append("\n═ ÉQUILIBRE CANAUX COULEUR ═")
        r_m, g_m, b_m = arr[:,:,0].mean(), arr[:,:,1].mean(), arr[:,:,2].mean()
        total = r_m + g_m + b_m + 1e-6
        report.append(f"  R: {r_m/total*100:.1f}%  G: {g_m/total*100:.1f}%  B: {b_m/total*100:.1f}%")
        if abs(r_m - b_m) > 50:
            report.append("  [⚠] Déséquilibre RGB prononcé → Filtre ou retouche couleur probable")

        # Image entropy
        report.append("\n═ ENTROPIE & COMPLEXITÉ ═")
        entropy_str = d.get("colors", {}).get("entropy", "N/A")
        report.append(f"  Entropie: {entropy_str}")
        report.append("  (>7.5 bits = image très riche en détails)")

        # Résolution suspicious
        report.append("\n═ CARACTÉRISTIQUES DIMENSION ═")
        w_img = d.get("image", {}).get("width", 0)
        h_img = d.get("image", {}).get("height", 0)
        common_res = [(1920,1080),(1280,720),(3840,2160),(4096,2160),(2048,1536)]
        if (w_img, h_img) in common_res:
            report.append(f"  [✓] Résolution standard: {w_img}×{h_img}")
        else:
            report.append(f"  [!] Résolution non standard: {w_img}×{h_img} → Recadrage possible")

        report.append("\n═ CONCLUSION ═")
        report.append("  Analyse complète. Consultez les alertes [⚠] ci-dessus.")
        report.append("  Pour une analyse approfondie, appliquez l'effet ELA")
        report.append("  depuis le sélecteur d'effets.")

        self.forensic_text.delete("1.0", tk.END)
        self.forensic_text.insert(tk.END, "\n".join(report))


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps, ImageDraw
    except ImportError:
        print("Installez Pillow: pip install Pillow")
        exit(1)
    try:
        import numpy as np
    except ImportError:
        print("Installez numpy: pip install numpy")
        exit(1)

    app = ImageAnalyzerApp()
    app.mainloop()

import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import threading

PANEL_BG = "#0d0d1a"
CARD_BG = "#16213e"
ACCENT = "#e94560"
TEXT_FG = "#e0e0e0"
MUTED = "#666688"
INPUT_BG = "#1e1e3a"
SUCCESS_BG = "#0a2a1a"


def make_label(parent, text, font_size=13, bold=False, color=TEXT_FG, **kw):
    weight = "bold" if bold else "normal"
    return ctk.CTkLabel(parent, text=text, font=("Segoe UI", font_size, weight),
                        text_color=color, **kw)


def make_textbox(parent, height=80, placeholder="", **kw):
    tb = ctk.CTkTextbox(parent, height=height, fg_color=INPUT_BG, text_color=TEXT_FG,
                        font=("Segoe UI", 13), corner_radius=8, border_width=1,
                        border_color="#2a2a4a", **kw)
    if placeholder:
        tb.insert("1.0", placeholder)
        tb.bind("<FocusIn>", lambda e, t=tb, p=placeholder: _clear_placeholder(t, p))
        tb.bind("<FocusOut>", lambda e, t=tb, p=placeholder: _restore_placeholder(t, p))
    return tb


def _clear_placeholder(tb, placeholder):
    if tb.get("1.0", "end-1c") == placeholder:
        tb.delete("1.0", "end")


def _restore_placeholder(tb, placeholder):
    if not tb.get("1.0", "end-1c").strip():
        tb.insert("1.0", placeholder)


def make_button(parent, text, command, width=160, accent=True, **kw):
    color = ACCENT if accent else CARD_BG
    hover = "#c73652" if accent else "#1e2a4a"
    return ctk.CTkButton(parent, text=text, command=command, width=width, height=38,
                         fg_color=color, hover_color=hover, text_color="white",
                         font=("Segoe UI", 13, "bold"), corner_radius=8, **kw)


class AttachBar(ctk.CTkFrame):
    """Barra para adjuntar imagen y/o audio."""
    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.image_path: str | None = None
        self.audio_path: str | None = None
        self._build()

    def _build(self):
        self._img_btn = ctk.CTkButton(self, text="+ Imagen / Captura", width=160, height=30,
                                      fg_color="#1e2a4a", hover_color="#2a3a5a",
                                      text_color=TEXT_FG, font=("Segoe UI", 12),
                                      corner_radius=6, command=self._pick_image)
        self._img_btn.pack(side="left", padx=(0, 8))

        self._aud_btn = ctk.CTkButton(self, text="+ Audio / Voz", width=140, height=30,
                                      fg_color="#1e2a4a", hover_color="#2a3a5a",
                                      text_color=TEXT_FG, font=("Segoe UI", 12),
                                      corner_radius=6, command=self._pick_audio)
        self._aud_btn.pack(side="left", padx=(0, 8))

        self._lbl = ctk.CTkLabel(self, text="", font=("Segoe UI", 11), text_color=MUTED)
        self._lbl.pack(side="left")

    def _pick_image(self):
        path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.webp *.gif"), ("Todos", "*.*")]
        )
        if path:
            self.image_path = path
            self._update_label()

    def _pick_audio(self):
        path = filedialog.askopenfilename(
            title="Seleccionar audio",
            filetypes=[("Audio", "*.mp3 *.wav *.ogg *.m4a *.flac *.aac"), ("Todos", "*.*")]
        )
        if path:
            self.audio_path = path
            self._update_label()

    def _update_label(self):
        parts = []
        if self.image_path:
            parts.append(f"Img: {self.image_path.split('/')[-1].split(chr(92))[-1]}")
        if self.audio_path:
            parts.append(f"Audio: {self.audio_path.split('/')[-1].split(chr(92))[-1]}")
        self._lbl.configure(text="  |  ".join(parts))

    def clear(self):
        self.image_path = None
        self.audio_path = None
        self._lbl.configure(text="")


class ResponseBox(ctk.CTkFrame):
    """Área de respuesta con botón copiar."""
    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color=SUCCESS_BG, corner_radius=10, **kw)
        self._build()

    def _build(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(10, 0))
        ctk.CTkLabel(header, text="Respuesta del Asistente", font=("Segoe UI", 12, "bold"),
                     text_color="#4caf82").pack(side="left")
        ctk.CTkButton(header, text="Copiar todo", width=90, height=26,
                      fg_color="#1a3a2a", hover_color="#2a4a3a",
                      text_color="#4caf82", font=("Segoe UI", 11),
                      corner_radius=5, command=self._copy).pack(side="right")

        self._text = ctk.CTkTextbox(self, fg_color="transparent", text_color=TEXT_FG,
                                    font=("Segoe UI", 13), state="disabled", wrap="word")
        self._text.pack(fill="both", expand=True, padx=12, pady=(6, 12))

    def set_text(self, text: str):
        self._text.configure(state="normal")
        self._text.delete("1.0", "end")
        self._text.insert("1.0", text)
        self._text.configure(state="disabled")

    def _copy(self):
        text = self._text.get("1.0", "end-1c")
        self._text.clipboard_clear()
        self._text.clipboard_append(text)

    def set_loading(self):
        self.set_text("Consultando a Gemini...")

    def set_error(self, msg: str):
        self.set_text(f"Error: {msg}")


class BasePanel(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=PANEL_BG, corner_radius=0)
        self.controller = controller
        self._response_box: ResponseBox | None = None
        self._attach: AttachBar | None = None
        self._loading = False

    def _run_async(self, fn, *args):
        if self._loading:
            return
        self._loading = True
        if self._response_box:
            self._response_box.set_loading()
        thread = threading.Thread(target=self._thread_wrapper, args=(fn, *args), daemon=True)
        thread.start()

    def _thread_wrapper(self, fn, *args):
        try:
            result = fn(*args)
            self.after(0, self._on_result, result)
        except Exception as e:
            self.after(0, self._on_error, str(e))
        finally:
            self._loading = False

    def _on_result(self, text: str):
        if self._response_box:
            self._response_box.set_text(text)

    def _on_error(self, msg: str):
        if self._response_box:
            self._response_box.set_error(msg)

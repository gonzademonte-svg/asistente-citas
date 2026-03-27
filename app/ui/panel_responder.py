import customtkinter as ctk
from app.ui.base_panel import (BasePanel, AttachBar, ResponseBox,
                                make_label, make_textbox, make_button,
                                CARD_BG, MUTED, ACCENT)

STAGE_OPTIONS = [
    "Primer contacto",
    "Nos conocemos un poco",
    "Ya hubo interés / coqueteo",
    "Enfriamiento / ghosteo parcial",
]


class PanelResponder(BasePanel):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=20)

        make_label(scroll, "¿Cómo Responder?", font_size=22, bold=True,
                   color=ACCENT, anchor="w").pack(fill="x", pady=(0, 4))
        make_label(scroll, "Pega el mensaje que recibiste y te digo exactamente qué responder.",
                   font_size=13, color=MUTED, anchor="w").pack(fill="x", pady=(0, 20))

        card = ctk.CTkFrame(scroll, fg_color=CARD_BG, corner_radius=12)
        card.pack(fill="x", pady=(0, 14))
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=16)

        make_label(inner, "Mensaje recibido", font_size=12, color=MUTED, anchor="w").pack(fill="x")
        self._msg = make_textbox(inner, height=90,
                                 placeholder="Pega aquí el mensaje que te enviaron...")
        self._msg.pack(fill="x", pady=(4, 12))

        make_label(inner, "Etapa de la conversación", font_size=12, color=MUTED, anchor="w").pack(fill="x")
        self._stage = ctk.CTkOptionMenu(inner, values=STAGE_OPTIONS, height=36,
                                        fg_color="#1e1e3a", text_color="white",
                                        button_color="#2a2a4a", button_hover_color="#3a3a5a",
                                        font=("Segoe UI", 13), corner_radius=8)
        self._stage.pack(fill="x", pady=(4, 12))

        make_label(inner, "Contexto adicional (opcional)", font_size=12, color=MUTED, anchor="w").pack(fill="x")
        self._extra = make_textbox(inner, height=60,
                                   placeholder="ej. llevamos 3 días hablando, quedamos en vernos pero no confirmó...")
        self._extra.pack(fill="x", pady=(4, 0))

        make_label(scroll, "Adjuntar captura de la conversación o audio (opcional)",
                   font_size=12, color=MUTED, anchor="w").pack(fill="x", pady=(12, 4))
        self._attach = AttachBar(scroll)
        self._attach.pack(fill="x", pady=(0, 14))

        make_button(scroll, "¿Cómo respondo?", command=self._submit).pack(anchor="w", pady=(0, 16))

        self._response_box = ResponseBox(scroll)
        self._response_box.pack(fill="x", pady=(0, 16))

    def _submit(self):
        msg = self._msg.get("1.0", "end-1c").strip()
        stage = self._stage.get()
        extra = self._extra.get("1.0", "end-1c").strip()

        if not msg:
            self._response_box.set_error("Escribe o pega el mensaje que recibiste.")
            return

        prompt = f"Etapa: {stage}\nMensaje recibido: {msg}\n"
        if extra:
            prompt += f"Contexto extra: {extra}\n"
        prompt += "\nSugiere 2-3 formas de responder a este mensaje."

        self._run_async(self.controller.ask, "responder", prompt,
                        self._attach.image_path, self._attach.audio_path)

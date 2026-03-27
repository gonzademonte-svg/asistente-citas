import customtkinter as ctk
from app.ui.base_panel import (BasePanel, AttachBar, ResponseBox,
                                make_label, make_textbox, make_button,
                                CARD_BG, MUTED, ACCENT)


class PanelTono(BasePanel):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=20)

        make_label(scroll, "Análisis de Tono e Interés", font_size=22, bold=True,
                   color=ACCENT, anchor="w").pack(fill="x", pady=(0, 4))
        make_label(scroll, "Pega los mensajes que te envió y te digo si realmente está interesada/o.",
                   font_size=13, color=MUTED, anchor="w").pack(fill="x", pady=(0, 20))

        card = ctk.CTkFrame(scroll, fg_color=CARD_BG, corner_radius=12)
        card.pack(fill="x", pady=(0, 14))
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=16)

        make_label(inner, "Mensajes de la otra persona", font_size=12, color=MUTED, anchor="w").pack(fill="x")
        self._msgs = make_textbox(inner, height=150,
                                  placeholder="Pega aquí uno o varios mensajes que recibiste...\n\n"
                                              "ej:\n\"Hola! Bien y tú? 😊\"\n\"Jaja si puede ser\"\n\"Ay no sé...")
        self._msgs.pack(fill="x", pady=(4, 12))

        make_label(inner, "Contexto de la relación (opcional)", font_size=12,
                   color=MUTED, anchor="w").pack(fill="x")
        self._ctx = make_textbox(inner, height=60,
                                 placeholder="ej. nos conocemos hace 2 semanas, ya salimos una vez...")
        self._ctx.pack(fill="x", pady=(4, 0))

        make_label(scroll, "Adjuntar captura de la conversación o audio (opcional)",
                   font_size=12, color=MUTED, anchor="w").pack(fill="x", pady=(12, 4))
        self._attach = AttachBar(scroll)
        self._attach.pack(fill="x", pady=(0, 14))

        make_button(scroll, "Analizar", command=self._submit).pack(anchor="w", pady=(0, 16))

        self._response_box = ResponseBox(scroll)
        self._response_box.pack(fill="x", pady=(0, 16))

    def _submit(self):
        msgs = self._msgs.get("1.0", "end-1c").strip()
        ctx = self._ctx.get("1.0", "end-1c").strip()

        if not msgs:
            self._response_box.set_error("Pega al menos un mensaje para analizar.")
            return

        prompt = f"Mensajes de la otra persona:\n{msgs}\n"
        if ctx:
            prompt += f"\nContexto: {ctx}"
        prompt += "\nAnaliza el nivel de interés y dame tu evaluación."

        self._run_async(self.controller.ask, "tono", prompt,
                        self._attach.image_path, self._attach.audio_path)

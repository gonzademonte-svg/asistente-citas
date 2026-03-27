import customtkinter as ctk
from app.ui.base_panel import (BasePanel, AttachBar, ResponseBox,
                                make_label, make_textbox, make_button,
                                CARD_BG, MUTED, ACCENT)

CONTEXT_OPTIONS = ["App de citas", "Red social / DM", "En persona", "Amigos en común", "Otro"]


class PanelInicio(BasePanel):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=20)

        make_label(scroll, "Iniciar Conversación", font_size=22, bold=True,
                   color=ACCENT, anchor="w").pack(fill="x", pady=(0, 4))
        make_label(scroll, "Cuéntame sobre la persona y te genero las mejores opciones de apertura.",
                   font_size=13, color=MUTED, anchor="w").pack(fill="x", pady=(0, 20))

        card = ctk.CTkFrame(scroll, fg_color=CARD_BG, corner_radius=12)
        card.pack(fill="x", pady=(0, 14))

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=16)

        row1 = ctk.CTkFrame(inner, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 10))

        col_a = ctk.CTkFrame(row1, fg_color="transparent")
        col_a.pack(side="left", fill="x", expand=True, padx=(0, 8))
        make_label(col_a, "Nombre / Apodo", font_size=12, color=MUTED, anchor="w").pack(fill="x")
        self._name = ctk.CTkEntry(col_a, placeholder_text="ej. Sofía", height=36,
                                  fg_color="#1e1e3a", text_color="white",
                                  font=("Segoe UI", 13), corner_radius=8)
        self._name.pack(fill="x", pady=(4, 0))

        col_b = ctk.CTkFrame(row1, fg_color="transparent")
        col_b.pack(side="left", fill="x", expand=True)
        make_label(col_b, "Edad aprox.", font_size=12, color=MUTED, anchor="w").pack(fill="x")
        self._age = ctk.CTkEntry(col_b, placeholder_text="ej. 24", height=36,
                                 fg_color="#1e1e3a", text_color="white",
                                 font=("Segoe UI", 13), corner_radius=8)
        self._age.pack(fill="x", pady=(4, 0))

        make_label(inner, "¿Dónde se conocieron / cómo la encontraste?", font_size=12,
                   color=MUTED, anchor="w").pack(fill="x", pady=(10, 0))
        self._where = ctk.CTkEntry(inner, placeholder_text="ej. Instagram, Tinder, clase de gym...",
                                   height=36, fg_color="#1e1e3a", text_color="white",
                                   font=("Segoe UI", 13), corner_radius=8)
        self._where.pack(fill="x", pady=(4, 10))

        make_label(inner, "Contexto / plataforma", font_size=12, color=MUTED, anchor="w").pack(fill="x")
        self._context = ctk.CTkOptionMenu(inner, values=CONTEXT_OPTIONS, height=36,
                                          fg_color="#1e1e3a", text_color="white",
                                          button_color="#2a2a4a", button_hover_color="#3a3a5a",
                                          font=("Segoe UI", 13), corner_radius=8)
        self._context.pack(fill="x", pady=(4, 10))

        make_label(inner, "Intereses observados / info extra (opcional)", font_size=12,
                   color=MUTED, anchor="w").pack(fill="x")
        self._interests = make_textbox(inner, height=70,
                                       placeholder="ej. le gustan los viajes, publica mucho sobre fitness...")
        self._interests.pack(fill="x", pady=(4, 0))

        attach_label = make_label(scroll, "Adjuntar captura de pantalla o audio (opcional)",
                                  font_size=12, color=MUTED, anchor="w")
        attach_label.pack(fill="x", pady=(12, 4))
        self._attach = AttachBar(scroll)
        self._attach.pack(fill="x", pady=(0, 14))

        make_button(scroll, "Generar apertura", command=self._submit).pack(anchor="w", pady=(0, 16))

        self._response_box = ResponseBox(scroll)
        self._response_box.pack(fill="x", pady=(0, 16))

    def _submit(self):
        name = self._name.get().strip()
        age = self._age.get().strip()
        where = self._where.get().strip()
        context = self._context.get()
        interests = self._interests.get("1.0", "end-1c").strip()

        prompt = f"Nombre: {name or 'desconocido'}\nEdad: {age or 'desconocida'}\n"
        prompt += f"Dónde: {where or 'no especificado'}\nContexto: {context}\n"
        if interests:
            prompt += f"Intereses/info extra: {interests}\n"
        prompt += "\nGenera 3 opciones de primer mensaje para iniciar conversación con esta persona."

        self._run_async(self.controller.ask, "inicio", prompt,
                        self._attach.image_path, self._attach.audio_path)

import customtkinter as ctk
from app.ui.base_panel import (BasePanel, AttachBar, ResponseBox,
                                make_label, make_textbox, make_button,
                                CARD_BG, MUTED, ACCENT)

GOAL_OPTIONS = [
    "Encuentro casual",
    "Primera cita (conocernos)",
    "Reconectar con alguien",
    "Pasar a otro nivel",
]


class PanelGuia(BasePanel):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self._build()

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=20)

        make_label(scroll, "Guía Paso a Paso", font_size=22, bold=True,
                   color=ACCENT, anchor="w").pack(fill="x", pady=(0, 4))
        make_label(scroll, "Dime en qué punto estás y qué quieres lograr. Te armo el plan.",
                   font_size=13, color=MUTED, anchor="w").pack(fill="x", pady=(0, 20))

        card = ctk.CTkFrame(scroll, fg_color=CARD_BG, corner_radius=12)
        card.pack(fill="x", pady=(0, 14))
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=16)

        make_label(inner, "Estado actual de la situación", font_size=12, color=MUTED, anchor="w").pack(fill="x")
        self._status = make_textbox(inner, height=100,
                                    placeholder="ej. Llevamos una semana hablando, hay química, "
                                                "pero nunca propuse vernos. Ella responde rápido...")
        self._status.pack(fill="x", pady=(4, 12))

        make_label(inner, "Mi objetivo", font_size=12, color=MUTED, anchor="w").pack(fill="x")
        self._goal = ctk.CTkOptionMenu(inner, values=GOAL_OPTIONS, height=36,
                                       fg_color="#1e1e3a", text_color="white",
                                       button_color="#2a2a4a", button_hover_color="#3a3a5a",
                                       font=("Segoe UI", 13), corner_radius=8)
        self._goal.pack(fill="x", pady=(4, 12))

        make_label(inner, "¿Hay algo que complique la situación? (opcional)", font_size=12,
                   color=MUTED, anchor="w").pack(fill="x")
        self._obstacles = make_textbox(inner, height=60,
                                       placeholder="ej. tiene novio, es muy ocupada, no conozco sus planes...")
        self._obstacles.pack(fill="x", pady=(4, 0))

        make_label(scroll, "Adjuntar captura o audio para más contexto (opcional)",
                   font_size=12, color=MUTED, anchor="w").pack(fill="x", pady=(12, 4))
        self._attach = AttachBar(scroll)
        self._attach.pack(fill="x", pady=(0, 6))

        btn_row = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_row.pack(fill="x", pady=(8, 16))
        make_button(btn_row, "Crear mi plan", command=self._submit).pack(side="left", padx=(0, 10))
        make_button(btn_row, "Guardar plan", command=self._save, accent=False).pack(side="left")

        self._response_box = ResponseBox(scroll)
        self._response_box.pack(fill="x", pady=(0, 16))

    def _submit(self):
        status = self._status.get("1.0", "end-1c").strip()
        goal = self._goal.get()
        obstacles = self._obstacles.get("1.0", "end-1c").strip()

        if not status:
            self._response_box.set_error("Describe el estado actual de la conversación.")
            return

        prompt = f"Objetivo: {goal}\nSituación actual: {status}\n"
        if obstacles:
            prompt += f"Complicaciones: {obstacles}\n"
        prompt += "\nCrea un plan paso a paso para concretar este objetivo."

        self._run_async(self.controller.ask, "guia", prompt,
                        self._attach.image_path, self._attach.audio_path)

    def _save(self):
        text = self._response_box._text.get("1.0", "end-1c")
        if text and text != "Consultando a Gemini...":
            self.controller.save("guia", "Plan guardado manualmente", text)
            self._response_box.set_text(text + "\n\n[Plan guardado en historial]")

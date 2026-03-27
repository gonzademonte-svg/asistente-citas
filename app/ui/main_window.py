import customtkinter as ctk
from app.ui.panel_inicio import PanelInicio
from app.ui.panel_responder import PanelResponder
from app.ui.panel_guia import PanelGuia
from app.ui.panel_tono import PanelTono

SIDEBAR_W = 200
NAV_ITEMS = [
    ("Iniciar\nConversación", "inicio"),
    ("Cómo\nResponder", "responder"),
    ("Guía Paso\na Paso", "guia"),
    ("Analizar\nTono", "tono"),
]

COLORS = {
    "sidebar_bg": "#1a1a2e",
    "active_btn": "#e94560",
    "inactive_btn": "#16213e",
    "hover_btn": "#0f3460",
    "logo_fg": "#e94560",
    "subtitle_fg": "#888888",
}


class MainWindow(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._active = None
        self._panels: dict[str, ctk.CTkFrame] = {}
        self._nav_buttons: dict[str, ctk.CTkButton] = {}

        self._build_sidebar()
        self._build_content_area()
        self._build_panels()
        self._switch("inicio")

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=SIDEBAR_W, fg_color=COLORS["sidebar_bg"], corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo = ctk.CTkLabel(sidebar, text="Asistente\nde Citas", font=("Segoe UI", 20, "bold"),
                            text_color=COLORS["logo_fg"])
        logo.pack(pady=(30, 4), padx=16)

        sub = ctk.CTkLabel(sidebar, text="Tu coach personal", font=("Segoe UI", 11),
                           text_color=COLORS["subtitle_fg"])
        sub.pack(pady=(0, 24), padx=16)

        sep = ctk.CTkFrame(sidebar, height=1, fg_color="#2a2a4a")
        sep.pack(fill="x", padx=16, pady=(0, 16))

        for label, key in NAV_ITEMS:
            btn = ctk.CTkButton(
                sidebar,
                text=label,
                height=60,
                corner_radius=10,
                fg_color=COLORS["inactive_btn"],
                hover_color=COLORS["hover_btn"],
                text_color="white",
                font=("Segoe UI", 13, "bold"),
                anchor="center",
                command=lambda k=key: self._switch(k),
            )
            btn.pack(fill="x", padx=12, pady=5)
            self._nav_buttons[key] = btn

        sep2 = ctk.CTkFrame(sidebar, height=1, fg_color="#2a2a4a")
        sep2.pack(fill="x", padx=16, pady=(16, 8), side="bottom")

        version = ctk.CTkLabel(sidebar, text="v1.0 · Gemini 2.0", font=("Segoe UI", 10),
                               text_color=COLORS["subtitle_fg"])
        version.pack(side="bottom", pady=(0, 12))

    def _build_content_area(self):
        self._content = ctk.CTkFrame(self, fg_color="#0d0d1a", corner_radius=0)
        self._content.pack(side="left", fill="both", expand=True)

    def _build_panels(self):
        classes = {
            "inicio": PanelInicio,
            "responder": PanelResponder,
            "guia": PanelGuia,
            "tono": PanelTono,
        }
        for key, cls in classes.items():
            panel = cls(self._content, self.controller)
            panel.place(relx=0, rely=0, relwidth=1, relheight=1)
            self._panels[key] = panel

    def _switch(self, key: str):
        if self._active == key:
            return
        self._active = key
        for k, btn in self._nav_buttons.items():
            btn.configure(fg_color=COLORS["active_btn"] if k == key else COLORS["inactive_btn"])
        for k, panel in self._panels.items():
            if k == key:
                panel.lift()
            else:
                panel.lower()

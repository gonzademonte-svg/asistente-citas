import customtkinter as ctk
from app.ui.main_window import MainWindow
from app.controller import Controller
from dotenv import load_dotenv

load_dotenv()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def main():
    app = ctk.CTk()
    app.title("Asistente de Citas")
    app.geometry("1000x680")
    app.minsize(900, 600)

    controller = Controller()
    window = MainWindow(app, controller)
    window.pack(fill="both", expand=True)

    app.mainloop()


if __name__ == "__main__":
    main()

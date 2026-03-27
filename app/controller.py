from app import gemini_service
from app import session_store


class Controller:
    def ask(self, module: str, prompt: str,
            image_path: str | None = None,
            audio_path: str | None = None) -> str:
        response = gemini_service.ask(module, prompt, image_path, audio_path)
        session_store.save_entry(module, prompt, response)
        return response

    def save(self, module: str, prompt: str, response: str) -> None:
        session_store.save_entry(module, prompt, response)

    def get_history(self, module: str | None = None, limit: int = 50) -> list:
        return session_store.get_history(module, limit)

    def clear_history(self) -> None:
        session_store.clear_history()

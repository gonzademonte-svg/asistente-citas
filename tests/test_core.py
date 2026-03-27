import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_session_store_save_and_read():
    from app import session_store
    session_store.clear_history()
    session_store.save_entry("test", "prompt de prueba", "respuesta de prueba")
    history = session_store.get_history()
    assert len(history) == 1
    assert history[0]["module"] == "test"
    assert history[0]["prompt"] == "prompt de prueba"
    assert history[0]["response"] == "respuesta de prueba"
    session_store.clear_history()


def test_session_store_filter_by_module():
    from app import session_store
    session_store.clear_history()
    session_store.save_entry("inicio", "p1", "r1")
    session_store.save_entry("tono", "p2", "r2")
    session_store.save_entry("inicio", "p3", "r3")
    result = session_store.get_history(module="inicio")
    assert len(result) == 2
    assert all(e["module"] == "inicio" for e in result)
    session_store.clear_history()


def test_session_store_clear():
    from app import session_store
    session_store.save_entry("guia", "p", "r")
    session_store.clear_history()
    assert session_store.get_history() == []


def test_gemini_service_invalid_key(monkeypatch):
    import google.generativeai as genai
    from app import gemini_service

    monkeypatch.setattr(os, "getenv", lambda key, default="": "invalid_key" if key == "GEMINI_API_KEY" else default)

    class FakeModel:
        def generate_content(self, parts):
            raise Exception("API error simulado")

    monkeypatch.setattr(genai, "GenerativeModel", lambda **kw: FakeModel())

    try:
        gemini_service.ask("inicio", "test prompt")
        assert False, "Deberia haber lanzado RuntimeError"
    except RuntimeError as e:
        assert "Error al contactar Gemini" in str(e)


def test_controller_delegates_to_gemini(monkeypatch):
    from app.controller import Controller
    from app import gemini_service, session_store

    session_store.clear_history()
    monkeypatch.setattr(gemini_service, "ask", lambda module, prompt, image=None, audio=None: "respuesta mock")

    ctrl = Controller()
    result = ctrl.ask("inicio", "prompt de prueba")
    assert result == "respuesta mock"

    history = session_store.get_history(module="inicio")
    assert len(history) == 1
    session_store.clear_history()

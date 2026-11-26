"""Evidências mínimas por cenário; nunca registra cookies, headers ou senhas."""

import json
import re
import warnings
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path

import pytest

EVIDENCE_ROOT = Path("evidencias") / "execucoes"
RESULT_FILE = "resultado.json"
MAX_NAME_LENGTH = 90
DIGEST_LENGTH = 10
SCREENSHOT_TIMEOUT_MS = 5_000
SENSITIVE_FIELDS = "input, textarea, [data-test='login-password']"


def safe_name(text: str) -> str:
    """Troca caracteres inválidos em nomes de arquivo por hífen."""
    return re.sub(r"[^a-zA-Z0-9_-]", "-", text)


def _run_id(config: pytest.Config) -> str:
    if not hasattr(config, "_qa_run_id"):
        config._qa_run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    return config._qa_run_id


def _folder(item: pytest.Item) -> Path:
    """Pasta única do cenário dentro da execução atual."""
    name = safe_name(item.name)[:MAX_NAME_LENGTH]
    digest = sha256(item.nodeid.encode()).hexdigest()[:DIGEST_LENGTH]
    path = Path(item.config.rootpath) / EVIDENCE_ROOT / _run_id(item.config) / f"{name}-{digest}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _overall_result(phases: dict) -> str:
    outcomes = {phase["resultado"] for phase in phases.values()}
    if "failed" in outcomes:
        return "failed"
    if "skipped" in outcomes:
        return "skipped"
    return "passed" if "teardown" in phases else "running"


def _record_phase(folder: Path, item: pytest.Item, report, call) -> None:
    path = folder / RESULT_FILE
    data = (
        json.loads(path.read_text(encoding="utf-8"))
        if path.exists()
        else {"cenario": item.nodeid, "fases": {}}
    )
    phase = {"resultado": report.outcome, "duracao_segundos": round(report.duration, 4)}
    if call.excinfo:
        phase["excecao"] = call.excinfo.typename
    data["fases"][report.when] = phase
    data["resultado"] = _overall_result(data["fases"])
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _should_capture(report) -> bool:
    return report.when == "call" or (report.when == "setup" and report.failed)


def _capture_screen(folder: Path, item: pytest.Item) -> None:
    page = item.funcargs.get("page")
    if page is None or page.is_closed():
        (folder / "sem-captura.txt").write_text(
            "Cenário sem sessão de interface disponível.", encoding="utf-8"
        )
        return
    try:
        page.screenshot(
            path=str(folder / "tela-final.png"),
            mask=[page.locator(SENSITIVE_FIELDS)],
            timeout=SCREENSHOT_TIMEOUT_MS,
        )
    except Exception as error:  # a evidência nunca deve derrubar o teste
        (folder / "captura-indisponivel.txt").write_text(type(error).__name__, encoding="utf-8")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    try:
        folder = _folder(item)
        _record_phase(folder, item, report, call)
        if _should_capture(report):
            _capture_screen(folder, item)
    except Exception as error:
        warnings.warn(
            f"Não foi possível gravar evidência: {type(error).__name__}",
            RuntimeWarning,
            stacklevel=2,
        )

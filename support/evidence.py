"""Evidências mínimas por cenário; nunca registra cookies, headers ou senhas."""

import json
import re
import warnings
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

import pytest


def _folder(item):
    config = item.config
    if not hasattr(config, "_qa_run_id"):
        config._qa_run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    name = re.sub(r"[^a-zA-Z0-9_-]", "-", item.name)[:90]
    digest = sha256(item.nodeid.encode()).hexdigest()[:10]
    path = (
        Path(config.rootpath)
        / "evidencias"
        / "execucoes"
        / config._qa_run_id
        / f"{name}-{digest}"
    )
    path.mkdir(parents=True, exist_ok=True)
    return path


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    try:
        folder = _folder(item)
        path = folder / "resultado.json"
        data = (
            json.loads(path.read_text(encoding="utf-8"))
            if path.exists()
            else {"cenario": item.nodeid, "fases": {}}
        )
        data["fases"][report.when] = {
            "resultado": report.outcome,
            "duracao_segundos": round(report.duration, 4),
        }
        if call.excinfo:
            data["fases"][report.when]["excecao"] = call.excinfo.typename
        phases = data["fases"]
        data["resultado"] = (
            "failed"
            if any(p["resultado"] == "failed" for p in phases.values())
            else (
                "skipped"
                if any(p["resultado"] == "skipped" for p in phases.values())
                else "passed" if "teardown" in phases else "running"
            )
        )
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        if report.when == "call" or (report.when == "setup" and report.failed):
            page = item.funcargs.get("page")
            if page is not None and not page.is_closed():
                try:
                    page.screenshot(
                        path=str(folder / "tela-final.png"),
                        mask=[
                            page.locator(
                                "input, textarea, [data-test='login-password']"
                            )
                        ],
                        timeout=5000,
                    )
                except Exception as error:
                    (folder / "captura-indisponivel.txt").write_text(
                        type(error).__name__, encoding="utf-8"
                    )
            else:
                (folder / "sem-captura.txt").write_text(
                    "Cenário sem sessão de interface disponível.", encoding="utf-8"
                )
    except Exception as error:
        warnings.warn(
            f"Não foi possível gravar evidência: {type(error).__name__}", RuntimeWarning
        )

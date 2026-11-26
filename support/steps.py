"""Capturas dos marcos da compra."""

import pytest

from support.evidence import _folder, safe_name

STEP_SCREENSHOT_TIMEOUT_MS = 10_000


@pytest.fixture
def evidence_step(request, page):
    def capture(label: str) -> None:
        page.screenshot(
            path=str(_folder(request.node) / f"{safe_name(label)}.png"),
            mask=[page.locator("input, textarea")],
            timeout=STEP_SCREENSHOT_TIMEOUT_MS,
        )

    return capture

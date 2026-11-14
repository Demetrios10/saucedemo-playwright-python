"""Capturas dos marcos da compra."""

import re

import pytest

from support.evidence import _folder


@pytest.fixture
def evidence_step(request, page):
    def capture(label):
        name = re.sub(r"[^a-zA-Z0-9_-]", "-", label)
        page.screenshot(
            path=str(_folder(request.node) / f"{name}.png"),
            mask=[page.locator("input, textarea")],
            timeout=10000,
        )

    return capture

"""Configuração simples; credenciais de demonstração podem vir do ambiente."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    base_url: str = "https://www.saucedemo.com/"
    username: str = os.getenv("SAUCE_USERNAME", "standard_user")
    password: str = os.getenv("SAUCE_PASSWORD", "secret_sauce")


settings = Settings()

"""
CyberArk PAM (Self-Hosted PVWA) connector — Privileged Account Security web services.

READ-ONLY identity/account inventory for IAM review and audit. This connector
resolves privileged *account metadata* (owner, username, address, safe) only.
It NEVER calls the password-retrieval endpoints and never returns secrets.

Auth: PVWA logon returns a session token used directly in the Authorization
header (no "Bearer" prefix).
  POST {base}/PasswordVault/API/auth/{method}/Logon   -> "<token>"
  GET  {base}/PasswordVault/API/Accounts?search=...    -> {value:[...]}

Env vars:
  CYBERARK_BASE_URL     e.g. https://pvwa.example.com
  CYBERARK_AUTH_METHOD  CyberArk | LDAP | RADIUS   (default CyberArk)
  CYBERARK_USERNAME     API/service account username
  CYBERARK_PASSWORD     API/service account password
"""

from __future__ import annotations

import os
from typing import Optional

import httpx

from .base import BaseConnector, ConnectorError, IdentityNode, TokenExpiredError, head_check

_ENV_BASE   = os.environ.get("CYBERARK_BASE_URL", "")
_ENV_METHOD = os.environ.get("CYBERARK_AUTH_METHOD", "CyberArk")
_ENV_USER   = os.environ.get("CYBERARK_USERNAME", "")
_ENV_PASS   = os.environ.get("CYBERARK_PASSWORD", "")

_TIMEOUT = httpx.Timeout(10.0, connect=5.0)


class CyberArkConnector(BaseConnector):
    provider_name = "cyberark"

    def __init__(self, base_url: str = "", auth_method: str = "",
                 username: str = "", password: str = ""):
        self.base_url = (base_url or _ENV_BASE).rstrip("/")
        self.auth_method = auth_method or _ENV_METHOD or "CyberArk"
        self.username = username or _ENV_USER
        self.password = password or _ENV_PASS
        if not self.base_url:
            raise ConnectorError("cyberark", "CYBERARK_BASE_URL not set")

    # ── session ──────────────────────────────────────────────────────────────────

    async def _logon(self) -> str:
        url = f"{self.base_url}/PasswordVault/API/auth/{self.auth_method}/Logon"
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(url, json={"username": self.username,
                                                "password": self.password,
                                                "concurrentSession": True})
        if resp.status_code == 200:
            # Body is a JSON-encoded token string.
            try:
                return resp.json()
            except Exception:
                return resp.text.strip('"')
        if resp.status_code in (401, 403):
            raise TokenExpiredError(self.provider_name, "PVWA logon failed — bad credentials")
        raise ConnectorError(self.provider_name, f"Logon returned {resp.status_code}", resp.status_code)

    async def _search_accounts(self, query: str, token: str) -> list[dict]:
        url = f"{self.base_url}/PasswordVault/API/Accounts"
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.get(url, params={"search": query, "limit": 5},
                                    headers={"Authorization": token})
        if resp.status_code == 200:
            return resp.json().get("value", [])
        if resp.status_code == 401:
            raise TokenExpiredError(self.provider_name, "Session token expired")
        raise ConnectorError(self.provider_name, f"Accounts query returned {resp.status_code}",
                             resp.status_code)

    async def _logoff(self, token: str) -> None:
        try:
            async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
                await client.post(f"{self.base_url}/PasswordVault/API/auth/Logoff",
                                  headers={"Authorization": token})
        except Exception:
            pass  # best-effort

    # ── node builder ──────────────────────────────────────────────────────────────

    def _build_node(self, acct: dict) -> IdentityNode:
        node = IdentityNode(
            provider=self.provider_name,
            provider_sub=acct.get("id", ""),
            username=acct.get("userName"),
            display_name=acct.get("name"),
            org=acct.get("safeName"),
            location=acct.get("address"),  # target host/address of the privileged account
            raw_profile={k: v for k, v in acct.items() if k != "secret"},  # never store secrets
        )
        return node

    # ── BaseConnector interface ───────────────────────────────────────────────────

    async def resolve(self, identifier: str, token: Optional[str] = None) -> Optional[IdentityNode]:
        if not (self.username and self.password):
            raise ConnectorError(self.provider_name,
                                 "CYBERARK_USERNAME / CYBERARK_PASSWORD required")
        session = await self._logon()
        try:
            accounts = await self._search_accounts(identifier, session)
        finally:
            await self._logoff(session)
        if not accounts:
            return None
        return self._build_node(accounts[0])

    async def health_check(self) -> bool:
        return await head_check(f"{self.base_url}/PasswordVault/API/Server", self.provider_name)

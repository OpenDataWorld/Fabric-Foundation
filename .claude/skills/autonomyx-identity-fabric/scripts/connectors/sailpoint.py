"""
SailPoint Identity Security Cloud (ISC) connector — API v3 / IGA.

Auth: OAuth 2.0 client credentials (Personal Access Token client).
  POST https://{tenant}.api.identitynow.com/oauth/token

Resolution:
  - direct:  GET /v3/identities/{id}
  - search:  GET /v3/identities?filters=alias eq "x"  (or emailAddress eq "x")
  - linkage: GET /v3/accounts?filters=identityId eq "{id}"
             each account's sourceName -> a cross-provider linkage stub,
             so SailPoint-correlated accounts join the identity graph.

Env vars:
  SAILPOINT_TENANT          e.g. acme  (=> acme.api.identitynow.com)
  SAILPOINT_BASE_URL        optional explicit base url (overrides tenant)
  SAILPOINT_CLIENT_ID       PAT / OAuth client id
  SAILPOINT_CLIENT_SECRET   PAT / OAuth client secret
"""

from __future__ import annotations

import os
import re
from typing import Optional

from .base import (
    BaseConnector,
    ConnectorError,
    IdentityNode,
    get_json,
    head_check,
    post_form,
)

_ENV_TENANT = os.environ.get("SAILPOINT_TENANT", "")
_ENV_BASE   = os.environ.get("SAILPOINT_BASE_URL", "")
_ENV_ID     = os.environ.get("SAILPOINT_CLIENT_ID", "")
_ENV_SECRET = os.environ.get("SAILPOINT_CLIENT_SECRET", "")


class SailPointConnector(BaseConnector):
    provider_name = "sailpoint"

    def __init__(self, tenant: str = "", base_url: str = "",
                 client_id: str = "", client_secret: str = ""):
        self.base_url = (base_url or _ENV_BASE
                         or (f"https://{tenant or _ENV_TENANT}.api.identitynow.com"
                             if (tenant or _ENV_TENANT) else ""))
        self.client_id = client_id or _ENV_ID
        self.client_secret = client_secret or _ENV_SECRET
        if not self.base_url:
            raise ConnectorError("sailpoint", "SAILPOINT_TENANT or SAILPOINT_BASE_URL not set")
        self.base_url = self.base_url.rstrip("/")

    # ── token ───────────────────────────────────────────────────────────────────

    async def _token(self) -> str:
        data = await post_form(
            f"{self.base_url}/oauth/token",
            self.provider_name,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )
        tok = data.get("access_token")
        if not tok:
            raise ConnectorError(self.provider_name, "Failed to obtain SailPoint token")
        return tok

    # ── lookups ──────────────────────────────────────────────────────────────────

    async def _get_identity(self, identity_id: str, token: str) -> Optional[dict]:
        try:
            return await get_json(
                f"{self.base_url}/v3/identities/{identity_id}", token, self.provider_name)
        except ConnectorError as e:
            if e.status_code == 404:
                return None
            raise

    async def _search_identity(self, query: str, token: str) -> Optional[dict]:
        attr = "emailAddress" if "@" in query else "alias"
        # SailPoint filter strings must escape embedded quotes.
        safe = query.replace('"', '\\"')
        data = await get_json(
            f"{self.base_url}/v3/identities", token, self.provider_name,
            params={"filters": f'{attr} eq "{safe}"', "limit": 1})
        items = data if isinstance(data, list) else []
        return items[0] if items else None

    async def _linked_accounts(self, identity_id: str, token: str) -> list[dict]:
        """Accounts correlated to this identity across all connected sources."""
        try:
            data = await get_json(
                f"{self.base_url}/v3/accounts", token, self.provider_name,
                params={"filters": f'identityId eq "{identity_id}"', "limit": 50})
        except ConnectorError:
            return []
        stubs = []
        for acct in (data if isinstance(data, list) else []):
            source = acct.get("sourceName") or acct.get("source", {}).get("name") or ""
            stubs.append({
                "provider": re.sub(r"[^a-z0-9]+", "_", source.lower()).strip("_") or "sailpoint_source",
                "provider_sub": acct.get("nativeIdentity") or acct.get("id", ""),
                "via": "sailpoint-correlation",
                "source_name": source,
            })
        return stubs

    # ── node builder ──────────────────────────────────────────────────────────────

    def _build_node(self, ident: dict, linked: list[dict] | None = None) -> IdentityNode:
        attrs = ident.get("attributes", {}) if isinstance(ident.get("attributes"), dict) else {}
        node = IdentityNode(
            provider=self.provider_name,
            provider_sub=ident.get("id", ""),
            email=(ident.get("emailAddress") or attrs.get("email") or "").lower() or None,
            email_verified=True,  # IGA-managed identities are authoritative
            phone=attrs.get("phone") or attrs.get("mobilePhone"),
            username=ident.get("alias") or attrs.get("uid"),
            display_name=ident.get("name") or attrs.get("displayName"),
            org=attrs.get("department") or attrs.get("company"),
            location=attrs.get("location") or attrs.get("country"),
            linked_account_stubs=linked or [],
            raw_profile=ident,
        )
        node.normalize_email()
        return node

    # ── BaseConnector interface ───────────────────────────────────────────────────

    async def resolve(self, identifier: str, token: Optional[str] = None) -> Optional[IdentityNode]:
        if not (self.client_id and self.client_secret):
            raise ConnectorError(
                self.provider_name, "SAILPOINT_CLIENT_ID / SAILPOINT_CLIENT_SECRET required")
        access = await self._token()
        ident = await self._get_identity(identifier, access)
        if not ident:
            ident = await self._search_identity(identifier, access)
        if not ident:
            return None
        linked = await self._linked_accounts(ident.get("id", ""), access)
        return self._build_node(ident, linked)

    async def health_check(self) -> bool:
        return await head_check(f"{self.base_url}/oauth/token", self.provider_name)

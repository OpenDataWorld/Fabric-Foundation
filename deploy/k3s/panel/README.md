# k3s Stack Catalog

A lightweight, desktop-style **catalog UI** for the cloud-native components
running on (or available to) your k3s cluster — laid out as CNCF-landscape-style
grouped logo-cards. Dependency-free static site (no build step, no framework),
served by a hardened non-root nginx and deployable in one command.

![layout](https://img.shields.io/badge/UI-vanilla%20JS-blue) ![cncf](https://img.shields.io/badge/style-CNCF%20landscape-5b6ee1)

## What it is

- **`site/`** — the entire UI: `index.html`, `styles.css`, `app.js`, and
  **`catalog.json`** (the catalog data). The page is rendered at runtime from
  `catalog.json`, so cataloguing is pure data — edit one file, no rebuild.
- **`10-panel.yaml`** — non-root nginx (`nginx-unprivileged`, port 8080,
  read-only root fs, dropped caps, `RuntimeDefault` seccomp), Service, and a
  Traefik Ingress with optional cert-manager TLS.
- **`kustomization.yaml`** — turns `site/*` into a content-hashed `panel-site`
  ConfigMap (edits auto-trigger a rollout) and pins the image.
- **`install.sh`** — one-command deploy.

## Deploy

```bash
cd deploy/k3s/panel
./install.sh catalog.example.com you@example.com   # TLS
# or
./install.sh catalog.example.com                   # no auto-TLS
# or manually, after setting the host in 10-panel.yaml:
kubectl apply -k .
```

## Cataloguing

`site/catalog.json` is the single source of truth:

```json
{
  "title": "k3s Stack Catalog",
  "subtitle": "…",
  "categories": [
    {
      "name": "Application",
      "items": [
        {
          "name": "Nextcloud",
          "logo": "☁️",
          "description": "Self-hosted file sync.",
          "image": "nextcloud:30-apache",
          "status": "deployed",     // deployed | available
          "cncf": false,            // shows a CNCF badge when true
          "docs": "https://nextcloud.com",
          "manifest": "../nextcloud"
        }
      ]
    }
  ]
}
```

Add/extend categories and items, re-apply, and the panel rolls out the new
catalog automatically. The UI provides category filtering, free-text search,
and per-card deployed/available status + CNCF badges.

It ships pre-catalogued with the companion [`../nextcloud`](../nextcloud) stack
(Nextcloud, PostgreSQL, Redis, Traefik, cert-manager) plus common CNCF add-ons
(Longhorn, Prometheus, Grafana) marked as *available*.

## Preview locally

```bash
cd site && python3 -m http.server 8080   # then open http://localhost:8080
```

## Notes

- Hardened: runs non-root with a read-only root filesystem (writable `tmp`/cache
  via `emptyDir`), all capabilities dropped.
- The catalog is descriptive, not a live cluster client — it does not call the
  Kubernetes API, so it needs no RBAC and exposes no cluster data. Wire the
  `status` field from your CI/GitOps if you want it to reflect live state.

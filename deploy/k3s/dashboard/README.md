# Kubernetes Dashboard on k3s

The official **[Kubernetes Dashboard](https://github.com/kubernetes/dashboard)**
(v2.7.0) — a web control panel to view and manage the cluster (workloads, pods,
logs, exec, scaling). Vendored as plain YAML (no Helm), packaged the same way as
the rest of `deploy/k3s/`.

> The Dashboard is an official sub-project of Kubernetes (a CNCF *graduated*
> project), so this is a first-party, CNCF-aligned control panel.

## What's here

| File | Purpose |
|------|---------|
| `upstream-dashboard.yaml` | Vendored upstream manifest (dashboard + metrics-scraper, RBAC, secrets) |
| `admin-user.yaml` | `admin-user` ServiceAccount + cluster-admin binding + login-token Secret |
| `kustomization.yaml` | Ties them together, pins images |
| `install.sh` | One-command deploy; prints a login token + access instructions |

## Install

```bash
cd deploy/k3s/dashboard
./install.sh
# or:  kubectl apply -k .
```

## Access (no public exposure — by design)

A cluster-admin panel should **not** be reachable from the internet, so there is
no Ingress. Reach it over a port-forward, tunnelled through SSH if remote:

```bash
# on the k3s host:
kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard 8443:443

# from your laptop (if the host is remote):
ssh -L 8443:localhost:8443 you@your-k3s-host
```

Open <https://localhost:8443> (accept the self-signed cert), pick **Token**, and
paste the token `install.sh` printed. To fetch it again later:

```bash
kubectl -n kubernetes-dashboard get secret admin-user-token \
  -o jsonpath='{.data.token}' | base64 -d; echo
```

## Security

- The `admin-user` token is **cluster-admin** — treat it like a root password.
  For read-only access, change the `ClusterRoleBinding` in `admin-user.yaml`
  from `cluster-admin` to the built-in `view` role.
- No Ingress is created. If you must expose it, put it behind an
  authenticating proxy — never raw.

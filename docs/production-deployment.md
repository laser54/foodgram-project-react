# Foodgram production deployment runbook

This runbook prepares the reviewed repository foundation for
`https://foodgram.larin.work`. It does not authorize changes to shared Traefik,
DNS, production data, or GitHub settings.

## Architecture

Traefik owns host ports 80/443. The `frontend` nginx gateway joins the existing
external `rag-stack_internal` network and exposes only container port 8080.
Traefik's `web` router applies `to-https@docker`; its `websecure` router uses
resolver `le`. Nginx serves the React SPA, `/api/docs/`, `/static/`, and
`/media/`, and proxies `/api/` and `/admin/` to Django on the private
`foodgram_internal` network. Postgres is never attached to Traefik.

The workflow publishes backend and frontend images to GHCR under both the full
Git SHA and `latest`. Deployments always consume the full SHA. `latest` is for
human discovery only.

## One-time Hermes prerequisites

1. Install Docker Engine with Compose v2 and `curl` on the VPS. Confirm the
   external Docker network `rag-stack_internal` already exists. Do not edit the
   shared Traefik stack.
2. Place a reviewed checkout at `/opt/foodgram`, owned by a dedicated deployment
   account. Install `infra/foodgram-deploy` as an executable at that same path.
   The account needs Docker access and write access only to
   `/opt/foodgram/releases`; it must not receive general sudo access.
3. Create `/etc/foodgram/foodgram.env` mode `0600` from `.env.example`. Generate
   unique database credentials and a long random Django secret. Do not copy the
   placeholders, expose this file to Actions, or commit it. `POSTGRES_DB` is the
   single database-name setting used both to initialize Postgres and connect
   Django; do not replace it with the legacy `DB_NAME` setting.
4. Create a dedicated SSH key outside this repository. Restrict its public key
   in the deployment account's `authorized_keys` (all on one line):

   ```text
   restrict,command="/opt/foodgram/infra/foodgram-deploy" ssh-ed25519 PUBLIC_KEY_COMMENT_AND_MATERIAL
   ```

   The forced command reads and strictly validates `SSH_ORIGINAL_COMMAND`; only
   `deploy FULL_GIT_SHA` and `status` are accepted. Keep password login and SSH
   agent/port/X11 forwarding disabled for this account.
5. Configure the GitHub `production` environment with protection appropriate to
   the repository, then add these Actions secrets:

   - `PRODUCTION_SSH_HOST`: the production host name or address.
   - `PRODUCTION_SSH_PORT`: the SSH port.
   - `PRODUCTION_SSH_USER`: the restricted deployment account.
   - `PRODUCTION_SSH_KEY`: the dedicated private key.
   - `PRODUCTION_SSH_KNOWN_HOSTS`: the exact host-key line obtained through a
     trusted VPS console or provider channel. Never populate it with
     `ssh-keyscan` inside CI.

6. Ensure both GHCR packages are readable by this repository's Actions token.
   No long-lived registry credential is required: each deploy pipes the job's
   short-lived token to the forced command, which uses a temporary credential
   directory in `/dev/shm` and removes it on exit.

Before enabling the workflow, Hermes should validate the installed checkout:

```bash
FOODGRAM_ENV_FILE=/opt/foodgram/.env.example \
  IMAGE_TAG=0000000000000000000000000000000000000000 \
  docker compose -f /opt/foodgram/infra/docker-compose.yml config --quiet
/opt/foodgram/infra/foodgram-deploy status
```

The zero SHA is only for interpolation during configuration validation; it is
not deployable and must never be pulled.

## Release behavior

Pushes to `master` run backend lint/check/tests and the frontend test/build on
pinned Python and Node versions. Only then are SHA and `latest` images
published. The serialized production job requests exactly `deploy <SHA>` over
strict host-key-checked SSH.

The server command pulls only the Foodgram backend/frontend images, leaves the
database container and unrelated Compose projects alone, runs normal committed
Django migrations and `collectstatic`, recreates only backend/frontend, and
waits for container health plus the public database-aware endpoint. A failed
health check restores the previously configured images. Database migrations are
not automatically reversed.

The private backend healthcheck connects over loopback but explicitly sends
`Host: foodgram.larin.work`, so it exercises the production Django host policy
without adding loopback addresses to `ALLOWED_HOSTS`. Postgres readiness and
Django use the same `POSTGRES_DB` value; this prevents the server-ready signal
from preceding creation of the database that the health endpoint reads.

Inspect the active revision, image references, and health:

```bash
sudo -u FOODGRAM_DEPLOY_ACCOUNT /opt/foodgram/infra/foodgram-deploy status
```

## Rollback

Find the previous full Git SHA from the last successful workflow, GHCR package,
or `/opt/foodgram/releases/previous.env`. Roll back through the same restricted
path; never use `latest`:

```bash
printf '%s' "$EPHEMERAL_GHCR_TOKEN" | \
  ssh -T foodgram-production "deploy PREVIOUS_FULL_GIT_SHA"
```

The token in this example must be supplied by an ephemeral credential source,
must not be placed in shell history, and must be unset immediately afterward.
If a release contains a non-backward-compatible schema migration, review that
migration's explicit reverse procedure and back up the database before release;
image rollback alone does not reverse database state.

## Known test and compatibility limits

Node `20.19.5` is deliberately pinned for deterministic compatibility with the
legacy Create React App tree and is used only in the image build stage and CI;
nginx is the production runtime. The test setup retains the timer alias expected
by the legacy Testing Library under this Node runtime. Upgrading
CRA/webpack-dev-server is deferred to LA5-12. The frontend suite contains one
anonymous-route smoke test and the backend suite covers the health endpoint;
broader application behavior remains untested technical debt. The backend is
flake8-clean. The legacy frontend has no standalone lint script and contains
existing CRA/ESLint warnings, so its production build deliberately retains
CRA's non-CI warning behavior (`CI=false`); this is not a claim that frontend
lint passes. This ticket does not change UI code to clear that deferred backlog.

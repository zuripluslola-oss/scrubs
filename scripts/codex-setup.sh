#!/usr/bin/env bash
# Codex environment setup script for Must Love Scrubs.
# Paste this into Codex's environment "setup script" field (or run it once).
# It prepares the production web app under web/.
set -e

echo "→ Installing web app dependencies…"
cd web
npm install

echo "→ Generating Prisma client…"
npx prisma generate

# The following need your secrets (DATABASE_URL etc.) set in the environment.
# Uncomment once they're configured:
# echo "→ Applying database migrations…"
# npx prisma migrate deploy
# echo "→ Importing prototype content…"
# node scripts/import-content.mjs

echo "✓ Setup complete. Run 'cd web && npm run dev' to start."

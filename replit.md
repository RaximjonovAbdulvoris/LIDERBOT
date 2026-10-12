# Workspace

## Overview

pnpm workspace monorepo using TypeScript. Each package manages its own dependencies.

## Stack

- **Monorepo tool**: pnpm workspaces
- **Node.js version**: 24
- **Package manager**: pnpm
- **TypeScript version**: 5.9
- **API framework**: Express 5
- **Database**: PostgreSQL + Drizzle ORM
- **Validation**: Zod (`zod/v4`), `drizzle-zod`
- **API codegen**: Orval (from OpenAPI spec)
- **Build**: esbuild (CJS bundle)

## Key Commands

- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- `pnpm --filter @workspace/api-server run dev` — run API server locally
- `python -m bot.main` — run the WB TAXI HUMO Telegram bot locally

See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details.

## WB TAXI HUMO Telegram Bot

Located in `bot/`. Long-polling Python Telegram bot built with `python-telegram-bot` 21.

- `bot/main.py` — entry point, registers conversation handlers
- `bot/config.py` — loads `TELEGRAM_BOT_TOKEN`, 2× `DRIVER_GROUP_*`, `BRAND_GROUP`, `CHALA_RASM_GROUP`, `OTHER_PARK_GROUP`, `ARCHIVE_GROUP` from env
- `bot/handlers/start.py` — `/start` and main menu (Ariza Tashlash / Brend Ariza)
- `bot/handlers/driver.py` — 13-step driver registration: name → phone (button) → docs warning → 8 doc photos (passport, license, tech passport, selfie, litsenziya) → 4 car photos → plate. Sends 2 albums (10-photo docs + 2-photo selfie/litsenziya) to one of 2 driver groups in round-robin order.
- `bot/handlers/brand.py` — branding application: warning (SPARK/NEXIA 3/<2016 not eligible) → name → phone → model → year → color. Sends formatted message to brand group.
- `bot/templates/` — optional template images (`passport_front.jpg`, etc.) shown to the user when each photo is requested. See `bot/templates/README.md`.

Workflow: `Telegram Bot` (console output, command `python -m bot.main`).

## Telegram operator queues

- Main queues: `DRIVER_GROUP_1` and `DRIVER_GROUP_2`. Groups 3/4 are no longer used.
- Main buttons: Tayyor, Chala rasm, Boshqa park, Jarayonda.
- `CHALA_RASM_GROUP` and `OTHER_PARK_GROUP`: Tayyor, O’chirish, Jarayonda.
- Jarayonda starts red and becomes yellow when clicked in every working queue.
  A move to another queue resets it to red.
- Tayyor copies the full application to `ARCHIVE_GROUP` without buttons, then
  removes its source messages. O’chirish deletes a secondary-queue application
  without archiving. Izoh berish and its text relay have been removed.
- Configure distinct numeric Telegram chat IDs for the four working queues and
  archive. Missing destinations block the corresponding action without deleting
  the original. Bot needs photo/message sending and message deletion permissions.
- A partial copy retains originals. Failed source cleanup remains tracked; click
  a button again after fixing permissions to retry cleanup without copying again.
  Telegram restrictions may prevent deletion of older messages.
- Each new application has its own ID, including repeat applications by one user.
  Existing numeric-ID buttons are supported when their saved records still exist.
  Existing visible keyboards update when Jarayonda is clicked; removed comment
  buttons no longer send messages. Existing applications are not bulk-migrated.
- Keep `PERSIST_DIR` on durable storage and run one bot process. Persistence is
  flushed before source deletion. A process crash or ambiguous network timeout
  during copying can still leave destination copies requiring manual cleanup.
- `.env.example` lists settings; configure them in the process environment.
  The application does not automatically load `.env` files.
- Offline checks: `python -m unittest discover -s tests -v`.

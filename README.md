# 180° Consulting Newsletter

A marketing/landing page for the 180 Degrees Consulting newsletter, built with
React, TypeScript, Vite and Framer Motion. Features a scroll-driven "what's
inside" section with a sticky visual panel, animated hero stats, and a
newsletter signup form.

## Development

```bash
npm install
npm run dev
```

The dev server runs on `http://localhost:5173`.

## Alloy sandbox

This repo is wired up for the Alloy sandbox via `docker-compose.alloy.yaml`
and `.alloy/environment.json`. The compose file runs the Vite dev server in
a Node container using `network_mode: host`, bound to port `5173`.

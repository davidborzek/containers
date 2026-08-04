# coder-workspace

A lean Alpine base image for [Coder](https://coder.com) workspaces focused on an
AI coding-agent workflow.

Ships (all on `PATH` in `/usr/local/bin` or via apk):

- `opencode` — the coding agent (point it at a model via `OPENCODE_API_KEY`)
- `code-server` — VS Code in the browser
- `tmux` — keep the agent session alive across SSH disconnects
- `git`, `git-lfs`, `gh`, `openssh-client`
- `nix` (flakes, single-user) + `direnv`/`nix-direnv` — enter per-project
  devShells with `nix develop` or automatically via a `.envrc` (`use flake`)

Runs as the non-root user `coder` (uid 1000), which owns the Nix store.

> Language toolchains are intentionally **not** baked in. Provide them
> per-project through a `flake.nix` devShell instead of bloating the image.

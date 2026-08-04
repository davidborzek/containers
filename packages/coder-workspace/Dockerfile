FROM debian:12-slim

ARG VERSION

# renovate: datasource=github-releases depName=coder/code-server
ARG CODE_SERVER_VERSION=4.130.0
# renovate: datasource=github-releases depName=cli/cli
ARG GH_VERSION=2.63.2
# renovate: datasource=github-releases depName=anomalyco/opencode
ARG OPENCODE_VERSION=1.18.12
# pinned nix-direnv direnvrc (provides `use flake`)
ARG NIX_DIRENV_VERSION=3.0.6

ENV LANG=C.UTF-8 \
    SHELL=/bin/bash \
    NIX_REMOTE="" \
    DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates curl wget jq unzip xz-utils \
        bash sudo procps \
        git git-lfs openssh-client \
        tmux direnv \
    && rm -rf /var/lib/apt/lists/*

# nix flakes config (honoured by the single-user store too)
RUN mkdir -p /etc/nix \
    && printf 'experimental-features = nix-command flakes\naccept-flake-config = true\n' > /etc/nix/nix.conf

# gh cli
RUN curl -fsSL "https://github.com/cli/cli/releases/download/v${GH_VERSION}/gh_${GH_VERSION}_linux_amd64.tar.gz" \
      | tar -xz -C /tmp \
    && install -m 0755 "/tmp/gh_${GH_VERSION}_linux_amd64/bin/gh" /usr/local/bin/gh \
    && rm -rf "/tmp/gh_${GH_VERSION}_linux_amd64"

# code-server (standalone, glibc)
RUN curl -fsSL https://code-server.dev/install.sh \
      | sh -s -- --method=standalone --prefix=/usr/local --version="${CODE_SERVER_VERSION}"

# opencode (installer reads $VERSION as the opencode version to fetch; pin it)
RUN curl -fsSL https://opencode.ai/install | env VERSION="${OPENCODE_VERSION}" bash \
    && install -m 0755 /root/.opencode/bin/opencode /usr/local/bin/opencode \
    && rm -rf /root/.opencode

# non-root user "coder" (uid 1000), owns the nix store (single-user)
RUN useradd -m -u 1000 -s /bin/bash coder \
    && echo 'coder ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/coder \
    && mkdir -m 0755 /nix \
    && chown coder:coder /nix

USER coder
ENV USER=coder \
    HOME=/home/coder
WORKDIR /home/coder

# nix (recent, single-user) + direnv/nix-direnv (auto-enter devShells via `use flake`)
RUN curl -fsSL https://nixos.org/nix/install | sh -s -- --no-daemon \
    && mkdir -p ~/.config/direnv \
    && curl -fsSL "https://raw.githubusercontent.com/nix-community/nix-direnv/${NIX_DIRENV_VERSION}/direnvrc" \
         -o ~/.config/direnv/direnvrc \
    && printf '%s\n' \
         '' \
         '# nix single-user + local tools on PATH' \
         '[ -f ~/.nix-profile/etc/profile.d/nix.sh ] && . ~/.nix-profile/etc/profile.d/nix.sh' \
         'export PATH="/usr/local/bin:$PATH"' \
         'eval "$(direnv hook bash)"' \
         >> ~/.bashrc \
    && printf '%s\n' '[ -f ~/.bashrc ] && . ~/.bashrc' > ~/.bash_profile

# make nix + local tools available in non-interactive shells too (Debian's
# .bashrc returns early when non-interactive, so PATH must be set here as well)
ENV PATH="/home/coder/.nix-profile/bin:/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin" \
    NIX_SSL_CERT_FILE="/etc/ssl/certs/ca-certificates.crt"

LABEL org.opencontainers.image.source="https://github.com/davidborzek/containers"

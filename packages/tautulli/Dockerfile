FROM python:3.13-alpine3.20

ARG VERSION

ENV TAUTULLI_DOCKER=True \
    TAUTULLI_BASEIMAGE_URL="https://github.com/Tautulli/tautulli-baseimage/archive/python3.tar.gz"

ENV UMASK="0002" \
    TZ="Etc/UTC"

USER root

RUN apk add --no-cache \
    catatonit \
    ca-certificates \
    curl \
    git \
    tar

RUN mkdir -p /tmp/base
RUN \
    curl -fsSL $TAUTULLI_BASEIMAGE_URL \
    | tar xzf - -C /tmp/base --strip-components=1 \ 
    && \
    pip install --no-cache-dir --upgrade pip \
    && \
    pip install --no-cache-dir --upgrade \
    --extra-index-url https://www.piwheels.org/simple \
    -r /tmp/base/requirements.txt

WORKDIR /app/tautulli

RUN git clone --depth 1 --branch "v${VERSION}" https://github.com/Tautulli/Tautulli /app/tautulli \
    && \
    git rev-parse HEAD > /app/tautulli/version.txt \
    && \
    echo "master" > /app/tautulli/branch.txt \
    && \
    rm -rf /app/tautulli/.git \
    && \
    mkdir -p /config \
    && \
    chown nobody:nogroup /config \
    && \
    rm -rf \
        /tmp/* \
        /root/.cache

USER nobody:nogroup
WORKDIR /config
VOLUME [ "/config" ]

ENTRYPOINT ["/usr/bin/catatonit", "--"]
CMD ["python", "/app/tautulli/Tautulli.py", "--datadir", "/config"]

LABEL org.opencontainers.image.source="https://github.com/Tautulli/Tautulli"
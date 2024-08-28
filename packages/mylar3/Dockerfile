FROM python:3.11-alpine3.20

ARG VERSION

ENV UMASK="0002" \
    TZ="Etc/UTC"

USER root

RUN apk add --no-cache \
    catatonit \
    ca-certificates \
    curl \
    nodejs \
    build-base \
    libffi-dev \
    zlib-dev \
    jpeg-dev \
    tar

WORKDIR /app/mylar3

RUN curl -fsSL "https://github.com/mylar3/mylar3/archive/v${VERSION}.tar.gz" \
    | tar xzf - -C /app/mylar3  --strip-components=1 \
    && \
    pip install --no-cache-dir -r /app/mylar3/requirements.txt \
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
CMD ["python", "/app/mylar3/Mylar.py", "--nolaunch", "--datadir", "/config/mylar"]

LABEL org.opencontainers.image.source="https://github.com/mylar3/mylar3"
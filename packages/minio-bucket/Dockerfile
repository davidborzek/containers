FROM minio/mc:RELEASE.2024-09-16T17-43-14Z AS minio-mc

FROM alpine:3.21.2

ARG VERSION

COPY --from=minio-mc /usr/bin/mc /usr/bin/mc

RUN apk add --no-cache \
    ca-certificates \
    bash \
    curl \
    jq

COPY ./entrypoint.sh /entrypoint.sh

ENV VERSION=${VERSION}

ENTRYPOINT [ "/entrypoint.sh" ]

LABEL org.opencontainers.image.source="https://github.com/minio/mc"

# containers

A collection of some container images providing different applications in the best case semantically versioned and rootless.

It also keeps things simple and minimalistic by preventing the usage of s6-overlay and using Alpine Linux as base image.

## Packages

Each package is available as `latest` tag and tags specifying the version.

> **Note:** The `test` package is a package for testing purposes without any application.=

| Package                                                                               | Image                            |
| ------------------------------------------------------------------------------------- | -------------------------------- |
| [minio-bucket](https://github.com/davidborzek/containers/pkgs/container/minio-bucket) | ghcr.io/davidborzek/minio-bucket |
| [mylar3](https://github.com/davidborzek/containers/pkgs/container/mylar3)             | ghcr.io/davidborzek/mylar3       |
| [tautulli](https://github.com/davidborzek/containers/pkgs/container/tautulli)         | ghcr.io/davidborzek/tautulli     |

## Credits

- [onedr0p/containers](https://github.com/onedr0p/containers)

#!/usr/bin/env python3

import argparse
import os
import yaml
import json
import subprocess
import requests


def get_published_version(image):
    res = requests.get(
        f"https://api.github.com/users/{owner}/packages/container/{image}/versions",
        headers={
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {gh_token}",
        },
    )

    if res.status_code == 404:
        return None

    if res.status_code != 200:
        raise RuntimeError(
            f"failed to check published ghcr.io version: status code {res.status_code}"
        )

    # TODO: this is paginated, should we handle that?
    versions = res.json()
    for version in versions:
        tags = version["metadata"]["container"]["tags"]
        if "latest" in tags:
            tags.remove("latest")
            return max(tags, key=len)


def load_package(path):
    try:
        file = open(path, "r")
    except FileNotFoundError:
        return
    else:
        package = yaml.safe_load(file)
        return package


def prepare_tag(name, version):
    return f"{registry}/{owner}/{name}:{version}"


def prepare_tags(package, version):
    tags = [
        prepare_tag(package["name"], "latest"),
    ]

    if package["semver"]:
        parts = version.split(".")
        while len(parts) > 1:
            tags.append(prepare_tag(package["name"], ".".join(parts)))
            parts = parts[:-1]
    else:
        tags.append(prepare_tag(package["name"], version))

    return tags


def prepare_package(path):
    build = {}

    package = load_package(os.path.join(path, "package.yaml"))
    if package is None:
        return

    build["name"] = package["name"]
    build["platforms"] = package["platforms"]

    version_path = os.path.join(path, "version.sh")
    if not os.path.exists(version_path):
        return

    out = subprocess.check_output(version_path)
    build["version"] = out.decode("utf-8").strip()

    if not force:
        published = get_published_version(package["name"])
        if published is not None and published == build["version"]:
            return

    build["tags"] = prepare_tags(package, build["version"])

    goss_config = os.path.join(path, "goss.yaml")
    goss_enabled = os.path.exists(goss_config)
    build["goss"] = {
        "enabled": goss_enabled,
        "config": goss_config if goss_enabled else None,
    }

    return build


def main():
    parser = argparse.ArgumentParser(
        prog="prepare", description="Prepare the environment for the build"
    )

    parser.add_argument(
        "--packages",
        "-p",
        action="store",
        dest="packages",
        help="The directory of the packages to prepare",
        default="./packages",
    )

    parser.add_argument(
        "--registry",
        "-r",
        action="store",
        dest="registry",
        help="The registry to push the packages",
        required=True,
    )

    parser.add_argument(
        "--owner",
        "-o",
        action="store",
        dest="owner",
        help="The owner of the packages",
        required=True,
    )

    parser.add_argument(
        "--force",
        "-f",
        action="store",
        dest="force",
        help="Force rebuild all packages",
        default="false",
    )

    parser.add_argument(
        "--limit",
        "-l",
        action="store",
        dest="limit",
        help="Limit the packages to build",
    )

    args = parser.parse_args()

    global owner, registry, force, gh_token
    owner = args.owner
    registry = args.registry
    force = args.force.lower() == "true"

    gh_token = os.getenv("GITHUB_TOKEN")
    if gh_token is None:
        raise ValueError("GITHUB_TOKEN is not set")

    limit = None
    if args.limit is not None and args.limit != "all":
        limit = args.limit.replace(" ", "").split(",")

    builds = []
    for root, dirs, _ in os.walk(args.packages):
        for dir in dirs:
            if limit is None or dir in limit:
                build = prepare_package(os.path.join(root, dir))
                if build is not None:
                    builds.append(build)

    print(json.dumps(builds))


if __name__ == "__main__":
    main()

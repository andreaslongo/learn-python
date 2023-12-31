#!/usr/bin/env bash

readonly local script_dir=$( cd "$( dirname "${BASH_SOURCE[0]:-${(%):-%x}}" )" && pwd )
readonly local parent_dir=$(dirname ${script_dir})

# Container user: uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)
readonly local uid=1000
readonly local gid=1000

# Use --publish <host_port>:<container_port> to enable networking.
# TODO: for dev: --volume ~/code/template-python:/root/code/template-python:Z,ro \
podman container attach "$(basename ${parent_dir})" 2>/dev/null || podman container run \
    --interactive \
    --name="$(basename ${parent_dir})" \
    --publish 8002:7878 \
    --pull=newer \
    --rm \
    --tty \
    --user ${uid}:${gid} \
    --userns keep-id:uid=${uid},gid=${gid} \
    --volume "${parent_dir}":/home/appuser/app:Z,rw \
    --volume ~/code/template-python/cargo.py:/usr/local/bin/cargo.py:Z,ro \
    --workdir /home/appuser/app \
        localhost/"$(basename ${parent_dir})":latest

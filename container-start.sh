#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

dockerd > /var/log/dockerd.log 2>&1 &

tini -g -- start.sh

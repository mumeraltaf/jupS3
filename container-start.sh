#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

/sbin/init --log-level=err

tini -g -- start.sh

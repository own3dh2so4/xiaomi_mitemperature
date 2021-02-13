#!/usr/bin/env bash

set -ex

isort app tests
autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place app tests
black app tests
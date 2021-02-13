#!/usr/bin/env bash

set -ex

isort --check-only app tests
black app tests --check
flake8 app
mypy app
vulture app --min-confidence 70
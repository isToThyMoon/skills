#!/usr/bin/env bash
# Fixtures are stored as SKILL.fixture.md so skill installers that scan for
# SKILL.md never pick them up; restore the real name in the run directory.
set -eu
cp -R "$(dirname "$0")/files/." .
for f in */SKILL.fixture.md; do mv "$f" "${f%SKILL.fixture.md}SKILL.md"; done

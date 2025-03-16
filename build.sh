#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Ensure uv is in PATH
export PATH="$HOME/.local/bin:$PATH"

# Install dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
    uv pip sync requirements.txt
else
    echo "Warning: requirements.txt not found!"
fi

# Collect static assets
uv run python manage.py collectstatic --no-input

# Apply migrations
uv run python manage.py migrate

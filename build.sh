#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
export PATH="/opt/render/.local/bin:$PATH"

# Install dependencies
if [ -f requirements.txt ]; then
    uv pip sync requirements.txt
else
    echo "Warning: requirements.txt not found!"
fi

# Collect static files
uv run python manage.py collectstatic --no-input

# Apply migrations
uv run python manage.py migrate

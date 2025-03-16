#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Ensure uv is in the PATH
export PATH="/opt/render/.local/bin:$PATH"

# Persist PATH change for future shell sessions
echo 'export PATH="/opt/render/.local/bin:$PATH"' >> $HOME/.profile

# Install dependencies
uv pip sync requirements.txt

# Collect static files
uv run python manage.py collectstatic --no-input

# Apply database migrations
uv run python manage.py migrate

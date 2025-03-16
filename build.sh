#!/usr/bin/env bash
# Exit on error
set -o errexit

# Add uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Modify this line as needed for your package manager (pip, poetry, etc.)
uv pip sync requirements.txt

# Convert static asset files
uv run python manage.py collectstatic --no-input

# Apply any outstanding database migrations
uv run python manage.py migrate
default:
	@just --list

# Run the development server
serve:
	uv run python manage.py runserver

# Run database migrations
migrate:
	uv run python manage.py migrate

# Make database migrations
makemigrations:
	uv run python manage.py makemigrations

# Create a superuser
createsuperuser:
	uv run python manage.py createsuperuser

# Run tests
test:
	uv run pytest

# Lint the codebase
lint:
	just _pre-commit run --all-files

# Helper for pre-commit
_pre-commit *args:
	uvx prek {{ args }}

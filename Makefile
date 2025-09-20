# Makefile

# Bring down all containers
down:
	docker compose down --remove-orphans

# Build all services
build:
	docker compose build

# Bring everything up
up:
	docker compose up

# Full reset: down → build → up
reset: down build up
	@echo "✅ Docker stack rebuilt and running."
.RECIPEPREFIX := $(.RECIPEPREFIX)

GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m

# ------------------------ Сервисы ------------------------

COMPOSE_F := -f $(SERVICE)/build/dev/docker-compose.yml

build:
	docker compose -p $(SERVICE) --env-file $(SERVICE)/build/.env ${COMPOSE_F} build

start:
	docker compose -p $(SERVICE) --env-file $(SERVICE)/build/.env ${COMPOSE_F} up

startb:
	docker compose -p $(SERVICE) --env-file $(SERVICE)/build/.env ${COMPOSE_F} up --build

startd:
	docker compose -p $(SERVICE) --env-file $(SERVICE)/build/.env ${COMPOSE_F} up --detach

down:
	docker compose -p $(SERVICE) --env-file $(SERVICE)/build/.env ${COMPOSE_F} down

restart:
	docker compose -p $(SERVICE) --env-file $(SERVICE)/build/.env ${COMPOSE_F} down
	docker compose -p $(SERVICE) --env-file $(SERVICE)/build/.env ${COMPOSE_F} up --detach

logs:
	docker logs -f $(SERVICE)

makemigrations:
	docker exec -it $(SERVICE) /bin/sh -c "alembic revision --autogenerate -m \"$(MESSAGE)\""

migrate:
	docker exec -it $(SERVICE) /bin/sh -c "alembic upgrade head"

exec:
	docker exec -it $(SERVICE) /bin/sh -c "$(COMMAND)"

# ------------------------ Инфраструктура ------------------------

COMPOSE_INFRA_F := -f infrastructure/docker-compose.yml

infra_build:
	docker compose -p infra --env-file infrastructure/.env ${COMPOSE_INFRA_F} up --build

infra_startd:
	docker compose -p infra --env-file infrastructure/.env ${COMPOSE_INFRA_F} up --detach

infra_down:
	docker compose -p infra --env-file infrastructure/.env ${COMPOSE_INFRA_F} down

infra_logs:
	docker compose -p infra logs -f

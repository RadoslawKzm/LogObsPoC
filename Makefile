.PHONY: down-api
down-api:
	@echo "Stopping API environment..."
	docker compose -f ./deployment/docker-compose.yaml stop api
	docker compose -f ./deployment/docker-compose.yaml rm -f api
	@echo "API environment stopped successfully"

.PHONY: build-api
build-api:
	@echo "Building API environment..."
	docker compose -f ./deployment/docker-compose.yaml build api
	@echo "API environment built successfully"

.PHONY: start-api
start-api:
	@echo "Upping API environment..."
	docker compose -f ./deployment/docker-compose.yaml up -d api
	@echo "API environment upped successfully"

.PHONY: up-api
up-api:
	@echo "Starting API environment..."
	@${MAKE} down-api
	@${MAKE} build-api
	@${MAKE} start-api
	@echo "API environment started successfully"

.PHONY: build-postgres
build-postgres:
	@echo "Building Postgres environment..."
	docker compose -f ./deployment/docker-compose.yaml build postgres
	@echo "Postgres environment built successfully"

.PHONY: up-postgres
up-postgres:
	@echo "Starting Postgres environment..."
	docker compose -f ./deployment/docker-compose.yaml up -d postgres
	@echo "Postgres environment started successfully"

.PHONY: down-postgres
down-postgres:
	@echo "Stopping Postgres environment..."
	docker compose -f ./deployment/docker-compose.yaml stop postgres
	docker compose -f ./deployment/docker-compose.yaml rm -f postgres
	@echo "Postgres environment stopped successfully"

.PHONY: down-postgres-v
down-postgres-v:
	@echo "Stopping and removing Postgres with volumes..."
	docker compose -f ./deployment/docker-compose.yaml down -v postgres
	rm -rf ./deployment/postgres_data
	@echo "Postgres and its volumes removed successfully"


.PHONY: up-db
up-db:
	@echo "Starting DB environment..."
	@${MAKE} down-postgres
	@${MAKE} build-postgres
	@${MAKE} up-postgres
	@echo "DB environment started successfully"

.PHONY: down-db
down-db:
	@echo "Stopping DB environment..."
	@${MAKE} down-postgres
	@echo "DB environment stopped successfully"

.PHONY: down-db-v
down-db-v:
	@echo "Stopping DB environment..."
	@${MAKE} down-postgres-v
	@echo "DB environment stopped successfully"


#
#
#
#
#.PHONY: up-dev
#up-build:
#	docker compose -f docker-compose.yaml build
#
#
#.PHONY: up-dev
#up-dev:
#	#docker compose -f docker-compose.yaml down
#	@${MAKE} down-dev
#	@${MAKE} up-build
#	docker compose -f docker-compose.yaml up -d
#
#.PHONY: up-db
#up-db:
#	#docker compose -f docker-compose.yaml down
#	@${MAKE} down-dev
#	@${MAKE} up-build
#	docker compose -f docker-compose.yaml up -d postgres-db
#	docker compose -f docker-compose.yaml up -d mongo-db
#
#.PHONY: down-dev
#down-dev:
#	docker compose -f docker-compose.yaml down
#
#.PHONY: down-dev-volumes
#down-dev-volumes:
#	docker compose -f docker-compose.yaml down -v
#
#.PHONY: up-backend
#up-backend:
#	docker compose -f docker-compose.yaml down backend
#	docker compose -f docker-compose.yaml build backend
#	docker compose -f docker-compose.yaml up -d backend
#
#.PHONY: up-locust
#up-locust:
#	docker compose -f locust-compose.yaml down
#	docker compose -f locust-compose.yaml up -d --scale locust-worker=4
#
#.PHONY: down-locust
#down-locust:
#	docker compose -f locust-compose.yaml down



#.PHONY: up-db
#up-frontend:
#	docker compose -f docker-compose.yaml down postgres-db
#	docker compose -f docker-compose.yaml build postgres-db
#	docker compose -f docker-compose.yaml up -d postgres-db

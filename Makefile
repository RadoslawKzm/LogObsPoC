### ----- API ----- ###
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
### ----- API ----- ###
###############################################################################

###############################################################################
### ----- WORKERS ----- ###
.PHONY: down-workers
down-workers:
	@echo "Stopping Workers"
	docker compose -f ./deployment/docker-compose.yaml stop worker-small
	docker compose -f ./deployment/docker-compose.yaml rm -f worker-small
	docker compose -f ./deployment/docker-compose.yaml stop worker-medium
	docker compose -f ./deployment/docker-compose.yaml rm -f worker-medium
	docker compose -f ./deployment/docker-compose.yaml stop worker-large
	docker compose -f ./deployment/docker-compose.yaml rm -f worker-large
	@echo "Workers stopped successfully"
.PHONY: build-workers
build-workers:
	@echo "Building Workers"
	docker compose -f ./deployment/docker-compose.yaml build worker-small
	docker compose -f ./deployment/docker-compose.yaml build worker-medium
	docker compose -f ./deployment/docker-compose.yaml build worker-large
	@echo "Workers built successfully"
.PHONY: start-workers
start-workers:
	@echo "Upping Workers"
	docker compose -f ./deployment/docker-compose.yaml up -d worker-small
	docker compose -f ./deployment/docker-compose.yaml up -d worker-medium
	docker compose -f ./deployment/docker-compose.yaml up -d worker-large
	@echo "Workers upped successfully"
.PHONY: up-workers
up-workers:
	@echo "Starting Workers"
	@${MAKE} down-workers
	@${MAKE} build-workers
	@${MAKE} start-workers
	@echo "Workers started successfully"
### ----- WORKERS ----- ###
###############################################################################

###############################################################################
### ----- POSTGRES ----- ###
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
### ----- POSTGRES ----- ###
###############################################################################

###############################################################################
### ----- RABBIT ----- ###
.PHONY: build-rabbit
build-rabbit:
	@echo "Building RabbitMQ environment..."
	docker compose -f ./deployment/docker-compose.yaml build rabbitmq
	@echo "RabbitMQ environment built successfully"
.PHONY: up-rabbit
up-rabbit:
	@echo "Starting RabbitMQ environment..."
	docker compose -f ./deployment/docker-compose.yaml up -d rabbitmq
	@echo "RabbitMQ environment started successfully"
.PHONY: down-rabbit
down-rabbit:
	@echo "Stopping RabbitMQ environment..."
	docker compose -f ./deployment/docker-compose.yaml stop rabbitmq
	docker compose -f ./deployment/docker-compose.yaml rm -f rabbitmq
	@echo "RabbitMQ environment stopped successfully"
.PHONY: down-rabbit-v
down-rabbit-v:
	@echo "Stopping and removing RabbitMQ with volumes..."
	docker compose -f ./deployment/docker-compose.yaml down -v rabbitmq
	rm -rf ./deployment/rabbitmq_data
	@echo "RabbitMQ and its volumes removed successfully"
### ----- RABBIT ----- ###
###############################################################################

###############################################################################
### ----- DATABASES ----- ###
.PHONY: build-db
build-db:
	@echo "Building DB environment..."
	@${MAKE} build-postgres
	@${MAKE} build-rabbit
.PHONY: up-db
up-db:
	@echo "Starting DB environment..."
	@${MAKE} down-db
	@${MAKE} build-db
	@${MAKE} up-postgres
	@${MAKE} up-rabbit
	@echo "DB environment started successfully"
.PHONY: down-db
down-db:
	@echo "Stopping DB environment..."
	@${MAKE} down-postgres
	@${MAKE} down-rabbit
	@echo "DB environment stopped successfully"
.PHONY: down-db-v
down-db-v:
	@echo "Stopping DB environment..."
	@${MAKE} down-postgres-v
	@${MAKE} down-rabbit-v
	@echo "DB environment stopped successfully"
### ----- DATABASES ----- ###
###############################################################################

###############################################################################
### ----- OBSERVABILITY ----- ###
.PHONY: build-obs
build-obs:
	@echo "Building Observability environment..."
	@${MAKE} build-loki
	@${MAKE} build-promtail
	@${MAKE} build-grafana
.PHONY: up-obs
up-obs:
	@echo "Starting Observability environment..."
	@${MAKE} down-obs
	@${MAKE} build-obs
	@${MAKE} up-loki
	@${MAKE} up-promtail
	@${MAKE} up-grafana
	@echo "Observability environment started successfully"
.PHONY: down-obs
down-obs:
	@echo "Stopping Observability environment..."
	@${MAKE} down-grafana
	@${MAKE} down-promtail
	@${MAKE} down-loki
	@echo "Observability environment stopped successfully"
.PHONY: down-obs-v
down-obs-v:
	@echo "Stopping Observability environment..."
	@${MAKE} down-grafana-v
	@${MAKE} down-promtail-v
	@${MAKE} down-loki-v
	@echo "Observability environment stopped successfully"

### ----- GRAFANA ----- ###
.PHONY: build-grafana
build-grafana:
	@echo "Building Grafana environment..."
	docker compose -f ./deployment/docker-compose.yaml build grafana
	@echo "Grafana environment built successfully"
.PHONY: up-grafana
up-grafana:
	@echo "Starting Grafana environment..."
	docker compose -f ./deployment/docker-compose.yaml up -d grafana
	@echo "Grafana environment started successfully"
.PHONY: down-grafana
down-grafana:
	@echo "Stopping Grafana environment..."
	docker compose -f ./deployment/docker-compose.yaml stop grafana
	docker compose -f ./deployment/docker-compose.yaml rm -f grafana
	@echo "Grafana environment stopped successfully"
.PHONY: down-grafana-v
down-grafana-v:
	@echo "Stopping and removing Grafana with volumes..."
	docker compose -f ./deployment/docker-compose.yaml down -v grafana
	rm -rf ./deployment/grafana_data
	@echo "Grafana and its volumes removed successfully"

### ----- LOKI ----- ###
.PHONY: build-loki
build-loki:
	@echo "Building Loki environment..."
	docker compose -f ./deployment/docker-compose.yaml build loki
	@echo "Loki environment built successfully"
.PHONY: up-loki
up-loki:
	@echo "Starting Loki environment..."
	docker compose -f ./deployment/docker-compose.yaml up -d loki
	@echo "Loki environment started successfully"
.PHONY: down-loki
down-loki:
	@echo "Stopping Loki environment..."
	docker compose -f ./deployment/docker-compose.yaml stop loki
	docker compose -f ./deployment/docker-compose.yaml rm -f loki
	@echo "Loki environment stopped successfully"
.PHONY: down-loki-v
down-loki-v:
	@echo "Stopping and removing Loki with volumes..."
	docker compose -f ./deployment/docker-compose.yaml down -v loki
	rm -rf ./deployment/loki_data
	@echo "Loki and its volumes removed successfully"

### ----- PROMTAIL ----- ###
.PHONY: build-promtail
build-promtail:
	@echo "Building Promtail environment..."
	docker compose -f ./deployment/docker-compose.yaml build promtail
	@echo "Promtail environment built successfully"
.PHONY: up-promtail
up-promtail:
	@echo "Starting Promtail environment..."
	docker compose -f ./deployment/docker-compose.yaml up -d promtail
	@echo "Promtail environment started successfully"
.PHONY: down-promtail
down-promtail:
	@echo "Stopping Promtail environment..."
	docker compose -f ./deployment/docker-compose.yaml stop promtail
	docker compose -f ./deployment/docker-compose.yaml rm -f promtail
	@echo "Promtail environment stopped successfully"
.PHONY: down-promtail-v
down-promtail-v:
	@echo "Stopping and removing Promtail with volumes..."
	docker compose -f ./deployment/docker-compose.yaml down -v promtail
	rm -rf ./deployment/promtail_data
	@echo "Promtail and its volumes removed successfully"



### ----- OBSERVABILITY ----- ###
###############################################################################

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

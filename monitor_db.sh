#!/bin/bash

LOG_FILE="/root/ac_service/db_monitor.log"
CONTAINER_NAME="ac_service_db_1"
DB_NAME="ac_db"
DB_USER="postgres"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Check if container is running
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    log_message "ERROR: Container $CONTAINER_NAME is not running!"
    exit 1
fi

# Check if database exists
if docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    # Check if we can connect to the database
    if docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1" >/dev/null 2>&1; then
        log_message "OK: Database $DB_NAME exists and is accessible."
    else
        log_message "ERROR: Database $DB_NAME exists but is not accessible."
    fi
else
    log_message "ERROR: Database $DB_NAME DOES NOT EXIST!"
    log_message "---- Docker Volumes ----"
    docker volume ls >> "$LOG_FILE"
    log_message "---- Docker Containers ----"
    docker ps -a >> "$LOG_FILE"
    log_message "---- Last 50 lines of DB logs ----"
    docker logs "$CONTAINER_NAME" | tail -n 50 >> "$LOG_FILE"
    log_message "---- Database Size ----"
    docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -c "SELECT pg_size_pretty(pg_database_size('$DB_NAME'));" >> "$LOG_FILE"
    log_message "---- Database Connections ----"
    docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -c "SELECT count(*) FROM pg_stat_activity WHERE datname = '$DB_NAME';" >> "$LOG_FILE"
    log_message "---- End of Report ----"
    exit 1
fi 
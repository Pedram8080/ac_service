#!/bin/bash

LOG_FILE="/root/ac_service/db_monitor.log"
CONTAINER_NAME="ac_service_db_1"
DB_NAME="ac_db"
DB_USER="postgres"
MAX_RETRIES=3
RETRY_INTERVAL=5

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

check_database() {
    # Check if container is running
    if ! docker ps | grep -q "$CONTAINER_NAME"; then
        log_message "ERROR: Container $CONTAINER_NAME is not running!"
        return 1
    }

    # Check if database exists and is accessible
    for i in $(seq 1 $MAX_RETRIES); do
        if docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
            # Check if we can actually connect to the database
            if docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1" >/dev/null 2>&1; then
                log_message "OK: Database $DB_NAME exists and is accessible."
                return 0
            else
                log_message "WARNING: Database $DB_NAME exists but is not accessible. Retry $i/$MAX_RETRIES"
            fi
        else
            log_message "ERROR: Database $DB_NAME DOES NOT EXIST! Retry $i/$MAX_RETRIES"
        fi
        sleep $RETRY_INTERVAL
    done

    # If we get here, all retries failed
    log_message "CRITICAL: Database check failed after $MAX_RETRIES retries!"
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
    return 1
}

# Main execution
check_database 
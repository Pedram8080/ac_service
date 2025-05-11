#!/bin/bash

LOG_FILE="/root/ac_service/db_monitor.log"
CONTAINER_NAME="ac_service_db_1"
DB_NAME="ac_db"
DB_USER="postgres"

# بررسی وجود دیتابیس
docker exec $CONTAINER_NAME psql -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw $DB_NAME

if [ $? -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - OK: Database $DB_NAME exists." >> $LOG_FILE
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ERROR: Database $DB_NAME DOES NOT EXIST!" >> $LOG_FILE
    echo "---- Docker Volumes ----" >> $LOG_FILE
    docker volume ls >> $LOG_FILE
    echo "---- Docker Containers ----" >> $LOG_FILE
    docker ps -a >> $LOG_FILE
    echo "---- Last 50 lines of DB logs ----" >> $LOG_FILE
    docker logs $CONTAINER_NAME | tail -n 50 >> $LOG_FILE
    echo "---- End of Report ----" >> $LOG_FILE
fi 
#!/bin/bash

# تنظیمات
BACKUP_DIR="/root/ac_service/backups"
DB_NAME="ac_db"
DB_USER="postgres"
CONTAINER_NAME="ac_service-db-1"
RETENTION_DAYS=7  # تعداد روزهایی که backup ها نگهداری می‌شوند

# ایجاد دایرکتوری backup اگر وجود نداشته باشد
mkdir -p $BACKUP_DIR

# گرفتن تاریخ و زمان برای نام فایل
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"

# گرفتن backup
echo "در حال گرفتن backup از دیتابیس..."
docker exec $CONTAINER_NAME pg_dump -U $DB_USER $DB_NAME > $BACKUP_FILE

# فشرده‌سازی فایل backup
gzip $BACKUP_FILE

# حذف فایل‌های قدیمی
echo "در حال پاک کردن فایل‌های قدیمی..."
find $BACKUP_DIR -name "backup_*.sql.gz" -type f -mtime +$RETENTION_DAYS -delete

echo "Backup با موفقیت انجام شد: $BACKUP_FILE.gz" 
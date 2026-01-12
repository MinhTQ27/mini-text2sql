# mini-text2sql

docker exec -it postgres_db bash

pg_restore -U postgres --dbname=postgres --host=localhost --port=5432 --username=postgres --password --verbose /home/gnoseau/code/mini-text2sql/src/pgdata/*.tar

psql -U postgres --dbname=postgres --host=localhost --port=5432 --username=postgres --password -f /home/gnoseau/code/mini-text2sql/src/*.sql

Create a pgdata folder and place a tar file inside 

có thể làm file bash để tự động chạy service và restore dữ liệu vào postgres

có thể encapsulate mật khẩu, username trong docker compose bằng biến của bash script 

<!-- using REST api -->

<!-- Nếu muốn container postgres tự động restore dữ liệu: tạo một file bash script 

#!/bin/bash

# Đợi cho PostgreSQL khởi động trước khi chạy lệnh pg_restore
until pg_isready -U postgres; do
  echo "Waiting for PostgreSQL to become available..."
  sleep 2
done

# Phục hồi dữ liệu từ backup.tar vào database mydb
pg_restore -U postgres -d mydb /docker-entrypoint-initdb.d/backup.tar

# Giữ container chạy
tail -f /dev/null -->

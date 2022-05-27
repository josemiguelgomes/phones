#brew services restart postgresql
#sudo systemctl restart postgresql.service
#createdb -h localhost -p 5432 -U zem
psql -h localhost -p 5432 -d postgres -a -f start.sql

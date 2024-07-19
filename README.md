### FASTAPI CRUD | ENTREGABLE | CESDE | NUEVAS TECNOLOGIAS

# commands to run with docker compose

```bash
docker-compose up --build
```

#### Comandos de docker para crear la imagen y correr el contenedor de la BD por separado
```bash
cd app/database

docker build . -t database
docker run -d --name database-container -p 5432:5432 database
```
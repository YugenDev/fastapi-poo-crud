# Utiliza la imagen oficial de PostgreSQL desde Docker Hub
FROM postgres:latest

# Variables de entorno para la base de datos
ENV POSTGRES_DB TiendaJPBB
ENV POSTGRES_USER myuser
ENV POSTGRES_PASSWORD mypassword

# Copia el archivo init.sql al contenedor Docker
COPY ./init.sql /docker-entrypoint-initdb.d/

CMD [ "postgres" ]
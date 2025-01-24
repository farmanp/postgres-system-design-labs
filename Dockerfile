FROM postgres:latest

# Install PostgreSQL extensions or tools
RUN apt-get update && apt-get install -y postgresql-contrib

# Copy initial scripts
COPY init.sql /docker-entrypoint-initdb.d/

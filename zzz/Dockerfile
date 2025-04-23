# Use the official PostgreSQL image as base image
FROM postgres:latest

# Set the environment variables
ENV POSTGRES_USER='postgres'
ENV POSTGRES_PASSWORD='dfgzxcqwe45'
ENV POSTGRES_DB='postgres2'

# Copy the initialization SQL script to the container
COPY init.sql /docker-entrypoint-initdb.d/

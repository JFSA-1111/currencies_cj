FROM postgres:13.5

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
COPY init.sql /docker-entrypoint-initdb.d/
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance

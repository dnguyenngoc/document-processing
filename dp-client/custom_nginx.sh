#!/bin/bash
export DOMAIN=localhost
export BE_HOST=localhost
export BE_PORT=8081
echo $DOMAIN

if [ "${DOMAIN}" = "localhost" ]; then
    echo 'Deploy server on localhost..........'
    envsubst '$${DOMAIN} $${BE_HOST} $${BE_PORT}' < local_nginx.conf > /etc/nginx/conf.d/app.conf
else
    echo 'Deploy server on staging or prodution.........'
    envsubst '$${DOMAIN} $${BE_HOST} $${BE_PORT}' < m_nginx.conf > /etc/nginx/conf.d/app.conf
fi
exec "$@"
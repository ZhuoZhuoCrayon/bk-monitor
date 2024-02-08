#!/bin/sh

mysql -e "CREATE DATABASE `bk_monitor_saas` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
mysql -e "CREATE DATABASE `bk_monitor_api` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"

env DJANGO_CONF_MODULE="" BKAPP_DEPLOY_ENV="web" python manage.py migrate

pytest alarm_backends/tests

python manage.py test alarm_backends.tests
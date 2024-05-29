#!/bin/bash

# Chemin vers le r�pertoire de l'application Flask
APP_DIR=`pwd`

# Nom du fichier de log pour Gunicorn
LOG_FILE=$APP_DIR/gunicorn.log

start() {
    echo "Démarrage du serveur Gunicorn..."
    cd $APP_DIR
    nohup gunicorn app:app >$LOG_FILE 2>&1 &
    echo "Serveur Gunicorn démarré."
}

stop() {
    echo "Arrêt du serveur Gunicorn..."
    pkill gunicorn
    echo "Serveur Gunicorn arrêté."
}

status() {
    if pgrep -x "gunicorn" > /dev/null
    then
        echo "Le serveur Gunicorn est en cours d'exécution."
    else
        echo "Le serveur Gunicorn n'est pas en cours d'exécution."
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 2
        start
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0

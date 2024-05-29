#!/bin/bash

# V�rifier le nombre d'arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 {start|query 'SELECT statement'}"
    exit 1
fi

# Charger les valeurs du fichier de configuration
app_dir=$(grep -oP '"app_dir": "\K([^"]*)' /home/syst/CareSyncAI/conf/config.json)
db_filename=$(grep -oP '"db_filename": "\K([^"]*)' /home/syst/CareSyncAI/conf/config.json)

# Chemin complet vers le fichier de base de donn�es
db_path="$app_dir/$db_filename"

# V�rifier si la commande est "start"
if [ "$1" = "start" ]; then
    sqlite3 "$db_path"
    exit 0
fi

# V�rifier si la commande est "query"
if [ "$1" = "query" ]; then
    # V�rifier le nombre d'arguments
    if [ $# -ne 2 ]; then
        echo "Usage: $0 query 'SELECT statement'"
        exit 1
    fi

    # Ex�cuter la requ�te SQL
    sqlite3 "$db_path" "$2"
    exit 0
fi

echo "Usage: $0 {start|query 'SELECT statement'}"
exit 1

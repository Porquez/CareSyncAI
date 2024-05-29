#!/bin/bash

# Vérifier le nombre d'arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 {start|query 'SELECT statement'}"
    exit 1
fi

# Charger les valeurs du fichier de configuration
app_dir=$(grep -oP '"app_dir": "\K([^"]*)' /home/syst/CareSyncAI/conf/config.json)
db_filename=$(grep -oP '"db_filename": "\K([^"]*)' /home/syst/CareSyncAI/conf/config.json)

# Chemin complet vers le fichier de base de données
db_path="$app_dir/$db_filename"

# Vérifier si la commande est "start"
if [ "$1" = "start" ]; then
    sqlite3 "$db_path"
    exit 0
fi

# Vérifier si la commande est "query"
if [ "$1" = "query" ]; then
    # Vérifier le nombre d'arguments
    if [ $# -ne 2 ]; then
        echo "Usage: $0 query 'SELECT statement'"
        exit 1
    fi

    # Exécuter la requête SQL
    sqlite3 "$db_path" "$2"
    exit 0
fi

echo "Usage: $0 {start|query 'SELECT statement'}"
exit 1

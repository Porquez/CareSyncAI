#!/bin/bash

# V�rification des param�tres
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <nom_de_votre_application> <URL_de_votre_depot> <votre_module> <votre_domaine>"
    exit 1
fi

# Assignation des parametres des variables
app_name=$1
repo_url=$2
module_name=$3
domain=$4

# Mise a jour du système
sudo apt update
sudo apt upgrade -y

# Installation de Python et de pip
sudo apt install -y python3 python3-pip

# Clonage du dépot Git de l'application
git clone $repo_url /var/www/$app_name

# Acces au répertoire de l'application
cd /var/www/$app_name

# Installation des dépendances de l'application
pip3 install -r requirements.txt

# Installation de Gunicorn
pip3 install gunicorn

# Création du fichier de configuration Gunicorn
cat <<EOF > gunicorn_config.py
bind = '0.0.0.0:8000'
workers = 3
EOF

# Configuration de Nginx pour servir l'application
cat <<EOF > /etc/nginx/sites-available/$app_name
server {
    listen 80;
    server_name $domain;

    location / {
        proxy_pass http://localhost:8000;
        include proxy_params;
        proxy_redirect off;
    }
}
EOF

# Activation du fichier de configuration Nginx
sudo ln -s /etc/nginx/sites-available/$app_name /etc/nginx/sites-enabled/$app_name

# V�rification de la configuration Nginx
sudo nginx -t

# Redemarrage de Nginx
sudo systemctl restart nginx

# Lancement de l'application avec Gunicorn
gunicorn -c gunicorn_config.py $module_name:app

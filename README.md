# Kubernetes & Cloud Quiz

Ce projet consiste en une application web de quiz interactif portant sur les thématiques de Kubernetes et Google Cloud. L'application repose sur une architecture microservices conteneurisée et déployée sur un environnement Cloud managé.

# Architecture du Projet

L'application est décomposée en plusieurs composants clés :

Service 1 (Frontend) : Interface utilisateur du quiz développée avec Flask.

Service 2 (Backend) : Gestion des scores et des statistiques, également sous Flask.

Base de données : Instance PostgreSQL pour la persistance des données et des scores.

Ingress NGINX : Contrôleur gérant le routage et l'exposition de l'application via une IP publique statique. 

# Stack Technique

Langage Python (Flask) 
Conteneurisation Docker & Docker Hub 
Orchestration Google Kubernetes Engine (GKE) Autopilot 
Base de données PostgreSQL 
Réseau Ingress NGINX & TLS (HTTPS auto-signé) 

# Sécurité (Focus Cybersécurité)

Le déploiement intègre plusieurs couches de sécurité avancées :
Isolation réseau : Utilisation de Network Policies pour restreindre les flux entre les pods.
Gestion des accès : Mise en œuvre du contrôle d'accès basé sur les rôles (RBAC).
Confidentialité : Utilisation des Secrets Kubernetes pour le stockage des identifiants sensibles.
Intégrité : Configuration de Security Contexts au niveau des pods.

# Guide de déploiement
# Étape 1 : Préparation des images (Docker)
Construire et envoyer les images vers Docker Hub pour que le cluster puisse les récupérer.

## Service 1 :

Bash
cd service-1
docker build -t znait/service-1:v2 .
docker push znait/service-1:v2

## Service 2 :

Bash
cd ../service-2
docker build -t znait/service-2:v4 .
docker push znait/service-2:v4


# Étape 2 : Lancement de l'infrastructure
Appliquer l'ensemble des configurations Kubernetes (Deployments, Services, RBAC, Ingress, etc.).

Bash
cd k8s-configs
kubectl apply -f .


# Étape 3 : Vérification du déploiement
Vérifier que tous les Pods sont dans l'état Running.

Bash
kubectl get pods


# Étape 4 : Accès à l'application
Récupérer l'adresse IP publique via l'Ingress :

Bash
kubectl get ingress gateway


# Modes d'accès :

## Accès Direct (Internet) :

https://<34.163.218.117> (Certificat auto-signé)

## Accès Local (Proxy) :

Bash
kubectl port-forward service/service-1 5000:80
Puis ouvrir : http://localhost:5000

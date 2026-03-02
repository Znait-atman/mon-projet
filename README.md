# Kubernetes & Cloud Quiz

Ce projet consiste en une application web de **quiz interactif** portant sur les thématiques de **Kubernetes** et **Google Cloud**.  
L’application repose sur une **architecture microservices conteneurisée**, déployée sur un **environnement Cloud managé**.

Vous pouvez y accéder directement via Internet :
- http://34.163.218.117  
- https://34.163.218.117 *(certificat auto-signé)*

---

## Interface du quiz

Vous pouvez réaliser le quiz en sélectionnant la bonne réponse à chaque question.

<img width="946" height="526" alt="Interface du quiz" src="https://github.com/user-attachments/assets/46def677-fea4-4b3d-9bae-849417e8cc3b" />

---

## Affichage du score

À la fin du quiz, votre score est affiché et il vous est demandé de saisir votre nom.

<img width="942" height="502" alt="Saisie du nom" src="https://github.com/user-attachments/assets/c51c5762-6b15-4100-8658-637eed64d345" />

---

## Validation du score

Après la saisie de votre nom, cliquez sur **OK** pour valider.

<img width="938" height="491" alt="Validation du score" src="https://github.com/user-attachments/assets/5b7506c2-6b7e-4442-93bd-08d458a61452" />

---

## Confirmation de sauvegarde

Un message de confirmation s’affiche indiquant que le score a bien été sauvegardé.

<img width="958" height="480" alt="Confirmation de sauvegarde" src="https://github.com/user-attachments/assets/c8819d85-df29-4911-bbac-0670df8ed018" />

---

## Statistiques

Vous pouvez consulter vos statistiques en cliquant sur le bouton **« Voir les statistiques »**.  
Les informations suivantes sont affichées :
- Numéro de la partie  
- Score moyen  
- Meilleur score  

<img width="909" height="460" alt="Statistiques" src="https://github.com/user-attachments/assets/07865d1e-54a3-498b-a9df-ef5d6a4dec75" />

---

# Architecture du projet

L’application est décomposée en plusieurs composants clés :

- **Service 1 (Frontend)** : Interface utilisateur du quiz développée avec Flask  
- **Service 2 (Backend)** : Gestion des scores et des statistiques, également développée avec Flask  
- **Base de données** : Instance PostgreSQL assurant la persistance des données  
- **Ingress NGINX** : Contrôleur gérant le routage et l’exposition de l’application via une IP publique statique  

---

# Stack technique

- Langage : Python (Flask)  
- Conteneurisation : Docker & Docker Hub  
- Orchestration : Google Kubernetes Engine (GKE) Autopilot  
- Base de données : PostgreSQL  
- Réseau : Ingress NGINX & TLS (HTTPS auto-signé)  

---

# Sécurité 

Le déploiement intègre plusieurs couches de sécurité :

- **Isolation réseau** : Utilisation de Network Policies pour restreindre les flux entre les pods  
- **Gestion des accès** : Mise en œuvre du contrôle d’accès basé sur les rôles (RBAC)  
- **Confidentialité** : Utilisation des Secrets Kubernetes pour le stockage des identifiants sensibles  
- **Intégrité** : Configuration de Security Contexts au niveau des pods  

---

# Guide de déploiement

```

## Etape 1: Préparation des images Docker

Construire et envoyer les images vers Docker Hub afin qu’elles puissent être récupérées par le cluster.

### Service 1

```bash
cd service-1
docker build -t znait/service-1:v2 .
docker push znait/service-1:v2

### Service 2
```bash
cd ../service-2
docker build -t znait/service-2:v4 .

## Étape 2 : Lancement de l’infrastructure

Appliquer l’ensemble des configurations Kubernetes (Deployments, Services, RBAC, Ingress, etc.).

```bash
cd k8s-configs
kubectl apply -f .

## Étape 3 : Vérification du déploiement

Vérifier que tous les pods sont dans l’état **Running**.

```bash
kubectl get pods

## Étape 4: Accès à l’application

Récupérer l’adresse IP publique exposée par l’Ingress.
```bash
kubectl get ingress gateway

## Modes d’accès

### Accès direct (Internet)

- http://34.163.218.117  
- https://34.163.218.117 *(certificat auto-signé)*

### Accès local (proxy Kubernetes)

```bash
kubectl port-forward service/service-1 5000:80

Puis ouvrir dans un navigateur :
http://localhost:5000

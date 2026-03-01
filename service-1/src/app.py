from flask import Flask, render_template_string, jsonify, request
import requests
import os

app = Flask(__name__)

# Template du quiz avec CSS et JavaScript
QUIZ_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>K8S Architecture Quiz</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .quiz-container { max-width: 800px; margin: 50px auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .question { font-size: 1.2rem; margin-bottom: 20px; font-weight: 600; color: #2c3e50; }
        .option { margin-bottom: 10px; }
        .btn-option { width: 100%; text-align: left; padding: 12px; border: 2px solid #e9ecef; transition: 0.3s; }
        .btn-option:hover { border-color: #3498db; background-color: #f1f9ff; }
        .header-cloud { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; }
    </style>
</head>
<body>
    <div class="container quiz-container">
        <div class="header-cloud text-center">
            <h1>Kubernetes & Cloud Quiz</h1>
            <p id="ip-display">Chargement de l'adresse...</p>
        </div>
        
        <div id="quiz-box">
            <div class="question" id="q-text">Chargement de la question...</div>
            <div id="options-box"></div>
            <div class="mt-4 text-end">
                <span id="score-box" class="badge bg-secondary p-2">Score: 0</span>
            </div>
        </div>
    </div>

    <script>
        // Récupérer l'IP de l'ingress (affichage)
        fetch('/api/ingress-ip')
            .then(response => response.json())
            .then(data => {
                document.getElementById('ip-display').textContent = 'IP: ' + data.ip;
            });

        const questions = [
            { q: "Quel outil permet de conteneuriser une application ?", a: ["Kubernetes", "Docker", "Ingress"], c: 1 },
            { q: "Quelle ressource Kubernetes expose une application à l'extérieur du cluster ?", a: ["Deployment", "Service", "ConfigMap"], c: 1 },
            { q: "Quel objet Kubernetes gère le routage HTTP/HTTPS vers les services ?", a: ["Ingress", "LoadBalancer", "Pod"], c: 0 },
            { q: "Dans GKE, quel mode de cluster gère automatiquement les nœuds ?", a: ["Standard", "Autopilot", "Bare Metal"], c: 1 },
            { q: "Quelle ressource Kubernetes permet de stocker des informations sensibles (mots de passe) ?", a: ["ConfigMap", "Secret", "PersistentVolume"], c: 1 },
            { q: "Comment s'appelle le fichier qui décrit la construction d'une image Docker ?", a: ["dockerfile", "Dockerfile", "containerfile"], c: 1 },
            { q: "Quelle commande kubectl permet de lister les pods ?", a: ["kubectl get pods", "kubectl list pods", "kubectl show pods"], c: 0 },
            { q: "Qu'est-ce qu'un ServiceAccount dans Kubernetes ?", a: ["Un compte pour les utilisateurs humains", "Une identité pour les applications", "Un type de service"], c: 1 },
            { q: "À quoi sert une NetworkPolicy ?", a: ["À limiter le trafic réseau entre pods", "À exposer un service", "À stocker des données"], c: 0 },
            { q: "Quelle sonde Kubernetes vérifie si un conteneur est prêt à recevoir du trafic ?", a: ["livenessProbe", "readinessProbe", "startupProbe"], c: 1 }
        ];

        let currentQ = 0;
        let score = 0;

        function loadQuestion() {
            const q = questions[currentQ];
            document.getElementById('q-text').textContent = q.q;
            const box = document.getElementById('options-box');
            box.innerHTML = '';
            q.a.forEach((opt, i) => {
                const btn = document.createElement('button');
                btn.className = 'btn btn-option mb-2';
                btn.textContent = opt;
                btn.onclick = () => checkAnswer(i);
                box.appendChild(btn);
            });
        }

        function checkAnswer(i) {
            if(i === questions[currentQ].c) score++;
            currentQ++;
            if(currentQ < questions.length) {
                loadQuestion();
            } else {
                // Fin du quiz
                let playerName = prompt("Bravo ! Votre score est " + score + "/" + questions.length + ". Entrez votre nom pour enregistrer votre score :");
                if(playerName) {
                    fetch('/api/score', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({player: playerName, score: score})
                    })
                    .then(response => response.json())
                    .then(data => {
                        if(data.status === 'ok') alert('Score enregistré !');
                        else alert('Erreur : ' + data.message);
                    });
                }
                // Afficher le score final et bouton stats
                document.getElementById('quiz-box').innerHTML = `
                    <h2>Quiz terminé !</h2>
                    <p>Votre score : ${score}/${questions.length}</p>
                    <button class="btn btn-primary" onclick="showStats()">Voir les statistiques</button>
                `;
            }
            document.getElementById('score-box').textContent = `Score: ${score}`;
        }

        function showStats() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    alert(`Parties jouées : ${data.total_games}\\nScore moyen : ${data.average_score.toFixed(2)}\\nMeilleur score : ${data.max_score}`);
                });
        }

        loadQuestion();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(QUIZ_TEMPLATE)

@app.route('/health')
def health():
    return jsonify({"status": "up"}), 200

@app.route('/api/ingress-ip')
def ingress_ip():
    return jsonify({"ip": request.host.split(':')[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
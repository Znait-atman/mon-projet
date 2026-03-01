from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# Le template HTML avec CSS intégré pour un look "Pro"
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
            <p>Projet GKE - IP: 34.163.218.117</p>
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
        const questions = [
            { q: "Quel objet expose notre IP publique sur GKE ?", a: ["Ingress", "Pod", "ConfigMap"], c: 0 },
            { q: "Pourquoi Postgres crashait au début ?", a: ["Mauvais mot de passe", "Dossier lost+found de Google", "Pas assez de RAM"], c: 1 },
            { q: "Quel mode GKE gère les serveurs pour nous ?", a: ["Standard", "Autopilot", "Bare Metal"], c: 1 },
            { q: "Comment isoler la DB en Cyber ?", a: ["Secret", "NetworkPolicy", "Ingress"], c: 1 }
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
                document.getElementById('quiz-box').innerHTML = `<h2>Quiz terminé !</h2><p>Votre score final : ${score}/${questions.length}</p><button class='btn btn-primary' onclick='location.reload()'>Recommencer</button>`;
            }
            document.getElementById('score-box').textContent = `Score: ${score}`;
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
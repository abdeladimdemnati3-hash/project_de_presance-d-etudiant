import json
import re
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Count, Q
from django.utils import timezone


# ─── Serve widget.js ────────────────────────────────────────────────────────

@require_GET
def widget_js(request):
    js = r"""
(function() {
  var API_URL   = window.CHATBOX_API_URL || '/api/widget/chat';
  var TITLE     = window.CHATBOX_TITLE   || '🤖 Assistant IA';
  var COLOR     = window.CHATBOX_COLOR   || '#2563eb';

  // Inject styles
  var style = document.createElement('style');
  style.textContent = `
    #gp-chat-btn {
      position: fixed; bottom: 24px; right: 24px; z-index: 9999;
      width: 56px; height: 56px; border-radius: 50%;
      background: ${COLOR}; color: #fff; border: none;
      font-size: 24px; cursor: pointer; box-shadow: 0 4px 16px rgba(0,0,0,.25);
      display: flex; align-items: center; justify-content: center;
      transition: transform .2s;
    }
    #gp-chat-btn:hover { transform: scale(1.1); }
    #gp-chat-box {
      position: fixed; bottom: 90px; right: 24px; z-index: 9999;
      width: 340px; max-height: 500px;
      background: #fff; border-radius: 16px;
      box-shadow: 0 8px 32px rgba(0,0,0,.18);
      display: flex; flex-direction: column; overflow: hidden;
      font-family: Inter, sans-serif;
      transition: opacity .2s, transform .2s;
    }
    #gp-chat-box.gp-hidden { opacity: 0; pointer-events: none; transform: translateY(20px); }
    #gp-chat-header {
      padding: 12px 16px; background: ${COLOR}; color: #fff;
      font-weight: 600; font-size: 15px;
      display: flex; justify-content: space-between; align-items: center;
    }
    #gp-chat-header button {
      background: none; border: none; color: #fff; font-size: 20px;
      cursor: pointer; line-height: 1;
    }
    #gp-chat-messages {
      flex: 1; overflow-y: auto; padding: 12px; display: flex;
      flex-direction: column; gap: 8px; min-height: 200px;
    }
    .gp-msg {
      max-width: 80%; padding: 8px 12px; border-radius: 12px;
      font-size: 13px; line-height: 1.45; word-break: break-word;
    }
    .gp-msg.gp-bot { background: #f0f4ff; color: #1e293b; align-self: flex-start; }
    .gp-msg.gp-user { background: ${COLOR}; color: #fff; align-self: flex-end; }
    .gp-typing { display: flex; gap: 4px; align-items: center; padding: 8px 12px; }
    .gp-typing span {
      width: 7px; height: 7px; border-radius: 50%; background: #94a3b8;
      animation: gp-bounce .9s infinite;
    }
    .gp-typing span:nth-child(2) { animation-delay: .15s; }
    .gp-typing span:nth-child(3) { animation-delay: .3s; }
    @keyframes gp-bounce {
      0%,80%,100% { transform: translateY(0); }
      40% { transform: translateY(-6px); }
    }
    #gp-chat-input-row {
      padding: 10px 12px; border-top: 1px solid #e2e8f0;
      display: flex; gap: 8px;
    }
    #gp-chat-input {
      flex: 1; border: 1px solid #cbd5e1; border-radius: 8px;
      padding: 8px 10px; font-size: 13px; outline: none;
      font-family: inherit;
    }
    #gp-chat-input:focus { border-color: ${COLOR}; }
    #gp-chat-send {
      background: ${COLOR}; color: #fff; border: none; border-radius: 8px;
      padding: 8px 14px; cursor: pointer; font-size: 13px;
    }
    #gp-chat-send:disabled { opacity: .6; cursor: not-allowed; }
  `;
  document.head.appendChild(style);

  // Build DOM
  var btn = document.createElement('button');
  btn.id = 'gp-chat-btn';
  btn.innerHTML = '&#129302;';
  btn.title = 'Assistant IA';
  document.body.appendChild(btn);

  var box = document.createElement('div');
  box.id = 'gp-chat-box';
  box.classList.add('gp-hidden');
  box.innerHTML = `
    <div id="gp-chat-header">
      <span>${TITLE}</span>
      <button id="gp-chat-close" title="Fermer">&times;</button>
    </div>
    <div id="gp-chat-messages">
      <div class="gp-msg gp-bot">Bonjour ! Je suis l'assistant du système GesPresence. Comment puis-je vous aider ?</div>
    </div>
    <div id="gp-chat-input-row">
      <input id="gp-chat-input" type="text" placeholder="Posez votre question..." autocomplete="off">
      <button id="gp-chat-send">Envoyer</button>
    </div>
  `;
  document.body.appendChild(box);

  var messages  = box.querySelector('#gp-chat-messages');
  var input     = box.querySelector('#gp-chat-input');
  var sendBtn   = box.querySelector('#gp-chat-send');
  var closeBtn  = box.querySelector('#gp-chat-close');

  btn.addEventListener('click', function() { box.classList.toggle('gp-hidden'); if (!box.classList.contains('gp-hidden')) input.focus(); });
  closeBtn.addEventListener('click', function() { box.classList.add('gp-hidden'); });

  function appendMsg(text, who) {
    var div = document.createElement('div');
    div.className = 'gp-msg gp-' + who;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
  }

  function showTyping() {
    var d = document.createElement('div');
    d.className = 'gp-msg gp-bot gp-typing';
    d.innerHTML = '<span></span><span></span><span></span>';
    messages.appendChild(d);
    messages.scrollTop = messages.scrollHeight;
    return d;
  }

  // Get CSRF token from cookie
  function getCsrf() {
    var m = document.cookie.match(/csrftoken=([^;]+)/);
    return m ? m[1] : '';
  }

  function send() {
    var text = input.value.trim();
    if (!text) return;
    appendMsg(text, 'user');
    input.value = '';
    sendBtn.disabled = true;
    var typing = showTyping();
    fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
      body: JSON.stringify({ message: text })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      typing.remove();
      appendMsg(data.reply || "Désolé, je n'ai pas compris.", 'bot');
    })
    .catch(function() {
      typing.remove();
      appendMsg("Erreur de connexion avec le serveur.", 'bot');
    })
    .finally(function() { sendBtn.disabled = false; input.focus(); });
  }

  sendBtn.addEventListener('click', send);
  input.addEventListener('keydown', function(e) { if (e.key === 'Enter') send(); });
})();
"""
    return HttpResponse(js, content_type='application/javascript')


# ─── Chat API ────────────────────────────────────────────────────────────────

@csrf_exempt
@require_POST
def chat_api(request):
    try:
        body = json.loads(request.body)
        message = (body.get('message') or '').strip()
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not message:
        return JsonResponse({'reply': "Veuillez écrire un message."})

    reply = _get_reply(message, request)
    return JsonResponse({'reply': reply})


# ─── Simple context-aware AI engine ─────────────────────────────────────────

def _get_reply(message: str, request) -> str:
    msg = message.lower()

    # Greetings
    if re.search(r'\b(bonjour|salut|hello|bonsoir|hi)\b', msg):
        return "Bonjour ! Je suis l'assistant IA de GesPresence. Je peux vous aider avec les présences, les étudiants, les cours et les statistiques."

    # Help / capabilities
    if re.search(r'\b(aide|help|que (peux|sais)-tu|fonctions|capacités)\b', msg):
        return (
            "Je peux vous aider avec :\n"
            "• Statistiques de présence (absences, retards, taux)\n"
            "• Informations sur les étudiants et groupes\n"
            "• Informations sur les cours et sessions\n"
            "• Questions sur les enseignants\n\n"
            "Exemples : « Combien d'absences aujourd'hui ? », « Quel est le taux de présence ? »"
        )

    # Absence stats
    if re.search(r'\babsence(s)?\b', msg):
        return _absences_stats(msg)

    # Presence / attendance rate
    if re.search(r'\b(présence|presence|taux|statistique|stat)\b', msg):
        return _presence_stats(msg)

    # Retard / late
    if re.search(r'\bretard(s)?\b', msg):
        return _retard_stats()

    # Students
    if re.search(r'\b(étudiant|etudiants?|élève|inscription)\b', msg):
        return _student_stats()

    # Courses
    if re.search(r'\b(cours|matière|module|session)\b', msg):
        return _cours_stats()

    # Teachers
    if re.search(r'\b(enseignant|professeur|prof)\b', msg):
        return _enseignant_stats()

    # Today
    if re.search(r'\b(aujourd\'hui|ce jour|journée)\b', msg):
        return _today_stats()

    # Goodbye
    if re.search(r'\b(au revoir|bye|merci|à bientôt)\b', msg):
        return "Au revoir ! N'hésitez pas à revenir si vous avez d'autres questions. 👋"

    # Fallback
    return (
        "Je n'ai pas bien compris votre question. "
        "Vous pouvez me poser des questions sur les absences, présences, "
        "étudiants, cours ou enseignants. Tapez « aide » pour en savoir plus."
    )


def _absences_stats(msg: str) -> str:
    try:
        from presences.models import Presence
        total_absences = Presence.objects.filter(statut='absent').count()
        total_justifie = Presence.objects.filter(statut='justifie').count()

        if re.search(r"\baujourd'?hui\b|\bce jour\b", msg):
            today = timezone.localdate()
            count = Presence.objects.filter(statut='absent', session__date_session=today).count()
            return f"Aujourd'hui, il y a {count} absence(s) enregistrée(s)."

        return (
            f"📊 Statistiques des absences :\n"
            f"• Total absences : {total_absences}\n"
            f"• Dont justifiées : {total_justifie}\n"
            f"• Non justifiées : {total_absences - total_justifie}"
        )
    except Exception:
        return "Impossible de récupérer les données d'absences pour le moment."


def _presence_stats(msg: str) -> str:
    try:
        from presences.models import Presence
        total = Presence.objects.count()
        presents = Presence.objects.filter(statut='present').count()
        rate = round(presents / total * 100, 1) if total > 0 else 0
        return (
            f"📈 Statistiques de présence :\n"
            f"• Total relevés : {total}\n"
            f"• Présents : {presents}\n"
            f"• Taux de présence global : {rate} %"
        )
    except Exception:
        return "Impossible de récupérer les statistiques de présence."


def _retard_stats() -> str:
    try:
        from presences.models import Presence
        count = Presence.objects.filter(statut='retard').count()
        return f"⏰ Nombre total de retards enregistrés : {count}"
    except Exception:
        return "Impossible de récupérer les données de retard."


def _student_stats() -> str:
    try:
        from accounts.models import Utilisateur, Etudiant
        count = Utilisateur.objects.filter(role='etudiant').count()
        return f"🎓 Nombre total d'étudiants inscrits : {count}"
    except Exception:
        return "Impossible de récupérer les informations sur les étudiants."


def _cours_stats() -> str:
    try:
        from cours.models import Cours, SessionCours
        nb_cours = Cours.objects.count()
        nb_sessions = SessionCours.objects.count()
        return (
            f"📚 Informations sur les cours :\n"
            f"• Nombre de cours/matières : {nb_cours}\n"
            f"• Nombre de sessions planifiées : {nb_sessions}"
        )
    except Exception:
        return "Impossible de récupérer les informations sur les cours."


def _enseignant_stats() -> str:
    try:
        from accounts.models import Utilisateur
        count = Utilisateur.objects.filter(role='enseignant').count()
        return f"👨‍🏫 Nombre total d'enseignants : {count}"
    except Exception:
        return "Impossible de récupérer les informations sur les enseignants."


def _today_stats() -> str:
    try:
        from presences.models import Presence
        from cours.models import SessionCours
        today = timezone.localdate()
        sessions = SessionCours.objects.filter(date_session=today).count()
        absences = Presence.objects.filter(statut='absent', session__date_session=today).count()
        presents = Presence.objects.filter(statut='present', session__date_session=today).count()
        return (
            f"📅 Aujourd'hui ({today.strftime('%d/%m/%Y')}) :\n"
            f"• Sessions planifiées : {sessions}\n"
            f"• Présents : {presents}\n"
            f"• Absents : {absences}"
        )
    except Exception:
        return "Impossible de récupérer les données d'aujourd'hui."

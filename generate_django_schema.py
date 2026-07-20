"""
Génère un PDF illustrant l'architecture Django (schéma détaillé en français).
Usage : python generate_django_schema.py
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

# ──────────────────────────────────────────────────────────────────
# Palette de couleurs
# ──────────────────────────────────────────────────────────────────
C_BG         = colors.HexColor("#0D1117")   # fond page
C_TITLE      = colors.HexColor("#58A6FF")   # titres bleu clair
C_SUBTITLE   = colors.HexColor("#3FB950")   # sous-titres vert
C_ARROW      = colors.HexColor("#F0883E")   # flèches orange
C_BOX_URL    = colors.HexColor("#1F6FEB")
C_BOX_VIEW   = colors.HexColor("#2EA043")
C_BOX_MODEL  = colors.HexColor("#8957E5")
C_BOX_TMPL   = colors.HexColor("#DB6D28")
C_BOX_ADMIN  = colors.HexColor("#C74B50")
C_BOX_DB     = colors.HexColor("#388BFD")
C_BOX_MIDD   = colors.HexColor("#6E7681")
C_BOX_STATIC = colors.HexColor("#A371F7")
C_BOX_FORMS  = colors.HexColor("#3FB950")
C_TEXT_LIGHT = colors.HexColor("#E6EDF3")
C_TEXT_DARK  = colors.HexColor("#0D1117")
C_NOTE       = colors.HexColor("#161B22")
C_NOTE_BDR   = colors.HexColor("#30363D")
C_CYCLE_BG   = colors.HexColor("#161B22")

PAGE_W, PAGE_H = A4  # 595 × 842 pts


# ──────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────
def draw_rounded_box(c, x, y, w, h, fill, stroke, text_lines,
                     radius=6, text_color=None, font="Helvetica-Bold",
                     font_size=9, padding=6):
    """Boîte arrondie avec texte multi-ligne centré."""
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(1.5)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    c.setFillColor(text_color or C_TEXT_LIGHT)
    c.setFont(font, font_size)
    line_h = font_size + 2
    total = len(text_lines) * line_h
    start_y = y + h / 2 + total / 2 - font_size
    for line in text_lines:
        c.drawCentredString(x + w / 2, start_y, line)
        start_y -= line_h


def arrow(c, x1, y1, x2, y2, label="", color=None, lw=1.8):
    """Flèche simple avec étiquette optionnelle."""
    import math
    col = color or C_ARROW
    c.setStrokeColor(col)
    c.setFillColor(col)
    c.setLineWidth(lw)
    c.line(x1, y1, x2, y2)
    # Pointe (triangle rempli)
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 7
    px = x2 - size * math.cos(ang)
    py = y2 - size * math.sin(ang)
    lx = px + size / 2 * math.sin(ang)
    ly = py - size / 2 * math.cos(ang)
    rx = px - size / 2 * math.sin(ang)
    ry = py + size / 2 * math.cos(ang)
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(lx, ly)
    p.lineTo(rx, ry)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    if label:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        c.setFont("Helvetica-Oblique", 7)
        c.setFillColor(C_ARROW)
        c.drawCentredString(mid_x, mid_y + 4, label)


def section_title(c, x, y, text, color=None):
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(color or C_TITLE)
    c.drawString(x, y, text)


def note_box(c, x, y, w, h, lines, font_size=8):
    c.setFillColor(C_NOTE)
    c.setStrokeColor(C_NOTE_BDR)
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, 4, fill=1, stroke=1)
    c.setFillColor(C_TEXT_LIGHT)
    c.setFont("Helvetica", font_size)
    ly = y + h - font_size - 4
    for line in lines:
        c.drawString(x + 6, ly, line)
        ly -= (font_size + 3)


# ──────────────────────────────────────────────────────────────────
# PAGE 1 – Architecture MVT + cycle requête/réponse
# ──────────────────────────────────────────────────────────────────
def page1(c):
    c.setFillColor(C_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # ── Titre principal ──────────────────────────────────────────
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(C_TITLE)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 38, "Architecture Django — Schéma Détaillé")
    c.setFont("Helvetica", 10)
    c.setFillColor(C_SUBTITLE)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 55, "Modèle MVT (Model – View – Template) | Page 1/2")

    # ── Ligne de séparation ──────────────────────────────────────
    c.setStrokeColor(C_TITLE)
    c.setLineWidth(1)
    c.line(30, PAGE_H - 62, PAGE_W - 30, PAGE_H - 62)

    # ──────────────────────────────────────────────────────────────
    # SECTION A : Cycle Requête → Réponse
    # ──────────────────────────────────────────────────────────────
    section_title(c, 30, PAGE_H - 80, "① Cycle Requête / Réponse")

    # Fond de la zone cycle
    cycle_y = PAGE_H - 280
    c.setFillColor(C_CYCLE_BG)
    c.setStrokeColor(C_NOTE_BDR)
    c.setLineWidth(1)
    c.roundRect(20, cycle_y, PAGE_W - 40, 185, 8, fill=1, stroke=1)

    BW, BH = 92, 42   # taille des boîtes

    # Boîtes du cycle
    boxes = [
        (32,  cycle_y + 70, C_BOX_MIDD,  ["Navigateur",  "/ Client"],     C_BOX_MIDD),
        (142, cycle_y + 70, C_BOX_MIDD,  ["Middleware",  "(Request)"],     C_NOTE_BDR),
        (252, cycle_y + 70, C_BOX_URL,   ["urls.py",     "URLConf"],       C_BOX_URL),
        (362, cycle_y + 70, C_BOX_VIEW,  ["views.py",    "Vue (View)"],    C_BOX_VIEW),
        (472, cycle_y + 70, C_BOX_MODEL, ["models.py",   "Modèle (ORM)"],  C_BOX_MODEL),
    ]

    for bx, by, fill, lines, stroke in boxes:
        draw_rounded_box(c, bx, by, BW, BH, fill, stroke, lines)

    # Flèches aller (haut)
    step = 110
    for i in range(4):
        x1 = 32 + i * step + BW
        y1 = cycle_y + 70 + BH / 2
        arrow(c, x1, y1, x1 + step - BW, y1)

    # Base de données (sous les modèles)
    db_x, db_y = 452, cycle_y + 5
    draw_rounded_box(c, db_x, db_y, 112, 40, C_BOX_DB, C_BOX_DB,
                     ["Base de données", "(PostgreSQL/MySQL/SQLite)"], font_size=7.5)
    arrow(c, db_x + 56, cycle_y + 70, db_x + 56, db_y + 40, label="ORM")

    # Template (au-dessus des vues)
    tmpl_x, tmpl_y = 342, cycle_y + 135
    draw_rounded_box(c, tmpl_x, tmpl_y, 112, 38, C_BOX_TMPL, C_BOX_TMPL,
                     ["templates/", "Template HTML"], font_size=8)
    arrow(c, 408, cycle_y + 70 + BH, 408, tmpl_y, label="render()")

    # Retour middleware → navigateur
    c.setStrokeColor(C_ARROW)
    c.setLineWidth(1.5)
    ret_y = cycle_y + 25
    c.line(32 + BW / 2, cycle_y + 70, 32 + BW / 2, ret_y)
    c.line(32 + BW / 2, ret_y, 32 + 4 * step + BW / 2, ret_y)
    c.line(32 + 4 * step + BW / 2, ret_y, 32 + 4 * step + BW / 2, cycle_y + 70)
    # Pointe retour
    arrow(c, 32 + BW / 2 + 2, ret_y, 32 + BW / 2, ret_y + 5,
          color=C_ARROW, lw=0)
    c.setFont("Helvetica-Oblique", 7.5)
    c.setFillColor(C_ARROW)
    c.drawCentredString(PAGE_W / 2 - 20, ret_y - 10, "← Réponse HTTP (HttpResponse / JSON / HTML)")

    # Légende middleware retour
    draw_rounded_box(c, 142, cycle_y + 135, 92, 38, C_BOX_MIDD, C_NOTE_BDR,
                     ["Middleware", "(Response)"], font_size=8)
    arrow(c, 188, cycle_y + 70, 188, cycle_y + 135, label="")

    # ──────────────────────────────────────────────────────────────
    # SECTION B : Les 5 composants clés
    # ──────────────────────────────────────────────────────────────
    section_title(c, 30, cycle_y - 18, "② Les Composants Clés de Django")

    comp_y   = cycle_y - 185
    comp_w   = 100
    comp_h   = 120
    gap      = 13
    total_w  = 5 * comp_w + 4 * gap
    start_x  = (PAGE_W - total_w) / 2

    components = [
        (C_BOX_URL,   "urls.py",     [
            "• URLconf",
            "• Routage des URL",
            "• Associe URL → Vue",
            "• path() / re_path()",
            "• include() pour",
            "  sous-modules",
        ]),
        (C_BOX_VIEW,  "views.py",    [
            "• Logique métier",
            "• FBV ou CBV",
            "• Récupère données",
            "• Retourne réponse",
            "• render() / redirect()",
            "• JsonResponse()",
        ]),
        (C_BOX_MODEL, "models.py",   [
            "• Définit les tables",
            "• ORM (QuerySet)",
            "• Héritage models.Model",
            "• Champs : CharField,",
            "  IntegerField…",
            "• Migrations auto",
        ]),
        (C_BOX_TMPL,  "templates/",  [
            "• Fichiers HTML",
            "• Moteur Jinja2-like",
            "• {{ variable }}",
            "• {% tag %}",
            "• Héritage templates",
            "• {% block %} / extends",
        ]),
        (C_BOX_ADMIN, "admin.py",    [
            "• Interface /admin/",
            "• CRUD automatique",
            "• register(Model)",
            "• Personnalisable",
            "• Filtres & recherche",
            "• Actions groupées",
        ]),
    ]

    for i, (color, title, lines) in enumerate(components):
        cx = start_x + i * (comp_w + gap)
        cy = comp_y

        # Boîte principale
        c.setFillColor(color)
        c.setStrokeColor(color)
        c.setLineWidth(1.5)
        c.roundRect(cx, cy, comp_w, comp_h, 6, fill=1, stroke=1)

        # En-tête
        c.setFillColor(C_TEXT_LIGHT)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawCentredString(cx + comp_w / 2, cy + comp_h - 16, title)

        # Ligne séparatrice
        c.setStrokeColor(colors.white)
        c.setLineWidth(0.5)
        c.line(cx + 4, cy + comp_h - 21, cx + comp_w - 4, cy + comp_h - 21)

        # Lignes de texte
        c.setFont("Helvetica", 7.5)
        c.setFillColor(C_TEXT_LIGHT)
        ty = cy + comp_h - 33
        for line in lines:
            c.drawString(cx + 6, ty, line)
            ty -= 12.5

    # ──────────────────────────────────────────────────────────────
    # SECTION C : Structure d'un projet Django
    # ──────────────────────────────────────────────────────────────
    struct_y = comp_y - 22
    section_title(c, 30, struct_y, "③ Structure d'un Projet Django")

    struct_lines = [
        "mon_projet/",
        "  manage.py          ← Commandes (runserver, migrate, createsuperuser…)",
        "  mon_projet/        ← Dossier de configuration principal",
        "    settings.py      ← Config : BDD, apps, middleware, static…",
        "    urls.py          ← URL racine du projet",
        "    wsgi.py / asgi.py← Point d'entrée serveur (WSGI/ASGI)",
        "  mon_app/           ← Application métier (ex: comptes, articles)",
        "    models.py        ← Modèles de données",
        "    views.py         ← Logique de traitement",
        "    urls.py          ← URL de l'application",
        "    admin.py         ← Enregistrement admin",
        "    migrations/      ← Historique des changements BDD",
        "    templates/       ← Fichiers HTML",
        "    static/          ← CSS, JS, images",
    ]

    note_box(c, 20, struct_y - 14 - len(struct_lines) * 12 - 6,
             PAGE_W - 40, len(struct_lines) * 12 + 16,
             struct_lines, font_size=8)

    # ── Pied de page ──────────────────────────────────────────────
    c.setStrokeColor(C_NOTE_BDR)
    c.setLineWidth(0.5)
    c.line(30, 18, PAGE_W - 30, 18)
    c.setFont("Helvetica-Oblique", 7.5)
    c.setFillColor(C_BOX_MIDD)
    c.drawCentredString(PAGE_W / 2, 8, "Django Framework — Résumé Schématique  |  Page 1 / 2")


# ──────────────────────────────────────────────────────────────────
# PAGE 2 – ORM, Middleware, Forms, Static, Settings, Commandes
# ──────────────────────────────────────────────────────────────────
def page2(c):
    c.setFillColor(C_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(C_TITLE)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 35, "Django — Concepts Avancés & Outils")
    c.setFont("Helvetica", 10)
    c.setFillColor(C_SUBTITLE)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 52, "ORM · Middleware · Formulaires · Signaux · Commandes  |  Page 2/2")
    c.setStrokeColor(C_TITLE)
    c.setLineWidth(1)
    c.line(30, PAGE_H - 60, PAGE_W - 60, PAGE_H - 60)

    # ──────────────────────────────────────────────────────────────
    # SECTION D : ORM détaillé
    # ──────────────────────────────────────────────────────────────
    orm_y = PAGE_H - 78
    section_title(c, 30, orm_y, "④ L'ORM Django (Object-Relational Mapping)")

    orm_blocks = [
        (30,  orm_y - 130, C_BOX_MODEL, "Définir un Modèle", [
            "class Article(models.Model):",
            "    titre = models.CharField(max_length=200)",
            "    contenu = models.TextField()",
            "    date = models.DateTimeField(auto_now_add=True)",
            "    auteur = models.ForeignKey(",
            "        User, on_delete=models.CASCADE)",
            "",
            "Champs courants :",
            "  CharField, TextField, IntegerField",
            "  DateField, BooleanField, ImageField",
            "  ForeignKey, ManyToManyField, OneToOneField",
        ]),
        (210, orm_y - 130, C_BOX_DB, "QuerySet (Lecture)", [
            "# Tous les objets",
            "Article.objects.all()",
            "",
            "# Filtrage",
            "Article.objects.filter(auteur=user)",
            "Article.objects.exclude(publie=False)",
            "",
            "# Un seul objet",
            "Article.objects.get(pk=1)",
            "",
            "# Tri & limite",
            "Article.objects.order_by('-date')[:5]",
        ]),
        (390, orm_y - 130, C_BOX_MIDD, "Écriture & Migrations", [
            "# Créer",
            "a = Article(titre='Hello')",
            "a.save()   # ou Article.objects.create(…)",
            "",
            "# Modifier",
            "a.titre = 'Nouveau titre'",
            "a.save()",
            "",
            "# Supprimer",
            "a.delete()",
            "",
            "Migrations :",
            "  makemigrations → migrate",
        ]),
    ]

    for bx, by, color, title, lines in orm_blocks:
        bw, bh = 165, 125
        c.setFillColor(C_NOTE)
        c.setStrokeColor(color)
        c.setLineWidth(2)
        c.roundRect(bx, by, bw, bh, 6, fill=1, stroke=1)
        # titre bloc
        c.setFillColor(color)
        c.roundRect(bx, by + bh - 20, bw, 20, 6, fill=1, stroke=0)
        c.setFillColor(C_TEXT_LIGHT)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(bx + bw / 2, by + bh - 13, title)
        # contenu
        c.setFont("Courier", 7.2)
        c.setFillColor(C_TEXT_LIGHT)
        ty = by + bh - 30
        for line in lines:
            c.drawString(bx + 6, ty, line)
            ty -= 9.5

    # ──────────────────────────────────────────────────────────────
    # SECTION E : Middleware, Forms, Signaux (3 colonnes)
    # ──────────────────────────────────────────────────────────────
    mid_y = orm_y - 148
    section_title(c, 30, mid_y, "⑤ Middleware · Formulaires · Signaux")

    col_blocks = [
        (30,  mid_y - 120, C_BOX_MIDD, "Middleware", [
            "Couche entre requête et vue.",
            "",
            "Ordre d'exécution :",
            "  Requête  → du haut vers le bas",
            "  Réponse  ← du bas vers le haut",
            "",
            "Middlewares courants :",
            "• SecurityMiddleware",
            "• SessionMiddleware",
            "• AuthenticationMiddleware",
            "• CsrfViewMiddleware",
            "• MessageMiddleware",
        ]),
        (210, mid_y - 120, C_BOX_FORMS, "Formulaires (forms.py)", [
            "class LoginForm(forms.Form):",
            "    email = forms.EmailField()",
            "    password = forms.CharField(",
            "        widget=forms.PasswordInput)",
            "",
            "ModelForm (auto depuis modèle) :",
            "class ArticleForm(forms.ModelForm):",
            "    class Meta:",
            "        model = Article",
            "        fields = ['titre','contenu']",
            "",
            "Validation : form.is_valid()",
            "Données : form.cleaned_data",
        ]),
        (390, mid_y - 120, C_BOX_STATIC, "Signaux (signals.py)", [
            "Réagir à des événements.",
            "",
            "Exemple post_save :",
            "@receiver(post_save,",
            "          sender=User)",
            "def on_user_created(sender,",
            "        instance, created, **kw):",
            "    if created:",
            "        send_welcome_email(instance)",
            "",
            "Signaux Django :",
            "• pre_save / post_save",
            "• pre_delete / post_delete",
            "• m2m_changed",
        ]),
    ]

    for bx, by, color, title, lines in col_blocks:
        bw, bh = 165, 115
        c.setFillColor(C_NOTE)
        c.setStrokeColor(color)
        c.setLineWidth(2)
        c.roundRect(bx, by, bw, bh, 6, fill=1, stroke=1)
        c.setFillColor(color)
        c.roundRect(bx, by + bh - 20, bw, 20, 6, fill=1, stroke=0)
        c.setFillColor(C_TEXT_LIGHT)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(bx + bw / 2, by + bh - 13, title)
        c.setFont("Courier", 7.2)
        c.setFillColor(C_TEXT_LIGHT)
        ty = by + bh - 30
        for line in lines:
            c.drawString(bx + 6, ty, line)
            ty -= 9.5

    # ──────────────────────────────────────────────────────────────
    # SECTION F : Settings, Static & Commandes manage.py
    # ──────────────────────────────────────────────────────────────
    bot_y = mid_y - 152
    section_title(c, 30, bot_y, "⑥ settings.py · Fichiers Statiques · Commandes manage.py")

    # settings
    c.setFillColor(C_NOTE)
    c.setStrokeColor(C_BOX_ADMIN)
    c.setLineWidth(2)
    c.roundRect(30, bot_y - 105, 170, 100, 6, fill=1, stroke=1)
    c.setFillColor(C_BOX_ADMIN)
    c.roundRect(30, bot_y - 5 - 20, 170, 20, 6, fill=1, stroke=0)
    c.setFillColor(C_TEXT_LIGHT)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(115, bot_y - 13, "settings.py — Configuration")
    settings_lines = [
        "INSTALLED_APPS  → apps activées",
        "DATABASES       → connexion BDD",
        "MIDDLEWARE      → liste middlewares",
        "TEMPLATES       → moteur templates",
        "STATIC_URL      → chemin statiques",
        "MEDIA_ROOT      → fichiers uploadés",
        "AUTH_USER_MODEL → modèle utilisateur",
        "SECRET_KEY      → clé cryptographique",
        "DEBUG           → mode développement",
    ]
    c.setFont("Helvetica", 7.5)
    c.setFillColor(C_TEXT_LIGHT)
    ty = bot_y - 32
    for line in settings_lines:
        c.drawString(36, ty, line)
        ty -= 9.5

    # static
    c.setFillColor(C_NOTE)
    c.setStrokeColor(C_BOX_STATIC)
    c.setLineWidth(2)
    c.roundRect(210, bot_y - 105, 165, 100, 6, fill=1, stroke=1)
    c.setFillColor(C_BOX_STATIC)
    c.roundRect(210, bot_y - 5 - 20, 165, 20, 6, fill=1, stroke=0)
    c.setFillColor(C_TEXT_LIGHT)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(292, bot_y - 13, "Fichiers Statiques & Médias")
    static_lines = [
        "static/   → CSS, JS, images du projet",
        "media/    → fichiers uploadés par users",
        "",
        "settings.py :",
        "  STATIC_URL  = '/static/'",
        "  MEDIA_URL   = '/media/'",
        "  MEDIA_ROOT  = BASE_DIR / 'media'",
        "",
        "collectstatic → prod (WhiteNoise/nginx)",
        "{% load static %} dans templates",
    ]
    c.setFont("Helvetica", 7.5)
    c.setFillColor(C_TEXT_LIGHT)
    ty = bot_y - 32
    for line in static_lines:
        c.drawString(216, ty, line)
        ty -= 9.5

    # manage.py commandes
    c.setFillColor(C_NOTE)
    c.setStrokeColor(C_SUBTITLE)
    c.setLineWidth(2)
    c.roundRect(385, bot_y - 105, 170, 100, 6, fill=1, stroke=1)
    c.setFillColor(C_SUBTITLE)
    c.roundRect(385, bot_y - 5 - 20, 170, 20, 6, fill=1, stroke=0)
    c.setFillColor(C_TEXT_DARK)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(470, bot_y - 13, "Commandes manage.py")
    cmd_lines = [
        "runserver      → lancer le serveur",
        "makemigrations → créer migrations",
        "migrate        → appliquer migrations",
        "createsuperuser→ admin compte",
        "shell          → console Python",
        "collectstatic  → regrouper statiques",
        "startapp <nom> → nouvelle app",
        "test           → lancer les tests",
        "dbshell        → console base données",
    ]
    c.setFont("Courier", 7.2)
    c.setFillColor(C_TEXT_LIGHT)
    ty = bot_y - 32
    for line in cmd_lines:
        c.drawString(391, ty, line)
        ty -= 9.5

    # ──────────────────────────────────────────────────────────────
    # SECTION G : Authentification & Sécurité
    # ──────────────────────────────────────────────────────────────
    auth_y = bot_y - 120
    section_title(c, 30, auth_y, "⑦ Authentification · Sécurité intégrée")

    auth_items = [
        ("Authentification", C_BOX_URL, [
            "• login() / logout() / authenticate()",
            "• @login_required (décorateur)",
            "• LoginView, LogoutView (CBV)",
            "• Permission : @permission_required",
            "• Groupes & permissions par modèle",
        ]),
        ("Protection CSRF", C_BOX_ADMIN, [
            "• Token auto dans les formulaires",
            "• {% csrf_token %} dans HTML",
            "• Middleware CsrfViewMiddleware",
            "• @csrf_exempt si API externe",
            "• Protection XSS via échappement auto",
        ]),
        ("Sessions & Cookies", C_BOX_VIEW, [
            "• request.session[clé] = valeur",
            "• Stockage : BDD / Cache / Cookie",
            "• SESSION_COOKIE_AGE (durée)",
            "• SESSION_COOKIE_SECURE (HTTPS)",
            "• Hashage mdp : PBKDF2 par défaut",
        ]),
    ]

    for i, (title, color, lines) in enumerate(auth_items):
        ax = 30 + i * 185
        ay = auth_y - 90
        aw, ah = 175, 85
        c.setFillColor(C_NOTE)
        c.setStrokeColor(color)
        c.setLineWidth(2)
        c.roundRect(ax, ay, aw, ah, 6, fill=1, stroke=1)
        c.setFillColor(color)
        c.roundRect(ax, ay + ah - 18, aw, 18, 6, fill=1, stroke=0)
        c.setFillColor(C_TEXT_LIGHT)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(ax + aw / 2, ay + ah - 11, title)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(C_TEXT_LIGHT)
        ty = ay + ah - 29
        for line in lines:
            c.drawString(ax + 6, ty, line)
            ty -= 11

    # ── Pied de page ──────────────────────────────────────────────
    c.setStrokeColor(C_NOTE_BDR)
    c.setLineWidth(0.5)
    c.line(30, 18, PAGE_W - 30, 18)
    c.setFont("Helvetica-Oblique", 7.5)
    c.setFillColor(C_BOX_MIDD)
    c.drawCentredString(PAGE_W / 2, 8, "Django Framework — Résumé Schématique  |  Page 2 / 2")


# ──────────────────────────────────────────────────────────────────
# Génération du PDF
# ──────────────────────────────────────────────────────────────────
def generate():
    output = "django_schema_fr.pdf"
    c = canvas.Canvas(output, pagesize=A4)
    c.setTitle("Architecture Django — Schéma Détaillé (FR)")
    c.setAuthor("Django Schema Generator")
    c.setSubject("Résumé schématique du framework Django")

    page1(c)
    c.showPage()
    page2(c)
    c.showPage()
    c.save()
    print(f"✓  PDF généré : {output}")


if __name__ == "__main__":
    generate()

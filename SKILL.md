---
name: glasscode
description: Analyse la qualité et la sécurité d'un code source (multi-langage via Semgrep) et affiche un rapport visuel coloré directement dans la console, avec tableau des problèmes classés par sévérité, score global et recommandations de correction. Utilise ce skill dès que l'utilisateur demande un audit de code, une review de sécurité, une analyse de vulnérabilités, un check de qualité, ou mentionne des mots comme "scan", "audit", "vulnérabilités", "code smell", même sans demander explicitement un "rapport".
---

# GlassCode — Audit de qualité & sécurité

Skill pour scanner un repo ou un dossier de code, détecter les failles de sécurité et les problèmes de qualité, et présenter le tout sous forme de rapport visuel dans le terminal — comme si le code devenait transparent.

## Pré-requis

Avant la première utilisation, vérifie que `semgrep` est installé :

```bash
semgrep --version || pip install semgrep --break-system-packages
```

Vérifie aussi que `rich` (Python) est disponible pour le rendu visuel :

```bash
python3 -c "import rich" || pip install rich --break-system-packages
```

## Workflow

Quand l'utilisateur demande un audit de code :

### 1. Lancer le scan

Exécute Semgrep sur le chemin cible avec les règles de sécurité et de qualité par défaut (multi-langage, auto-détection) :

```bash
semgrep --config=auto --json --quiet -o /tmp/semgrep_results.json <chemin_du_code>
```

Si l'utilisateur veut un focus précis, utilise des configs ciblées :
- Sécurité uniquement : `--config=p/security-audit`
- OWASP Top 10 : `--config=p/owasp-top-ten`
- Secrets exposés (clés API, tokens) : `--config=p/secrets`

### 2. Parser et classer les résultats

Lis `/tmp/semgrep_results.json` et regroupe les findings par sévérité :
- 🔴 **CRITIQUE / ERROR** — failles de sécurité exploitables (injection, secrets en dur, etc.)
- 🟠 **ÉLEVÉ / WARNING** — mauvaises pratiques à risque
- 🟡 **MOYEN / INFO** — code smells, dette technique
- 🟢 **OK** — aucun souci détecté sur ce fichier

### 3. Générer le rapport visuel console

Utilise le script `scripts/render_report.py` (voir ci-dessous) qui prend le JSON Semgrep en entrée et affiche :
- Un tableau coloré (fichier / ligne / sévérité / message) via `rich`
- Une barre de score global de qualité (% de fichiers sans souci critique)
- Un top 3 des problèmes les plus urgents à corriger, avec un extrait de code et une suggestion de fix

```bash
python3 scripts/render_report.py /tmp/semgrep_results.json <chemin_du_code>
```

Le second argument (le chemin scanné) sert à afficher des chemins relatifs propres et à calculer le score sur l'ensemble des fichiers scannés.

### 4. Résumer à l'utilisateur

Après l'affichage, donne un résumé court en français :
- Nombre total de problèmes par sévérité
- Les 2-3 corrections prioritaires à faire en premier
- Ne recopie jamais tout le tableau en texte, le rendu visuel console suffit

## Notes importantes

- Si Semgrep timeout sur un trop gros repo, propose de scanner dossier par dossier ou d'exclure les dépendances (`node_modules`, `venv`, `vendor`, etc.) via `--exclude`.
- Si l'utilisateur veut comparer deux scans (avant/après correction), garde les fichiers JSON horodatés dans `/tmp/` et fais un diff du nombre de findings.
- Ne jamais auto-corriger le code sans demander confirmation à l'utilisateur — propose les fixes, applique-les seulement si demandé explicitement.

## Fichiers du skill

```
glasscode/
├── SKILL.md
├── scripts/
│   └── render_report.py   # point d'entrée (délègue au package glasscode)
└── glasscode/             # package SOLID : parsing / scoring / rendering
```

Le rendu peut aussi être appelé via le package : `python3 -m glasscode <json> <chemin>`.
Format CI : ajoute `-f json` et/ou `--fail-under N`.
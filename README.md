# 🪟 GlassCode

> Rends ton code **transparent** : un audit qualité & sécurité (via [Semgrep](https://semgrep.dev)) présenté sous forme de rapport visuel coloré dans le terminal — tableau par sévérité, score global et corrections prioritaires.

[![CI](https://github.com/yangassojeanyves/glasscode/actions/workflows/ci.yml/badge.svg)](https://github.com/yangassojeanyves/glasscode/actions)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

GlassCode fonctionne en autonomie **et** comme [skill Claude Code](#-utilisation-comme-skill-claude-code).

---

## ✨ Fonctionnalités

- 🎨 **Rapport console coloré** (tableau fichier / ligne / sévérité / règle / message) via `rich`
- 📊 **Score de qualité** (% de fichiers sans faille critique) avec verdict
- 🎯 **Top 3 des corrections prioritaires** avec extrait de code et fix suggéré
- 🤖 **Sortie JSON + seuil `--fail-under`** pour bloquer une CI
- 🧩 **Architecture SOLID** : ajoute un scanner, un score ou un format sans toucher l'existant

---

## 🚀 Installation

```bash
pip install glasscode          # depuis PyPI (si publié)
# ou, depuis les sources :
git clone https://github.com/yangassojeanyves/glasscode
cd glasscode && pip install .
```

Pour lancer les scans, il te faut aussi Semgrep :

```bash
pip install "glasscode[scan]"   # installe semgrep en plus
```

---

## 🧑‍💻 Utilisation

### ⚡ Démarrage rapide (copier-coller)

```bash
# 1. installer (avec le scanner Semgrep)
pip install "glasscode[scan]"

# 2. scanner ton projet -> produit un JSON
semgrep --config=auto --json --quiet -o results.json ./mon_projet

# 3. afficher le rapport visuel
glasscode results.json ./mon_projet
```

C'est tout : tu obtiens le tableau coloré, le score et les corrections prioritaires.

### Détail des deux étapes

**1. Scanner avec Semgrep** (génère le JSON brut) :

```bash
semgrep --config=auto --json --quiet -o results.json ./mon_projet
```

Configs ciblées possibles : `p/security-audit`, `p/owasp-top-ten`, `p/secrets`.

**2. Afficher le rapport** avec GlassCode :

```bash
glasscode results.json ./mon_projet            # rapport console coloré (défaut)
glasscode results.json ./mon_projet -f json    # sortie machine (CI / tooling)
glasscode results.json ./mon_projet --fail-under 80   # échoue si score < 80
```

Sans rien installer, directement depuis le dépôt cloné :

```bash
python -m glasscode results.json ./mon_projet
```

### Options de la commande

| Argument | Description |
|---|---|
| `report` | Chemin du JSON produit par `semgrep --json` *(obligatoire)* |
| `root` | Dossier scanné — chemins relatifs + calcul du score *(optionnel)* |
| `-f`, `--format` | `rich` (défaut, console colorée) ou `json` (machine) |
| `--fail-under N` | Renvoie le code de sortie `1` si le score est `< N` (gate CI) |

### Exemple d'intégration CI (GitHub Actions)

```yaml
- run: pip install "glasscode[scan]"
- run: semgrep --config=auto --json -o results.json .
- run: glasscode results.json . --fail-under 80   # bloque le merge si trop de failles
```

#### Aperçu

```
🔎 GlassCode — Problèmes détectés
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ Sévérité    ┃ Fichier       ┃ Ligne ┃ Règle          ┃ Message            ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ 🔴 CRITIQUE │ app/utils.py  │    12 │ subprocess-use │ shell=True : ...   │
│ 🟠 ÉLEVÉ    │ app/main.py   │    40 │ debug-enabled  │ debug=True ...     │
└─────────────┴───────────────┴───────┴────────────────┴────────────────────┘

📊 Synthèse — Score qualité : ████████████░░░░░░░░ 60% (À risque)
🎯 Corrections prioritaires...
```

---

## 🤖 Utilisation comme skill Claude Code

Copie le dossier dans tes skills personnels :

```bash
cp -r glasscode ~/.claude/skills/glasscode
```

Ensuite, dans Claude Code, demande simplement *« audite ce code »*, *« scan de
sécurité »* ou *« cherche les vulnérabilités »* — le skill se déclenche, lance
Semgrep et affiche le rapport. Le contrat du skill est dans [`SKILL.md`](SKILL.md).

---

## 🏗️ Architecture (SOLID)

Le pipeline est une chaîne d'abstractions injectées (Dependency Inversion) :

```
ReportSource → ScanResultParser → ScoreStrategy → ReportRenderer
   (lecture)      (Adapter)         (Strategy)        (Strategy)
                         \                                /
                          AuditReportService  (Facade)
                                   ▲
                          build_service()  (Factory)
```

| Principe SOLID | Application |
|---|---|
| **S**RP | lecture, parsing, scoring, rendu sont des classes distinctes |
| **O**CP | nouveau scanner/score/format = nouvelle classe, registre des renderers |
| **L**SP | tout `ReportRenderer` est interchangeable (rich ↔ json) |
| **I**SP | interfaces minimales (`read`, `parse`, `compute`, `render`) + erreurs typées |
| **D**IP | la Facade dépend des ABC, jamais de Semgrep/rich en dur |

Patterns : **Adapter** (Semgrep→domaine), **Strategy** (score & rendu),
**Factory** (assemblage), **Facade** (orchestration).

Voir [`CONTRIBUTING.md`](CONTRIBUTING.md) pour savoir où brancher une extension.

---

## 🧪 Tests

```bash
pip install -e ".[dev]"
pytest -q
```

---

## 📄 Licence

[MIT](LICENSE) © Jean-Yves Yangasso

# Contribuer à GlassCode

Merci de ton intérêt ! 🪟

## Mettre en place l'environnement

```bash
git clone https://github.com/Yves-Yangasso/skills-claudecode-glasscode
cd skills-claudecode-glasscode
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

## Architecture (où ajouter quoi)

Le code suit SOLID ; chaque extension est une **nouvelle classe**, pas une
modification de l'existant (Open/Closed) :

| Tu veux... | Ajoute une classe qui implémente... | Dans |
|---|---|---|
| Supporter un autre scanner (Bandit, ESLint...) | `ScanResultParser` | `glasscode/parsing/` |
| Changer le calcul du score | `ScoreStrategy` | `glasscode/scoring/` |
| Un nouveau format de sortie (Markdown, SARIF...) | `ReportRenderer` | `glasscode/rendering/` |
| Une autre source de données (stdin, URL...) | `ReportSource` | `glasscode/sources.py` |

Pense à enregistrer un nouveau renderer dans `_RENDERERS` (`factory.py`).

## Règles

- Toute nouvelle fonctionnalité vient avec ses tests (`pytest`).
- Garde les modules petits et à responsabilité unique.
- Pas de dépendance réseau dans le cœur ; `rich` reste importé paresseusement.

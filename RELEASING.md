# Publier GlassCode sur PyPI

Pour que `pip install glasscode` fonctionne pour tout le monde.

## Prérequis (une seule fois)

1. Créer un compte sur https://pypi.org/account/register/ et activer la 2FA.
2. Générer un token API : https://pypi.org/manage/account/token/
   (portée « Entire account » au début), puis le copier (`pypi-…`).
3. Installer les outils :
   ```bash
   pip install build twine
   ```

## À chaque release

1. **Bumper la version** dans `pyproject.toml` *et* `glasscode/__init__.py`
   (une version PyPI ne peut jamais être ré-uploadée).
2. **Construire** les archives :
   ```bash
   rm -rf dist/
   python -m build
   ```
3. **Vérifier** les métadonnées :
   ```bash
   twine check dist/*
   ```
4. **(Recommandé) tester sur TestPyPI** avant le vrai PyPI :
   ```bash
   twine upload --repository testpypi dist/*
   pip install --index-url https://test.pypi.org/simple/ glasscode
   ```
5. **Publier** :
   ```bash
   twine upload dist/*
   ```
   - Username : `__token__`
   - Password : ton token `pypi-…`

## Après publication

- `pip install glasscode` est disponible mondialement.
- Crée un tag git : `git tag v1.0.0 && git push --tags`.

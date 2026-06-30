"""Command-line entrypoint."""

from __future__ import annotations

import argparse
import sys

from .errors import GlassCodeError
from .factory import AVAILABLE_FORMATS, build_service


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="glasscode",
        description="Affiche un rapport d'audit visuel à partir d'un JSON Semgrep.",
    )
    parser.add_argument("report", help="Chemin du fichier JSON produit par semgrep --json")
    parser.add_argument(
        "root",
        nargs="?",
        default=None,
        help="Dossier scanné (pour des chemins relatifs et le calcul du score)",
    )
    parser.add_argument(
        "-f", "--format",
        choices=AVAILABLE_FORMATS,
        default="rich",
        help="Format de sortie (défaut : rich)",
    )
    parser.add_argument(
        "--fail-under",
        type=int,
        default=None,
        metavar="N",
        help="Sort en code 1 si le score est strictement inférieur à N (pour la CI)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        service = build_service(args.report, root=args.root, fmt=args.format)
        _result, score = service.run()
    except GlassCodeError as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1

    if args.fail_under is not None and score.value < args.fail_under:
        print(
            f"Score {score.value}% < seuil requis {args.fail_under}%.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

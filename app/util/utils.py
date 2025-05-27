import argparse
import os
import sys

from ascii_colors import ASCIIColors

from app import __version__ as core_version
from app.conf import settings


def check_env_file():
    if not os.path.exists('.env'):
        warning_msg = "Warning: Startup directory must contain .env file for multi-instance support."
        ASCIIColors.yellow(warning_msg)

        if sys.stdin.isatty():
            response = input("Do you want to continue? [y/N]: ")
            if response.lower() != "y":
                ASCIIColors.red("Server startup cancelled")
                return False
    return True

def parse_args(is_uvicorn_mode: bool=False):
    parser = argparse.ArgumentParser(
        description="FastAPI Server with separate working and input directories"
    )

    parser.add_argument(
        "--host",
        default=settings.HOST,
        help="Server host (default: from env or 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=settings.PORT,
        help="Server port (default: from env or 8000)"
    )
    args = parser.parse_args()
    return args

def display_splash_screen(args: argparse.Namespace):
    ASCIIColors.cyan(f"""
        ╔══════════════════════════════════════════════════════════════╗
        ║                   🚀 MOSS Server v{core_version}                      ║
        ║          Fast, Lightweight RAG Server Implementation         ║
        ╚══════════════════════════════════════════════════════════════╝
        """)
    ASCIIColors.magenta("\n📡 Server Configuration:")
    ASCIIColors.white("    ├─ Host: ", end="")
    ASCIIColors.yellow(f"{args.host}")
    ASCIIColors.white("    ├─ Port: ", end="")
    ASCIIColors.yellow(f"{args.port}")
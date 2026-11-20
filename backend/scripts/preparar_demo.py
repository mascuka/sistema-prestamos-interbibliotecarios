"""Prepara la base de la demo publicada en Vercel.

Corre en cada build (``[tool.vercel.scripts]`` en ``pyproject.toml``): aplica las migraciones y,
si la base todavía no tiene datos, carga la red de demostración. ``DATABASE_URL`` la pone la
integración de Vercel con Neon. Sin esa variable (por ejemplo, en una compilación local) no hace
nada.

La contraseña de los usuarios de demostración es pública a propósito: es una demo para mostrar
el sistema, con datos inventados. Se puede cambiar con la variable ``SEED_PASSWORD``.

También crea el usuario ``visitante``, el que muestra el login (los mismos valores
están en ``frontend/.env.production``). Para que nadie pueda modificar los datos, el proyecto de
Vercel define ``USUARIOS_SOLO_LECTURA=*``: todos los usuarios ven, ninguno modifica.
"""

import os
import subprocess
import sys

CLAVE_DEMO = "Biblioteca2026"
USUARIO_VISITANTE = "visitante"
CLAVE_VISITANTE = "visitante1"


def main() -> int:
    if not os.environ.get("DATABASE_URL"):
        print("Sin DATABASE_URL: no se prepara la base de la demo.")
        return 0
    print("Aplicando las migraciones...")
    subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)
    entorno = {
        **os.environ,
        "ENTORNO": "desarrollo",
        "SEED_PASSWORD": os.environ.get("SEED_PASSWORD") or CLAVE_DEMO,
    }
    subprocess.run([sys.executable, "-m", "app.db.seed"], env=entorno, check=True)
    entorno_visitante = {
        **os.environ,
        "VITE_DEMO_USUARIO": os.environ.get("VITE_DEMO_USUARIO") or USUARIO_VISITANTE,
        "VITE_DEMO_CLAVE": os.environ.get("VITE_DEMO_CLAVE") or CLAVE_VISITANTE,
    }
    subprocess.run([sys.executable, "-m", "app.db.visitante"], env=entorno_visitante, check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

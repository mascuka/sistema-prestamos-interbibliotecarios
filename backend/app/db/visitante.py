"""Usuario visitante de la demo publicada: ve todo y no puede modificar nada.

Uso: ``python -m app.db.visitante`` (lo corre ``scripts/preparar_demo.py`` en cada build). Crea el
usuario ``VITE_DEMO_USUARIO``, con rol administrador para que vea todo, y la contraseña
``VITE_DEMO_CLAVE``, si todavía no existe. Que no pueda modificar nada lo asegura
``USUARIOS_SOLO_LECTURA`` en el backend.
"""

import os
import sys

from sqlalchemy import select

from app.config.security import hashear_clave
from app.db.models import UsuarioORM
from app.db.session import crear_fabrica_sesiones
from app.models.usuario import Rol, validar_clave, validar_username


def asegurar_visitante(usuario: str, clave: str) -> bool:
    """Crea el usuario visitante si no existe. Devuelve si lo creó."""
    username = validar_username(usuario)
    validar_clave(clave)
    with crear_fabrica_sesiones()() as sesion:
        if sesion.scalar(select(UsuarioORM.id).where(UsuarioORM.username == username)):
            return False
        sesion.add(
            UsuarioORM(
                username=username,
                password_hash=hashear_clave(clave),
                nombre="Visitante",
                rol=Rol.ADMIN.value,
                activo=True,
            )
        )
        sesion.commit()
        return True


def main() -> int:
    usuario = os.environ.get("VITE_DEMO_USUARIO")
    clave = os.environ.get("VITE_DEMO_CLAVE")
    if not usuario or not clave:
        print("Sin VITE_DEMO_USUARIO o VITE_DEMO_CLAVE: no se crea el visitante.")
        return 0
    creado = asegurar_visitante(usuario, clave)
    print(f"Visitante {usuario!r}: {'creado' if creado else 'ya existía'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

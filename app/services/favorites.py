import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FAVORITOS_FILE = BASE_DIR / "utils" / "favoritos.json"
def cargar_favoritos():
    if FAVORITOS_FILE.exists():
        try:
            with open(FAVORITOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {} 
    return {}
def guardar_favorito(usuario: str, pokemon: dict):
    favoritos = cargar_favoritos()
    if usuario not in favoritos:
        favoritos[usuario] = []
    pokemon_id = len(favoritos[usuario]) + 1
    favorito_obj = {
        "id": pokemon_id,
        "pokemon": pokemon
    }
    favoritos[usuario].append(favorito_obj)
    with open(FAVORITOS_FILE, "w", encoding="utf-8") as f:
        json.dump(favoritos, f, indent=2, ensure_ascii=False)

def listar_favoritos(usuario: str):
    favoritos=cargar_favoritos()
    return favoritos.get(usuario, [])

def eliminar_favorito(usuario: str, id_fav: int):
    favoritos=cargar_favoritos()
    if usuario not in favoritos:
        return False
    nuevos =[f for f in favoritos[usuario] if f["id"] != id_fav]
    if len(nuevos) ==len(favoritos[usuario]):
        return False
    favoritos[usuario] = nuevos
    with open(FAVORITOS_FILE, "w", encoding="utf-8") as f:
        json.dump(favoritos, f, indent=2, ensure_ascii=False)
    return True

def buscar_favorito(usuario: str, id_fav: int):
    favoritos = cargar_favoritos()
    for f in favoritos.get(usuario, []):
        if f["id"] == id_fav:
            return f
    return {}
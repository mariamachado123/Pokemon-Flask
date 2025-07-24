from models.zodiac import calcular_signo_zodiacal
from services.pokemon import obtener_pokemon
signo_pokemon = {
    "Aries": "charmander",
    "Tauro": "bulbasaur",
    "Géminis": "pidgey",
    "Cáncer": "squirtle",
    "Leo": "flareon",
    "Virgo": "bellsprout",
    "Libra": "pikachu",
    "Escorpio": "zubat",
    "Sagitario": "growlithe",
    "Capricornio": "onix",
    "Acuario": "psyduck",
    "Piscis": "gyarados"
}
def obtener_horoscopo(nombre: str, fecha_nacimiento: str):
    signo = calcular_signo_zodiacal(fecha_nacimiento)
    nombre_pokemon = signo_pokemon.get(signo, "pikachu")
    datos_pokemon = obtener_pokemon(nombre_pokemon)
    return {
        "usuario": nombre,
        "signo": signo,
        "pokemon": datos_pokemon
    }

from flask import Flask, request, jsonify
from services.horoscope import obtener_horoscopo
from services.favorites import guardar_favorito, listar_favoritos, eliminar_favorito, buscar_favorito
from services.pokemon import buscar_pokemon, obtener_pokemon
from datetime import datetime

app = Flask(__name__)
def validar_fecha(fecha_str):
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

@app.route("/horoscopo", methods=["POST"])
def horoscopo():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON inválido o vacío"}), 400

    nombre=data.get("nombre")
    fecha=data.get("fecha_nacimiento")

    if not nombre or not nombre.strip():
        return jsonify({"error": "Nombre no puede estar vacío"}), 400
    if not fecha or not validar_fecha(fecha):
        return jsonify({"error": "Fecha inválida"}), 400

    resultado = obtener_horoscopo(nombre.strip(), fecha)
    return jsonify(resultado)

@app.route("/favoritos", methods=["POST"])
def add_favorito():
    try:
        data=request.get_json()
        print("Datos recibidos:", data)
        usuario=data.get("usuario")
        pokemon_nombre=data.get("pokemon")

        if not usuario or not usuario.strip() or not pokemon_nombre or not pokemon_nombre.strip():
            return jsonify({"error": "Datos incompletos"}), 400

        poke_data=obtener_pokemon(pokemon_nombre.strip())
        print("Resultado de obtener_pokemon:", poke_data)

        if not poke_data:
            return jsonify({"error": "Pokémon no encontrado"}), 404

        guardar_favorito(usuario.strip(), poke_data)
        return jsonify({"mensaje": "Favorito guardado"})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

@app.route("/favoritos", methods=["GET"])
def get_favoritos():
    usuario = request.args.get("usuario")
    if not usuario or not usuario.strip():
        return jsonify({"error": "Falta nombre de usuario"}), 400

    favoritos = listar_favoritos(usuario.strip())
    return jsonify({"usuario": usuario.strip(), "favoritos": favoritos})

@app.route("/favoritos", methods=["DELETE"])
def delete_favorito():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON inválido o vacío"}), 400

    usuario = data.get("usuario")
    id_fav = data.get("id")

    if not usuario or not usuario.strip() or not id_fav:
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        id_fav = int(id_fav)
    except ValueError:
        return jsonify({"error": "ID inválido"}), 400

    eliminado = eliminar_favorito(usuario.strip(), id_fav)
    if eliminado:
        return jsonify({"mensaje": "Favorito eliminado"})
    else:
        return jsonify({"error": "Favorito no encontrado"}), 404

@app.route("/favoritos/<int:id_fav>", methods=["GET"])
def get_favorito(id_fav):
    usuario = request.args.get("usuario")
    if not usuario or not usuario.strip():
        return jsonify({"error": "Falta nombre de usuario"}), 400

    favorito = buscar_favorito(usuario.strip(), id_fav)
    if not favorito:
        return jsonify({"error": "Favorito no encontrado"}), 404
    return jsonify(favorito)

@app.route("/pokemon", methods=["GET"])
def buscar_poke():
    nombre = request.args.get("nombre")
    tipo = request.args.get("tipo")

    if not nombre and not tipo:
        return jsonify({"error": "Se requiere al menos nombre o tipo"}), 400

    resultados = buscar_pokemon(nombre=nombre, tipo=tipo)
    return jsonify({"resultados": resultados})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

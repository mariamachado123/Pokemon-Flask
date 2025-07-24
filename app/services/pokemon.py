import requests
def obtener_pokemon(nombre_o_id: str):
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre_o_id.lower()}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    data = resp.json()
    return {
        "nombre": data["name"],
        "imagen": data["sprites"]["front_default"],
        "tipo": [t["type"]["name"] for t in data["types"]],
        "altura": data["height"],
        "peso": data["weight"],
        "habilidades": [h["ability"]["name"] for h in data["abilities"]],
    }

def buscar_pokemon(nombre=None, tipo=None):
    resultados = []
    if nombre:
        p=obtener_pokemon(nombre)
        if p:
            if tipo:
                if tipo.lower() in p["tipo"]:
                    resultados.append(p)
            else:
                resultados.append(p)
    elif tipo:
        url=f"https://pokeapi.co/api/v2/type/{tipo.lower()}"
        resp=requests.get(url)
        if resp.status_code==200:
            data=resp.json()
            pokemon_list=data["pokemon"]
            for entry in pokemon_list[:10]:
                p_name=entry["pokemon"]["name"]
                p_data=obtener_pokemon(p_name)
                if p_data:
                    resultados.append(p_data)
    return resultados

from fastapi import FastAPI, Body
import csv
import json
from datetime import datetime
import os

app = FastAPI()

ruta_csv = os.path.join(os.path.dirname(__file__), "historial.csv")
ruta_json = os.path.join(os.path.dirname(__file__), "historial.json")

# Inicializar CSV
if not os.path.exists(ruta_csv):
    with open(ruta_csv, mode="w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["fecha", "accion", "estado", "detalle"])

# Inicializar JSON
if not os.path.exists(ruta_json):
    with open(ruta_json, "w", encoding="utf-8") as archivo:
        json.dump([], archivo)

def guardar_historial(accion, estado, detalle="", detalle_json=None):
    registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "accion": accion,
        "estado": estado,
        "detalle": detalle
    }

    # Guardar en CSV
    with open(ruta_csv, mode="a", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow([registro["fecha"], registro["accion"], registro["estado"], registro["detalle"]])

    # Guardar en JSON
    with open(ruta_json, "r+", encoding="utf-8") as archivo:
        data = json.load(archivo)
        registro_json = {
            "fecha": registro["fecha"],
            "accion": accion,
            "estado": estado,
            "detalle": detalle_json if detalle_json else detalle
        }
        data.append(registro_json)
        archivo.seek(0)
        json.dump(data, archivo, indent=4, ensure_ascii=False)

def formato_producto(prod: dict, titulo: str) -> str:
    return (
        f"{titulo}\n"
        f"  nombre: {prod['nombre']}\n"
        f"  valor: {prod['valor']}\n"
        f"  existencias: {prod['existencias']}"
    )

productos = [
    {"codigo": 1, "nombre": "esfero", "valor": 3500, "existencias": 10},
    {"codigo": 2, "nombre": "cuaderno", "valor": 5000, "existencias": 15},
    {"codigo": 3, "nombre": "lapiz", "valor": 200, "existencias": 12}
]

@app.get("/")
def mensaje():
    return "Bienvenido a FastAPI ingeniero"

@app.get("/uno/")
def mensaje3(nombre: str, edad: int):
    return f"Su nombre es {nombre}, su edad es {edad}"

@app.get("/productos")
def listProductos():
    detalle = "\n".join([formato_producto(p, f"PRODUCTO {p['codigo']}") for p in productos])
    detalle_json = productos
    guardar_historial("listar", "ok", detalle, detalle_json)
    return productos

@app.get("/producto/{cod}")
def findProductos(cod: int):
    for prod in productos:
        if prod["codigo"] == cod:
            detalle = formato_producto(prod, "CONSULTADO")
            guardar_historial("buscar", "ok", detalle, prod)
            return prod
    guardar_historial("buscar", "error", f"producto {cod} no encontrado", {"error": "no encontrado"})
    return {"mensaje": "Producto no encontrado"}

@app.post("/productos")
def createProducto(
    cod: int = Body(),
    nom: str = Body(),
    val: float = Body(),
    exi: int = Body()
):
    nuevo = {
        "codigo": cod,
        "nombre": nom,
        "valor": val,
        "existencias": exi,
    }
    productos.append(nuevo)
    detalle = formato_producto(nuevo, "CREADO")
    guardar_historial("crear", "ok", detalle, nuevo)
    return productos

@app.put("/productos/{cod}")
def updateProducto(
    cod: int,
    nom: str = Body(),
    val: float = Body(),
    exi: int = Body()
):
    for prod in productos:
        if prod["codigo"] == cod:
            antes = prod.copy()
            prod["nombre"] = nom
            prod["valor"] = val
            prod["existencias"] = exi
            despues = prod.copy()
            detalle = f"{formato_producto(antes, 'ANTES')}\n{formato_producto(despues, 'DESPUÉS')}"
            detalle_json = {"antes": antes, "despues": despues}
            guardar_historial("actualizar", "ok", detalle, detalle_json)
            return productos
    guardar_historial("actualizar", "error", f"producto {cod} no encontrado", {"error": "no encontrado"})
    return {"mensaje": "Producto no encontrado"}

@app.delete("/productos/{cod}")
def deleteProducto(cod: int):
    for prod in productos:
        if prod["codigo"] == cod:
            eliminado = prod.copy()
            productos.remove(prod)
            detalle = f"{formato_producto(eliminado, 'ANTES')}\nDESPUÉS\n  producto eliminado"
            detalle_json = {"antes": eliminado, "despues": "eliminado"}
            guardar_historial("eliminar", "ok", detalle, detalle_json)
            return productos
    guardar_historial("eliminar", "error", f"producto {cod} no encontrado", {"error": "no encontrado"})
    return {"mensaje": "Producto no encontrado"}

@app.get("/productos-validado/{cod}")
def buscar_producto_validado(cod: int):
    if cod <= 0:
        guardar_historial("buscar", "error", "codigo <= 0", {"error": "codigo <= 0"})
        return {"error": "El código debe ser mayor a cero"}
    for prod in productos:
        if prod["codigo"] == cod:
            detalle = formato_producto(prod, "ENCONTRADO")
            guardar_historial("buscar", "ok", detalle, prod)
            return prod
    guardar_historial("buscar", "error", "producto no existe", {"error": "no existe"})
    return {"mensaje": "Producto no existe"}

@app.post("/productos-validado")
def crear_producto_validado(
    nom: str = Body(),
    val: float = Body(),
    exi: int = Body(),
):
    if val <= 0 or exi <= 0:
        guardar_historial("crear", "error", "valor o existencias <= 0", {"error": "valores invalidos"})
        return {"error": "El valor y las existencias deben ser mayores a cero"}
    nuevo_codigo = max([p["codigo"] for p in productos]) + 1 if productos else 1
    nuevo = {
        "codigo": nuevo_codigo,
        "nombre": nom,
        "valor": val,
        "existencias": exi,
    }
    productos.append(nuevo)
    detalle = formato_producto(nuevo, "CREADO")
    guardar_historial("crear", "ok", detalle, nuevo)
    return {"mensaje": "Producto creado correctamente", "producto": nuevo}

@app.put("/productos-validado/{cod}")
def actualizar_producto_validado(
    cod: int,
    nom: str = Body(),
    val: float = Body(),
    exi: int = Body()
):
    if val <= 0 or exi <= 0:
        guardar_historial("actualizar", "error", "valores inválidos", {"error": "valores invalidos"})
        return {"error": "El valor y las existencias deben ser mayores a cero"}
    for prod in productos:
        if prod["codigo"] == cod:
            antes = prod.copy()
            prod["nombre"] = nom
            prod["valor"] = val
            prod["existencias"] = exi
            despues = prod.copy()
            detalle = f"{formato_producto(antes, 'ANTES')}\n{formato_producto(despues, 'DESPUÉS')}"
            detalle_json = {"antes": antes, "despues": despues}
            guardar_historial("actualizar", "ok", detalle, detalle_json)
            return {"mensaje": "Producto actualizado", "antes": antes, "despues": despues}
    guardar_historial("actualizar", "error", "producto no existe", {"error": "no existe"})
    return {"error": "Producto no existe"}

@app.delete("/productos-validado/{cod}")
def eliminar_producto_validado(cod: int):
    for prod in productos:
        if prod["codigo"] == cod:
            eliminado = prod.copy()
            productos.remove(prod)
            detalle = f"{formato_producto(eliminado, 'ANTES')}\nDESPUÉS\n  producto eliminado"
            detalle_json = {"antes": eliminado, "despues": "eliminado"}
            guardar_historial("eliminar", "ok", detalle, detalle_json)
            return {"mensaje": "Producto eliminado", "producto": eliminado}
    guardar_historial("eliminar", "error", "producto no existe", {"error": "no existe"})
    return {"error": "Producto no existe"}

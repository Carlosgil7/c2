from fastapi import FastAPI, Body

app = FastAPI()
productos = [
    {
        "codigo": 1,
        "nombre": "esfero",
        "valor": 3500,
        "existencias": 10
    },
    {
        "codigo": 2,
        "nombre": "cuaderno",
        "valor": 5000,
        "existencias": 15
    },
    {
        "codigo": 3,
        "nombre": "lapiz",
        "valor": 200,
        "existencias": 12
    }
]

@app.get("/")
def mensaje():
    return "bienvenido a FastAPI ingeniero"

@app.get("/{nombre}/{codigo}")
def mensaje2(nombe: str, codigo1: int):
    return f"nombre {nombre} su codigo es {codigo1}"

@app.get("/uno/")
def mensaje3(nombre: str, edad: int):
    return f"su nombre es {nombre} su edad es {edad}"

@app.get("/productos")
def listProductos():
    return productos

@app.get("/producto/{cod}")
def findProductos(cod: int):
    for prod in productos:
        if prod["codigo"] == cod:
            return prod

@app.get("/productos")
def createProducto(cod: int, nom: str, val: float, exi: int):
    productos.append({
        "codigo": cod,
        "nombre": nom,
        "valor": val,
        "existencias": exi,
    })
    return productos

@app.post("/productos")
def createProducto(cod: int, nom: str, val: float, exi: int):
    productos.append({
        "codigo": cod,
        "nombre": nom,
        "valor": val,
        "existencias": exi,
    })
    return productos

@app.post("/productos2")
def createProducto2(
    cod: int = Body(),
    nom: str = Body(),
    val: float = Body(),
    exi: int = Body(),
):
    productos.append({
        "codigo": cod,
        "nombre": nom,
        "valor": val,
        "existencias": exi,
    })
    return productos

@app.put("/productos/{cod}")
def updateProducto(cod: int,
                   nom: str = Body(),
                   val: float = Body(),
                   exi: int = Body()):
    for prod in productos:
        if prod["codigo"] == cod:
            prod["nombre"] == nom
            prod["valor"] == val
            prod["existencias"] = exi
            return productos

@app.delete("/productos/{cod}")
def deleteProducto(cod: int):
    for prod in productos:
        if prod["codigo"] == cod:
            productos.remove(prod)
            return productos

# 1 y 2. Buscar con validación
@app.get("/productos-validado/{cod}")
def buscar_producto_validado(cod: int):
    if cod <= 0:
        return {"error": "El código debe ser mayor a cero"}

    for prod in productos:
        if prod["codigo"] == cod:
            return prod

    return {"mensaje": "Producto no existe"}

# 3 y 4. Crear con consecutivo y validación
@app.post("/productos-validado")
def crear_producto_validado(
    nom: str = Body(),
    val: float = Body(),
    exi: int = Body(),
):
    if val <= 0 or exi <= 0:
        return {"error": "El valor y las existencias deben ser mayores a cero"}
    nuevo_codigo = max([p["codigo"] for p in productos]) + 1 if productos else 1

    nuevo = {
        "codigo": nuevo_codigo,
        "nombre": nom,
        "valor": val,
        "existencias": exi,
    }

    productos.append(nuevo)

    return {
        "mensaje": "Producto creado correctamente",
        "producto": nuevo
    }


# 5, 6 y 7. Actualizar con validaciones
@app.put("/productos-validado/{cod}")
def actualizar_producto_validado(
    cod: int,
    nom: str = Body(),
    val: float = Body(),
    exi: int = Body()
):
    if val <= 0 or exi <= 0:
        return {"error": "El valor y las existencias deben ser mayores a cero"}

    for prod in productos:
        if prod["codigo"] == cod:
            antes = prod.copy()

            prod["nombre"] = nom
            prod["valor"] = val
            prod["existencias"] = exi

            return {
                "mensaje": "Producto actualizado",
                "antes": antes,
                "despues": prod
            }

    return {"error": "Producto no existe"}


# 8. Eliminar con validación
@app.delete("/productos-validado/{cod}")
def eliminar_producto_validado(cod: int):
    for prod in productos:
        if prod["codigo"] == cod:
            eliminado = prod.copy()
            productos.remove(prod)

            return {
                "mensaje": "Producto eliminado",
                "producto": eliminado
            }

    return {"error": "Producto no existe"}


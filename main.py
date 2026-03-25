from fastapi import FastAPI, Body

app=FastAPI()
productos=[
    {
        "codigo":1,
        "nombre":"esfero",
        "valor":3500,
        "existencias":10
    },
    {
        "codigo":2,
        "nombre":"cuaderno",
        "valor":5000,
        "existencias":15
    },
    {
        "codigo":3,
        "nombre":"lapiz",
        "valor":200,
        "existencias":12
    }
]

@app.get("/")
def mensaje():
    return "bienvenido a FastAPI ingeniero"

@app.get("/{nombre}/{codigo}")
def mensaje2(nombe:str, codigo1:int):
    return f"nombre {nombre} su codigo es {codigo1}"

@app.get("/uno/")
def mensaje3(nombre:str,edad:int):
    return f"su nombre es {nombre} su edad es {edad}"

@app.get("/productos")
def listProductos():
    return productos

@app.get("/producto/{cod}")
def findProductos(cod:int):
    if cod <= 0:
        return {"error":"el codigo debe ser mayor a cero"}
    for prod in productos:
        if prod["codigo"]==cod:
            return prod
    return {"mensaje":"producto no existe"}

@app.get("/productos")
def createProducto(cod:int,nom:str,val:float,exi:int):

    nuevo_codigo = max([p["codigo"] for p in productos]) + 1 if productos else 1

    if val <= 0 or exi <= 0:
        return {"error":"valor y existencias deben ser mayores a cero"}

    productos.append({
        "codigo":nuevo_codigo,
        "nombre": nom,
        "valor": val,
        "existencias": exi,
    })
    return productos

@app.post("/productos")
def createProducto(cod:int,nom:str,val:float,exi:int):

    nuevo_codigo = max([p["codigo"] for p in productos]) + 1 if productos else 1

    if val <= 0 or exi <= 0:
        return {"error":"valor y existencias deben ser mayores a cero"}

    productos.append({
        "codigo":nuevo_codigo,
        "nombre": nom,
        "valor": val,
        "existencias": exi,
    })
    return productos

@app.post("/productos2")
def createProducto2(
    cod:int=Body(),
    nom:str=Body(),
    val:float=Body(),
    exi:int=Body(),
    ):

    nuevo_codigo = max([p["codigo"] for p in productos]) + 1 if productos else 1

    if val <= 0 or exi <= 0:
        return {"error":"valor y existencias deben ser mayores a cero"}

    productos.append({
        "codigo":nuevo_codigo,
        "nombre": nom,
        "valor": val,
        "existencias": exi,
    })
    return productos

@app.put("/productos/{cod}")
def updateProducto(cod:int,
    nom:str=Body(),
    val:float=Body(),
    exi:int=Body()):

    if val <= 0 or exi <= 0:
        return {"error":"valor y existencias deben ser mayores a cero"}

    for prod in productos:
        if prod["codigo"]==cod:
            anterior = prod.copy()

            prod["nombre"]=nom
            prod["valor"]=val
            prod["existencias"]=exi

            return {
                "antes": anterior,
                "despues": prod
            }

    return {"error":"producto no existe"}

@app.delete("/productos/{cod}")
def deleteProducto(cod:int):
    for prod in productos:
        if prod["codigo"]==cod:
            eliminado = prod
            productos.remove(prod)
            return {"eliminado": eliminado}

    return {"error":"producto no existe"}


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
    for prod in productos:
        if prod["codigo"]==cod:
            return prod

@app.get("/productos")
def createProducto(cod:int,nom:str,val:float,exi:int):
    productos.append({
        "codigo":cod,
        "nombre": nom,
        "valor": val,
        "existencias": exi,
    })
    return productos

@app.post("/productos")
def createProducto(cod:int,nom:str,val:float,exi:int):
    productos.append({
        "codigo":cod,
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
    productos.append({
        "codigo":cod,
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
    for prod in productos:
        if prod["codigo"]==cod:
           prod["nombre"]==nom
           prod["valor"]==val
           prod["existencias"]=exi
    return productos

@app.delete("/productos/{cod}")
def deleteProducto(cod:int):
    for prod in productos:
        if prod["codigo"]==cod:
            productos.remove(prod)
    return productos
        
                    





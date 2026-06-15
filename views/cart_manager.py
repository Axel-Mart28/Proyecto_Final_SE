# views/cart_manager.py
# Carrito en memoria — lista compartida entre todas las vistas

_carrito = []

def agregar_al_carrito(producto: dict):
    # Si el producto ya está en el carrito, aumenta la cantidad
    for item in _carrito:
        if item["id"] == producto["id"]:
            item["cantidad"] += 1
            return
    # Si no está, lo agrega con cantidad 1
    _carrito.append({**producto, "cantidad": 1})

def obtener_carrito():
    return _carrito

def eliminar_del_carrito(producto_id: int):
    global _carrito
    _carrito = [item for item in _carrito if item["id"] != producto_id]

def limpiar_carrito():
    _carrito.clear()

def obtener_total():
    return sum(item["precio"] * item["cantidad"] for item in _carrito)
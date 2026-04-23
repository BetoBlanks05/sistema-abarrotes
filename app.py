from flask import Flask, request, jsonify
from database import get_db
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.get("/")
def home():
    return render_template("index.html")

# PRODUCTOS
@app.post("/products")
def crear_producto():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (%s, %s, %s, %s)",
        (data["nombre"], data["categoria"], data["precio"], data["stock"])
    )
    db.commit()
    return jsonify({"message": "Producto creado"}), 201

@app.get("/products")
def obtener_productos():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    return jsonify(cursor.fetchall())

@app.get("/products/<int:id_producto>")
def obtener_producto(id_producto):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id_producto,))
    producto = cursor.fetchone()
    if producto:
        return jsonify(producto)
    return jsonify({"error": "Producto no encontrado"}), 404

@app.patch("/products/<int:id_producto>")
def actualizar_producto(id_producto):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE productos SET nombre=%s, categoria=%s, precio=%s, stock=%s WHERE id=%s",
        (data.get("nombre"), data.get("categoria"), data.get("precio"), data.get("stock"), id_producto)
    )
    db.commit()
    return jsonify({"message": "Producto actualizado"})

@app.delete("/products/<int:id_producto>")
def eliminar_producto(id_producto):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM productos WHERE id=%s", (id_producto,))
    db.commit()
    return jsonify({"message": "Producto eliminado"}), 204


# CARRITO
@app.post("/cart")
def agregar_carrito():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO carrito (id_producto, cantidad) VALUES (%s, %s)",
        (data["id_producto"], data["cantidad"])
    )
    db.commit()
    return jsonify({"message": "Producto agregado al carrito"}), 201

@app.get("/cart")
def ver_carrito():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT carrito.id, productos.nombre, carrito.cantidad, productos.precio
        FROM carrito
        JOIN productos ON carrito.id_producto = productos.id
    """)
    return jsonify(cursor.fetchall())

@app.delete("/cart/<int:id_producto>")
def eliminar_item_carrito(id_producto):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM carrito WHERE id_producto=%s", (id_producto,))
    db.commit()
    return jsonify({"message": "Item eliminado"}), 204


# PEDIDOS
@app.post("/orders")
def confirmar_pedido():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT carrito.id_producto, carrito.cantidad, productos.precio
        FROM carrito
        JOIN productos ON carrito.id_producto = productos.id
    """)
    carrito = cursor.fetchall()
    if not carrito:
        return jsonify({"error": "Carrito vacío"}), 400

    total = sum(item["precio"] * item["cantidad"] for item in carrito)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor2 = db.cursor()
    cursor2.execute(
        "INSERT INTO pedidos (total, estado, fecha) VALUES (%s, %s, %s)",
        (total, "confirmado", fecha)
    )
    db.commit()
    id_pedido = cursor2.lastrowid

    for item in carrito:
        cursor2.execute(
            "INSERT INTO pedido_items (id_pedido, id_producto, cantidad) VALUES (%s, %s, %s)",
            (id_pedido, item["id_producto"], item["cantidad"])
        )

    cursor2.execute("DELETE FROM carrito")
    db.commit()

    return jsonify({
        "message": "Pedido confirmado",
        "id_pedido": id_pedido,
        "total": total
    }), 201

@app.get("/orders")
def obtener_pedidos():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedidos")
    return jsonify(cursor.fetchall())

if __name__ == "__main__":
    app.run(debug=True)



const API = "http://localhost:5000";

async function cargarCatalogo() {
  const res = await fetch("http://localhost:5000/products");
  const productos = await res.json();
  const contenedor = document.getElementById("catalogo");
  contenedor.innerHTML = "";

  productos.forEach(p => {
    const div = document.createElement("div");
    div.className = "producto";
    div.innerHTML = `
      <h3>${p.nombre}</h3>
      <p>Categoría: ${p.categoria}</p>
      <p>Precio: $${p.precio}</p>
      <p>Stock: ${p.stock}</p>
      <button onclick="agregarAlCarrito(${p.id})">Agregar al carrito</button>
    `;
    contenedor.appendChild(div);
  });
}

cargarCatalogo();


async function agregarAlCarrito(id_producto) {
  await fetch(`${API}/cart`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id_producto, cantidad: 1 })
  });
  cargarCarrito();
}

async function cargarCarrito() {
  const res = await fetch(`${API}/cart`);
  const items = await res.json();
  const ul = document.getElementById("carrito-lista");
  ul.innerHTML = "";

  items.forEach(i => {
    const li = document.createElement("li");
    li.textContent = `${i.nombre} x${i.cantidad} ($${i.precio})`;
    ul.appendChild(li);
  });
}

async function confirmarPedido() {
  const res = await fetch(`${API}/orders`, { method: "POST" });
  const data = await res.json();
  alert(`Pedido confirmado. Total: $${data.total}`);
  cargarCarrito();
  cargarPedidos();
}

async function cargarPedidos() {
  const res = await fetch(`${API}/orders`);
  const pedidos = await res.json();
  const ul = document.getElementById("pedidos-lista");
  ul.innerHTML = "";

  pedidos.forEach(p => {
    const li = document.createElement("li");
    li.textContent = `Pedido #${p.id} - $${p.total} - ${p.fecha}`;
    ul.appendChild(li);
  });
}

cargarCarrito();
cargarPedidos();

// 🔥 URL DE TU BACKEND EN RENDER
const API_URL = "https://papeleria-app-vf6w.onrender.com";


// ===============================
// 💾 GUARDAR PRODUCTO
// ===============================
function guardar() {
  const codigo = document.getElementById("codigo").value;
  const nombre = document.getElementById("nombre").value;
  const piezas = document.getElementById("piezas").value;
  const precio_compra = document.getElementById("precio_compra").value;
  const porcentaje = document.getElementById("porcentaje").value;

  if (!nombre || !piezas) {
    alert("Completa nombre y piezas");
    return;
  }

  fetch(`${API_URL}/guardar`, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json" 
    },
    body: JSON.stringify({
      codigo,
      nombre,
      piezas: Number(piezas),
      precio_compra: Number(precio_compra),
      porcentaje: Number(porcentaje)
    })
  })
  .then(res => {
    if (!res.ok) throw new Error("Error servidor");
    return res.json();
  })
  .then(data => {
    alert("✅ Guardado correctamente");
    limpiarCampos();
    verFaltantes();
  })
  .catch(err => {
    console.log("ERROR REAL:", err);
    alert("❌ Error al guardar");
  });
}


// ===============================
// 🗑 ELIMINAR PRODUCTO
// ===============================
function eliminar(codigo) {
  fetch(`${API_URL}/eliminar/${codigo}`, {
    method: "DELETE"
  })
  .then(() => {
    alert("Producto eliminado");
    verFaltantes();
  });
}


// ===============================
// 📦 VER FALTANTES
// ===============================
function verFaltantes() {
  fetch(`${API_URL}/faltantes`)
    .then(res => res.json())
    .then(data => {
      const lista = document.getElementById("lista");
      lista.innerHTML = "";

      let totalCompra = 0;
      let totalGanancia = 0;

      data.forEach(item => {

        totalCompra += (item.precio_compra || 0) * item.piezas;
        totalGanancia += ((item.precio_venta || 0) - (item.precio_compra || 0)) * item.piezas;

        const li = document.createElement("li");
        li.innerHTML = `
          <strong>${item.nombre}</strong><br>
          Código: ${item.codigo || "N/A"}<br>
          Piezas: ${item.piezas}
          <div class="precio">
            Compra: $${item.precio_compra || 0} <br>
            Venta: $${item.precio_venta || 0}
          </div>
          <button onclick="eliminar('${item.codigo}')">
            ✅ Comprado / Eliminar
          </button>
        `;
        lista.appendChild(li);
      });

      document.getElementById("totalCompra").innerText = totalCompra.toFixed(2);
      document.getElementById("totalGanancia").innerText = totalGanancia.toFixed(2);

    })
    .catch(err => {
      console.log("Error:", err);
    });
}


// ===============================
// 🧹 LIMPIAR CAMPOS
// ===============================
function limpiarCampos() {
  document.getElementById("codigo").value = "";
  document.getElementById("nombre").value = "";
  document.getElementById("piezas").value = "";
  document.getElementById("precio_compra").value = "";
  document.getElementById("porcentaje").value = "";
}


// ===============================
// 🌙 MODO OSCURO
// ===============================
function toggleTheme() {
  document.body.classList.toggle("dark");
}


// ===============================
// 🚀 CARGAR LISTA AL ABRIR
// ===============================
verFaltantes();

(function () {
  const frm = document.getElementById("frmDescarga");
  const rbComprobantes = document.getElementById("comprobantes");
  const rbGuias = document.getElementById("guias");
  const grpRuc = document.getElementById("grpRuc");
  const lblCorrelativo = document.getElementById("lblCorrelativo");

  const rucInput = document.getElementById("ruc");
  const serieInput = document.getElementById("serie");
  const corrInput = document.getElementById("correlativo");

  // Cambios de UI: ocultar RUC cuando es Guías, mostrar cuando es Comprobantes
  function updateUiByTipo() {
    const isGuias = rbGuias.checked;
    grpRuc.classList.toggle("d-none", isGuias);

    // (opcional) Cambiar etiqueta
    lblCorrelativo.textContent = isGuias ? "Número" : "Correlativo";

    // (opcional) limpiar RUC si es Guías
    if (isGuias) rucInput.value = "";
  }

  rbComprobantes.addEventListener("change", updateUiByTipo);
  rbGuias.addEventListener("change", updateUiByTipo);
  updateUiByTipo();

  // Helper: descargar blob con nombre del header Content-Disposition
  async function downloadFromResponse(resp) {
    const blob = await resp.blob();

    // intentar obtener el nombre desde Content-Disposition
    const cd = resp.headers.get("Content-Disposition") || "";
    let filename = "archivo.xml";
    const match = /filename\*=UTF-8''([^;]+)|filename="?([^"]+)"?/i.exec(cd);
    if (match) {
      filename = decodeURIComponent(match[1] || match[2] || filename);
    }

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  // Enviar al backend
  frm.addEventListener("submit", async (ev) => {
    ev.preventDefault();

    const isGuias = rbGuias.checked;
    const ruc = rucInput.value.trim();
    const serie = serieInput.value.trim();
    const correlativo = corrInput.value.trim();

    // Validaciones mínimas
    if (!serie || !correlativo) {
      alert("Serie y Correlativo/Número son obligatorios.");
      return;
    }
    if (!isGuias && !ruc) {
      alert("RUC es obligatorio para Comprobantes.");
      return;
    }

    // Endpoint y payload según tipo
    let url = "/api/comprobantes";
    let payload = { rucEmisor: ruc, serie, correlativo };

    if (isGuias) {
      url = "/api/guias";
      // Para guías NO enviamos ruc; backend recibe {serie, numero}
      payload = { serie, numero: correlativo };
    }

    // Deshabilitar botón para evitar doble click
    const btn = document.getElementById("btnDescargar");
    btn.disabled = true;
    btn.textContent = "Procesando...";

    try {
      const resp = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!resp.ok) {
        const txt = await resp.text();
        throw new Error(txt || "Error en la descarga.");
      }

      await downloadFromResponse(resp);
    } catch (err) {
      console.error(err);
      alert("No se pudo completar la descarga.\n" + (err?.message || err));
    } finally {
      btn.disabled = false;
      btn.textContent = "Descargar";
    }
  });
})();

(function () {
  // ====== Overlay helpers ======
  const overlay = document.getElementById("loadingOverlay");
  const overlayText = document.getElementById("loadingText");

  function showLoading(text = "Procesando…") {
    overlayText.textContent = text;
    overlay.style.display = "flex";
  }
  function hideLoading() {
    overlay.style.display = "none";
  }

  // ====== UI y formulario ======
  const frm = document.getElementById("frmDescarga");
  const rbComprobantes = document.getElementById("comprobantes");
  const rbGuias = document.getElementById("guias");
  const grpRuc = document.getElementById("grpRuc");
  const lblCorrelativo = document.getElementById("lblCorrelativo");

  const rucInput = document.getElementById("ruc");
  const serieInput = document.getElementById("serie");
  const corrInput = document.getElementById("correlativo");
  const btn = document.getElementById("btnDescargar");

  function updateUiByTipo() {
    const isGuias = rbGuias.checked;
    grpRuc.classList.toggle("d-none", isGuias);
    lblCorrelativo.textContent = isGuias ? "Número" : "Correlativo";
    if (isGuias) rucInput.value = "";
  }
  rbComprobantes.addEventListener("change", updateUiByTipo);
  rbGuias.addEventListener("change", updateUiByTipo);
  updateUiByTipo();

  // Descarga desde response (cierra overlay al final)
  async function downloadFromResponse(resp) {
    const blob = await resp.blob();

    // Nombre desde Content-Disposition
    const cd = resp.headers.get("Content-Disposition") || "";
    let filename = "archivo.xml";
    const m = /filename\*=UTF-8''([^;]+)|filename="?([^"]+)"?/i.exec(cd);
    if (m) filename = decodeURIComponent(m[1] || m[2] || filename);

    const url = URL.createObjectURL(blob);
    try {
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      // dar un frame para que el navegador inicie la descarga
      await new Promise(r => requestAnimationFrame(r));
    } finally {
      URL.revokeObjectURL(url);
      hideLoading();  // <-- cierre aquí también
    }
  }

  frm.addEventListener("submit", async (ev) => {
    ev.preventDefault();

    const isGuias = rbGuias.checked;
    const ruc = rucInput.value.trim();
    const serie = serieInput.value.trim();
    const correlativo = corrInput.value.trim();

    if (!serie || !correlativo) {
      alert("Serie y Correlativo/Número son obligatorios.");
      return;
    }
    if (!isGuias && !ruc) {
      alert("RUC es obligatorio para Comprobantes.");
      return;
    }

    let url = "/api/comprobantes";
    let payload = { rucEmisor: ruc, serie, correlativo };
    let msg = "Consultando comprobante…";

    if (isGuias) {
      url = "/api/guias";
      payload = { serie, numero: correlativo };
      msg = "Consultando guía…";
    }

    btn.disabled = true;
    btn.textContent = "Procesando…";
    showLoading(msg);

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

      await downloadFromResponse(resp); // hideLoading() se llama dentro
    } catch (err) {
      console.error(err);
      alert("No se pudo completar la descarga.\n" + (err?.message || err));
      hideLoading(); // cierre de respaldo
    } finally {
      btn.disabled = false;
      btn.textContent = "Descargar";
    }
  });
})();

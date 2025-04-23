function ajustarLayout() {
    const app = document.getElementById("app");
    const larguraTela = window.innerWidth;

    if (larguraTela < 500) {
      app.classList.add("mobile-view");
    } else {
      app.classList.remove("mobile-view");
    }
  }

  // Executa no carregamento
  ajustarLayout();

  // Executa sempre que a janela for redimensionada
  window.addEventListener("resize", ajustarLayout);
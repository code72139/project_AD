class FavoritoService {
  static async agregar(atractivoId) {
    const response = await fetch("/api/favoritos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ atractivo_id: parseInt(atractivoId) }),
    });
    return response.json();
  }

  static async eliminar(idFavorito) {
    const response = await fetch(`/api/favoritos/${idFavorito}`, {
      method: "DELETE",
    });
    return response.json();
  }
}

class ComentarioService {
  static async listar(atractivoId, page = 1, perPage = 10) {
    const response = await fetch(`/comentarios/atractivo/${atractivoId}?page=${page}&per_page=${perPage}`);
    return response.json();
  }

  static async agregar(atractivoId, texto) {
    const response = await fetch("/comentarios", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ atractivo_id: atractivoId, texto }),
    });
    return response.json();
  }

  static async editar(idComentario, texto) {
    const response = await fetch(`/comentarios/${idComentario}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ texto }),
    });
    return response.json();
  }

  static async eliminar(idComentario) {
    const response = await fetch(`/comentarios/${idComentario}`, {
      method: "DELETE",
    });
    return response.json();
  }
}

class ComentarioItem {
  constructor(comentario, onEliminar, onEditar) {
    this.comentario = comentario;
    this.onEliminar = onEliminar;
    this.onEditar = onEditar;
    this.element = this.render();
  }

  render() {
    const div = document.createElement("div");
    div.classList.add("comentario-item");

    div.innerHTML = `
      <p>${this.comentario.texto}</p>
      <button class="btn-editar">Editar</button>
      <button class="btn-eliminar">Eliminar</button>
    `;

    div.querySelector(".btn-eliminar").onclick = async () => {
      if (confirm("¿Quieres eliminar este comentario?")) {
        await this.onEliminar(this.comentario.id);
        div.remove();
      }
    };

    div.querySelector(".btn-editar").onclick = async () => {
      const nuevoTexto = prompt("Editar comentario:", this.comentario.texto);
      if (nuevoTexto === null) return;
      if (nuevoTexto.trim() === "") {
        alert("El texto no puede quedar vacío.");
        return;
      }

      const success = await this.onEditar(this.comentario.id, nuevoTexto.trim());
      if (success) {
        this.comentario.texto = nuevoTexto.trim();
        div.querySelector("p").textContent = nuevoTexto.trim();
      }
    };

    return div;
  }
}

class AtractivoItem {
  constructor(data) {
    this.data = data;
    this.idFavorito = data.id_favorito || data.idFavorito || null;
    this.commentPage = 1;
    this.loadingComments = false;
    this.hasMoreComments = true;
    this.element = this.render();
    this.initEvents();
    this.cargarComentarios();
  }

  render() {
    const template = document.getElementById("atractivo-template");
    const clone = template.content.cloneNode(true);
    const contenedor = document.createElement("div");
    contenedor.classList.add("atractivo-wrapper");
    contenedor.appendChild(clone);

    this.btnFavorito = contenedor.querySelector(".btn-favorito");
    this.comentariosLista = contenedor.querySelector(".comentarios-lista");
    this.inputComentario = contenedor.querySelector(".nuevo-comentario");
    this.btnComentar = contenedor.querySelector(".btn-comentar");
    this.atractivoDiv = contenedor.querySelector(".atractivo");

    this.atractivoDiv.dataset.atractivoId = this.data.id_atractivo;
    contenedor.querySelector("h3").textContent = this.data.nombre;
    contenedor.querySelector("p").textContent = this.data.descripcion;

    this.actualizarFavoritoUI(this.data.es_favorito);
    return contenedor;
  }

  initEvents() {
    this.btnFavorito.onclick = () => this.toggleFavorito();
    this.btnComentar.onclick = (event) => {
      event.preventDefault();
      this.agregarComentario();
    };
    const formComentario = this.element.querySelector(".comentario-formulario");
    if (formComentario) {
      formComentario.onsubmit = (event) => {
        event.preventDefault();
        this.agregarComentario();
      };
    }
  }

  async toggleFavorito() {
    try {
      if (this.btnFavorito.classList.contains("favorito-activo")) {
        if (!this.idFavorito) {
          alert("Error: no se encontró el ID del favorito para eliminar.");
          return;
        }
        const result = await FavoritoService.eliminar(this.idFavorito);
        if (result.success || result.mensaje) {
          this.actualizarFavoritoUI(false);
          this.idFavorito = null;
          if (window.location.pathname.includes('/favorito')) {
            this.atractivoDiv.remove();
            const container = document.getElementById('atractivos-lista');
            if (!container.querySelector('.atractivo')) {
              container.innerHTML = "<p>No tienes atractivos guardados en favoritos.</p>";
            }
          }
          alert(result.mensaje || "Favorito eliminado");
        }
      } else {
        const result = await FavoritoService.agregar(this.data.id_atractivo);
        if (result.favorito && result.favorito.id) {
          this.idFavorito = result.favorito.id;
          this.actualizarFavoritoUI(true);
          alert(result.mensaje || "Favorito agregado");
        } else {
          alert("Error al agregar favorito");
        }
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error al procesar la operación de favorito");
    }
  }

  actualizarFavoritoUI(esFavorito) {
    if (esFavorito) {
      this.btnFavorito.textContent = "Quitar de Favoritos";
      this.btnFavorito.classList.add("favorito-activo");
    } else {
      this.btnFavorito.textContent = "Agregar a Favoritos";
      this.btnFavorito.classList.remove("favorito-activo");
    }
    this.btnFavorito.dataset.esFavorito = esFavorito;
  }

  async cargarComentarios(page = this.commentPage) {
    if (this.loadingComments || (!this.hasMoreComments && page > 1)) return;

    try {
      this.loadingComments = true;
      const response = await ComentarioService.listar(this.data.id_atractivo, page);

      if (page === 1) {
        this.comentariosLista.innerHTML = "";
      }

      if (!response.items || !response.items.length) {
        if (page === 1) {
          this.comentariosLista.innerHTML = "<p>No hay comentarios aún.</p>";
        }
        this.hasMoreComments = false;
        return;
      } else {
        const noCommentsMsg = this.comentariosLista.querySelector("p");
        if (page === 1 && noCommentsMsg && noCommentsMsg.textContent === "No hay comentarios aún.") {
          noCommentsMsg.remove();
        }
      }

      const fragment = document.createDocumentFragment();
      response.items.forEach(comentario => {
        const comentarioItem = new ComentarioItem(
          comentario,
          async (id) => {
            const data = await ComentarioService.eliminar(id);
            alert(data.mensaje || data.error || "Error al eliminar comentario.");
            return !!data.mensaje;
          },
          async (id, texto) => {
            const data = await ComentarioService.editar(id, texto);
            if (data.error) {
              alert(data.error);
              return false;
            }
            alert(data.mensaje || "Comentario editado correctamente.");
            return true;
          }
        );
        fragment.appendChild(comentarioItem.element);
      });
      this.comentariosLista.appendChild(fragment);
      this.commentPage = page + 1;
      if (response.items.length < (response.per_page || 10)) {
        this.hasMoreComments = false;
      }

    } catch (error) {
      console.error(`Error cargando comentarios para atractivo ${this.data.id_atractivo}:`, error);
      if (page === 1) this.comentariosLista.innerHTML = "<p>Error al cargar comentarios.</p>";
      this.hasMoreComments = false;
    } finally {
      this.loadingComments = false;
    }
  }

  async agregarComentario() {
    const texto = this.inputComentario.value.trim();
    if (!texto) {
      alert("El comentario no puede estar vacío.");
      return;
    }

    try {
      const nuevoComentario = await ComentarioService.agregar(this.data.id_atractivo, texto);
      this.inputComentario.value = "";

      if (nuevoComentario && nuevoComentario.id) {
        const noCommentsMsg = this.comentariosLista.querySelector("p");
        if (noCommentsMsg && (noCommentsMsg.textContent === "No hay comentarios aún." || noCommentsMsg.textContent === "Error al cargar comentarios.")) {
          noCommentsMsg.remove();
        }

        const comentarioItem = new ComentarioItem(
          nuevoComentario,
          async (id) => {
            const data = await ComentarioService.eliminar(id);
            alert(data.mensaje || data.error || "Error al eliminar comentario.");
            return !!data.mensaje;
          },
          async (id, nuevoTexto) => {
            const data = await ComentarioService.editar(id, nuevoTexto);
            if (data.error) {
              alert(data.error);
              return false;
            }
            alert(data.mensaje || "Comentario editado correctamente.");
            return true;
          }
        );
        this.comentariosLista.appendChild(comentarioItem.element);
      } else {
        alert(nuevoComentario.error || "No se pudo agregar el comentario.");
      }
    } catch (error) {
      console.error("Error agregando comentario:", error);
      alert("Error al enviar el comentario.");
    }
  }
}

class AtractivoList {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.page = 1;
    this.loading = false;
    this.hasMore = true;
    this.sentinel = document.createElement("div");
    this.sentinel.id = "loading-sentinel";
    this.sentinel.style.height = "1px";
    this.container.appendChild(this.sentinel);
    this.initInfiniteScroll();
    this.cargar();
  }

  async cargar() {
    if (this.loading || !this.hasMore) return;

    try {
      this.loading = true;
      const response = await fetch(`/atractivos?page=${this.page}&per_page=20`);
      if (!response.ok) throw new Error("Error al cargar atractivos");
      const data = await response.json();

      const atractivos = data.items || [];
      if (!atractivos.length) {
        if (this.page === 1) this.container.innerHTML = "<p>No hay atractivos disponibles.</p>";
        this.hasMore = false;
        return;
      }

      const fragment = document.createDocumentFragment();
      atractivos.forEach(a => {
        const item = new AtractivoItem(a);
        fragment.appendChild(item.element);
      });
      this.container.insertBefore(fragment, this.sentinel);

      this.hasMore = data.metadata ? this.page < data.metadata.total_pages : atractivos.length === 20;
      this.page += 1;
    } catch (err) {
      console.error("Error:", err);
      alert(err.message);
    } finally {
      this.loading = false;
    }
  }

  initInfiniteScroll() {
    const observer = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && !this.loading && this.hasMore) {
        this.cargar();
      }
    });
    observer.observe(this.sentinel);
  }
}

class FavoritosList {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    if (!this.container) {
      console.error(`Contenedor con ID '${containerId}' no encontrado.`);
      return;
    }
    this.page = 1;
    this.loading = false;
    this.hasMore = true;

    this.sentinel = document.createElement("div");
    this.sentinel.id = "favoritos-loading-sentinel";
    this.sentinel.style.height = "1px";
    this.container.appendChild(this.sentinel);

    this.initInfiniteScroll();
    this.cargar();
  }

  async cargar() {
    if (this.loading || !this.hasMore) return;

    this.loading = true;
    try {
      if (this.page === 1) {
        let child = this.container.firstChild;
        while (child && child !== this.sentinel) {
          const nextChild = child.nextSibling;
          this.container.removeChild(child);
          child = nextChild;
        }
      }

      const response = await fetch(`/api/favoritos?page=${this.page}&per_page=20`);
      if (!response.ok) throw new Error(`Error al cargar favoritos (${response.status})`);
      const data = await response.json();
      const favoritos = data.favoritos || [];

      if (!favoritos.length) {
        this.hasMore = false;
        if (this.page === 1 && !this.container.querySelector(".atractivo-wrapper")) {
          const noFavoritosMessage = document.createElement('p');
          noFavoritosMessage.textContent = "No tienes atractivos guardados en favoritos.";
          if (this.sentinel.parentNode === this.container) {
            this.container.insertBefore(noFavoritosMessage, this.sentinel);
          } else {
            this.container.appendChild(noFavoritosMessage);
          }
        }
        if (this.sentinel.parentNode === this.container) {
          this.sentinel.remove();
        }
        return;
      }

      const existingMessage = Array.from(this.container.childNodes).find(node => node.nodeName === 'P' && node !== this.sentinel && !node.closest('.atractivo-wrapper'));
      if (existingMessage) {
        existingMessage.remove();
      }

      const fragment = document.createDocumentFragment();
      favoritos.forEach(fav => {
        const atractivoData = {
          id_atractivo: fav.atractivo.id,
          nombre: fav.atractivo.nombre,
          descripcion: fav.atractivo.descripcion,
          es_favorito: true,
          id_favorito: fav.id
        };
        const item = new AtractivoItem(atractivoData);
        fragment.appendChild(item.element);
      });
      this.container.insertBefore(fragment, this.sentinel);

      this.hasMore = data.total_pages ? this.page < data.total_pages : favoritos.length === 20;
      if (!this.hasMore && this.sentinel.parentNode === this.container) {
        this.sentinel.remove();
      }
      this.page += 1;

    } catch (error) {
      console.error("Error cargando favoritos:", error);
      this.hasMore = false;
      if (this.sentinel.parentNode === this.container) {
        this.sentinel.remove();
      }
      const hasContent = this.container.querySelector(".atractivo-wrapper");
      if (this.page === 1 && !hasContent) {
        let child = this.container.firstChild;
        while (child && child !== this.sentinel && child.id !== "favoritos-loading-sentinel") {
          const nextChild = child.nextSibling;
          this.container.removeChild(child);
          child = nextChild;
        }
        const errorMessage = document.createElement('p');
        errorMessage.textContent = `Error al cargar favoritos: ${error.message}`;
        const currentSentinel = document.getElementById("favoritos-loading-sentinel");
        if (currentSentinel && currentSentinel.parentNode === this.container) {
          this.container.insertBefore(errorMessage, currentSentinel);
        } else {
          this.container.appendChild(errorMessage);
        }
      } else if (this.page > 1) {
        alert(`Error al cargar más favoritos: ${error.message}`);
      }
    } finally {
      this.loading = false;
    }
  }

  initInfiniteScroll() {
    if (!this.container || !document.getElementById(this.sentinel.id) || this.sentinel.parentNode !== this.container) {
      if (this.hasMore) {
      }
      return;
    }

    const observer = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && !this.loading && this.hasMore) {
        this.cargar();
      }
    }, {
      root: null,
      threshold: 0.1
    });
    observer.observe(this.sentinel);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const listaId = "atractivos-lista";

  if (window.location.pathname.endsWith("/favoritos")) {
    new FavoritosList(listaId);
  } else {

    new AtractivoList(listaId);
  }
});

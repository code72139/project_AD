// Servicio para operaciones CRUD de favoritos
class FavoritoService {
  static async agregar(atractivoId) {
    const response = await fetch("/favoritos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ atractivo_id: parseInt(atractivoId) }),
    });
    return response.json();
  }
  static async eliminar(idFavorito) {
    const response = await fetch(`/favoritos/${idFavorito}`, { method: "DELETE" });
    return response.json();
  }
}

// Servicio para operaciones CRUD de comentarios
class ComentarioService {
  static async listar(atractivoId) {
    const response = await fetch(`/comentarios/atractivo/${atractivoId}`);
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

// Componente para un atractivo
class AtractivoItem {
  constructor(data) {
    this.data = data;
    this.idFavorito = data.id_favorito || data.idFavorito || null;
    this.element = this.render();
    this.initEvents();
    this.cargarComentarios();
  }
  render() {
    const template = document.getElementById("atractivo-template");
    const clone = template.content.cloneNode(true);
    this.btnFavorito = clone.querySelector(".btn-favorito");
    this.comentariosLista = clone.querySelector(".comentarios-lista");
    this.inputComentario = clone.querySelector(".nuevo-comentario");
    this.btnComentar = clone.querySelector(".btn-comentar");
    this.atractivoDiv = clone.querySelector(".atractivo");
    this.atractivoDiv.dataset.atractivoId = this.data.id_atractivo;
    clone.querySelector("h3").textContent = this.data.nombre;
    clone.querySelector("p").textContent = this.data.descripcion;
    this.actualizarFavoritoUI(this.data.es_favorito);
    return clone;
  }
  initEvents() {
    this.btnFavorito.onclick = () => this.toggleFavorito();
    this.btnComentar.onclick = () => this.agregarComentario();
  }
  async toggleFavorito() {
    if (this.btnFavorito.classList.contains("favorito-activo")) {
      if (!this.idFavorito) {
        alert("Error: no se encontró el ID del favorito para eliminar.");
        return;
      }
      const result = await FavoritoService.eliminar(this.idFavorito);
      this.actualizarFavoritoUI(false);
      this.idFavorito = null;  // Ya no está favorito
      alert(result.mensaje || "Favorito eliminado");
    } else {
      const result = await FavoritoService.agregar(this.data.id_atractivo);

      if (result.favorito && result.favorito.id) {
        this.idFavorito = result.favorito.id;  // Guardamos el ID que retorna el backend
        this.actualizarFavoritoUI(true);
        alert(result.mensaje || "Favorito agregado");
      } else {
        alert("Error al agregar favorito");
      }
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
  }

  async cargarComentarios() {
    const comentarios = await ComentarioService.listar(this.data.id_atractivo);
    this.comentariosLista.innerHTML = "";

    if (!comentarios.length) {
      this.comentariosLista.innerHTML = "<p>No hay comentarios aún.</p>";
      return;
    }

    const fragment = document.createDocumentFragment();

    comentarios.forEach((comentario) => {
      const comentarioItem = new ComentarioItem(
        comentario,
        async (idComentario) => {
          const data = await ComentarioService.eliminar(idComentario);
          alert(data.mensaje || data.error);
        },
        async (idComentario, nuevoTexto) => {
          const data = await ComentarioService.editar(idComentario, nuevoTexto);
          if (data.error) {
            alert(data.error);
            return false;
          }
          alert("Comentario editado correctamente.");
          return true;
        }
      );
      fragment.appendChild(comentarioItem.element);
    });

    this.comentariosLista.appendChild(fragment);
  }

  async agregarComentario() {
    const texto = this.inputComentario.value.trim();
    if (!texto) return;

    const nuevoComentario = await ComentarioService.agregar(this.data.id_atractivo, texto);
    this.inputComentario.value = "";

    if (nuevoComentario && nuevoComentario.id) {
      const comentarioItem = new ComentarioItem(
        nuevoComentario,
        async (idComentario) => {
          const data = await ComentarioService.eliminar(idComentario);
          alert(data.mensaje || data.error);
        },
        async (idComentario, nuevoTexto) => {
          const data = await ComentarioService.editar(idComentario, nuevoTexto);
          if (data.error) {
            alert(data.error);
            return false;
          }
          alert("Comentario editado correctamente.");
          return true;
        }
      );
      this.comentariosLista.appendChild(comentarioItem.element);
    }
  }


}

class ComentarioItem {
  constructor(comentario, onEliminar, onEditar) {
    this.comentario = comentario;
    this.onEliminar = onEliminar; // callback para eliminar
    this.onEditar = onEditar; // callback para editar
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


// Componente para la lista de atractivos
class AtractivoList {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
  }
  async cargar() {
    try {
      const response = await fetch("/atractivos");
      if (!response.ok) throw new Error("Error al cargar atractivos");
      const atractivos = await response.json();
      this.container.innerHTML = "";
      if (!atractivos.length) {
        this.container.innerHTML = "<p>No hay atractivos disponibles.</p>";
        return;
      }

      const fragment = document.createDocumentFragment(); // Crear fragmento para batch insert

      atractivos.forEach((data) => {
        const item = new AtractivoItem(data);
        fragment.appendChild(item.element); // Append a fragment, no al DOM aún
      });

      this.container.appendChild(fragment); // Insertar todo junto al DOM, una sola vez

    } catch (error) {
      mostrarError(error.message);
    }
  }
  async mostrar() {
    try {
      const atractivos = await AtractivoService.obtenerTodos();
      this.container.innerHTML = "";
      atractivos.forEach(data => {
        const atractivoItem = new AtractivoItem(data);
        this.container.appendChild(atractivoItem.elemento);
      });
    } catch (error) {
      mostrarError("Error al cargar los atractivos.", this.container);
    }
  }

  async filtrar(nombre) {
    try {
      const atractivos = await AtractivoService.filtrar(nombre);
      this.container.innerHTML = "";
      atractivos.forEach(data => {
        const atractivoItem = new AtractivoItem(data);
        this.container.appendChild(atractivoItem.elemento);
      });
    } catch (error) {
      mostrarError("Error al cargar los atractivos.", this.container);
    }
  }


}

// Función para mostrar errores
function mostrarError(mensaje) {
  const container = document.getElementById("atractivos-lista");
  container.innerHTML = `<div class="error">${mensaje}</div>`;
}

// Evento de carga del DOM
document.addEventListener("DOMContentLoaded", () => {
  const lista = new AtractivoList("atractivos-lista");
  lista.cargar();
});
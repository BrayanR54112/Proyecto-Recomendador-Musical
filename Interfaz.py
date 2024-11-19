import tkinter as tk
from tkinter import messagebox
import webbrowser
from Recomendador import Pila, RecomendadorMusical

mapa_canciones_youtube = {
    "Vivir Mi Vida - Marc Anthony": "https://www.youtube.com/watch?v=YXnjy5YlDwk",
    "La Bicicleta - Shakira ft. Carlos Vives": "https://www.youtube.com/watch?v=-UV0QGLmYys",
    "Condor Herido - Diomedes Diaz": "https://www.youtube.com/watch?v=abc123def456",
    "We Will Rock You - Queen": "https://www.youtube.com/watch?v=-tJYN-eG1zk",
    "Perfect - Ed Sheeran": "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
}


class InterfazRecomendador:
    def abrir_enlace_youtube(self):
        seleccion = self.lista_canciones.curselection()  # Obtener selección del usuario
        if seleccion:
            cancion = self.lista_canciones.get(seleccion)  # Obtener la canción seleccionada
            enlace = mapa_canciones_youtube.get(cancion)  # Buscar enlace en el diccionario
            if enlace:
                webbrowser.open(enlace)  # Abrir el enlace en el navegador
                messagebox.showinfo("Abriendo YouTube", f"Reproduciendo: {cancion}")
            else:
                messagebox.showerror("Error", "No se encontró un enlace para esta canción.")
        else:
            messagebox.showwarning("Advertencia", "Selecciona una canción de la lista.")
    def __init__(self, root, recomendador):
        self.root = root
        self.recomendador = recomendador
        self.pila = Pila()

        # Configurar ventana principal
        self.root.title("Recomendador Musical")
        self.root.geometry("600x700")  # Tamaño ajustado

        # Frame principal para organizar el contenido
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Sección: Estado emocional
        emocion_frame = tk.Frame(main_frame)
        emocion_frame.pack(fill=tk.X, pady=5)
        tk.Label(emocion_frame, text="¿Cómo te sientes hoy?").pack(side=tk.LEFT, padx=5)
        self.entrada_emocion = tk.Entry(emocion_frame, width=30)
        self.entrada_emocion.pack(side=tk.LEFT, padx=5)
        tk.Button(emocion_frame, text="Obtener recomendaciones", command=self.recomendar_por_emocion).pack(side=tk.LEFT, padx=5)

        # Sección: Canciones recomendadas
        canciones_frame = tk.Frame(main_frame)
        canciones_frame.pack(fill=tk.X, pady=5)
        tk.Label(canciones_frame, text="Canciones recomendadas:").pack(anchor=tk.W, padx=5)
        self.lista_canciones = tk.Listbox(canciones_frame, width=50, height=10)
        self.lista_canciones.pack(padx=5, pady=5)
        tk.Button(canciones_frame, text="Apilar canción seleccionada", command=self.apilar_cancion).pack(pady=5)
        tk.Button(canciones_frame, text="Abrir en YouTube", command=self.abrir_enlace_youtube).pack(pady=5)

        # Sección: Canciones apiladas
        apiladas_frame = tk.Frame(main_frame)
        apiladas_frame.pack(fill=tk.X, pady=5)
        tk.Label(apiladas_frame, text="Canciones apiladas:").pack(anchor=tk.W, padx=5)
        self.lista_apiladas = tk.Listbox(apiladas_frame, width=50, height=10)
        self.lista_apiladas.pack(padx=5, pady=5)

        # Sección: Recomendación por artista
        artista_frame = tk.Frame(main_frame)
        artista_frame.pack(fill=tk.X, pady=5)
        tk.Label(artista_frame, text="Buscar canciones por artista:").pack(side=tk.LEFT, padx=5)
        self.entrada_artista = tk.Entry(artista_frame, width=30)
        self.entrada_artista.pack(side=tk.LEFT, padx=5)
        tk.Button(artista_frame, text="Buscar por artista", command=self.recomendar_por_artista).pack(side=tk.LEFT, padx=5)


    def recomendar_por_emocion(self):
        emocion = self.entrada_emocion.get().strip().lower()
        if not emocion:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un estado emocional.")
            return

        canciones = self.recomendador.recomendar_canciones(emocion)
        self.lista_canciones.delete(0, tk.END)
        if canciones:
            for cancion in canciones:
                self.lista_canciones.insert(tk.END, cancion)
        else:
            messagebox.showinfo("Sin recomendaciones", f"No hay canciones recomendadas para el estado {emocion}.")

    def apilar_cancion(self):
        seleccion = self.lista_canciones.curselection()
        if seleccion:
            cancion = self.lista_canciones.get(seleccion)
            self.pila.apilar(cancion)
            self.lista_apiladas.insert(tk.END, cancion)
        else:
            messagebox.showwarning("Advertencia", "Selecciona una canción para apilar.")

    def recomendar_por_artista(self):
        artista = self.entrada_artista.get().strip()
        if not artista:
            messagebox.showwarning("Advertencia", "Por favor, ingresa el nombre de un artista.")
            return

        canciones = self.recomendador.recomendar_por_artista(artista)
        self.lista_canciones.delete(0, tk.END)
        if canciones:
            for cancion in canciones:
                self.lista_canciones.insert(tk.END, cancion)
        else:
            messagebox.showinfo("Sin recomendaciones", f"No hay canciones recomendadas para el artista {artista}.")


def main():
    recomendador = RecomendadorMusical()
    
    # Agregar canciones de ejemplo
    recomendador.agregar_cancion("feliz", "Vivir Mi Vida - Marc Anthony", "Marc Anthony")
    recomendador.agregar_cancion("feliz", "La Bicicleta - Shakira ft. Carlos Vives", "Shakira")
    recomendador.agregar_cancion("triste", "Condor Herido - Diomedes Diaz", "Diomedes Diaz")
    recomendador.agregar_cancion("energético", "We Will Rock You - Queen", "Queen")
    recomendador.agregar_cancion("relajado", "Perfect - Ed Sheeran", "Ed Sheeran")

    root = tk.Tk()
    interfaz = InterfazRecomendador(root, recomendador)
    root.mainloop()

main()
        

    

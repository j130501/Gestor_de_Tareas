import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class Tarea:
    def __init__(self, titulo, descripcion, fecha, hora):
        self.titulo = titulo
        self.descripcion = descripcion
        self.completada = False
        self.fecha = fecha
        self.hora = hora

    def __str__(self):
        return f"{self.titulo} ({self.fecha} {self.hora})"

    def estado(self):
        return "Completada" if self.completada else "Pendiente"

    def get_datetime(self):
        # Devuelve un objeto datetime para ordenar las tareas por fecha/hora
        return datetime.strptime(f"{self.fecha} {self.hora}", "%d/%m/%Y %H:%M")


class GestorTareas:
    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, titulo, descripcion, fecha, hora):
        if not titulo:
            raise ValueError("El título no puede estar vacío")
        tarea = Tarea(titulo, descripcion, fecha, hora)
        self.tareas.append(tarea)

    def obtener_tareas(self):
        # Ordenar las tareas por fecha y hora
        return sorted(self.tareas, key=lambda tarea: tarea.get_datetime())

    def marcar_completada(self, indice):
        if 0 <= indice < len(self.tareas):
            self.tareas[indice].completada = True
        else:
            raise IndexError("Índice fuera de rango")

    def eliminar_tarea(self, indice):
        if 0 <= indice < len(self.tareas):
            del self.tareas[indice]
        else:
            raise IndexError("Índice fuera de rango")


class GestorTareasGUI:
    def __init__(self, root, gestor):
        self.gestor = gestor
        self.root = root
        self.root.title("Gestor de Tareas")

        # Establecer un diseño más limpio con padding
        self.frame = ttk.Frame(root, padding="15")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # **Encabezado**
        self.encabezado = ttk.Label(self.frame, text="**Gestor de Tareas**", font=("Arial", 16, "bold"))
        self.encabezado.grid(row=0, column=0, columnspan=2, pady=10)

        # **Campos de Entrada**
        self.titulo_label = ttk.Label(self.frame, text="Nombre de la tarea:")
        self.titulo_label.grid(row=1, column=0, sticky=tk.W, pady=5)

        self.titulo_entry = ttk.Entry(self.frame, width=30)
        self.titulo_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

        self.descripcion_label = ttk.Label(self.frame, text="Descripción:")
        self.descripcion_label.grid(row=2, column=0, sticky=tk.W, pady=5)

        self.descripcion_entry = ttk.Entry(self.frame, width=50)
        self.descripcion_entry.grid(row=2, column=1, sticky=tk.W, pady=5)

        self.fecha_label = ttk.Label(self.frame, text="Fecha (DD/MM/YYYY):")
        self.fecha_label.grid(row=3, column=0, sticky=tk.W, pady=5)

        self.fecha_entry = ttk.Entry(self.frame, width=20)
        self.fecha_entry.grid(row=3, column=1, sticky=tk.W, pady=5)

        self.hora_label = ttk.Label(self.frame, text="Hora (HH:MM):")
        self.hora_label.grid(row=4, column=0, sticky=tk.W, pady=5)

        self.hora_entry = ttk.Entry(self.frame, width=10)
        self.hora_entry.grid(row=4, column=1, sticky=tk.W, pady=5)

        # **Botón para agregar tarea**
        self.agregar_btn = ttk.Button(self.frame, text="Agregar Tarea", command=self.agregar_tarea, width=20)
        self.agregar_btn.grid(row=5, column=1, sticky=tk.W, pady=10)

        # **Filtro de tareas**
        self.filtro_label = ttk.Label(self.frame, text="Filtrar tareas:")
        self.filtro_label.grid(row=6, column=0, sticky=tk.W, pady=5)

        self.filtro_combobox = ttk.Combobox(self.frame, values=["Todos", "Pendientes", "Completadas"], width=20)
        self.filtro_combobox.set("Todos")  # Valor por defecto
        self.filtro_combobox.grid(row=6, column=1, sticky=tk.W, pady=5)
        self.filtro_combobox.bind("<<ComboboxSelected>>", self.actualizar_lista)

        # **Lista de tareas**
        self.tareas_listbox = tk.Listbox(self.frame, height=10, width=50)
        self.tareas_listbox.grid(row=7, column=1, sticky=tk.W, pady=5)

        # **Botones de acción**
        self.completar_btn = ttk.Button(self.frame, text="Marcar como Completada", command=self.marcar_completada)
        self.completar_btn.grid(row=8, column=1, sticky=tk.W, pady=5)

        self.eliminar_btn = ttk.Button(self.frame, text="Eliminar Tarea", command=self.eliminar_tarea)
        self.eliminar_btn.grid(row=9, column=1, sticky=tk.W, pady=5)

        # **Botón de salir**
        self.salir_btn = ttk.Button(self.frame, text="Salir", command=self.salir)
        self.salir_btn.grid(row=10, column=1, sticky=tk.W, pady=10)

        # **Actualizar la lista de tareas al inicio**
        self.actualizar_lista()

    def agregar_tarea(self):
        titulo = self.titulo_entry.get()
        descripcion = self.descripcion_entry.get()
        fecha = self.fecha_entry.get()
        hora = self.hora_entry.get()

        # Validación de la fecha y hora
        try:
            datetime.strptime(fecha, "%d/%m/%Y")  # Verificar formato de fecha
        except ValueError:
            messagebox.showerror("Error", "La fecha debe estar en el formato DD/MM/YYYY")
            return

        try:
            datetime.strptime(hora, "%H:%M")  # Verificar formato de hora
        except ValueError:
            messagebox.showerror("Error", "La hora debe estar en el formato HH:MM")
            return

        try:
            self.gestor.agregar_tarea(titulo, descripcion, fecha, hora)
            self.actualizar_lista()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def actualizar_lista(self, event=None):
        self.tareas_listbox.delete(0, tk.END)
        filtro = self.filtro_combobox.get()

        for indice, tarea in enumerate(self.gestor.obtener_tareas()):
            if filtro == "Todos" or (filtro == "Pendientes" and not tarea.completada) or (filtro == "Completadas" and tarea.completada):
                estado = tarea.estado()
                self.tareas_listbox.insert(tk.END, f"{indice + 1}. {tarea.titulo} - {estado} - {tarea.fecha} {tarea.hora}")

    def marcar_completada(self):
        seleccion = self.tareas_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            self.gestor.marcar_completada(indice)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para marcar como completada")

    def eliminar_tarea(self):
        seleccion = self.tareas_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            self.gestor.eliminar_tarea(indice)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para eliminar")

    def salir(self):
        """Función para confirmar la salida de la aplicación"""
        resultado = messagebox.askquestion("Salir", "¿Está seguro que desea salir?")
        if resultado == "yes":
            self.root.quit()

def run():
    root = tk.Tk()
    gestor = GestorTareas()
    app = GestorTareasGUI(root, gestor)
    root.mainloop()

if __name__ == "__main__":
    run()

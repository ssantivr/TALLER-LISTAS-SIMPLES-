# Modern To-Do List

Aplicación de lista de tareas en **Python puro** con interfaz gráfica **Tkinter** en modo oscuro. Las tareas se almacenan en una **lista enlazada simple implementada a mano**, sin usar listas, diccionarios ni conjuntos de Python para guardar o gestionar los nodos.

Proyecto académico de Ingeniería de Software (4.º semestre) enfocado en estructuras de datos y programación orientada a objetos.

---

## Características

- Agregar, completar, editar y eliminar tareas.
- Filtros **All / Pending / Completed** con contador en cada uno.
- Barra de progreso animada con porcentaje de tareas completadas.
- Edición en línea: doble clic sobre el título (Enter guarda, Escape cancela).
- Botón **Clear completed** para borrar todas las tareas terminadas de una vez.
- Estados vacíos personalizados según el filtro activo.
- Scroll con rueda del ratón y barra de desplazamiento oscura que se oculta cuando no hace falta.
- Validación visual: si intentas agregar una tarea vacía, el campo parpadea en rojo.
- Multiplataforma (Windows, macOS, Linux): usa widgets propios dibujados en `Canvas` y elige automáticamente una fuente disponible.

---

## Requisitos

- **Python 3.8 o superior**
- **Tkinter** (incluido con Python en Windows y macOS)
- Sin dependencias externas: solo se usa la biblioteca estándar.

En Linux, si Tkinter no está instalado:

```bash
sudo apt install python3-tk
```

---

## Instalación y ejecución

```bash
unzip todo_app.zip
cd todo_app
python main.py
```

En algunos sistemas el comando es `python3 main.py`.

---

## Uso

| Acción | Cómo hacerlo |
|---|---|
| Agregar tarea | Escribir en el campo y presionar **Enter** o el botón **Add** |
| Completar / reabrir | Clic en el círculo a la izquierda de la tarea |
| Editar título | **Doble clic** sobre el texto; **Enter** guarda, **Esc** cancela |
| Eliminar | Clic en la **✕** a la derecha de la tarea |
| Filtrar | Pestañas **All**, **Pending** o **Completed** |
| Limpiar terminadas | Botón **Clear completed** (se activa si hay tareas completadas) |

---

## Estructura del proyecto

```
todo_app/
├── main.py                 Punto de entrada (clase Application)
│
├── task_node.py            Nodo de la lista (TaskNode)
├── singly_linked_list.py   Lista enlazada simple (SinglyLinkedList)
├── task_filter.py          Reglas de filtrado (TaskFilter)
│
├── todo_view.py            Ventana principal, coordina todos los componentes
├── header_view.py          Título, fecha, resumen y barra de progreso
├── input_field.py          Campo de texto con placeholder y validación visual
├── filter_bar.py           Selector All / Pending / Completed
├── task_row_view.py        Tarjeta de una tarea (con edición en línea)
├── footer_view.py          Contador de tareas y botón Clear completed
├── empty_state_view.py     Mensaje cuando no hay tareas que mostrar
│
├── scrollable_frame.py     Contenedor con scroll y barra oscura
├── rounded_button.py       Botón redondeado dibujado en Canvas
├── progress_bar.py         Barra de progreso animada
├── check_circle.py         Casilla circular de completado
├── shapes.py               Generador de formas redondeadas (ShapeFactory)
│
├── theme.py                Paleta de colores (Theme)
└── font_set.py             Tipografías (FontSet)
```

---

##
- Fechas límite y prioridades por tarea.
- Búsqueda por texto.
- Pruebas unitarias de `SinglyLinkedList` con `unittest`.

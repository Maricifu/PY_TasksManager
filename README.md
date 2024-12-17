# Task Manager

Link a la app: [Cute Task Manager](https://cute-task-manager.streamlit.app/)

Interfaz del gestor de tareas:

![Task Manager Interface 1](https://github.com/Maricifu/PY_TasksManager/blob/main/Resources/image1.png?raw=true)
> Imagen de referencia de la interfaz para la función principal del gestor de tareas

![Task Manager Interface 2](https://github.com/Maricifu/PY_TasksManager/blob/main/Resources/image2.png?raw=true)
> Imagen de referencia de la interfaz de la función de listar tareas

![Task Manager Interface 3](https://github.com/Maricifu/PY_TasksManager/blob/main/Resources/image3.png?raw=true)
> Imagen de referencia de la interfaz de la función para marcar, editar y eliminar tarea

![Task Manager Interface 4](https://github.com/Maricifu/PY_TasksManager/blob/main/Resources/image4.png?raw=true)
> Imagen de referencia de la interfaz para eliminar tareas completadas, exportar tareas creadas e importar tareas en formato .JSON

Esctructura del directorio de distribución:

```bash
TasksManager/
├── requirements.txt        # dependencias a instalar
├── Resources/
│   └── (.png)              # recursos para el repo
├── main.py                 # source code
├── tasks.db                # archivo db de la app
└── tasks.json              # archivo json de la app
```

Pasos para iniciar el proyecto desde el código fuente en tu IDE:

## 1. Instalar Python

- Descarga Python desde la página oficial: python.org/downloads.
- Durante la instalación, asegúrate de seleccionar "Add Python to PATH".

    ```bash
    python --version
    ```

- En macOS/Linux:

    ```bash
    python3 --version
    ```

## 2. Instalar Visual Studio Code (o IDE de preferencia)

- Descarga e instala Visual Studio Code.
- Instala la extensión Python en VS Code:
  - Abre VS Code.
  - Ve a la pestaña Extensiones (icono de cuadritos en el lado izquierdo o ``Ctrl+Shift+X``).
  - Busca Python e instálala.

## 3. Configurar un entorno virtual

Es recomendable usar un entorno virtual para instalar las dependencias del proyecto sin afectar el sistema global o activa uno si ya lo tienes.

1. Crea un entorno virtual en la carpeta de tu proyecto:

    ```bash
    python -m venv .venv
    ```

    En macOS/Linux:

    ```bash
    python3 -m venv .venv
    ```

2. Activa el entorno virtual:

    - En Windows:

        ```bash
        .venv\Scripts\activate
        ```

    - En macOS/Linux:

        ```bash
        source .venv/bin/activate
        ```

3. Asegúrate de que el entorno está activado; tu terminal debería mostrar algo como ``(.venv)`` al inicio.

## 4. Instalar dependencias

Instala las dependencias (si no las tienes en tu .venv) desde el archivo ubicado en el directorio de distribución usando:

```bash
pip install -r requirements.txt
```

> Asegúrate de estar en el directorio raíz del proyecto

## 5. Ejecutar tu aplicación

Ejecuta tu aplicación desde la terminal con:

```bash
streamlit run main.py
```

Esto abrirá tu aplicación en el navegador. Si usas VS Code, abre el terminal integrado ``(Ctrl+ñ)`` y ejecuta el comando desde ahí.

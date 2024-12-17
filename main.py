import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

st.set_page_config(
    layout="wide"  # Usa el modo de diseño más ancho
)

# Aplicar estilo CSS para que el contenido ocupe todo el ancho
st.markdown(
    """
    <style>
        .st-emotion-cache-5uxhw4 {
            margin-top:20px;
        }
        .st-emotion-cache-1cvow4s h1 {
            color: #b71d62;
        }
        /* Hacer que el contenido ocupe todo el ancho de la pantalla */
        .block-container {
            padding: 19px;
            width: 50%;
            height: auto;  /* Hace que el contenedor ocupe toda la altura visible del navegador */
        }
        
        
        /* Estilo para el pie de página */
        .footer {
            text-align: center;
            padding: 20px;
            font-size: 14px;
            color: #ffffff;
            background-color: #b71d62;
            margin-top: auto;
        }

        .footer a {
            color: #FF8ABE;
            text-decoration: none;
        }

        .footer a:hover {
            text-decoration: underline;
        }
        
        /* Estilo base de los botones */
        .stButton > button {
            color: #fffff; 
            padding: 10px 20px;
            border-radius: 30px;
            cursor: pointer;
            transition: background-color 0.3s ease;  /* Transición suave para el cambio de color */
        }

        /* Efecto hover: cuando el mouse pasa sobre el botón */
        .stButton > button:hover {
            background-color: #621339;
            color: #ffff;
            border-color: #390C22;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Configuración de la base de datos
DATABASE_URL = "sqlite:///tasks.db"
Base = declarative_base()

# Modelo de la base de datos
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    relevance = Column(String, default="Normal")

# Inicialización de la base de datos
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Funciones para la gestión de tareas
def add_task(title, description, relevance):
    task = Task(title=title, description=description, relevance=relevance)
    session.add(task)
    session.commit()

def list_tasks():
    return session.query(Task).all()

def mark_task_completed(task_id):
    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        task.completed = not task.completed 
        session.commit()

def delete_task(task_id):
    session.query(Task).filter_by(id=task_id).delete()
    session.commit()
    
def delete_completed_tasks():
    session.query(Task).filter_by(completed=True).delete()
    session.commit()

def export_tasks(file_path):
    tasks = list_tasks()
    tasks_data = [
        {"id": task.id, "title": task.title, "description": task.description, "completed": task.completed}
        for task in tasks
    ]
    with open(file_path, 'w') as f:
        json.dump(tasks_data, f)

def import_tasks(uploaded_file):
    try:
        tasks_data = json.load(uploaded_file)
        for task_data in tasks_data:
            task = Task(
                title=task_data['title'],
                description=task_data['description'],
                completed=task_data['completed'],
                relevance=task_data.get('relevance', "Normal")
            )
            session.add(task)
        session.commit()
    except Exception as e:
        st.error(f"Error al importar tareas: {e}")

# Interfaz con Streamlit
st.title("🌷 Cute Task Manager")

# Agregar una nueva tarea
st.header("Agregar Tarea:")
if "title_input" not in st.session_state:
    st.session_state.title_input = ""
if "desc_input" not in st.session_state:
    st.session_state.desc_input = ""
if "relevance_input" not in st.session_state:
    st.session_state.relevance_input = "Normal"

title = st.text_input("Título de la tarea", key="title_input")
description = st.text_area("Descripción de la tarea", key="desc_input")
relevance = st.selectbox("Relevancia", ["Alta", "Normal", "Baja"], key="relevance_input")

if st.button("🪄 Agregar"):
    if title:
        add_task(title, description, relevance)
        st.success("Tarea agregada exitosamente")
        st.session_state.clear()  # Limpia todo el session_state
        st.rerun()  # Reinicia la aplicación
    else:
        st.error("El título de la tarea es obligatorio")


# Listar todas las tareas con diseño de sticky notes
st.header("Mis Tareas:")
tasks = list_tasks()

for task in tasks:
    with st.container():
        # Sticky note estilo CSS
        sticky_style = f"""
            box-shadow: 4px 4px 8px rgba(96, 1, 43, 0.8);
            padding: 3px;
            border-radius: 8px;
            background-color: {'#7F003B' if task.relevance == 'Alta' else '#831B4B' if task.relevance == 'Normal' else '#833157'};
            width: 100%;
            min-height: auto;
            position: relative;
        """

        # Contenido del sticky note
        st.markdown(
            f"""
            <div style="{sticky_style}">
                <h5 style="color: #fff; font-weight: bold;">{task.title} ({task.relevance})</h5>
                <p style="color: #e4e4e4; font-size: 14px;">{task.description}</p>
                <p style="color: #ffb5c8; font-style: italic;">
                    Status: {"Completada" if task.completed else "Pendiente"}
                </p>
            </div>
            """, unsafe_allow_html=True
        )

        # Crear botones en una fila alineada (ver, editar, eliminar)
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:  # Botón verde - completar tarea
            if st.button("✔️ Marcar tarea cómo completada", key=f"complete_{task.id}"):
                mark_task_completed(task.id)
                st.rerun()
        with col2:  # Botón azul - editar tarea
            if st.button("✏️ Editar", key=f"edit_{task.id}"):
                st.session_state.editing_task = task.id
                st.rerun()
        with col3:  # Botón rojo - eliminar tarea
            if st.button("🗑️ Eliminar", key=f"delete_{task.id}"):
                delete_task(task.id)
                st.rerun()
                
        # Funcionalidad de edición (modal)
        if "editing_task" in st.session_state:
            editing_task = session.query(Task).filter_by(id=st.session_state.editing_task).first()
            st.header("Editar Tarea")
            updated_title = st.text_input("Nuevo Título", value=editing_task.title)
            updated_desc = st.text_area("Nueva Descripción", value=editing_task.description)
            updated_relevance = st.selectbox("Relevancia", ["Alta", "Normal", "Baja"], index=["Alta", "Normal", "Baja"].index(editing_task.relevance))

            if st.button("Guardar Cambios"):
                editing_task.title = updated_title
                editing_task.description = updated_desc
                editing_task.relevance = updated_relevance
                session.commit()
                del st.session_state.editing_task
                st.success("Tarea actualizada exitosamente")
                st.rerun()


# Eliminar tareas completadas
st.header("Eliminar Tareas Completadas:")
if st.button("💖 Eliminar Tareas Completadas"):
    delete_completed_tasks()
    st.success("Tareas completadas eliminadas")
    st.rerun()

# Exportar e importar tareas
st.header("Exportar e Importar Tareas:")
export_file = st.text_input("Nombre del archivo para exportar (e.g., tasks.json)")
if st.button("✨ Exportar mis Tareas"):
    if export_file:
        if not export_file.endswith(".json"):
            export_file += ".json"
        export_tasks(export_file)
        st.success(f"Tareas exportadas a {export_file}")
    else:
        st.error("Por favor, proporciona un nombre de archivo válido")

uploaded_file = st.file_uploader("Selecciona un archivo JSON para importar tareas")
if uploaded_file is not None:
    if st.button("Importar Tareas"):
        try:
            tasks_data = json.load(uploaded_file)
            for task_data in tasks_data:
                task = Task(
                    title=task_data['title'],
                    description=task_data['description'],
                    completed=task_data.get('completed', False),
                    relevance=task_data.get('relevance', "Normal")
                )
                session.add(task)
            session.commit()
            st.success("Tareas importadas exitosamente")
            st.rerun()
        except Exception as e:
            st.error(f"Error al importar tareas: {e}")
                     
    if "tasks" not in st.session_state:
        st.session_state.tasks = list_tasks()
        
        # actualizar tareas
        st.session_state.tasks = list_tasks()


# Mensaje con enlace a tu perfil de GitHub
st.markdown(
    """
    <div class="footer">
        Desarrollado por <a href="https://github.com/MariCifu" target="_blank">MariCifu 😼</a>
    </div>
    """,
    unsafe_allow_html=True
)

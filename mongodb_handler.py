"""
MongoDB Handler para Portal Sagrado Noche Profunda
Este archivo maneja todas las operaciones de base de datos con MongoDB
"""

import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import json
from datetime import datetime

class MongoDBHandler:
    """Clase para manejar todas las operaciones con MongoDB"""
    
    def __init__(self):
        """Inicializa la conexión a MongoDB"""
        self.client = None
        self.db = None
        self._connect()
    
    def _connect(self):
        """Establece la conexión con MongoDB Atlas"""
        try:
            # Obtener la connection string desde los secrets de Streamlit
            connection_string = st.secrets["mongodb"]["connection_string"]
            
            # Conectar a MongoDB
            self.client = MongoClient(connection_string)
            
            # Seleccionar la base de datos
            self.db = self.client["portal_sagrado"]
            
            # Verificar la conexión
            self.client.admin.command('ping')
            
        except Exception as e:
            st.error(f"❌ Error al conectar con MongoDB: {str(e)}")
            raise
    
    def get_collection(self, collection_name):
        """Obtiene una colección específica"""
        return self.db[collection_name]
    
    # =====================================================
    # FUNCIONES PARA AUTH_CONFIG (Contraseña)
    # =====================================================
    
    def cargar_auth_config(self):
        """Carga la configuración de autenticación"""
        try:
            collection = self.get_collection("auth_config")
            config = collection.find_one({"tipo": "config"})
            
            if not config:
                # Si no existe, crear con contraseña por defecto
                config_default = {
                    "tipo": "config",
                    "password": "portal1058*",
                    "fecha_creacion": datetime.now().strftime("%Y-%m-%d"),
                    "ultima_actualizacion": None
                }
                collection.insert_one(config_default)
                return config_default
            
            return config
            
        except Exception as e:
            st.error(f"Error al cargar configuración: {str(e)}")
            return {"password": "portal1058*"}
    
    def guardar_auth_config(self, config):
        """Guarda la configuración de autenticación"""
        try:
            collection = self.get_collection("auth_config")
            config["tipo"] = "config"
            config["ultima_actualizacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            collection.update_one(
                {"tipo": "config"},
                {"$set": config},
                upsert=True
            )
            return True
            
        except Exception as e:
            st.error(f"Error al guardar configuración: {str(e)}")
            return False
    
    # =====================================================
    # FUNCIONES GENÉRICAS PARA CUALQUIER COLECCIÓN
    # =====================================================
    
    def cargar_datos(self, collection_name):
        """Carga todos los documentos de una colección"""
        try:
            collection = self.get_collection(collection_name)
            datos = list(collection.find({}, {"_id": 0}))
            return datos if datos else []
            
        except Exception as e:
            st.error(f"Error al cargar datos de {collection_name}: {str(e)}")
            return []
    
    def guardar_datos(self, collection_name, datos):
        """Guarda datos en una colección (reemplaza todo)"""
        try:
            collection = self.get_collection(collection_name)
            
            # Limpiar la colección
            collection.delete_many({})
            
            # Insertar nuevos datos
            if isinstance(datos, list) and len(datos) > 0:
                collection.insert_many(datos)
            elif isinstance(datos, dict):
                collection.insert_one(datos)
            
            return True
            
        except Exception as e:
            st.error(f"Error al guardar datos en {collection_name}: {str(e)}")
            return False
    
    def agregar_documento(self, collection_name, documento):
        """Agrega un documento a una colección"""
        try:
            collection = self.get_collection(collection_name)
            resultado = collection.insert_one(documento)
            return str(resultado.inserted_id)
            
        except Exception as e:
            st.error(f"Error al agregar documento: {str(e)}")
            return None
    
    def actualizar_documento(self, collection_name, filtro, datos):
        """Actualiza un documento en una colección"""
        try:
            collection = self.get_collection(collection_name)
            collection.update_one(filtro, {"$set": datos}, upsert=True)
            return True
            
        except Exception as e:
            st.error(f"Error al actualizar documento: {str(e)}")
            return False
    
    def eliminar_documento(self, collection_name, filtro):
        """Elimina un documento de una colección"""
        try:
            collection = self.get_collection(collection_name)
            collection.delete_one(filtro)
            return True
            
        except Exception as e:
            st.error(f"Error al eliminar documento: {str(e)}")
            return False
    
    def buscar_documento(self, collection_name, filtro):
        """Busca un documento específico en una colección"""
        try:
            collection = self.get_collection(collection_name)
            documento = collection.find_one(filtro, {"_id": 0})
            return documento
            
        except Exception as e:
            st.error(f"Error al buscar documento: {str(e)}")
            return None

# =====================================================
# INSTANCIA GLOBAL DEL HANDLER
# =====================================================

@st.cache_resource
def get_mongodb_handler():
    """Obtiene la instancia única del handler de MongoDB"""
    return MongoDBHandler()

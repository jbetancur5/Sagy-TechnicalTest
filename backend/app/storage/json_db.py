import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path
import threading


class JSONDatabase:
    """Manejador de base de datos JSON para facturas."""
    
    def __init__(self, db_path: str = "data/invoices.json"):
        """
        Inicializa el manejador de base de datos JSON.
        
        Args:
            db_path: Ruta al archivo JSON de almacenamiento
        """
        self.db_path = db_path
        self.lock = threading.Lock()
        self._ensure_db_exists()
    
    def _ensure_db_exists(self) -> None:
        """Crea el archivo JSON si no existe."""
        # Crear directorio si no existe
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        # Crear archivo con estructura inicial si no existe
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump({"invoices": [], "last_id": 0}, f, indent=2, ensure_ascii=False)
    
    def _read_db(self) -> Dict[str, Any]:
        """
        Lee el contenido completo de la base de datos.
        
        Returns:
            Diccionario con la estructura completa de la BD
        """
        with self.lock:
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Asegurar estructura correcta
                    if "invoices" not in data:
                        data["invoices"] = []
                    if "last_id" not in data:
                        data["last_id"] = 0
                    return data
            except (json.JSONDecodeError, FileNotFoundError):
                # Si hay error, reinicializar
                return {"invoices": [], "last_id": 0}
    
    def _write_db(self, data: Dict[str, Any]) -> None:
        """
        Escribe el contenido completo a la base de datos.
        
        Args:
            data: Diccionario con la estructura completa de la BD
        """
        with self.lock:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add_invoice(self, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agrega una nueva factura a la base de datos.
        
        Args:
            invoice_data: Diccionario con los datos de la factura
            
        Returns:
            Diccionario con la factura creada incluyendo su ID
        """
        db = self._read_db()
        
        # Generar nuevo ID
        new_id = db["last_id"] + 1
        
        # Agregar ID y timestamp
        invoice_data["id"] = new_id
        invoice_data["created_at"] = datetime.now().isoformat()
        
        # Agregar a la lista
        db["invoices"].append(invoice_data)
        db["last_id"] = new_id
        
        # Guardar
        self._write_db(db)
        
        return invoice_data
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las facturas almacenadas.
        
        Returns:
            Lista de diccionarios con todas las facturas
        """
        db = self._read_db()
        return db["invoices"]
    
    def get_by_id(self, invoice_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene una factura específica por su ID.
        
        Args:
            invoice_id: ID de la factura a buscar
            
        Returns:
            Diccionario con la factura o None si no existe
        """
        db = self._read_db()
        for invoice in db["invoices"]:
            if invoice.get("id") == invoice_id:
                return invoice
        return None
    
    def update_invoice(self, invoice_id: int, invoice_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Actualiza una factura existente.
        
        Args:
            invoice_id: ID de la factura a actualizar
            invoice_data: Nuevos datos de la factura
            
        Returns:
            Diccionario con la factura actualizada o None si no existe
        """
        db = self._read_db()
        
        for i, invoice in enumerate(db["invoices"]):
            if invoice.get("id") == invoice_id:
                # Mantener ID y created_at originales
                invoice_data["id"] = invoice_id
                invoice_data["created_at"] = invoice.get("created_at")
                invoice_data["updated_at"] = datetime.now().isoformat()
                
                db["invoices"][i] = invoice_data
                self._write_db(db)
                return invoice_data
        
        return None
    
    def delete_invoice(self, invoice_id: int) -> bool:
        """
        Elimina una factura de la base de datos.
        
        Args:
            invoice_id: ID de la factura a eliminar
            
        Returns:
            True si se eliminó, False si no existía
        """
        db = self._read_db()
        
        initial_length = len(db["invoices"])
        db["invoices"] = [inv for inv in db["invoices"] if inv.get("id") != invoice_id]
        
        if len(db["invoices"]) < initial_length:
            self._write_db(db)
            return True
        
        return False
    
    def count(self) -> int:
        """
        Cuenta el número total de facturas.
        
        Returns:
            Número de facturas almacenadas
        """
        db = self._read_db()
        return len(db["invoices"])


# Instancia global del manejador de base de datos
db = JSONDatabase()

from datetime import datetime
from typing import Optional, Dict, Any


class Invoice:
    """Modelo interno de una factura procesada."""
    
    def __init__(
        self,
        id: int,
        consumo: Optional[float],
        tarifa: Optional[float],
        costo: Optional[float],
        total: Optional[float],
        fecha_emision: Optional[str],
        validaciones: Dict[str, Any],
        raw_text: str,
        filename: str,
        created_at: str
    ):
        self.id = id
        self.consumo = consumo
        self.tarifa = tarifa
        self.costo = costo
        self.total = total
        self.fecha_emision = fecha_emision
        self.validaciones = validaciones
        self.raw_text = raw_text
        self.filename = filename
        self.created_at = created_at
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el modelo a un diccionario."""
        return {
            "id": self.id,
            "consumo": self.consumo,
            "tarifa": self.tarifa,
            "costo": self.costo,
            "total": self.total,
            "fecha_emision": self.fecha_emision,
            "validaciones": self.validaciones,
            "raw_text": self.raw_text,
            "filename": self.filename,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Invoice":
        """Crea una instancia desde un diccionario."""
        return cls(
            id=data["id"],
            consumo=data.get("consumo"),
            tarifa=data.get("tarifa"),
            costo=data.get("costo"),
            total=data.get("total"),
            fecha_emision=data.get("fecha_emision"),
            validaciones=data.get("validaciones", {}),
            raw_text=data.get("raw_text", ""),
            filename=data.get("filename", ""),
            created_at=data.get("created_at", "")
        )

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class InvoiceBase(BaseModel):
    """Schema base para una factura."""
    consumo: Optional[float] = Field(None, description="Consumo en unidades (kWh, m³, etc.)")
    tarifa: Optional[float] = Field(None, description="Tarifa por unidad")
    costo: Optional[float] = Field(None, description="Costo del servicio")
    total: Optional[float] = Field(None, description="Total de la factura")
    fecha_emision: Optional[str] = Field(None, description="Fecha de emisión de la factura")
    tipo_servicio: Optional[str] = Field(None, description="Tipo de servicio (Gas, Agua, Energía, Aseo)")
    raw_text: str = Field(..., description="Texto completo extraído de la factura")


class InvoiceCreate(InvoiceBase):
    """Schema para crear una nueva factura."""
    filename: str = Field(..., description="Nombre del archivo original")
    validaciones: Dict[str, Any] = Field(..., description="Resultado de las validaciones")


class InvoiceResponse(InvoiceBase):
    """Schema de respuesta para una factura."""
    id: int = Field(..., description="ID único de la factura")
    filename: str = Field(..., description="Nombre del archivo original")
    validaciones: Dict[str, Any] = Field(..., description="Resultado de las validaciones")
    created_at: str = Field(..., description="Fecha y hora de creación")
    
    class Config:
        from_attributes = True


class ValidationResult(BaseModel):
    """Schema para el resultado de validaciones."""
    consistency_checks: Dict[str, Any] = Field(..., description="Detalles de las validaciones realizadas")
    passed: bool = Field(..., description="Indica si todas las validaciones pasaron")


class InvoiceProcessResult(BaseModel):
    """Schema para el resultado del procesamiento de una factura."""
    success: bool = Field(..., description="Indica si el procesamiento fue exitoso")
    message: str = Field(..., description="Mensaje descriptivo del resultado")
    invoice: Optional[InvoiceResponse] = Field(None, description="Datos de la factura procesada")
    errors: Optional[list[str]] = Field(None, description="Lista de errores si los hubo")


class ErrorResponse(BaseModel):
    """Schema para respuestas de error."""
    detail: str = Field(..., description="Descripción del error")
    error_type: str = Field(..., description="Tipo de error")

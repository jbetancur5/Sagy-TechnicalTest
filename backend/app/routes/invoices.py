import os
import tempfile
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas import InvoiceResponse, InvoiceProcessResult, ErrorResponse
from app.storage import db
from app.services import invoice_extractor, invoice_validator, ocr_processor


router = APIRouter(
    prefix="/invoices",
    tags=["invoices"]
)


@router.post(
    "/upload",
    response_model=InvoiceProcessResult,
    status_code=status.HTTP_201_CREATED,
    summary="Procesar y cargar una factura",
    description="Recibe un archivo PDF o imagen de factura, extrae datos, valida y almacena"
)
async def upload_invoice(file: UploadFile = File(...)):
    """
    Endpoint para procesar una nueva factura.
    
    Args:
        file: Archivo PDF o imagen de la factura
        
    Returns:
        Resultado del procesamiento con datos extraídos y validaciones
    """
    # Validar que se haya enviado un archivo
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionó ningún archivo"
        )
    
    # Validar formato del archivo
    if not ocr_processor.is_supported_format(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato de archivo no soportado. Use PDF o imágenes (JPG, PNG, etc.)"
        )
    
    # Guardar archivo temporalmente
    temp_file = None
    try:
        # Crear archivo temporal
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            content = await file.read()
            temp.write(content)
            temp_file = temp.name
        
        # Extraer datos de la factura
        extracted_data = invoice_extractor.extract_invoice_data(temp_file)
        
        # Verificar si la extracción fue exitosa
        if not extracted_data.get("extraction_success", False):
            return InvoiceProcessResult(
                success=False,
                message="No se pudo extraer texto del archivo",
                invoice=None,
                errors=[extracted_data.get("error", "Error desconocido")]
            )
        
        # Validar datos extraídos
        validation_result = invoice_validator.validate_invoice(extracted_data)
        
        # Preparar datos para almacenar
        invoice_data = {
            "consumo": extracted_data.get("consumo"),
            "tarifa": extracted_data.get("tarifa"),
            "costo": extracted_data.get("costo"),
            "total": extracted_data.get("total"),
            "fecha_emision": extracted_data.get("fecha_emision"),
            "tipo_servicio": extracted_data.get("tipo_servicio"),
            "raw_text": extracted_data.get("raw_text", ""),
            "filename": file.filename,
            "validaciones": validation_result
        }
        
        # Guardar en la base de datos
        saved_invoice = db.add_invoice(invoice_data)
        
        # Preparar respuesta
        invoice_response = InvoiceResponse(**saved_invoice)
        
        return InvoiceProcessResult(
            success=True,
            message="Factura procesada exitosamente" if validation_result["passed"] else "Factura procesada con advertencias",
            invoice=invoice_response,
            errors=None
        )
        
    except Exception as e:
        # Manejar errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la factura: {str(e)}"
        )
    
    finally:
        # Limpiar archivo temporal
        if temp_file and os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
            except Exception:
                pass


@router.get(
    "",
    response_model=List[InvoiceResponse],
    summary="Listar todas las facturas",
    description="Obtiene todas las facturas almacenadas en el sistema"
)
async def get_all_invoices():
    """
    Endpoint para obtener todas las facturas.
    
    Returns:
        Lista de todas las facturas almacenadas
    """
    try:
        invoices = db.get_all()
        return [InvoiceResponse(**invoice) for invoice in invoices]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las facturas: {str(e)}"
        )


@router.get(
    "/{invoice_id}",
    response_model=InvoiceResponse,
    summary="Obtener una factura específica",
    description="Obtiene los detalles de una factura por su ID"
)
async def get_invoice_by_id(invoice_id: int):
    """
    Endpoint para obtener una factura específica.
    
    Args:
        invoice_id: ID de la factura a buscar
        
    Returns:
        Datos de la factura solicitada
    """
    try:
        invoice = db.get_by_id(invoice_id)
        
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró la factura con ID {invoice_id}"
            )
        
        return InvoiceResponse(**invoice)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la factura: {str(e)}"
        )


@router.get(
    "/stats/summary",
    summary="Obtener estadísticas",
    description="Obtiene estadísticas generales del sistema"
)
async def get_stats():
    """
    Endpoint para obtener estadísticas del sistema.
    
    Returns:
        Estadísticas generales
    """
    try:
        invoices = db.get_all()
        total_invoices = len(invoices)
        
        # Contar facturas válidas
        valid_invoices = sum(
            1 for inv in invoices 
            if inv.get("validaciones", {}).get("passed", False)
        )
        
        # Calcular totales
        total_amount = sum(
            inv.get("total", 0) or 0 
            for inv in invoices
        )
        
        return {
            "total_invoices": total_invoices,
            "valid_invoices": valid_invoices,
            "invalid_invoices": total_invoices - valid_invoices,
            "validation_rate": round((valid_invoices / total_invoices * 100), 2) if total_invoices > 0 else 0,
            "total_amount": round(total_amount, 2)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )

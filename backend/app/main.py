from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import invoices_router


# Crear instancia de FastAPI
app = FastAPI(
    title="Invoice Processing API",
    description="API para procesamiento y validación de facturas de servicios públicos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir routers
app.include_router(invoices_router)


# Endpoint raíz
@app.get(
    "/",
    tags=["root"],
    summary="Health check",
    description="Verifica que el servidor esté funcionando"
)
async def root():
    """
    Endpoint raíz para verificar el estado del servidor.
    
    Returns:
        Mensaje de bienvenida y estado del servicio
    """
    return {
        "message": "Invoice Processing API",
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs"
    }


# Endpoint de salud
@app.get(
    "/health",
    tags=["health"],
    summary="Health check endpoint",
    description="Verifica el estado de salud del servidor"
)
async def health_check():
    """
    Endpoint de salud para monitoreo.
    
    Returns:
        Estado de salud del servicio
    """
    return {
        "status": "healthy",
        "service": "invoice-processing-api"
    }


# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Manejador global de excepciones no capturadas.
    
    Args:
        request: Request de FastAPI
        exc: Excepción capturada
        
    Returns:
        Respuesta JSON con el error
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Error interno del servidor",
            "error": str(exc)
        }
    )


# Ejecutar con: uvicorn app.main:app --reload --port 8001
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )

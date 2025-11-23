# Sistema de Procesamiento de Facturas 

Sistema completo para el procesamiento automático de facturas eléctricas utilizando FastAPI y React. Extrae información clave, valida datos y proporciona una interfaz moderna para gestionar facturas.

## Características

- **Extracción inteligente con PDFPLUMBER, PYTESSERACT y REGEX**: Utilizadas para extraer, leer y buscar patrones de datos de facturas en PDF o imágenes
- **Validación automática**: Verifica consistencia de datos extraídos
- **Interfaz moderna**: Frontend en React con TailwindCSS 
- **Gestión completa**: Lista, visualiza y procesa múltiples facturas
- **API RESTful**: Backend robusto con FastAPI
- **Persistencia**: Almacenamiento en archivo JSON


## Stack Tecnológico

### Backend
- **FastAPI** - Framework web
- **Python** 3.11+
- **python-multipart** - Manejo de archivos
- **python-dotenv** - Variables de entorno

### Frontend
- **React** 19.2.0
- **Vite** 7.2.4 - Build tool
- **TailwindCSS** 4.1.17 - Estilos
- **TypeScript** 5.7.3
- **React Router** Navegación
- **Axios** 1.13.2 - Cliente HTTP
- **Lucide React** - Iconos

## Requisitos Previos

- **Node.js** 20.19+ o 22.12+ (para Vite 7)
- **Python** 3.11 o superior


## 🚀 Instalación y Configuración

### 1️⃣ Clonar el repositorio

``bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo

### Crear entorno virtual:
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

### Instalar dependencias:
pip install -r requirements.txt

### Iniciar el servidor:
uvicorn main:app --reload --port 8001
El backend estará corriendo localmente en: http://localhost:8001

### Configurar Frontend:
En otra terminal:
- cd frontend
- npm install

### Configurar variables de entorno:
Crear archivo .env en la carpeta frontend/:
VITE_API_URL=http://localhost:8001

### Iniciar el servidor de desarrollo:
npm run dev
El frontend estará corriendo en: http://localhost:5173

### Uso
- Abrir la aplicación en el navegador: http://localhost:5173
- Subir factura: Arrastra o selecciona un archivo PDF/imagen de una factura
- Procesar: Haz clic en "Procesar factura" y espera la extracción
- Ver resultados: Revisa los datos extraídos y validaciones
- Gestionar: Accede a todas las facturas procesadas desde "Ver todas las facturas"


## Estructura del Proyecto
```
.
├── backend/
│   ├── main.py              # Punto de entrada FastAPI
│   ├── database.py          # Configuración SQLAlchemy
│   ├── models.py            # Modelos de base de datos
│   ├── schemas.py           # Schemas Pydantic
│   ├── crud.py              # Operaciones CRUD
│   ├── gemini_service.py    # Integración con Gemini AI
│   ├── requirements.txt     # Dependencias Python
│   └── .env                 # Variables de entorno (crear)
│
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Home.tsx           # Página principal (upload)
    │   │   ├── InvoiceList.tsx    # Lista de facturas
    │   │   └── InvoiceDetail.tsx  # Detalle de factura
    │   ├── components/
    │   │   ├── FileUploader.tsx   # Componente de carga
    │   │   ├── InvoiceCard.tsx    # Card de factura
    │   │   └── ValidationBadge.tsx # Badge de validación
    │   ├── services/
    │   │   └── api.ts             # Cliente API
    │   ├── App.tsx                # Router principal
    │   └── index.css              # Estilos globales
    ├── package.json
    └── .env                       # Variables de entorno (crear)
```


## API Endpoints
Backend (Puerto 8001)
| Método   | Endpoint                    | Descripción                     |
|----------|-----------------------------|---------------------------------|
| **POST** | `/invoices/upload`          | Sube y procesa una factura      |
| **GET**  | `/invoices`                 | Lista todas las facturas        |
| **GET**  | `/invoices/{id}`            | Obtiene una factura específica  |
| **GET**  | `/invoices/stats/summary`   | Estadísticas generales          |

Ejemplo de request:
curl -X POST http://localhost:8001/invoices/upload \
  -F "file=@factura.pdf"
  
### Configuración Avanzada
Cambiar puerto del backend
En backend/, modificar el comando de inicio:
uvicorn main:app --reload --port PUERTO_DESEADO
Importante: Si cambias el puerto, actualiza VITE_API_URL en frontend/.env


## Autor
Juanmartin Betancur Arango

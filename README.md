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


## Crear entorno virtual:
python -m venv venv
### Windows
venv\Scripts\activate
### Linux/Mac
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
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # Punto de entrada FastAPI, configuración CORS
│   │   ├── models.py               # Modelos internos de datos
│   │   ├── schemas.py              # Esquemas Pydantic para validación
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── invoices.py         # Endpoints: POST /invoices/upload, GET /invoices, etc.
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ocr.py              # Extracción de texto (pdfplumber + Tesseract OCR)
│   │   │   ├── extractor.py        # Extracción de datos con regex (consumo, tarifa, total, etc.)
│   │   │   └── validator.py        # Validación de coherencia contable
│   │   │
│   │   └── storage/
│   │       ├── __init__.py
│   │       └── json_db.py          # CRUD thread-safe sobre JSON
│   │
│   ├── data/
│   │   └── invoices.json           # Base de datos JSON
│   │
│   ├── requirements.txt            # Dependencias del proyecto
│   ├── .env                        # Variables de entorno (crear)
│   ├── .gitignore
│   └── venv/                       # Entorno virtual (no subir a Git)
│
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Home.tsx                 # Página principal (upload)
    │   │   ├── InvoiceList.tsx          # Lista de facturas
    │   │   └── InvoiceDetail.tsx        # Detalle de factura
    │   ├── components/
    │   │   ├── FileUploader.tsx         # Componente de carga
    │   │   ├── InvoiceCard.tsx          # Card de factura
    │   │   └── ValidationBadge.tsx      # Badge de validación
    │   ├── services/
    │   │   └── api.ts                   # Cliente API + utilidades
    │   ├── App.tsx                      # Router principal
    │   ├── main.tsx                     # Entry point
    │   └── index.css                    # Estilos globales + Tailwind
    ├── public/                          # Assets estáticos
    ├── package.json                     # Dependencias y scripts
    ├── vite.config.ts                   # Configuración Vite
    ├── tailwind.config.js               # Configuración Tailwind
    └── .env 
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

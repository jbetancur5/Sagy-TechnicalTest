# 📊 Procesador de Facturas - Frontend

Sistema profesional de procesamiento de facturas con React + Vite + TailwindCSS conectado a backend FastAPI.

## 🚀 Características

- ✅ Subida de facturas (PDF/Imágenes)
- ✅ Extracción automática de datos
- ✅ Validaciones en tiempo real
- ✅ Vista previa de archivos
- ✅ Historial de facturas
- ✅ Diseño moderno y responsivo
- ✅ Manejo de errores robusto

## 🛠️ Stack Tecnológico

- **React 19** - Framework UI
- **Vite 7** - Build tool
- **TailwindCSS 4** - Estilos
- **TypeScript** - Type safety
- **React Router 7** - Navegación
- **Axios** - Cliente HTTP

## 📁 Estructura del Proyecto

```
frontend/
├── .env                      # Variables de entorno
├── src/
│   ├── components/           # Componentes reutilizables
│   │   ├── FileUploader.tsx  # Subida de archivos
│   │   ├── InvoiceCard.tsx   # Tarjeta de factura
│   │   └── ValidationBadge.tsx # Badge de validación
│   ├── pages/               # Páginas principales
│   │   ├── Home.tsx         # Página de inicio
│   │   ├── InvoiceList.tsx  # Lista de facturas
│   │   └── InvoiceDetail.tsx # Detalle de factura
│   ├── services/            # Servicios API
│   │   └── api.ts           # Cliente API
│   ├── App.tsx              # Componente raíz
│   └── main.tsx             # Punto de entrada
├── tailwind.config.js       # Configuración de Tailwind
└── package.json             # Dependencias
```

## ⚙️ Configuración

### 1. Variables de Entorno

El archivo `.env` ya está creado con:

```env
VITE_API_URL=http://localhost:8000
```

**Importante:** Si tu backend corre en otro puerto, actualiza esta URL.

### 2. Instalación

Las dependencias ya están instaladas. Si necesitas reinstalar:

```bash
npm install
```

## 🏃 Ejecución

### Modo Desarrollo

```bash
npm run dev
```

La aplicación estará disponible en: `http://localhost:5173`

### Build de Producción

```bash
npm run build
```

### Vista Previa de Build

```bash
npm run preview
```

## 📱 Rutas de la Aplicación

| Ruta           | Descripción                                 |
| -------------- | ------------------------------------------- |
| `/`            | Página principal - Subir y procesar factura |
| `/invoices`    | Lista de todas las facturas                 |
| `/invoice/:id` | Detalle de una factura específica           |

## 🔌 API Endpoints Utilizados

### Backend FastAPI

```typescript
POST / invoices / upload; // Subir factura
GET / invoices; // Obtener todas las facturas
GET / invoices / { id }; // Obtener factura específica
```

## 📊 Datos de Factura

Estructura de datos que maneja la aplicación:

```typescript
interface Invoice {
  id: string;
  consumo?: number;
  tarifa?: number;
  costo?: number;
  total?: number;
  fecha_emision?: string;
  raw_text?: string;
  validaciones: {
    [key: string]: "Passed" | "Failed" | string;
  };
  tipo_servicio?: string;
}
```

## 🎨 Componentes Principales

### FileUploader

- Drag & drop de archivos
- Validación de tipos (PDF, PNG, JPG, JPEG)
- Vista previa de imágenes
- Estados de carga

### InvoiceCard

- Resumen visual de factura
- Indicadores de validación
- Información clave destacada
- Navegación a detalle

### ValidationBadge

- Estado visual de validaciones
- ✓ Verde para "Passed"
- ✗ Rojo para "Failed"

## 🎯 Flujo de Uso

1. **Subir Factura** → Selecciona archivo PDF o imagen
2. **Procesar** → Click en "Procesar factura"
3. **Revisar Datos** → Ver información extraída y validaciones
4. **Ver Detalles** → Acceder a información completa
5. **Historial** → Consultar todas las facturas procesadas

## 🔧 Scripts Disponibles

```bash
npm run dev      # Desarrollo con hot-reload
npm run build    # Build de producción
npm run preview  # Vista previa del build
npm run lint     # Linter de código
```

## 🐛 Manejo de Errores

La aplicación incluye:

- ✅ Validación de tipos de archivo
- ✅ Feedback visual de errores
- ✅ Mensajes de error descriptivos
- ✅ Reintentos en caso de fallo
- ✅ Estados de carga consistentes

## 🚀 Despliegue

### Vercel / Netlify

1. Conecta tu repositorio
2. Configura las variables de entorno:
   - `VITE_API_URL=https://tu-backend-url.com`
3. Deploy automático en cada commit

### Build Manual

```bash
npm run build
# Los archivos estáticos estarán en dist/
```

## 📝 Notas Importantes

- El backend debe estar corriendo en `http://localhost:8000` (o la URL configurada en `.env`)
- Los archivos deben ser PDF o imágenes (PNG, JPG, JPEG)
- Tamaño máximo recomendado: 10MB
- CORS debe estar habilitado en el backend

## 🎨 Personalización

### Colores

Edita `tailwind.config.js` para cambiar el esquema de colores:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Personaliza aquí
      }
    }
  }
}
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea tu feature branch
3. Commit tus cambios
4. Push al branch
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de uso libre para fines educativos y comerciales.

---

**¿Problemas?** Asegúrate de que:

- ✅ El backend esté corriendo
- ✅ Las variables de entorno estén configuradas
- ✅ CORS esté habilitado en el backend
- ✅ Las dependencias estén instaladas

**Desarrollado con ❤️ usando React + Vite + TailwindCSS**

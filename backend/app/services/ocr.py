import os
from typing import Optional
from pathlib import Path
import pdfplumber
from PIL import Image
import pytesseract


class OCRProcessor:
    """Procesador de OCR para extraer texto de documentos."""
    
    def __init__(self):
        """Inicializa el procesador OCR."""
        # Configuración de pytesseract para Windows
        # Si Tesseract está instalado en otra ubicación, cambiar esta ruta
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    def extract_from_pdf(self, file_path: str) -> Optional[str]:
        """
        Extrae texto de un archivo PDF usando pdfplumber.
        
        Args:
            file_path: Ruta al archivo PDF
            
        Returns:
            Texto extraído o None si hay error
        """
        try:
            text_content = []
            
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
            
            full_text = "\n".join(text_content)
            
            if not full_text.strip():
                return None
            
            return full_text
            
        except Exception as e:
            print(f"Error al extraer texto del PDF: {str(e)}")
            return None
    
    def extract_from_image(self, file_path: str) -> Optional[str]:
        """
        Extrae texto de una imagen usando pytesseract (OCR).
        
        Args:
            file_path: Ruta al archivo de imagen
            
        Returns:
            Texto extraído o None si hay error
        """
        try:
            # Abrir imagen
            image = Image.open(file_path)
            
            # Configurar pytesseract para español
            custom_config = r'--oem 3 --psm 6 -l spa'
            
            # Realizar OCR
            text = pytesseract.image_to_string(image, config=custom_config)
            
            if not text.strip():
                # Intentar sin configuración personalizada
                text = pytesseract.image_to_string(image)
            
            if not text.strip():
                return None
            
            return text
            
        except Exception as e:
            print(f"Error al extraer texto de la imagen: {str(e)}")
            return None
    
    def extract_text(self, file_path: str) -> Optional[str]:
        """
        Extrae texto de un archivo detectando automáticamente el tipo.
        
        Args:
            file_path: Ruta al archivo (PDF o imagen)
            
        Returns:
            Texto extraído o None si hay error
        """
        if not os.path.exists(file_path):
            print(f"El archivo no existe: {file_path}")
            return None
        
        # Detectar tipo de archivo por extensión
        file_extension = Path(file_path).suffix.lower()
        
        # Extensiones de PDF
        if file_extension == '.pdf':
            return self.extract_from_pdf(file_path)
        
        # Extensiones de imágenes comunes
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif']
        if file_extension in image_extensions:
            return self.extract_from_image(file_path)
        
        # Tipo no soportado
        print(f"Tipo de archivo no soportado: {file_extension}")
        return None
    
    def is_supported_format(self, filename: str) -> bool:
        """
        Verifica si el formato del archivo es soportado.
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            True si el formato es soportado, False en caso contrario
        """
        supported_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif']
        file_extension = Path(filename).suffix.lower()
        return file_extension in supported_extensions


# Instancia global del procesador OCR
ocr_processor = OCRProcessor()

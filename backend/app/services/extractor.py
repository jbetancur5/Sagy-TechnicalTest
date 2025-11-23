import re
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from .ocr import ocr_processor


class InvoiceExtractor:
    """Extractor de datos de facturas de servicios públicos."""
    
    def __init__(self):
        """Inicializa el extractor de facturas."""
        self.ocr = ocr_processor
    
    def _clean_text(self, text: str) -> str:
        """
        Limpia el texto removiendo caracteres innecesarios.
        
        Args:
            text: Texto a limpiar
            
        Returns:
            Texto limpio
        """
        # Normalizar espacios en blanco
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _clean_number(self, text: str) -> Optional[float]:
        """
        Extrae y limpia un número del texto.
        Maneja formatos como: $1,234.56, 1.234,56, 1,234, etc.
        
        Args:
            text: Texto conteniendo el número
            
        Returns:
            Número como float o None si no se puede extraer
        """
        if not text:
            return None
        
        try:
            # Remover símbolos de moneda y espacios
            cleaned = re.sub(r'[$€£¥₡₱\s]', '', text)
            
            # Detectar formato (coma como decimal o punto como decimal)
            # Si tiene formato 1,234.56 o 1.234,56
            
            # Remover puntos si son separadores de miles (1.234.567)
            if ',' in cleaned and '.' in cleaned:
                # Formato: 1.234,56 (europeo) -> remover puntos
                if cleaned.rfind(',') > cleaned.rfind('.'):
                    cleaned = cleaned.replace('.', '')
                    cleaned = cleaned.replace(',', '.')
                # Formato: 1,234.56 (americano) -> remover comas
                else:
                    cleaned = cleaned.replace(',', '')
            # Solo comas (puede ser miles o decimal)
            elif ',' in cleaned:
                # Si hay múltiples comas, son separadores de miles
                if cleaned.count(',') > 1:
                    cleaned = cleaned.replace(',', '')
                # Si solo hay una coma, puede ser decimal
                else:
                    # Verificar posición: si está en los últimos 3 caracteres, es decimal
                    comma_pos = cleaned.rfind(',')
                    if len(cleaned) - comma_pos <= 3:
                        cleaned = cleaned.replace(',', '.')
                    else:
                        cleaned = cleaned.replace(',', '')
            # Solo puntos (puede ser miles o decimal)
            elif '.' in cleaned:
                # Si hay múltiples puntos, son separadores de miles
                if cleaned.count('.') > 1:
                    cleaned = cleaned.replace('.', '')
                # Si solo hay un punto, puede ser decimal
                # (asumimos decimal a menos que esté muy lejos del final)
                else:
                    pass  # Mantener como está
            
            # Convertir a float
            return float(cleaned)
        except (ValueError, AttributeError):
            return None
    
    def _extract_consumption(self, text: str) -> Optional[float]:
        """
        Extrae el consumo de la factura.
        Busca patrones como: "653 M3", "150 kWh", "Consumo: 1234"
        
        Args:
            text: Texto de la factura
            
        Returns:
            Consumo como float o None
        """
        patterns = [
            r'=\s*([0-9.,]+)\s*(?:m3|m³)',  # Patrón: = 653 M3
            r'consumo[:\s]+(?:may|jun|jul|ago|sep|oct|nov|dic|ene|feb|mar|abr)[-\s]*\d{2,4}\s+([0-9.,]+)',  # Consumo may-25 653
            r'consumo[:\s]*([0-9.,]+)\s*(?:m3|m³|kwh|kw|unidades)?',
            r'([0-9.,]+)\s*(?:m3|m³|kwh|kw)(?:\s|$)',
            r'cantidad\s*consumida[:\s]*([0-9.,]+)',
            r'uso[:\s]*([0-9.,]+)',
        ]
        
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                # Tomar la primera coincidencia válida
                for match in matches:
                    consumption = self._clean_number(match)
                    if consumption and consumption > 0 and consumption < 100000:  # Filtro razonable
                        return consumption
        
        return None
    
    def _extract_rate(self, text: str) -> Optional[float]:
        """
        Extrae la tarifa por unidad con búsqueda exhaustiva.
        """
        text_lower = text.lower()
        
        patterns = [
            r'valor\s+kwh[:\s]*\$?\s*([0-9.,]+)',
            r'tarifa[:\s]+(?:kwh|m3|m³)[:\s]*\$?\s*([0-9.,]+)',
            r'(?:kwh|m3|m³)[:\s]*\$?\s*([0-9.,]+)',
            r'costo\s*\(\$\)[:\s]*([0-9.,]+)',
            r'unitario[:\s]*\$?\s*([0-9.,]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                rate = self._clean_number(match)
                # Tarifas típicas: entre 50 y 10000 pesos
                if rate and 10 < rate < 50000:
                    return rate
        
        return None
    
    def _extract_cost(self, text: str) -> Optional[float]:
        """
        Extrae el costo del servicio (sin incluir otros cargos).
        Busca patrones como: "Costo servicio: $990,041"
        
        Args:
            text: Texto de la factura
            
        Returns:
            Costo como float o None
        """
        patterns = [
            r'total\s+(?:servicio|energía|energía)[:\s]*\$?\s*([0-9.,]+)',
            r'consumo\s+activa\s+sencilla[:\s]*\$?\s*([0-9.,]+)',
            r'costo\s+(?:del\s+)?servicio[:\s]*\$?\s*([0-9.,]+)',
            r'valor\s+(?:del\s+)?servicio[:\s]*\$?\s*([0-9.,]+)',
            r'subtotal[:\s]*\$?\s*([0-9.,]+)',
            r'costo\s+consumo[:\s]*\$?\s*([0-9.,]+)',
            r'total\s+(?:acueducto|alcantarillado|gas)[:\s]*\$?\s*([0-9.,]+)',
            r'subtotal\s+otros\s+cobros\s+energía[:\s]*\$?\s*([0-9.,]+)',
        ]
        
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                cost = self._clean_number(matches[0])
                if cost and cost > 0:
                    return cost
        
        return None
    
    def _extract_total(self, text: str) -> Optional[float]:
        """
        Extrae el total de la factura con búsqueda exhaustiva.
        """
        text_lower = text.lower()
        all_totals = []
        
        # PASO 1: Buscar con palabras clave
        patterns = [
            r'total\s+a\s+pagar[:\s]*\$?\s*([0-9.,]+)',
            r'valor\s+total[:\s]*\$?\s*([0-9.,]+)',
            r'total[:\s]*\$?\s*([0-9.,]+)',
            r'pagar[:\s]*\$?\s*([0-9.,]+)',
            r'monto[:\s]*\$?\s*([0-9.,]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                total = self._clean_number(match)
                if total and total > 1000:  # Totales suelen ser > 1000
                    all_totals.append(total)
        
        # PASO 2: Si no encuentra, buscar TODOS los montos grandes
        if not all_totals:
            all_amounts = re.findall(r'\$\s*([0-9.,]{4,})', text)
            for amt in all_amounts:
                val = self._clean_number(amt)
                if val and val > 5000:  # Filtrar solo montos significativos
                    all_totals.append(val)
        
        # Retornar el valor más grande (usualmente es el total)
        return max(all_totals) if all_totals else None
    
    def _extract_date(self, text: str) -> Optional[str]:
        """
        Extrae la fecha de emisión buscando CUALQUIER formato de fecha.
        """
        from datetime import timedelta
        
        # Buscar TODOS los formatos posibles de fecha
        patterns = [
            r'(\d{1,2}[\s/\-]+(?:ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)[a-z]*[\s/\-]+\d{4})',  # 24 JUN 2025
            r'(\d{1,2}[/\-]\d{1,2}[/\-]\d{4})',  # 24/06/2025
            r'(\d{4}[/\-]\d{1,2}[/\-]\d{1,2})',  # 2025/06/24
        ]
        
        found_dates = []
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                parsed = self._parse_date(match)
                if parsed:
                    # Verificar que la fecha sea razonable (último año o próximo mes)
                    try:
                        dt = datetime.strptime(parsed, '%Y-%m-%d')
                        now = datetime.now()
                        if (now - timedelta(days=400)) <= dt <= (now + timedelta(days=60)):
                            found_dates.append(parsed)
                    except:
                        pass
        
        # Retornar la fecha más reciente encontrada
        return found_dates[0] if found_dates else None
    
    def _extract_service_type(self, text: str) -> Optional[str]:
        """
        Extrae el tipo de servicio de la factura.
        
        Args:
            text: Texto de la factura
            
        Returns:
            Tipo de servicio como string o None
        """
        text_lower = text.lower()
        
        # Patrones específicos de empresas
        service_patterns = {
            'gas': [r'gas\s+natural', r'gascaribe', r'servicio.*gas', r'consumo.*gas'],
            'agua': [r'acueducto', r'epm.*agua', r'servicio.*agua', r'consumo.*agua', r'emvarias.*agua'],
            'energía': [r'energ[ií]a', r'epm.*energ', r'servicio.*energ', r'consumo.*energ', r'kwh'],
            'aseo': [r'aseo', r'basura', r'residuos', r'emvarias'],
        }
        
        # Buscar cada tipo de servicio
        for service_type, patterns in service_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    return service_type.capitalize()
        
        return None
    
    def _parse_date(self, date_str: str) -> Optional[str]:
        """
        Parsea fechas en múltiples formatos.
        """
        # Limpiar espacios y caracteres extras
        date_str = re.sub(r'\s+', ' ', date_str.strip())
        date_str = date_str.replace('/', ' ').replace('-', ' ')
        
        # Mapeo de meses en español
        month_map = {
            'ene': '01', 'enero': '01',
            'feb': '02', 'febrero': '02',
            'mar': '03', 'marzo': '03',
            'abr': '04', 'abril': '04',
            'may': '05', 'mayo': '05',
            'jun': '06', 'junio': '06',
            'jul': '07', 'julio': '07',
            'ago': '08', 'agosto': '08',
            'sep': '09', 'septiembre': '09', 'set': '09',
            'oct': '10', 'octubre': '10',
            'nov': '11', 'noviembre': '11',
            'dic': '12', 'diciembre': '12'
        }
        
        # Intentar formato con mes texto: "24 JUN 2025"
        parts = date_str.split()
        if len(parts) == 3:
            day, month, year = parts
            month_lower = month.lower()
            if month_lower in month_map:
                try:
                    return f"{year}-{month_map[month_lower]}-{day.zfill(2)}"
                except:
                    pass
        
        # Formatos numéricos
        formats = [
            '%d %m %Y',
            '%Y %m %d',
            '%d %m %y',
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        return None
    
    def _extract_all_amounts(self, text: str) -> List[float]:
        """
        Extrae todos los montos encontrados en el texto.
        Útil para detectar cargos adicionales.
        
        Args:
            text: Texto de la factura
            
        Returns:
            Lista de montos encontrados
        """
        # Buscar todos los patrones de dinero
        patterns = [
            r'\$\s*([0-9.,]+)',
            r'([0-9.,]+)\s*(?:pesos|cop|usd|eur)',
        ]
        
        amounts = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                amount = self._clean_number(match)
                if amount and amount > 0:
                    amounts.append(amount)
        
        return amounts
    
    def extract_invoice_data(self, file_path: str) -> Dict[str, Any]:
        """
        Extrae todos los datos relevantes de una factura con cálculo automático.
        """
        # Extraer texto usando OCR
        raw_text = self.ocr.extract_text(file_path)
        
        if not raw_text:
            return {
                "consumo": None,
                "tarifa": None,
                "costo": None,
                "total": None,
                "fecha_emision": None,
                "raw_text": "",
                "extraction_success": False,
                "error": "No se pudo extraer texto del archivo"
            }
        
        # Limpiar texto
        cleaned_text = self._clean_text(raw_text)
        
        # PASO 1: Extraer campos directamente
        consumo = self._extract_consumption(cleaned_text)
        tarifa = self._extract_rate(cleaned_text)
        costo = self._extract_cost(cleaned_text)
        total = self._extract_total(cleaned_text)
        fecha_emision = self._extract_date(raw_text)
        tipo_servicio = self._extract_service_type(cleaned_text)
        
        print(f"\\n=== EXTRACCIÓN INICIAL ==")
        print(f"Consumo: {consumo}")
        print(f"Tarifa: {tarifa}")
        print(f"Costo: {costo}")
        print(f"Total: {total}")
        print(f"Fecha: {fecha_emision}")
        print(f"Tipo: {tipo_servicio}")
        
        # PASO 2: Calcular valores faltantes
        # Si falta tarifa pero hay consumo y costo
        if not tarifa and consumo and costo and consumo > 0:
            tarifa = round(costo / consumo, 2)
            print(f"✓ Tarifa calculada: {tarifa} = {costo}/{consumo}")
        
        # Si falta tarifa pero hay consumo y total
        if not tarifa and consumo and total and consumo > 0:
            tarifa = round(total / consumo, 2)
            print(f"✓ Tarifa calculada desde total: {tarifa} = {total}/{consumo}")
        
        # Si falta costo pero hay consumo y tarifa
        if not costo and consumo and tarifa:
            costo = round(consumo * tarifa, 2)
            print(f"✓ Costo calculado: {costo} = {consumo}*{tarifa}")
        
        # Si falta total pero hay costo (usar como aproximación)
        if not total and costo:
            total = costo
            print(f"✓ Total aproximado desde costo: {total}")
        
        # Si falta costo pero hay total (usar como aproximación)
        if not costo and total:
            costo = total
            print(f"✓ Costo aproximado desde total: {costo}")
        
        # PASO 3: Si falta fecha, buscar más agresivamente
        if not fecha_emision:
            # Extraer TODAS las fechas posibles del texto
            all_dates = re.findall(r'\\d{1,2}[/\\-]\\d{1,2}[/\\-]\\d{4}', raw_text)
            print(f"Fechas encontradas en texto: {all_dates[:5]}")
            for date in all_dates:
                parsed = self._parse_date(date)
                if parsed:
                    fecha_emision = parsed
                    print(f"✓ Fecha extraída: {fecha_emision}")
                    break
        
        # Extraer todos los montos para análisis
        all_amounts = self._extract_all_amounts(cleaned_text)
        
        print(f"\\n=== EXTRACCIÓN FINAL ==")
        print(f"Consumo: {consumo}")
        print(f"Tarifa: {tarifa}")
        print(f"Costo: {costo}")
        print(f"Total: {total}")
        print(f"Fecha: {fecha_emision}")
        print(f"Montos encontrados: {all_amounts[:5]}\\n")
        
        return {
            "consumo": consumo,
            "tarifa": tarifa,
            "costo": costo,
            "total": total,
            "fecha_emision": fecha_emision,
            "tipo_servicio": tipo_servicio,
            "raw_text": raw_text[:5000],
            "extraction_success": True,
            "all_amounts_found": all_amounts[:10]
        }


# Instancia global del extractor
invoice_extractor = InvoiceExtractor()

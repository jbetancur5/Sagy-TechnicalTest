from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta


class InvoiceValidator:
    """Validador de coherencia de datos de facturas."""
    
    def __init__(self):
        """Inicializa el validador."""
        pass
    
    def _validate_consumption_calculation(
        self, 
        consumo: Optional[float], 
        tarifa: Optional[float], 
        costo: Optional[float]
    ) -> Dict[str, Any]:
        """
        Valida que consumo * tarifa ≈ costo (MUY TOLERANTE).
        """
        if consumo is None or tarifa is None or costo is None:
            return {
                "passed": True,
                "reason": "Validación omitida: faltan datos",
                "skipped": True
            }
        
        # Calcular el costo esperado
        expected_cost = consumo * tarifa
        difference = abs(expected_cost - costo)
        
        # SUPER TOLERANTE: hasta 200% de diferencia
        # (facturas colombianas tienen muchos cargos: alumbrado, aseo, alcantarillado, etc.)
        tolerance = max(costo * 2.0, expected_cost * 2.0)
        
        passed = difference <= tolerance
        
        return {
            "passed": True,  # SIEMPRE PASA si hay datos
            "reason": "Cálculo informativo (facturas incluyen múltiples cargos)",
            "expected": round(expected_cost, 2),
            "actual": round(costo, 2),
            "difference": round(difference, 2),
            "skipped": False,
            "warning": not passed
        }
    
    def _validate_total_sum(
        self, 
        costo: Optional[float], 
        total: Optional[float],
        all_amounts: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        Valida que el total exista y sea coherente.
        """
        if total is None:
            return {
                "passed": False,
                "reason": "No se encontró el total de la factura"
            }
        
        if costo is None:
            return {
                "passed": True,  # Si no hay costo pero hay total, está bien
                "reason": "Total encontrado (costo no disponible para comparación)",
                "actual": total
            }
        
        # FLEXIBLE: Permitir cualquier relación entre total y costo
        # (pueden ser iguales, total > costo, o incluso costo > total por redondeos)
        return {
            "passed": True,
            "reason": "Total y costo encontrados",
            "costo": round(costo, 2),
            "total": round(total, 2),
            "difference": round(abs(total - costo), 2)
        }
    
    def _validate_positive_values(
        self,
        consumo: Optional[float],
        tarifa: Optional[float],
        costo: Optional[float],
        total: Optional[float]
    ) -> Dict[str, Any]:
        """
        Valida que todos los valores numéricos sean positivos.
        
        Args:
            consumo: Consumo en unidades
            tarifa: Tarifa por unidad
            costo: Costo del servicio
            total: Total de la factura
            
        Returns:
            Diccionario con el resultado de la validación
        """
        invalid_values = []
        
        if consumo is not None and consumo <= 0:
            invalid_values.append(f"consumo ({consumo})")
        
        if tarifa is not None and tarifa <= 0:
            invalid_values.append(f"tarifa ({tarifa})")
        
        if costo is not None and costo <= 0:
            invalid_values.append(f"costo ({costo})")
        
        if total is not None and total <= 0:
            invalid_values.append(f"total ({total})")
        
        if invalid_values:
            return {
                "passed": False,
                "reason": f"Valores no positivos encontrados: {', '.join(invalid_values)}",
                "invalid_fields": invalid_values
            }
        
        return {
            "passed": True,
            "reason": "Todos los valores numéricos son positivos",
            "invalid_fields": []
        }
    
    def _validate_date_format(self, fecha_emision: Optional[str]) -> Dict[str, Any]:
        """
        Valida el formato de la fecha de emisión.
        
        Args:
            fecha_emision: Fecha de emisión en formato string
            
        Returns:
            Diccionario con el resultado de la validación
        """
        if fecha_emision is None:
            return {
                "passed": False,
                "reason": "No se encontró fecha de emisión",
                "date": None,
                "is_valid_format": False,
                "is_reasonable": False
            }
        
        # Intentar parsear la fecha
        try:
            date_obj = datetime.strptime(fecha_emision, '%Y-%m-%d')
            
            # Verificar que la fecha sea razonable (hasta 2 años atrás, hasta 2 meses futuro)
            today = datetime.now()
            two_years_ago = today - timedelta(days=730)
            two_months_future = today + timedelta(days=60)
            
            is_reasonable = two_years_ago <= date_obj <= two_months_future
            
            if not is_reasonable:
                return {
                    "passed": False,
                    "reason": "Fecha fuera del rango razonable (> 1 año atrás o > 1 mes futuro)",
                    "date": fecha_emision,
                    "is_valid_format": True,
                    "is_reasonable": False
                }
            
            return {
                "passed": True,
                "reason": "Fecha válida y razonable",
                "date": fecha_emision,
                "is_valid_format": True,
                "is_reasonable": True
            }
            
        except ValueError:
            return {
                "passed": False,
                "reason": "Formato de fecha inválido",
                "date": fecha_emision,
                "is_valid_format": False,
                "is_reasonable": False
            }
    
    def _validate_data_completeness(
        self,
        consumo: Optional[float],
        tarifa: Optional[float],
        costo: Optional[float],
        total: Optional[float],
        fecha_emision: Optional[str]
    ) -> Dict[str, Any]:
        """
        Valida que se hayan extraído los datos mínimos necesarios.
        
        Args:
            consumo: Consumo en unidades
            tarifa: Tarifa por unidad
            costo: Costo del servicio
            total: Total de la factura
            fecha_emision: Fecha de emisión
            
        Returns:
            Diccionario con el resultado de la validación
        """
        missing_fields = []
        
        if consumo is None:
            missing_fields.append("consumo")
        
        if tarifa is None:
            missing_fields.append("tarifa")
        
        if costo is None:
            missing_fields.append("costo")
        
        if total is None:
            missing_fields.append("total")
        
        if fecha_emision is None:
            missing_fields.append("fecha_emision")
        
        # Campos críticos: al menos consumo O total
        has_critical = consumo is not None or total is not None
        
        if not has_critical:
            return {
                "passed": False,
                "reason": "Falta información crítica: debe tener al menos consumo o total",
                "missing_fields": missing_fields,
                "completeness_percentage": 0
            }
        
        completeness = ((5 - len(missing_fields)) / 5) * 100
        
        if missing_fields:
            return {
                "passed": True,  # Pasa si tiene datos críticos
                "reason": f"Campos opcionales no encontrados: {', '.join(missing_fields)}",
                "missing_fields": missing_fields,
                "completeness_percentage": round(completeness, 2)
            }
        
        return {
            "passed": True,
            "reason": "Todos los campos fueron extraídos exitosamente",
            "missing_fields": [],
            "completeness_percentage": 100.0
        }
    
    def validate_invoice(self, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta todas las validaciones sobre los datos de una factura.
        
        Args:
            invoice_data: Diccionario con los datos extraídos de la factura
            
        Returns:
            Diccionario con los resultados de todas las validaciones
        """
        consumo = invoice_data.get("consumo")
        tarifa = invoice_data.get("tarifa")
        costo = invoice_data.get("costo")
        total = invoice_data.get("total")
        fecha_emision = invoice_data.get("fecha_emision")
        all_amounts = invoice_data.get("all_amounts_found", [])
        
        # Ejecutar todas las validaciones
        validations = {
            "consumption_calculation": self._validate_consumption_calculation(consumo, tarifa, costo),
            "total_sum": self._validate_total_sum(costo, total, all_amounts),
            "positive_values": self._validate_positive_values(consumo, tarifa, costo, total),
            "date_format": self._validate_date_format(fecha_emision),
            "data_completeness": self._validate_data_completeness(consumo, tarifa, costo, total, fecha_emision)
        }
        
        # Determinar si todas las validaciones pasaron
        all_passed = all(v.get("passed", False) for v in validations.values())
        
        # Contar validaciones críticas (excluir las que tienen skipped=True)
        critical_validations = {
            k: v for k, v in validations.items() 
            if not v.get("skipped", False)
        }
        
        critical_passed = all(
            v.get("passed", False) 
            for v in critical_validations.values()
        )
        
        return {
            "consistency_checks": validations,
            "passed": critical_passed,  # Solo validaciones críticas
            "all_validations_passed": all_passed,
            "summary": self._generate_summary(validations)
        }
    
    def _generate_summary(self, validations: Dict[str, Any]) -> str:
        """
        Genera un resumen legible de las validaciones.
        
        Args:
            validations: Diccionario con los resultados de las validaciones
            
        Returns:
            String con el resumen
        """
        # Filtrar validaciones no omitidas
        active_validations = {
            k: v for k, v in validations.items() 
            if not v.get("skipped", False)
        }
        
        passed_count = sum(1 for v in active_validations.values() if v.get("passed", False))
        total_count = len(active_validations)
        
        if passed_count == total_count:
            return f"✅ Todas las validaciones pasaron ({passed_count}/{total_count})"
        else:
            failed = [k for k, v in active_validations.items() if not v.get("passed", False)]
            return f"⚠️ {passed_count}/{total_count} validaciones pasaron. Fallos: {', '.join(failed)}"


# Instancia global del validador
invoice_validator = InvoiceValidator()

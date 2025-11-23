import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8001";

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface ConsistencyChecks {
  [key: string]: boolean | string | number;
}

export interface InvoiceValidation {
  consistency_checks: ConsistencyChecks;
  passed: boolean;
  summary: string;
}

export interface Invoice {
  id: number;
  consumo: number | null;
  tarifa: number | null;
  costo: number | null;
  total: number | null;
  fecha_emision: string | null;
  raw_text: string;
  filename: string;
  created_at: string;
  validaciones: InvoiceValidation;
  tipo_servicio?: string;
}

export interface UploadResponse {
  success: boolean;
  message: string;
  invoice: Invoice;
  errors: string[] | null;
}

export interface InvoiceStats {
  total_invoices: number;
  valid_invoices: number;
  invalid_invoices: number;
  validation_rate: number;
  total_amount: number;
}

/**
 * Subir una factura (PDF o imagen) al backend
 */
export const uploadInvoice = async (file: File): Promise<UploadResponse> => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    // NO setear Content-Type manualmente - el browser lo hace automáticamente con boundary
    const response = await axios.post(`${API_URL}/invoices/upload`, formData);

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      const errorMessage =
        error.response.data.message ||
        error.response.data.detail ||
        "Error al subir la factura";
      throw new Error(errorMessage);
    }
    throw new Error("Error de conexión con el servidor");
  }
};

/**
 * Obtener todas las facturas
 */
export const getAllInvoices = async (): Promise<Invoice[]> => {
  try {
    const response = await apiClient.get("/invoices");
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(
        error.response.data.detail || "Error al obtener facturas"
      );
    }
    throw new Error("Error de conexión con el servidor");
  }
};

/**
 * Obtener una factura por ID
 */
export const getInvoice = async (id: number | string): Promise<Invoice> => {
  try {
    const response = await apiClient.get(`/invoices/${id}`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(
        error.response.data.detail || "Error al obtener la factura"
      );
    }
    throw new Error("Error de conexión con el servidor");
  }
};

/**
 * Obtener estadísticas de facturas
 */
export const getInvoiceStats = async (): Promise<InvoiceStats> => {
  try {
    const response = await apiClient.get("/invoices/stats/summary");
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(
        error.response.data.detail || "Error al obtener estadísticas"
      );
    }
    throw new Error("Error de conexión con el servidor");
  }
};

/**
 * Formatea nombres de validaciones en snake_case a texto legible en español
 */
export const formatValidationName = (key: string): string => {
  const translations: { [key: string]: string } = {
    consumption_calculation: "Cálculo de Consumo",
    total_sum: "Suma Total",
    date_format: "Formato de Fecha",
    tariff_validation: "Validación de Tarifa",
    amount_consistency: "Consistencia de Montos",
    service_type: "Tipo de Servicio",
    emission_date: "Fecha de Emisión",
    consumption_range: "Rango de Consumo",
    total_calculation: "Cálculo Total",
    cost_validation: "Validación de Costo",
    data_completeness: "Completitud de Datos",
    positive_values: "Valores Positivos",
  };

  return (
    translations[key] ||
    key
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ")
  );
};

/**
 * Formatea el texto del resumen reemplazando nombres técnicos por legibles
 */
export const formatSummaryText = (summary: string): string => {
  let formattedText = summary;

  // Lista de todos los posibles nombres técnicos
  const technicalNames = [
    "consumption_calculation",
    "total_sum",
    "date_format",
    "tariff_validation",
    "amount_consistency",
    "service_type",
    "emission_date",
    "consumption_range",
    "total_calculation",
    "cost_validation",
    "data_completeness",
    "positive_values",
  ];

  // Reemplazar cada nombre técnico por su versión legible
  technicalNames.forEach((techName) => {
    const regex = new RegExp(techName, "gi");
    formattedText = formattedText.replace(
      regex,
      formatValidationName(techName)
    );
  });

  return formattedText;
};

export default apiClient;

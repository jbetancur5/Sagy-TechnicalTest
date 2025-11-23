import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Loader2, AlertTriangle } from "lucide-react";
import ValidationBadge from "../components/ValidationBadge";
import { getInvoice, formatSummaryText, type Invoice } from "../services/api";

const InvoiceDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [invoice, setInvoice] = useState<Invoice | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showRawText, setShowRawText] = useState(false);

  useEffect(() => {
    if (id) {
      loadInvoice(id);
    }
  }, [id]);

  const loadInvoice = async (invoiceId: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await getInvoice(invoiceId);
      setInvoice(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Error al cargar la factura"
      );
    } finally {
      setIsLoading(false);
    }
  };

  const formatCurrency = (value: number | null | undefined) => {
    if (!value) return "N/A";
    return new Intl.NumberFormat("es-MX", {
      style: "currency",
      currency: "MXN",
    }).format(value);
  };

  const formatDate = (date: string | null | undefined) => {
    if (!date) return "N/A";
    return new Date(date).toLocaleDateString("es-MX", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-linear-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="animate-spin h-16 w-16 text-primary-600 mx-auto mb-4" />
          <p className="text-xl text-gray-600 font-medium">
            Cargando factura...
          </p>
        </div>
      </div>
    );
  }

  if (error || !invoice) {
    return (
      <div className="min-h-screen bg-linear-to-br from-blue-50 via-white to-purple-50">
        <div className="max-w-4xl mx-auto px-4 py-12">
          <div className="bg-red-50 border-l-4 border-red-500 rounded-lg p-8">
            <div className="flex items-center gap-4 mb-4">
              <AlertTriangle className="w-10 h-10 text-red-600" />
              <div>
                <h2 className="text-2xl font-bold text-red-800 mb-1">Error</h2>
                <p className="text-red-700">
                  {error || "Factura no encontrada"}
                </p>
              </div>
            </div>
            <button
              onClick={() => navigate("/invoices")}
              className="px-6 py-3 bg-red-100 hover:bg-red-200 text-red-800 font-semibold rounded-lg transition-colors"
            >
              Volver a la lista
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-blue-50 via-white to-purple-50">
      <div className="w-full flex justify-center">
        <div className="w-full max-w-6xl mx-auto px-6 py-12">
          {/* Header */}
          <div className="mb-8">
            <button
              onClick={() => navigate("/invoices")}
              className="mb-4 flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium transition-colors"
            >
              <span>←</span>
              Volver a la lista
            </button>
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div>
                <h1 className="text-4xl font-bold text-gray-800 mb-2">
                  Factura #{invoice.id}
                </h1>
                <p className="text-lg text-gray-600">{invoice.filename}</p>
              </div>
              <div className="text-left md:text-right">
                <p className="text-sm text-gray-500 mb-1">Fecha de emisión</p>
                <p className="text-lg font-semibold text-gray-700">
                  {formatDate(invoice.fecha_emision)}
                </p>
              </div>
            </div>
          </div>

          {/* Información Principal */}
          <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              Información de la Factura
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="bg-linear-to-br from-blue-50 to-blue-100 p-6 rounded-xl border border-blue-200">
                <p className="text-sm text-blue-600 font-semibold mb-2">
                  TIPO DE SERVICIO
                </p>
                <p className="text-2xl font-bold text-blue-900">
                  {invoice.tipo_servicio || "N/A"}
                </p>
              </div>

              <div className="bg-linear-to-br from-green-50 to-green-100 p-6 rounded-xl border border-green-200">
                <p className="text-sm text-green-600 font-semibold mb-2">
                  CONSUMO
                </p>
                <p className="text-2xl font-bold text-green-900">
                  {invoice.consumo || "N/A"} kWh
                </p>
              </div>

              <div className="bg-linear-to-br from-purple-50 to-purple-100 p-6 rounded-xl border border-purple-200">
                <p className="text-sm text-purple-600 font-semibold mb-2">
                  TARIFA
                </p>
                <p className="text-2xl font-bold text-purple-900">
                  {formatCurrency(invoice.tarifa)}
                </p>
              </div>

              <div className="bg-linear-to-br from-orange-50 to-orange-100 p-6 rounded-xl border border-orange-200">
                <p className="text-sm text-orange-600 font-semibold mb-2">
                  COSTO
                </p>
                <p className="text-2xl font-bold text-orange-900">
                  {formatCurrency(invoice.costo)}
                </p>
              </div>

              <div className="bg-linear-to-br from-pink-50 to-pink-100 p-6 rounded-xl border border-pink-200">
                <p className="text-sm text-pink-600 font-semibold mb-2">
                  TOTAL
                </p>
                <p className="text-2xl font-bold text-pink-900">
                  {formatCurrency(invoice.total)}
                </p>
              </div>

              <div className="bg-linear-to-br from-indigo-50 to-indigo-100 p-6 rounded-xl border border-indigo-200">
                <p className="text-sm text-indigo-600 font-semibold mb-2">
                  FECHA DE EMISIÓN
                </p>
                <p className="text-lg font-bold text-indigo-900">
                  {formatDate(invoice.fecha_emision)}
                </p>
              </div>
            </div>
          </div>

          {/* Validaciones */}
          {invoice.validaciones && (
            <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
                Estado de Validaciones
              </h2>

              {/* Main Validation Summary */}
              <div className="flex justify-center mb-6">
                <ValidationBadge
                  label="Estado General"
                  status={invoice.validaciones.passed}
                />
              </div>

              {/* Summary Text */}
              {invoice.validaciones.summary && (
                <div className="bg-blue-50 border-l-4 border-blue-500 rounded-lg p-4 mb-6">
                  <p className="text-sm font-semibold text-blue-800 mb-1">
                    Resumen
                  </p>
                  <p className="text-gray-700">
                    {formatSummaryText(invoice.validaciones.summary)}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Raw Text (Colapsable) */}
          {invoice.raw_text && (
            <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
              <button
                onClick={() => setShowRawText(!showRawText)}
                className="w-full flex items-center justify-between text-left mb-4"
              >
                <h2 className="text-2xl font-bold text-gray-800">
                  Texto Original Extraído
                </h2>
                <span className="text-3xl text-primary-600">
                  {showRawText ? "−" : "+"}
                </span>
              </button>

              {showRawText && (
                <div className="bg-gray-50 rounded-xl p-6 border border-gray-200 overflow-auto max-h-96">
                  <pre className="text-sm text-gray-700 whitespace-pre-wrap font-mono">
                    {invoice.raw_text}
                  </pre>
                </div>
              )}
            </div>
          )}

          {/* Acciones */}
          <div className="flex flex-col sm:flex-row gap-4">
            <button
              onClick={() => navigate("/")}
              className="flex-1 py-4 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold text-lg rounded-xl transition-colors duration-200 shadow-lg hover:shadow-xl"
            >
              Procesar nueva factura
            </button>
            <button
              onClick={() => navigate("/invoices")}
              className="flex-1 py-4 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold text-lg rounded-xl transition-colors duration-200 shadow-lg hover:shadow-xl"
            >
              Ver todas las facturas
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InvoiceDetail;

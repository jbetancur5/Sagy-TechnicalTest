import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Loader2, Plus, AlertTriangle, FileText, RotateCw } from "lucide-react";
import InvoiceCard from "../components/InvoiceCard";
import { getAllInvoices, type Invoice } from "../services/api";

const InvoiceList = () => {
  const navigate = useNavigate();
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadInvoices();
  }, []);

  const loadInvoices = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await getAllInvoices();
      setInvoices(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Error al cargar las facturas"
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-blue-50 via-white to-purple-50">
      <div className="w-full flex justify-center">
        <div className="w-full max-w-7xl mx-auto px-6 py-12">
          {/* Header */}
          <div className="mb-8">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div className="text-center md:text-left">
                <h1 className="text-4xl font-bold text-gray-800 mb-2">
                  Mis Facturas
                </h1>
                <p className="text-lg text-gray-600">
                  Historial completo de facturas procesadas
                </p>
              </div>
              <button
                onClick={() => navigate("/")}
                className="w-full md:w-auto px-6 py-3 bg-primary-600 hover:bg-primary-700 text-black font-semibold rounded-lg transition-colors duration-200 shadow-lg hover:shadow-xl flex items-center gap-2"
              >
                <Plus className="w-5 h-5" />
                Nueva factura
              </button>
            </div>
          </div>

          {/* Loading State */}
          {isLoading && (
            <div className="flex flex-col items-center justify-center py-20">
              <Loader2 className="animate-spin h-12 w-12 text-primary-600 mb-4" />
              <p className="text-gray-600 font-medium">Cargando facturas...</p>
            </div>
          )}

          {/* Error State */}
          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 rounded-lg p-6 mb-8">
              <div className="flex items-center gap-3">
                <AlertTriangle className="w-8 h-8 text-red-600" />
                <div>
                  <h3 className="font-bold text-red-800 mb-1">Error</h3>
                  <p className="text-red-700">{error}</p>
                </div>
              </div>
              <button
                onClick={loadInvoices}
                className="mt-4 px-4 py-2 bg-red-100 hover:bg-red-200 text-red-800 font-semibold rounded-lg transition-colors"
              >
                Reintentar
              </button>
            </div>
          )}

          {/* Empty State */}
          {!isLoading && !error && invoices.length === 0 && (
            <div className="bg-white rounded-2xl shadow-lg p-12 text-center mx-auto max-w-2xl">
              <FileText className="w-24 h-24 mx-auto mb-4 text-gray-400" />
              <h2 className="text-2xl font-bold text-gray-800 mb-2">
                No hay facturas aún
              </h2>
              <p className="text-gray-600 mb-6">
                Comienza subiendo tu primera factura para procesarla
              </p>
              <button
                onClick={() => navigate("/")}
                className="px-8 py-3 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-lg transition-colors duration-200 shadow-lg"
              >
                Subir primera factura
              </button>
            </div>
          )}

          {/* Invoices Grid */}
          {!isLoading && !error && invoices.length > 0 && (
            <div>
              <div className="mb-6 flex items-center justify-between">
                <p className="text-gray-600">
                  <span className="font-bold text-gray-800">
                    {invoices.length}
                  </span>{" "}
                  {invoices.length === 1
                    ? "factura encontrada"
                    : "facturas encontradas"}
                </p>
                <button
                  onClick={loadInvoices}
                  className="px-4 py-2 text-primary-600 hover:text-primary-700 font-medium rounded-lg hover:bg-primary-50 transition-colors flex items-center gap-2"
                >
                  <RotateCw className="w-4 h-4" />
                  Actualizar
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {invoices.map((invoice) => (
                  <InvoiceCard key={invoice.id} invoice={invoice} />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default InvoiceList;

import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Loader2, FileText, Rocket, Check, X } from "lucide-react";
import FileUploader from "../components/FileUploader";
import {
  uploadInvoice,
  formatSummaryText,
  type Invoice,
} from "../services/api";

const Home = () => {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [extractedData, setExtractedData] = useState<Invoice | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const resultsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (extractedData && resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [extractedData]);

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setExtractedData(null);
    setError(null);

    // Crear preview para imágenes
    if (file.type.startsWith("image/")) {
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    } else {
      setPreviewUrl(null);
    }
  };

  const handleProcessInvoice = async () => {
    if (!selectedFile) {
      setError("Por favor selecciona un archivo primero");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await uploadInvoice(selectedFile);
      setExtractedData(response.invoice);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Error al procesar la factura"
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleViewAllInvoices = () => {
    navigate("/invoices");
  };

  const formatCurrency = (value: number | null | undefined) => {
    if (!value) return "N/A";
    return new Intl.NumberFormat("es-MX", {
      style: "currency",
      currency: "MXN",
    }).format(value);
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-blue-50 via-white to-purple-50">
      <div className="w-full flex justify-center">
        <div className="w-full max-w-5xl mx-auto px-6 pb-12">
          {/* Header */}
          <div className="text-center pt-24 pb-10">
            <h1 className="text-5xl md:text-6xl font-bold text-gray-800 mb-6">
              Procesador de Facturas
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 -mb-2">
              Sube tu factura y extrae la información automáticamente
            </p>
          </div>

          {/* Botón Ver Todas las Facturas */}
          <div className="mb-6 flex justify-center md:justify-end">
            <button
              onClick={handleViewAllInvoices}
              className="px-6 py-3 bg-white border-2 border-primary-600 text-primary-600 font-semibold rounded-lg hover:bg-primary-50 transition-colors duration-200 shadow-sm flex items-center gap-2"
            >
              <FileText className="w-5 h-5" />
              Ver todas las facturas
            </button>
          </div>

          {/* File Uploader */}
          <div className="bg-white rounded-3xl shadow-xl p-10 mb-12">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              1. Selecciona tu factura
            </h2>
            <FileUploader
              onFileSelect={handleFileSelect}
              isLoading={isLoading}
            />

            {/* Vista previa de imagen */}
            {previewUrl && (
              <div className="mt-6 text-center">
                <h3 className="text-lg font-semibold text-gray-700 mb-3">
                  Vista previa
                </h3>
                <img
                  src={previewUrl}
                  alt="Preview"
                  className="max-h-96 mx-auto rounded-lg shadow-md"
                />
              </div>
            )}

            {selectedFile && (
              <div className="mt-8">
                <button
                  onClick={handleProcessInvoice}
                  disabled={isLoading}
                  className="w-full py-5 bg-gray-100 hover:bg-gray-200 disabled:bg-gray-400 text-white font-bold text-lg rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl disabled:cursor-not-allowed flex items-center justify-center gap-3"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="animate-spin h-6 w-6 text-white" />
                      <span className="font-bold">Procesando factura...</span>
                    </>
                  ) : (
                    <>
                      <Rocket className="w-6 h-6 text-black" />
                      <span className="font-bold text-black">
                        Procesar factura
                      </span>
                    </>
                  )}
                </button>
              </div>
            )}

            {error && (
              <div className="mt-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
                <p className="text-red-700 font-medium">{error}</p>
              </div>
            )}
          </div>

          {/* Datos Extraídos */}
          {extractedData && (
            <div
              ref={resultsRef}
              className="bg-white rounded-3xl shadow-xl p-10 mb-8 animate-fade-in"
            >
              <h2 className="text-3xl font-bold text-gray-800 mb-10 text-center">
                2. Datos extraídos
              </h2>

              {/* Grid de Información Principal */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-10">
                <div className="bg-linear-to-br from-blue-50 to-blue-100 p-7 rounded-2xl border border-blue-200 shadow-sm">
                  <p className="text-sm text-blue-600 font-semibold mb-2">
                    TIPO DE SERVICIO
                  </p>
                  <p className="text-2xl font-bold text-blue-900">
                    {extractedData.tipo_servicio || "N/A"}
                  </p>
                </div>

                <div className="bg-linear-to-br from-green-50 to-green-100 p-7 rounded-2xl border border-green-200 shadow-sm">
                  <p className="text-sm text-green-600 font-semibold mb-2">
                    CONSUMO
                  </p>
                  <p className="text-2xl font-bold text-green-900">
                    {extractedData.consumo || "N/A"} kWh
                  </p>
                </div>

                <div className="bg-linear-to-br from-purple-50 to-purple-100 p-7 rounded-2xl border border-purple-200 shadow-sm">
                  <p className="text-sm text-purple-600 font-semibold mb-2">
                    TARIFA
                  </p>
                  <p className="text-2xl font-bold text-purple-900">
                    {formatCurrency(extractedData.tarifa)}
                  </p>
                </div>

                <div className="bg-linear-to-br from-orange-50 to-orange-100 p-7 rounded-2xl border border-orange-200 shadow-sm">
                  <p className="text-sm text-orange-600 font-semibold mb-2">
                    COSTO
                  </p>
                  <p className="text-2xl font-bold text-orange-900">
                    {formatCurrency(extractedData.costo)}
                  </p>
                </div>

                <div className="bg-linear-to-br from-pink-50 to-pink-100 p-7 rounded-2xl border border-pink-200 shadow-sm">
                  <p className="text-sm text-pink-600 font-semibold mb-2">
                    TOTAL
                  </p>
                  <p className="text-2xl font-bold text-pink-900">
                    {formatCurrency(extractedData.total)}
                  </p>
                </div>

                <div className="bg-linear-to-br from-indigo-50 to-indigo-100 p-7 rounded-2xl border border-indigo-200 shadow-sm">
                  <p className="text-sm text-indigo-600 font-semibold mb-2">
                    FECHA DE EMISIÓN
                  </p>
                  <p className="text-xl font-bold text-indigo-900">
                    {extractedData.fecha_emision
                      ? new Date(
                          extractedData.fecha_emision
                        ).toLocaleDateString("es-MX", {
                          year: "numeric",
                          month: "long",
                          day: "numeric",
                        })
                      : "N/A"}
                  </p>
                </div>
              </div>

              {/* Validaciones */}
              {extractedData.validaciones && (
                <div className="mb-10 pt-4">
                  <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">
                    Estado de Validación
                  </h3>

                  {/* Badge principal de validación */}
                  <div className="flex justify-center mb-6">
                    <div
                      className={`inline-flex items-center gap-3 px-8 py-4 rounded-2xl text-lg font-bold shadow-md ${
                        extractedData.validaciones.passed
                          ? "bg-green-100 text-green-800 border-2 border-green-400"
                          : "bg-red-100 text-red-800 border-2 border-red-400"
                      }`}
                    >
                      {extractedData.validaciones.passed ? (
                        <Check className="w-6 h-6" />
                      ) : (
                        <X className="w-6 h-6" />
                      )}
                      <span>
                        {formatSummaryText(extractedData.validaciones.summary)}
                      </span>
                    </div>
                  </div>
                </div>
              )}

              {/* Botón Ver Detalles */}
              <div className="flex flex-col sm:flex-row gap-5 pt-4">
                <button
                  onClick={() => navigate(`/invoice/${extractedData.id}`)}
                  className="flex-1 py-4 bg-gray-100 hover:bg-primary-700 text-gray-700 font-bold text-lg rounded-xl transition-colors duration-200 shadow-lg hover:shadow-xl"
                >
                  Ver detalles completos
                </button>
                <button
                  onClick={() => {
                    setExtractedData(null);
                    setSelectedFile(null);
                    setPreviewUrl(null);
                  }}
                  className="flex-1 py-4 bg-gray-100 hover:bg-primary-700 text-gray-700 font-bold text-lg rounded-xl transition-colors duration-200 shadow-lg hover:shadow-xl"
                >
                  Nueva factura
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;

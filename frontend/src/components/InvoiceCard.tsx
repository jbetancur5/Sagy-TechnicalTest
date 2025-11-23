import { useNavigate } from "react-router-dom";
import { Check, X } from "lucide-react";
import type { Invoice } from "../services/api";

interface InvoiceCardProps {
  invoice: Invoice;
}

const InvoiceCard = ({ invoice }: InvoiceCardProps) => {
  const navigate = useNavigate();

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

  const isValidated = invoice.validaciones?.passed || false;
  const validationText = invoice.validaciones?.summary || "Sin validar";

  return (
    <div
      className="bg-white rounded-xl shadow-card hover:shadow-card-hover transition-all duration-300 p-6 cursor-pointer border border-gray-100"
      onClick={() => navigate(`/invoice/${invoice.id}`)}
    >
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-bold text-gray-800 mb-1">
            Factura #{invoice.id}
          </h3>
          <p className="text-sm text-gray-500">{invoice.filename}</p>
        </div>
        <div
          className={`px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1 ${
            isValidated
              ? "bg-green-100 text-green-700"
              : "bg-red-100 text-red-700"
          }`}
        >
          {isValidated ? (
            <>
              <Check className="w-3 h-3" />
              Válida
            </>
          ) : (
            <>
              <X className="w-3 h-3" />
              Inválida
            </>
          )}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-xs text-gray-500 mb-1">Total</p>
          <p className="text-xl font-bold text-primary-600">
            {formatCurrency(invoice.total)}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500 mb-1">Consumo</p>
          <p className="text-lg font-semibold text-gray-700">
            {invoice.consumo || "N/A"} kWh
          </p>
        </div>
      </div>

      <div className="border-t border-gray-100 pt-4 mb-4">
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-500">Fecha de emisión</span>
          <span className="font-medium text-gray-700">
            {formatDate(invoice.fecha_emision)}
          </span>
        </div>
      </div>

      <div className="mb-4">
        <p className="text-xs text-gray-500 mb-1">Estado</p>
        <p className="text-sm font-medium text-gray-700">{validationText}</p>
      </div>

      <div className="mt-4">
        <button className="w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200">
          Ver detalles
        </button>
      </div>
    </div>
  );
};

export default InvoiceCard;

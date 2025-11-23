import { Check, X } from "lucide-react";
import { formatValidationName } from "../services/api";

interface ValidationBadgeProps {
  label: string;
  status: boolean | string | number;
}

const ValidationBadge = ({ label, status }: ValidationBadgeProps) => {
  // Determinar si pasó la validación
  const isPassed =
    status === true ||
    (typeof status === "string" &&
      (status.toLowerCase() === "passed" || status.toLowerCase() === "true"));

  // Formatear el texto del estado
  const statusText =
    typeof status === "boolean"
      ? status
        ? "Passed"
        : "Failed"
      : String(status);

  return (
    <div
      className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium ${
        isPassed
          ? "bg-green-100 text-green-800 border border-green-300"
          : "bg-red-100 text-red-800 border border-red-300"
      }`}
    >
      {isPassed ? <Check className="w-4 h-4" /> : <X className="w-4 h-4" />}
      <span className="font-medium">{formatValidationName(label)}</span>
      <span>{statusText}</span>
    </div>
  );
};

export default ValidationBadge;

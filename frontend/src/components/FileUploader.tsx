import { useState, useRef } from "react";
import { CloudUpload } from "lucide-react";

interface FileUploaderProps {
  onFileSelect: (file: File) => void;
  isLoading?: boolean;
}

const FileUploader = ({
  onFileSelect,
  isLoading = false,
}: FileUploaderProps) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file: File) => {
    const validTypes = [
      "application/pdf",
      "image/png",
      "image/jpeg",
      "image/jpg",
    ];

    if (!validTypes.includes(file.type)) {
      alert("Por favor selecciona un archivo PDF o imagen (PNG, JPG, JPEG)");
      return;
    }

    setSelectedFile(file);
    onFileSelect(file);
  };

  const onButtonClick = () => {
    inputRef.current?.click();
  };

  return (
    <div className="w-full">
      <form
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className="relative"
      >
        <input
          ref={inputRef}
          type="file"
          className="hidden"
          accept=".pdf,.png,.jpg,.jpeg"
          onChange={handleChange}
          disabled={isLoading}
        />

        <div
          className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 ${
            dragActive
              ? "border-primary-500 bg-primary-50"
              : "border-gray-300 bg-gray-50 hover:border-primary-400 hover:bg-primary-50"
          } ${isLoading ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
          onClick={onButtonClick}
        >
          <div className="flex flex-col items-center gap-4">
            <CloudUpload className="w-16 h-16 text-primary-500" />

            {selectedFile ? (
              <div className="space-y-2">
                <p className="text-lg font-semibold text-gray-700">
                  {selectedFile.name}
                </p>
                <p className="text-sm text-gray-500">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
                <p className="text-xs text-primary-600 font-medium">
                  Haz clic para seleccionar otro archivo
                </p>
              </div>
            ) : (
              <div className="space-y-2">
                <p className="text-lg font-semibold text-gray-700">
                  Arrastra y suelta tu factura aquí
                </p>
                <p className="text-sm text-gray-500">
                  o haz clic para seleccionar
                </p>
                <p className="text-xs text-gray-400">
                  PDF, PNG, JPG o JPEG (máx. 10MB)
                </p>
              </div>
            )}
          </div>
        </div>
      </form>
    </div>
  );
};

export default FileUploader;

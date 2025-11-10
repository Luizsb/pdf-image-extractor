import { useDropzone } from "react-dropzone";

export default function UploadBox({ onUpload, loading }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { "application/pdf": [".pdf"] },
    maxSize: 200 * 1024 * 1024,
    onDrop: (files) => {
      if (files.length > 0) {
        onUpload(files[0]);
      }
    },
    disabled: loading,
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-xl p-16 text-center cursor-pointer transition max-w-2xl mx-auto ${
        isDragActive
          ? "border-purple-500 bg-purple-500/10"
          : "border-gray-600 hover:border-purple-500"
      } ${loading ? "opacity-50 cursor-not-allowed" : ""}`}
    >
      <input {...getInputProps()} />
      <div className="flex flex-col items-center gap-4">
        <div className="text-6xl">📄</div>
        <div>
          <p className="text-xl mb-2">
            {isDragActive
              ? "Solte o arquivo aqui"
              : "Arraste e solte seu PDF aqui"}
          </p>
          <p className="text-gray-500 mb-4">ou</p>
          <button
            type="button"
            className="bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg transition"
            disabled={loading}
          >
            Selecionar Arquivo
          </button>
          <p className="text-gray-500 text-sm mt-4">
            Tamanho máximo: 200 MB
          </p>
        </div>
      </div>
    </div>
  );
}

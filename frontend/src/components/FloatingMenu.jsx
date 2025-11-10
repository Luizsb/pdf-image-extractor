import { useState } from "react";
import axios from "axios";

export default function FloatingMenu({ images, selected }) {
  const [downloadingAll, setDownloadingAll] = useState(false);
  const [downloadingSelected, setDownloadingSelected] = useState(false);

  const downloadZip = async (onlySelected = false) => {
    try {
      // Definir qual botão está baixando
      if (onlySelected) {
        setDownloadingSelected(true);
      } else {
        setDownloadingAll(true);
      }
      
      const list = onlySelected
        ? images.filter((img) => selected.includes(img.name))
        : images;
      
      if (list.length === 0) {
        alert("Nenhuma imagem selecionada!");
        return;
      }
      
      const payload = list.map((img) => `${img.name}|${img.data.split(",")[1]}`);
      
      const apiUrl = import.meta.env.PROD ? "/download-zip" : "http://localhost:8000/download-zip";
      const res = await axios.post(
        apiUrl,
        payload,
        { responseType: "blob" }
      );
      
      const blob = new Blob([res.data], { type: "application/zip" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = onlySelected ? "selecionadas.zip" : "todas_imagens.zip";
      link.click();
      URL.revokeObjectURL(url);
      
    } catch (err) {
      console.error("Erro:", err);
      alert("Erro ao baixar ZIP");
    } finally {
      if (onlySelected) {
        setDownloadingSelected(false);
      } else {
        setDownloadingAll(false);
      }
    }
  };

  const isAnyDownloading = downloadingAll || downloadingSelected;

  return (
    <div className="fixed bottom-6 right-6 bg-[#1e1e1e] rounded-2xl shadow-2xl p-4 w-64 border border-purple-500/30">
      <h4 className="font-semibold text-purple-400 mb-2">📁 Downloads</h4>
      <p className="text-sm text-gray-400 mb-4">
        Selecionadas: {selected.length} / {images.length}
      </p>
      
      <button
        onClick={() => downloadZip(false)}
        disabled={isAnyDownloading}
        className={`w-full py-2 rounded-lg mb-2 transition flex items-center justify-center gap-2 ${
          downloadingAll 
            ? "bg-purple-700 cursor-wait" 
            : isAnyDownloading 
            ? "bg-gray-700 opacity-50 cursor-not-allowed"
            : "bg-purple-600 hover:bg-purple-700"
        }`}
      >
        {downloadingAll ? (
          <>
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            Preparando...
          </>
        ) : (
          "📦 Baixar Todas"
        )}
      </button>
      
      <button
        onClick={() => downloadZip(true)}
        disabled={selected.length === 0 || isAnyDownloading}
        className={`w-full py-2 rounded-lg transition flex items-center justify-center gap-2 ${
          downloadingSelected 
            ? "bg-green-700 cursor-wait" 
            : selected.length === 0 || isAnyDownloading 
            ? "bg-gray-700 opacity-50 cursor-not-allowed"
            : "bg-green-600 hover:bg-green-700"
        }`}
      >
        {downloadingSelected ? (
          <>
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            Preparando...
          </>
        ) : (
          "✅ Baixar Selecionadas"
        )}
      </button>
      
      {isAnyDownloading && (
        <p className="text-xs text-yellow-400 mt-2 text-center">
          Criando arquivo ZIP...
        </p>
      )}
    </div>
  );
}

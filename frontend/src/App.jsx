import { useState } from "react";
import axios from "axios";
import UploadBox from "./components/UploadBox";
import ImageGrid from "./components/ImageGrid";
import FloatingMenu from "./components/FloatingMenu";

function App() {
  const [images, setImages] = useState([]);
  const [selected, setSelected] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleUpload = async (file) => {
    try {
      setLoading(true);
      setError("");
      
      const formData = new FormData();
      formData.append("file", file);
      
      const apiUrl = import.meta.env.PROD ? "/api/extract" : "http://localhost:8000/extract";
      const res = await axios.post(apiUrl, formData);
      setImages(res.data.images);
      
    } catch (err) {
      console.error("Erro completo:", err);
      console.error("Resposta do servidor:", err.response?.data);
      const errorMessage = err.response?.data?.detail || err.message || "Erro ao processar PDF";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setImages([]);
    setSelected([]);
    setError("");
  };

  return (
    <div className="min-h-screen bg-[#0f0f0f] text-white p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-purple-500 mb-2 text-center">
          Extrator de Imagens PDF
        </h1>
        <p className="text-gray-400 mb-8 text-center">
          Envie um PDF para extrair todas as suas imagens
        </p>

        {error && (
          <div className="bg-red-900/30 border border-red-500 text-red-300 px-4 py-3 rounded-lg mb-4 max-w-2xl mx-auto">
            {error}
          </div>
        )}

        {loading && (
          <div className="text-center mb-8">
            <div className="inline-block w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mb-2"></div>
            <p className="text-purple-400">Processando PDF...</p>
          </div>
        )}

        {images.length === 0 ? (
          <UploadBox onUpload={handleUpload} loading={loading} />
        ) : (
          <>
            <button
              onClick={handleReset}
              className="mb-6 bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded-lg transition"
            >
              ⬅️ Enviar outro PDF
            </button>
            <ImageGrid 
              images={images} 
              selected={selected} 
              setSelected={setSelected} 
            />
            <FloatingMenu 
              images={images} 
              selected={selected} 
            />
          </>
        )}
      </div>
    </div>
  );
}

export default App;

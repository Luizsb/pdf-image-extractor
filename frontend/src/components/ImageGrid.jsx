export default function ImageGrid({ images, selected, setSelected }) {
  const toggleSelect = (imgName) => {
    if (selected.includes(imgName)) {
      setSelected(selected.filter((name) => name !== imgName));
    } else {
      setSelected([...selected, imgName]);
    }
  };

  // Agrupar por página
  const imagesByPage = {};
  images.forEach((img) => {
    const page = img.page || 1;
    if (!imagesByPage[page]) {
      imagesByPage[page] = [];
    }
    imagesByPage[page].push(img);
  });

  const pages = Object.keys(imagesByPage).sort((a, b) => Number(a) - Number(b));

  return (
    <div className="space-y-8">
      {pages.map((pageNum) => (
        <div key={pageNum}>
          <h3 className="text-xl font-semibold text-purple-400 mb-4">
            📄 Página {pageNum} ({imagesByPage[pageNum].length} {imagesByPage[pageNum].length === 1 ? 'imagem' : 'imagens'})
          </h3>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {imagesByPage[pageNum].map((img) => (
              <div
                key={img.name}
                className="bg-[#1a1a1a] rounded-lg overflow-hidden hover:shadow-lg hover:shadow-purple-500/20 transition"
              >
                <div className="aspect-square bg-[#2a2a2a] overflow-hidden">
                  <img
                    src={img.data}
                    alt={img.name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-3 flex items-center justify-between">
                  <label className="flex items-center gap-2 cursor-pointer hover:text-purple-300 transition">
                    <input
                      type="checkbox"
                      checked={selected.includes(img.name)}
                      onChange={() => toggleSelect(img.name)}
                      className="w-4 h-4 accent-purple-600 cursor-pointer"
                    />
                    <span className="text-sm">Selecionar</span>
                  </label>
                  <a
                    href={img.data}
                    download={img.name}
                    className="bg-purple-600/20 hover:bg-purple-600 px-3 py-1 rounded text-sm transition flex items-center gap-1"
                  >
                    ⬇️ <span className="hidden sm:inline">Baixar</span>
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

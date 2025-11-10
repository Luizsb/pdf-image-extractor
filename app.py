import streamlit as st
import fitz
import os
import shutil
from zipfile import ZipFile
from io import BytesIO

st.set_page_config(page_title="Extrator de Imagens de PDF", page_icon="🖼️", layout="wide")

# ===== CSS =====
st.markdown("""
<style>
/* Botão flutuante fixo */
.fab {
    position: fixed;
    bottom: 25px;
    right: 25px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 50%;
    width: 64px;
    height: 64px;
    font-size: 28px;
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    transition: background-color 0.3s, transform 0.2s;
    z-index: 999;
}
.fab:hover {
    background-color: #45a049;
    transform: scale(1.05);
}

/* Painel de downloads */
.download-panel {
    position: fixed;
    bottom: 100px;
    right: 25px;
    background-color: #1e1e1ee6;
    color: #fff;
    padding: 1rem 1.2rem;
    border-radius: 16px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    width: 260px;
    z-index: 1000;
    animation: fadeIn 0.3s ease;
}
.download-panel h4 {
    margin-top: 0;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# ===== UI =====
st.title("🖼️ Extrator de Imagens de PDF")
st.caption("Envie um PDF, visualize as imagens extraídas e baixe do seu jeito.")

uploaded_file = st.file_uploader("📂 Envie seu PDF", type=["pdf"])

if uploaded_file:
    output_dir = "imagens_extraidas"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        total_imagens = 0
        for page_num, page in enumerate(doc, start=1):
            imagens = page.get_images(full=True)
            for img_index, img in enumerate(imagens, start=1):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n >= 4:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                base_img = f"pagina{page_num:03d}_img{img_index:02d}.png"
                pix.save(os.path.join(output_dir, base_img))
                total_imagens += 1

    if total_imagens == 0:
        st.warning("Nenhuma imagem encontrada neste PDF.")
    else:
        st.success(f"✅ {total_imagens} imagem(ns) extraída(s).")

        imagens = sorted(os.listdir(output_dir))
        selecionadas = []

        cols = st.columns(4)
        for idx, img_file in enumerate(imagens):
            col = cols[idx % 4]
            with col:
                st.image(os.path.join(output_dir, img_file), use_container_width=True)
                checked = st.checkbox("Selecionar", key=img_file)
                if checked:
                    selecionadas.append(img_file)
                st.download_button(
                    "⬇️ Baixar",
                    data=open(os.path.join(output_dir, img_file), "rb").read(),
                    file_name=img_file,
                    mime="image/png",
                    use_container_width=True,
                )

        # ZIPs
        all_zip = BytesIO()
        with ZipFile(all_zip, "w") as zipf:
            for img in imagens:
                zipf.write(os.path.join(output_dir, img), img)
        all_zip.seek(0)

        selected_zip = None
        if selecionadas:
            selected_zip = BytesIO()
            with ZipFile(selected_zip, "w") as zipf:
                for img in selecionadas:
                    zipf.write(os.path.join(output_dir, img), img)
            selected_zip.seek(0)

        # ===== BOTÃO FLUTUANTE =====
        st.markdown('<button class="fab" id="fab">⬇️</button>', unsafe_allow_html=True)

        # ===== PAINEL (renderiza via HTML + Streamlit) =====
        st.markdown(f"""
        <div class="download-panel" id="download-panel" style="display:none;">
            <h4>📁 Downloads</h4>
            <p>Selecionadas: <b>{len(selecionadas)}</b> / {len(imagens)}</p>
        </div>
        """, unsafe_allow_html=True)

        # ===== BOTÕES DENTRO DO PAINEL =====
        panel = st.container()
        with panel:
            st.download_button(
                "📦 Baixar todas (ZIP)",
                data=all_zip,
                file_name="todas_as_imagens.zip",
                mime="application/zip",
                use_container_width=True,
            )
            st.download_button(
                "✅ Baixar selecionadas (ZIP)",
                data=selected_zip if selected_zip else b"",
                file_name="selecionadas.zip",
                mime="application/zip",
                disabled=not bool(selecionadas),
                use_container_width=True,
            )
            if selecionadas:
                if st.button("🧹 Limpar seleção", use_container_width=True):
                    st.experimental_rerun()

        # ===== JS: alterna painel =====
        st.markdown("""
        <script>
        const fab = window.parent.document.getElementById("fab");
        const panel = window.parent.document.getElementById("download-panel");
        if (fab && panel) {
            fab.addEventListener("click", () => {
                panel.style.display = panel.style.display === "none" ? "block" : "none";
            });
        }
        </script>
        """, unsafe_allow_html=True)

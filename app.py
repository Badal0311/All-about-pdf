import os
import streamlit as st
from PyPDF2 import PdfReader, PdfWriter 



def main():
    st.set_page_config(page_title="Ask ur PDF",
                       page_icon="📄")

    hide_st_style = """
            <style>
            #mainMenue {visibility: hidden;}
            footer {visibility: hidden;}
            #header {visibility: hidden;}
            </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # st.write(st.set_page_config)
    st.header("Explore your PDF 🤔💭")
    
    #uploading file
    pdf = st.file_uploader("Upload your PDF ", type="pdf")

    # extract the text
    if pdf is not None:
        option = st.selectbox("What you want to do with PDF📜", [
            "Meta Data📂",
            "Extract Raw Text📄",
            "Extract Links🔗",
            "Extract Images🖼️",
            "Make PDF password protected🔐",
            "PDF Annotation📝"
            ])
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        if option == "Meta Data📂":
            st.write(pdf_reader.metadata)
        elif option == "Make PDF password protected🔐":
            pswd = st.text_input("Enter yourpass word", type="password")
            if pswd:
                with st.spinner("Encrypting..."):
                    pdf_writer = PdfWriter()
                    for page_num in range(len(pdf_reader.pages)):
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                        
                    pdf_writer.encrypt(pswd)
                    with open(f"{pdf.name.split('.')[0]}_encrypted.pdf", "wb") as f:
                        pdf_writer.write(f)

                    st.success("Encryption Successful!")
                    st.download_button(
                        label="Download Encrypted PDF",
                        data=open(f"{pdf.name.split('.')[0]}_encrypted.pdf", "rb").read(),
                        file_name=f"{pdf.name.split('.')[0]}_encrypted.pdf",
                        mime="application/octet-stream",
                    )
                    try:
                        os.remove(f"{pdf.name.split('.')[0]}_encrypted.pdf")
                    except: pass
        elif option == "Extract Raw Text📄":
            st.write(text)
        elif option == "Extract Links🔗":
            for page in pdf_reader.pages:
                if "/Annots" in page:
                    for annot in page["/Annots"]:
                        subtype = annot.get_object()["/Subtype"]
                        if subtype == "/Link":
                            try:
                                st.write(annot.get_object()["/A"]["/URI"])
                            except: pass
        elif option == "Extract Images🖼️":
            for page in pdf_reader.pages:
                try:
                    for img in page.images:
                        st.write(img.name)
                        st.image(img.data)
                except: pass
        elif option == "PDF Annotation📝":
            for page in pdf_reader.pages:
                if "/Annots" in page:
                    for annot in page["/Annots"]:
                        obj = annot.get_object()
                        st.write(obj)
                        st.write("***********")
                        annotation = {"subtype": obj["/Subtype"], "location": obj["/Rect"]}
                        st.write(annotation)
        
    

if __name__ == "__main__":
    main()
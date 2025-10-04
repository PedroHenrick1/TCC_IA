from pathlib import Path
from docling.document_converter import DocumentConverter
from .models import ProcessedDocument
from itertools import chain

def process_pdfs_in_folder(folder_path: str):
    folder = Path(folder_path)
    converter = DocumentConverter()
    files = chain(folder.glob("*.pdf"), folder.glob("*.docx"), folder.glob("*.txt"), folder.glob("*.csv"))

    for pdf_file in files:
        file_hash = ProcessedDocument.calculate_hash(pdf_file)
        doc_entry = ProcessedDocument.objects.filter(file_path=str(pdf_file)).first()

        # Verifica se já existe e se o conteúdo mudou
        if doc_entry and doc_entry.file_hash == file_hash:
            print(f"Já processado: {pdf_file.name}")
            continue

        print(f"Processando: {pdf_file.name}")
        result = converter.convert(str(pdf_file)).document # Converte o documento em partes para ficar mais fácil da IA entender
        content = result.export_to_markdown() # Exporta em formado .MD

        if doc_entry: # Se o arquivo já foi criado e deseja modificar entre aqui
            doc_entry.file_hash = file_hash
            doc_entry.content = content
            doc_entry.save()
        else: # Se o arquivo não foi criado 
            ProcessedDocument.objects.create(
                file_path=str(pdf_file),
                file_hash=file_hash,
                content=content
            )


def load_all_docs():
    docs = ProcessedDocument.objects.all().values_list("content", flat=True)
    return "\n\n".join(docs)

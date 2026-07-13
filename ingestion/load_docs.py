from llama_index.core import Document, SimpleDirectoryReader
from llama_index.core.readers.base import BaseReader
from llama_index.readers.file import PyMuPDFReader



def load_documents(input_dir:str='data/raw') -> list[Document]:

    """
    Load documents from a directory using PyMuPDF for PDF files

    Args:
        input_dir=Path to the directory containing the source files

    Returns:
        A list of the loaded documents 
    
    """

    parser=PyMuPDFReader() # create an instance(Object) of the PyMuPDFReader

    #File extractor dictionaary
    file_extractor:dict[str, BaseReader]= {".pdf":parser}

    # Create an instance of the SimpleDirectoryReader
    reader=SimpleDirectoryReader(
        input_dir=input_dir, # path to the directory
        filename_as_id=True,#Use the file name as document id
        file_extractor=file_extractor
    )

    documents=reader.load_data() #loads data and returns a list of documents
    return documents



def main():
    #documents=load_documents()
    #print(type(documents)) #list
    #print(len(documents))  # 189
    #print(type(documents[0]))
    #print(documents[0].id_)
    #print(documents[0].metadata)
    #print(documents[0].text[:500])  # first 500 characters
    #print(vars(documents[0]))

    pass


if __name__=="main":
    main()

from typing import List
from create_dataset.main.document_store import BaseDocumentStore
from abc import abstractmethod
from create_dataset.main.schema import Document

class Pipeline:
    def __init__(self, document_store: BaseDocumentStore):
        self.document_store = document_store
        
    def start_pipeline(self):
        documents = self.process_dataset()
        self.__ingest_dataset(documents)
        self.end_process()
     
    @abstractmethod   
    def process_dataset(self) -> List[Document]:
        """
        Function to process dataset for ingestion
        """
        pass
    
    def __ingest_dataset(self, documents: List[Document]):
        self.document_store.write_documents(documents=documents)
    
    @abstractmethod   
    def end_process(self):
        """
        Closing pipeline conditions
        """
        pass
    
        
    def read_document_store(self, print_val = False):
        return self.document_store.get_all_documents(print_val)
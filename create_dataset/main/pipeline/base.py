import os
from typing import List
from create_dataset.main.document_store import BaseDocumentStore
from abc import abstractmethod
from create_dataset.main.schema import Document

class Pipeline:
    def __init__(self, document_store: BaseDocumentStore, mandatory_envs: List[str] = []):
        self.document_store = document_store
        self.check_mandatory_envs(mandatory_envs)
        
    def check_mandatory_envs(self, mandatory_envs):
        for env in mandatory_envs:
            if not os.environ.get(env):
                raise Exception(f"Environment variable {env} not set for pipeline !!!!")
        
    def start_pipeline(self, **kwargs):
        documents = self.process_dataset(**kwargs)
        self.__ingest_dataset(documents)
        self.end_process()
     
    @abstractmethod   
    def process_dataset(self, **kwargs) -> List[Document]:
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
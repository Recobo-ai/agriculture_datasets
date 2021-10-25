import logging
from create_dataset.main.pipeline import Pipeline
from create_dataset.main.document_store import BaseDocumentStore
from typing import List
from create_dataset.main.schema.document import Document


logger = logging.getLogger(__name__)

class TranslationPipeline(Pipeline):
    def __init__(self, document_store: BaseDocumentStore):
        super(TranslationPipeline, self).__init__(document_store=document_store)
        
    def process_dataset(self) -> List[Document]:
        # # testing
        # text_list = ["test3", "text4"]
        # documents_objects = [Document(text=x, meta={'some_key':'value', 'another_key':'value1'}) for x in text_list]
        # return documents_objects
        pass
    
    def end_process(self):
        pass
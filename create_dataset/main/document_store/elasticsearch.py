import logging
from create_dataset.main.schema import Document
from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk
from create_dataset.main.schema import Document
from create_dataset.main.document_store import BaseDocumentStore
from typing import List

logger = logging.getLogger(__name__)

class ElasticsearchDocumentStore(BaseDocumentStore):
    def __init__(
                self,
                index: str,
                host: str = "localhost",
                port: int = 9200,
                create_index: bool = True,
                refresh_type: str = "wait_for",
        ):
            self.client = Elasticsearch(
                hosts=[{"host": host, "port": port}], scheme="http", timeout=30, max_retries=10, retry_on_timeout=True)

            self.index = index
            self._connect(create_index) 
            self.refresh_type = refresh_type
            
    def _connect(self, create_index):
        self.client = Elasticsearch(hosts=[{"host": "localhost", 
                                        "port": 9200}], scheme="http", timeout=30, max_retries=10, retry_on_timeout=True)
        if create_index:
            self.client.indices.create(index=self.index)
            
    def get_all_documents(self, print_val = False):
        body = {"query": {"match_all": {}}}
        res = self.client.search(index=self.index, body=body)
        if print_val:
            print("Got %d Hits:" % res['hits']['total']['value'])
            for hit in res['hits']['hits']:
                print(f"{hit['_source']}")
        return res
    
    def write_documents(self, documents: List[Document]):
        documents_to_index = []
        for doc in documents:
            _doc = {
                "_op_type": "index",
                "_index": self.index,
                **doc.to_dict(field_map={"text": "text"})
            }

            # rename id for elastic
            _doc["_id"] = str(_doc.pop("id"))

            # expand meta and store in elastic search as flat values
            if "meta" in _doc.keys():
                for k, v in _doc["meta"].items():
                    _doc[k] = v
                _doc.pop("meta")
            documents_to_index.append(_doc)
        
        for success, info in parallel_bulk(self.client, documents_to_index, request_timeout=300, refresh="wait_for"):
            if not success:
                raise Exception(f'Parallel Bulk error {info}')

        


from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk
from create_dataset.main import document_store
from create_dataset.main.schema import Document

def connect(index, create = False):

    client = Elasticsearch(hosts=[{"host": "localhost", 
                                    "port": 9200}], scheme="http", timeout=30, max_retries=10, retry_on_timeout=True)
    if create:
        client.indices.create(index=index)
    return client
    
def ingest(client, index, text_list):
    documents_objects = [Document(text=x) for x in text_list]

    documents_to_index = []
    for doc in documents_objects:
        _doc = {
            "_op_type": "index",
            "_index": index,
            **doc.to_dict(field_map={"text": "text"})
        }

        # rename id for elastic
        _doc["_id"] = str(_doc.pop("id"))

        if "meta" in _doc.keys():
            for k, v in _doc["meta"].items():
                _doc[k] = v
            _doc.pop("meta")
        documents_to_index.append(_doc)
    for success, info in parallel_bulk(client, documents_to_index, request_timeout=300, refresh="wait_for"):
        if not success:
            raise Exception(f'Parallel Bulk error {info}')
    return client

def get_all_documents(client, index):
    body = {"query": {"match_all": {}}}
    res = client.search(index=index, body=body)
    # print("Got %d Hits:" % res['hits']['total']['value'])
    # for hit in res['hits']['hits']:
    #     print(f"{hit['_source']}")
        
def test_connection():
    index = "test_es"
    create = False
    text_list = ["list1", "text2"]
    client = connect(index, create=create)
    # ingest(client=client, text_list=text_list)
    get_all_documents(client=client, index=index)
    
def test_document_store():
    index = "test_es1"
    create = False
    text_list = ["test3", "text4"]
    documents_objects = [Document(text=x, meta={'some_key':'value', 'another_key':'value1'}) for x in text_list]
    from create_dataset.main.document_store import ElasticsearchDocumentStore
    document_store = ElasticsearchDocumentStore(index=index, create_index=create)
    document_store.write_documents(documents=documents_objects)
    res = document_store.get_all_documents(print_val=True)
    print(f"output: {res}")
    
test_document_store()

import logging
from create_dataset.main.pipeline import Pipeline
from create_dataset.main.document_store import BaseDocumentStore
from typing import List
from create_dataset.main.schema.document import Document
import requests
import os
import json

logger = logging.getLogger(__name__)

class TranslationPipeline(Pipeline):
    def __init__(self, document_store: BaseDocumentStore):
        mandatory_envs = ['deepL_URL', 'deepL_key', 'google_URL', 'google_key']
        super(TranslationPipeline, self).__init__(document_store=document_store, mandatory_envs=mandatory_envs)
        
    def translate_google(self):
        pass
    
    def translate_deepL(self, text, target_lang):
        url = os.getenv('deepL_URL')
        auth_key = os.getenv('deepL_key')
        querystring = {"auth_key":auth_key,"text":text,"target_lang":target_lang}

        response = requests.request("GET", url, data="", headers={}, params=querystring).json()
        if 'translations' in response and len(response['translations']) > 0 and 'text' in response['translations'][0]:
            return response['translations'][0]['text']
        return None
    
    def create_translation(self, text):
        meta = {}
        german_translation = self.translate_deepL(text=text, target_lang="DE")
        if german_translation:
            meta['german_translation'] = german_translation
            english_back_translation = self.translate_deepL(text=german_translation, target_lang="EN")
            if english_back_translation:
                meta['english_back_translation'] = english_back_translation
        french_translation = self.translate_deepL(text=text, target_lang="FR")
        if french_translation:    
            meta['french_translation'] = french_translation
        
        document = Document(text=text, meta=meta)
        return document
        
    def process_dataset(self, file_path) -> List[Document]:
        # read from file_path here to create list of text
        text_list = ["This is a test sentence", "Hello world"]
        documents_objects = []
        for text in text_list:
            documents_objects.append(self.create_translation(text=text))
        return documents_objects
    
    def end_process(self):
        pass
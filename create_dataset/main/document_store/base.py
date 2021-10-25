import logging
from abc import abstractmethod, ABC
from typing import Any, Optional, Dict, List, Union
from create_dataset.main.schema import Document

logger = logging.getLogger(__name__)


class BaseDocumentStore(ABC):
    """
    Base class for implementing Document Stores.
    """
    index: Optional[str]

    @abstractmethod
    def write_documents(self, documents: Union[List[dict], List[Document]], index: Optional[str] = None):
        """Method to write documents to document store

        Args:
            documents (Union[List[dict], List[Document]]): documents to ingest in Document class format
            index (Optional[str], optional): index for document store. Defaults to None.
        """
        pass
    
    @abstractmethod
    def get_all_documents(self, print_val = False):
        """
        Method to retrieve all documents from document store
        """
        pass

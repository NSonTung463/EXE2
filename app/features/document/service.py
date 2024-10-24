from .config import db
import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


class FirebaseProvider:
    def __init__(self):
        self.collection_name = "Documents"
        self.db = db

    def upload_doc(self, data):
        """
        Uploads a document to Firestore.

        :param collection_name: Name of the Firestore collection
        :param data: Dictionary containing the document data
        :return: document is successfully uploaded, error otherwise
        """
        try:
            self.db.collection(self.collection_name).add(data)
            return f"Document uploaded successfully to collection {self.collection_name}."
        except Exception as e:
            return (f"An error occurred: {e}")

    def get_doc(self, document_id):
        """
        Retrieves a document from Firestore by collection name and document ID.

        :param collection_name: Name of the Firestore collection
        :param document_id: ID of the Firestore document
        :return: Dictionary containing the document data or None if document is not found
        """
        try:
            doc_ref = self.db.collection(self.collection_name).document(document_id)
            doc = doc_ref.get()
            if doc.exists:
                print(f"Document with ID {document_id} retrieved successfully from collection {self.collection_name}.")
                return doc.to_dict()
            else:
                print(f"No document found with ID {document_id} in collection {self.collection_name}.")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def delete_doc(self, document_id):
        """
        Deletes a document from Firestore by collection name and document ID.

        :param collection_name: Name of the Firestore collection
        :param document_id: ID of the Firestore document
        :return: document is successfully deleted, False otherwise
        """
        try:
            doc_ref = self.db.collection(self.collection_name).document(document_id)
            doc = doc_ref.get()
            if doc.exists:
                doc_ref.delete()
                return f"Document with ID {document_id} deleted successfully from collection {self.collection_name}."
            else:
                print(f"No document found with ID {document_id} in collection {self.collection_name}.")
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
    def update_doc(self, document_id, data):
        """
        Updates a document in Firestore by collection name and document ID.

        :param collection_name: Name of the Firestore collection
        :param document_id: ID of the Firestore document
        :param data: Dictionary containing the updated document data
        :return: document is successfully updated, error otherwise
        """

        try:
            doc_ref = self.db.collection(self.collection_name).document(document_id)
            doc = doc_ref.get()
            if doc.exists:
                doc_ref.update(data)
                return f"Document with ID {document_id} updated successfully in collection {self.collection_name}."
            else:
                print(f"No document found with ID {document_id} in collection {self.collection_name}.")
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        


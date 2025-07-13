from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import json

def json_to_documents(json_data):
    """
    Convert JSON data to a list of Document objects.
    Each product in the JSON is converted into a Document with relevant fields.
    """
    documents = []
    for product in json_data["products"]:
        content = f"""
        Product Name: {product['product_name']}
        Description: {product['product_description']}
        How to Use: {product.get('how_to_use', '')}
        Caution: {product.get('caution', '')}
        Price: {product['price']}
        Details: {product.get('product_details', {})}
        """
        doc = Document(page_content=content, metadata={"product_name": product["product_name"], "price": product["price"]})
        documents.append(doc)
    return documents

if __name__ == "__main__":
    # Load JSON from file
    with open("rag/products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # Convert JSON to Document objects
    docs = json_to_documents(products)
    
    # Create a vector store from the documents
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(docs, embedding)

    # Save for reuse
    vectorstore.save_local("zus_products_index")
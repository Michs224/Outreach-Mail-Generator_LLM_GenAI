import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self, file_path="app/resource/portfolio_data.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chromedb_client = chromadb.PersistentClient("app/resource/vs_portfolio")
        self.collection = self.chromedb_client.get_or_create_collection("portfolio")
        
    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                            metadatas={"Links" : row["Links"]},
                            ids=[str(uuid.uuid1())])
    
    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get("metadatas", [])
from dotenv import load_dotenv
import os

username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
mongodb_url = "mongodb+srv://${username}:${password}@gsoosp1.fmv77zg.mongodb.net/"
mongodb_db = "mydatabase"

from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
# mongodb_url = f"mongodb+srv://{username}:{password}@gsoosp1.fmv77zg.mongodb.net/"

mongodb_url = "mongodb+srv://usermcu:its!1905MDB@route.283ji9u.mongodb.net/"
mongodb_db = "data"


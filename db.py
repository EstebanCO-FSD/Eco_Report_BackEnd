# ---------------------------
# Este archivo maneja la conexión a MongoDB Atlas.
# ---------------------------

from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = "mongodb+srv://<user>:<pass>@ecoreportcluster.bjndgnv.mongodb.net/?retryWrites=true&w=majority"
DBNAME = "eco_report_db"

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DBNAME]

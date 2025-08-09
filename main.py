import uvicorn
from gui import app 
if __name__ == "__main__":
    uvicorn.run(app,port=10000)

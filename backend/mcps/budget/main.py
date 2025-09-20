from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Budget MCP Service is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3002)

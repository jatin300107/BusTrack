import uvicorn

if __name__ == "__main__":
    uvicorn.run("bustrack.main:app", host="0.0.0.1", port=10000, reload=True)
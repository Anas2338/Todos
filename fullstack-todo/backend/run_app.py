"""
Script to run the Todo API application
"""
import uvicorn
from main import app


def run_server():
    """Run the FastAPI server."""
    print("Starting Todo API server...")
    print("Visit http://localhost:8000 to access the API")
    print("Visit http://localhost:8000/docs for API documentation")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )


if __name__ == "__main__":
    run_server()
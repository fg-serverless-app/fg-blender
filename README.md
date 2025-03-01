# Blender API Project

This project provides a Python API for interacting with Blender, allowing for automation of 3D modeling tasks and integration with other systems.

## Project Structure

```
.
├── Dockerfile
├── fastapi_server.py
├── index.html
├── data/
│   ├── startup.blend
│   └── output/
│       └── out_0001.png
└── static/
    └── favicon.ico
```

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## Docker Image Build

1. Build the Docker image:
   ```bash
   docker build -t blender-api .
   ```

2. Run the container:
   ```bash
   docker run -d --apus all -p 8000:8000 blender-api
   ```

3. Access the API:
   ```
   http://localhost:8000
   ```

## Usage

Run the FastAPI server:
```bash
uvicorn fastapi_server:app --reload
```

The API will be available at `http://localhost:8000`

## Examples

Example API call:
```python
import requests

response = requests.post('http://localhost:8000/render', json={
    'scene': 'data/startup.blend',
    'output': 'data/output/out_0001.png'
})
print(response.json())
```

## License

MIT
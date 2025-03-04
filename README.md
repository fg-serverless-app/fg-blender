# Huawei Cloud FunctionGraph Blender Rendering API

A serverless Blender rendering solution built on Huawei Cloud FunctionGraph, feature:

- Image rendering (e.g. PNG/JPEG)
- Animation rendering (e.g. MP4/AVI)
- GPU-accelerated rendering capabilities

## Project Structure

```
.
├── Dockerfile                 # Container build configuration
├── fastapi_server.py          # FastAPI main application
├── requirements.txt           # Python dependencies
├── data/
│   ├── startup.blend          # Base Blender scene template
│   └── output/                # Rendering output directory
└── README.md                  # Project documentation
```

## Docker Image Build

```bash
# Build image (requires Docker)
docker build -t swr.[region].myhuaweicloud.com/[organization]/blender-api:[version] .

# Push to SWR registry
docker push swr.[region].myhuaweicloud.com/[organization]/blender-api:[version]
```

## Deployment to Huawei Cloud FunctionGraph

1. Container Image Preparation
   - Build and push image to SWR registry using above commands

2. Function Creation
   - Runtime: Container Image
   - Function Type: Event Function
   - Instance Configuration:
     - GPU Type: NVIDIA-L2/NVIDIA-T4
     - GPU Memory: 24GB/16GB
     - Memory: ≥8GB
   - Environment Variables:
     ```env
     # Required parameters
     ENDPOINT = "obs.[region].myhuaweicloud.com"  # Refer to https://console.huaweicloud.com/apiexplorer/#/endpoint/OBS
     ```

## Client Usage

Use with [fg-blender-client](https://github.com/fg-serverless-app/fg-blender-client)

## Important Notes
1. Set function timeout to 900 seconds (15 minutes) or more
2. Ensure OBS bucket and FunctionGraph are in same region
3. Configure delegated permissions (OBS OperateAccess) for first-time setup
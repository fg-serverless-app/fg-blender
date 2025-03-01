from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uuid
import bpy
import os

app = FastAPI()

class TaskRequest(BaseModel):
    renderType: str
    inputFile: str
    outputFile: str
    outputFormat: str
    startFrame: int
    endFrame: int
    threads: int
    engine: str

@app.get("/", response_class=HTMLResponse)
async def get_client():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/task")
async def submit_task(task: TaskRequest):
    try:
        task_id = str(uuid.uuid4())
        
        # 检查输入文件是否存在
        if not os.path.exists(task.inputFile):
            raise HTTPException(status_code=400, detail="输入文件不存在")
            
        # 加载Blender文件
        bpy.ops.wm.open_mainfile(filepath=task.inputFile)
        
        # 设置渲染参数
        bpy.context.scene.frame_start = task.startFrame
        bpy.context.scene.frame_end = task.endFrame
        bpy.context.scene.render.threads = task.threads
        bpy.context.scene.render.engine = task.engine
        bpy.context.scene.render.filepath = task.outputFile
        bpy.context.scene.render.image_settings.file_format = task.outputFormat
        
        # 启用GPU渲染
        bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
        bpy.context.scene.cycles.device = 'GPU'
        bpy.context.preferences.addons['cycles'].preferences.get_devices()
        for device in bpy.context.preferences.addons['cycles'].preferences.devices:
            device.use = True

        # 执行渲染
        bpy.ops.render.render(animation=True)
        
        return JSONResponse({
            "taskId": task_id,
            "status": "渲染完成",
            "outputFile": task.outputFile
        })
    except Exception as e:
        import logging
        logging.basicConfig(filename='error.log', level=logging.ERROR)
        logging.error(f"Error occurred in submit_task: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
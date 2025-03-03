from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
import uuid
import bpy
import os

app = FastAPI()

from enum import Enum

class RenderEngine(str, Enum):
    CYCLES = "CYCLES"
    BLENDER_EEVEE = "BLENDER_EEVEE"
    BLENDER_WORKBENCH = "BLENDER_WORKBENCH"

class TaskRequest(BaseModel):
    renderType: str
    inputFile: str
    outputFile: str
    outputFormat: str
    startFrame: int
    endFrame: int
    frameStep: int
    threads: int
    engine: RenderEngine
    containerFormat: Optional[str] = "MPEG4"

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
            raise HTTPException(status_code=400, detail="input file not exist")
            
        # 加载Blender文件
        bpy.ops.wm.open_mainfile(filepath=task.inputFile)
        
        # 设置渲染参数
        bpy.context.scene.frame_start = task.startFrame
        bpy.context.scene.frame_end = task.endFrame
        bpy.context.scene.frame_step = task.frameStep
        bpy.context.scene.render.threads = task.threads
        bpy.context.scene.render.engine = task.engine
        bpy.context.scene.render.filepath = task.outputFile
        bpy.context.scene.render.image_settings.file_format = task.outputFormat
        if task.outputFormat == "FFMPEG":
            container_format = "MPEG4" if task.containerFormat == "" else task.containerFormat
            bpy.context.scene.render.ffmpeg.format = container_format
            # WEBM格式特殊配置
            if container_format == "WEBM":
                # 设置WEBM格式参数
                bpy.context.scene.render.ffmpeg.codec = 'WEBM'
                bpy.context.scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
                bpy.context.scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
                bpy.context.scene.render.ffmpeg.video_bitrate = 15000
                bpy.context.scene.render.ffmpeg.gopsize = 12
            elif container_format == "DV":
                # 设置DV格式参数
                bpy.context.scene.render.resolution_x = 720  # DV要求宽度必须720
                bpy.context.scene.render.resolution_y = 576   # PAL标准高度
                bpy.context.scene.render.fps = 25             # PAL标准帧率
        
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
# 视频最后一帧获取器

一个简单的 Python 工具，用于从视频文件中提取最后一帧并保存为图片。

**✨ 已集成虚拟环境，无需额外安装任何依赖！**

## 功能

- 从视频文件中提取最后一帧
- 支持多种视频格式（MP4、AVI、MKV、MOV 等）
- 自动生成输出文件名或自定义输出路径
- 完善的错误处理

## 使用方法

### 方法一：拖拽使用（最简单）

直接把视频文件**拖拽到 `run.bat`** 上即可，会自动在视频同目录生成 `xxx_last_frame.png`。

### 方法二：命令行使用

```bash
# 基本用法（自动生成输出文件名）
run.bat video.mp4

# 指定输出路径
run.bat video.mp4 output.png
```

### 方法三：作为模块导入

```python
from extract_last_frame import extract_last_frame

# 提取最后一帧
output_path = extract_last_frame("video.mp4")
print(f"保存到: {output_path}")

# 指定输出路径
output_path = extract_last_frame("video.mp4", "custom_output.png")
```

## 支持的格式

### 输入视频格式
- MP4
- AVI
- MKV
- MOV
- WMV
- 以及其他 OpenCV 支持的视频格式

### 输出图片格式
- PNG（推荐，无损）
- JPG
- BMP
- 以及其他 OpenCV 支持的图片格式

## 示例

```bash
# 处理单个视频
python extract_last_frame.py "C:\Videos\my_video.mp4"

# 输出：✅ 最后一帧已成功保存到: C:\Videos\my_video_last_frame.png
```

## 许可证

MIT License

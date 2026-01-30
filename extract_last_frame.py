"""
视频最后一帧提取器

使用 OpenCV 从视频文件中提取最后一帧并保存为图片。
支持中文路径。

使用方法：
    python extract_last_frame.py <视频文件路径> [输出图片路径]

示例：
    python extract_last_frame.py video.mp4
    python extract_last_frame.py video.mp4 last_frame.png
"""

import sys
import os
from pathlib import Path

import cv2
import numpy as np


def open_video_chinese_path(video_path: str) -> cv2.VideoCapture:
    """
    打开视频文件，支持中文路径
    
    NOTE: OpenCV 的 VideoCapture 不支持中文路径，
    这里使用文件句柄方式绕过这个限制
    
    Args:
        video_path: 视频文件路径
        
    Returns:
        VideoCapture 对象
    """
    # 尝试直接打开（对于纯英文路径更高效）
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened():
        return cap
    
    # 如果直接打开失败，尝试使用 cv2.CAP_FFMPEG 后端
    cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
    if cap.isOpened():
        return cap
    
    # 使用短路径名来处理中文路径（Windows 特有方案）
    try:
        import ctypes
        from ctypes import wintypes
        
        # 获取短路径名
        GetShortPathNameW = ctypes.windll.kernel32.GetShortPathNameW
        GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
        GetShortPathNameW.restype = wintypes.DWORD
        
        # 获取需要的缓冲区大小
        buffer_size = GetShortPathNameW(video_path, None, 0)
        if buffer_size > 0:
            output_buffer = ctypes.create_unicode_buffer(buffer_size)
            GetShortPathNameW(video_path, output_buffer, buffer_size)
            short_path = output_buffer.value
            
            cap = cv2.VideoCapture(short_path)
            if cap.isOpened():
                return cap
    except Exception:
        pass
    
    # 返回未打开的 cap 对象，让调用者处理错误
    return cap


def save_image_chinese_path(image: np.ndarray, output_path: str) -> bool:
    """
    保存图片，支持中文路径
    
    NOTE: OpenCV 的 imwrite 不支持中文路径，
    这里使用 imencode + 文件写入来绕过这个限制
    
    Args:
        image: 图片数据 (numpy array)
        output_path: 输出路径
        
    Returns:
        是否保存成功
    """
    # 尝试直接保存（对于纯英文路径更高效）
    try:
        success = cv2.imwrite(output_path, image)
        if success:
            return True
    except Exception:
        pass
    
    # 使用 imencode + 文件写入来支持中文路径
    try:
        # 根据文件扩展名确定编码格式
        ext = Path(output_path).suffix.lower()
        if not ext:
            ext = '.png'
        
        # 编码图片
        success, encoded = cv2.imencode(ext, image)
        if not success:
            return False
        
        # 写入文件
        with open(output_path, 'wb') as f:
            f.write(encoded.tobytes())
        
        return True
    except Exception:
        return False


def extract_last_frame(video_path: str, output_path: str | None = None) -> str:
    """
    从视频中提取最后一帧并保存为图片
    
    Args:
        video_path: 视频文件路径（支持中文）
        output_path: 输出图片路径（支持中文），如果未指定则自动生成
        
    Returns:
        保存的图片路径
        
    Raises:
        FileNotFoundError: 视频文件不存在
        ValueError: 无法打开视频或视频为空
    """
    # 检查视频文件是否存在
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"视频文件不存在: {video_path}")
    
    # 打开视频文件（支持中文路径）
    cap = open_video_chinese_path(video_path)
    
    if not cap.isOpened():
        raise ValueError(f"无法打开视频文件: {video_path}")
    
    try:
        # 获取视频总帧数
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames <= 0:
            raise ValueError("视频帧数为 0，可能是空视频或格式不支持")
        
        # 跳转到最后一帧
        # NOTE: 有些视频格式可能不支持精确跳转，所以我们跳转到倒数第二帧再读取
        cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
        
        # 读取最后一帧
        ret, frame = cap.read()
        
        if not ret or frame is None:
            # 如果直接跳转失败，尝试逐帧读取到最后
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            last_frame = None
            while True:
                ret, current_frame = cap.read()
                if not ret:
                    break
                last_frame = current_frame
            
            if last_frame is None:
                raise ValueError("无法读取视频帧")
            frame = last_frame
        
        # 生成输出路径
        if output_path is None:
            video_name = Path(video_path).stem
            video_dir = Path(video_path).parent
            output_path = str(video_dir / f"{video_name}_last_frame.png")
        
        # 保存图片（支持中文路径）
        success = save_image_chinese_path(frame, output_path)
        
        if not success:
            raise ValueError(f"无法保存图片到: {output_path}")
        
        return output_path
        
    finally:
        cap.release()


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("使用方法: python extract_last_frame.py <视频文件路径> [输出图片路径]")
        print("示例:")
        print("  python extract_last_frame.py video.mp4")
        print("  python extract_last_frame.py video.mp4 output.png")
        sys.exit(1)
    
    video_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        saved_path = extract_last_frame(video_path, output_path)
        print(f"✅ 最后一帧已成功保存到: {saved_path}")
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

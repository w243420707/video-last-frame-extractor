"""
视频最后一帧提取器

使用 OpenCV 从视频文件中提取最后一帧并保存为图片。

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


def extract_last_frame(video_path: str, output_path: str | None = None) -> str:
    """
    从视频中提取最后一帧并保存为图片
    
    Args:
        video_path: 视频文件路径
        output_path: 输出图片路径，如果未指定则自动生成
        
    Returns:
        保存的图片路径
        
    Raises:
        FileNotFoundError: 视频文件不存在
        ValueError: 无法打开视频或视频为空
    """
    # 检查视频文件是否存在
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"视频文件不存在: {video_path}")
    
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    
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
        
        # 保存图片
        success = cv2.imwrite(output_path, frame)
        
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

#!/usr/bin/env python3
"""
chat2podcast 自动滚动截图工具
==============================
让用户打开微信聊天窗口，脚本自动截图 + 模拟 Page Up 滚动，
无需手动操作，只需保持微信在前台即可。

用法：
    python3 auto_screenshot.py --duration 120 --output ~/Desktop/screenshots
    python3 auto_screenshot.py --duration 60 --interval 2.5 --output ~/Desktop/wechat_shots

参数：
    --duration   总截图时长（秒），默认 120 秒
    --interval   每次截图间隔（秒），默认 2.0 秒
    --output     截图保存目录，默认 ~/Desktop/chat2podcast_screenshots
    --countdown  开始前倒计时（秒），默认 5 秒，用于切换到微信窗口

时长参考（每次截图约覆盖 8-12 条消息，取决于消息长短）：
    30 秒  → 约 120-180 条消息（适合近 1-2 天）
    60 秒  → 约 240-360 条消息（适合近 3-5 天）
    120 秒 → 约 480-720 条消息（适合近 1-2 周）
    300 秒 → 约 1200-1800 条消息（适合近 1 个月）

注意：
    - 运行前请确保 CatPaw Desk 已获得「录屏与系统录音」权限
      系统设置 → 隐私与安全性 → 录屏与系统录音 → 开启 CatPaw Desk
    - 截图时请保持微信窗口在前台，不要切换到其他应用
    - 建议先将微信聊天窗口滚动到最新消息处，再运行脚本
"""

import subprocess
import time
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime


def check_screencapture_permission():
    """检查截图权限"""
    test_path = "/tmp/chat2podcast_test.png"
    result = subprocess.run(
        ["screencapture", "-x", "-t", "png", test_path],
        capture_output=True
    )
    if os.path.exists(test_path):
        os.remove(test_path)
        return True
    return False


def countdown(seconds: int):
    """倒计时，提示用户切换到微信"""
    print(f"\n⚠️  请在 {seconds} 秒内切换到微信聊天窗口！")
    print("   脚本将自动截图并向上滚动，请保持微信在前台。\n")
    for i in range(seconds, 0, -1):
        print(f"\r   倒计时：{i} 秒...", end="", flush=True)
        time.sleep(1)
    print("\r   开始截图！                    ")


def scroll_up():
    """模拟 Page Up 键，向上滚动聊天记录"""
    subprocess.run([
        "osascript", "-e",
        'tell application "System Events" to key code 116'
    ], capture_output=True)


def take_screenshot(output_dir: Path, index: int) -> str:
    """截取当前屏幕"""
    filename = output_dir / f"chat_{index:04d}.png"
    subprocess.run([
        "screencapture", "-x", "-t", "png", str(filename)
    ], capture_output=True)
    return str(filename)


def estimate_messages(duration: float, interval: float) -> tuple[int, int]:
    """估算能截到的消息数量"""
    shots = int(duration / interval)
    min_msgs = shots * 8
    max_msgs = shots * 14
    return min_msgs, max_msgs


def main():
    parser = argparse.ArgumentParser(
        description="微信聊天记录自动滚动截图工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
时长参考：
  30 秒  → 约 120-180 条消息（近 1-2 天）
  60 秒  → 约 240-360 条消息（近 3-5 天）
  120 秒 → 约 480-720 条消息（近 1-2 周）
  300 秒 → 约 1200-1800 条消息（近 1 个月）
        """
    )
    parser.add_argument("--duration", type=float, default=120,
                        help="总截图时长（秒），默认 120")
    parser.add_argument("--interval", type=float, default=2.0,
                        help="截图间隔（秒），默认 2.0")
    parser.add_argument("--output", type=str,
                        default=str(Path.home() / "Desktop" / "chat2podcast_screenshots"),
                        help="截图保存目录")
    parser.add_argument("--countdown", type=int, default=5,
                        help="开始前倒计时（秒），默认 5")
    parser.add_argument("--no-scroll", action="store_true",
                        help="只截图不滚动（手动滚动模式）")
    args = parser.parse_args()

    # 创建输出目录
    output_dir = Path(args.output)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = output_dir / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    # 检查权限
    print("🔍 检查截图权限...")
    if not check_screencapture_permission():
        print("\n❌ 截图权限不足！")
        print("   请前往：系统设置 → 隐私与安全性 → 录屏与系统录音")
        print("   找到 CatPaw Desk 并开启权限，然后重新运行。")
        sys.exit(1)
    print("✅ 截图权限正常")

    # 估算消息数
    min_msgs, max_msgs = estimate_messages(args.duration, args.interval)
    total_shots = int(args.duration / args.interval)
    
    print(f"\n📊 本次截图计划：")
    print(f"   总时长：{args.duration} 秒")
    print(f"   截图间隔：{args.interval} 秒")
    print(f"   预计截图数：{total_shots} 张")
    print(f"   预计覆盖消息：{min_msgs} - {max_msgs} 条")
    print(f"   保存目录：{output_dir}")
    
    if not args.no_scroll:
        print(f"\n💡 提示：脚本会自动按 Page Up 键向上滚动，")
        print(f"   请确保微信聊天窗口处于焦点状态。")
    else:
        print(f"\n💡 手动滚动模式：请在截图过程中手动向上滚动聊天记录。")

    # 倒计时
    countdown(args.countdown)

    # 开始截图
    print(f"\n📸 开始截图...")
    start_time = time.time()
    shot_count = 0
    
    try:
        while True:
            elapsed = time.time() - start_time
            if elapsed >= args.duration:
                break
            
            # 截图
            shot_count += 1
            filepath = take_screenshot(output_dir, shot_count)
            
            # 进度显示
            remaining = args.duration - elapsed
            progress = (elapsed / args.duration) * 100
            bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
            print(f"\r   [{bar}] {progress:.0f}% | 已截 {shot_count} 张 | 剩余 {remaining:.0f}s", 
                  end="", flush=True)
            
            # 等待间隔
            time.sleep(args.interval * 0.6)
            
            # 滚动
            if not args.no_scroll:
                scroll_up()
                time.sleep(args.interval * 0.4)
            else:
                time.sleep(args.interval * 0.4)
    
    except KeyboardInterrupt:
        print(f"\n\n⏹️  用户中断截图")
    
    print(f"\n\n✅ 截图完成！")
    print(f"   共截图：{shot_count} 张")
    print(f"   保存位置：{output_dir}")
    print(f"\n📋 下一步：")
    print(f"   将以下路径告诉 chat2podcast：")
    print(f"   {output_dir}")


if __name__ == "__main__":
    main()

"""\nUpload video vers TikTok via tiktok-uploader (session cookie).\n"""
import argparse
import os
import sys
import tempfile

def upload(video_path: str, title: str, description: str):
    try:
        from tiktok_uploader.upload import upload_video
    except ImportError:
        print("tiktok-uploader non installe.")
        sys.exit(1)

    session_id = os.environ.get("TIKTOK_SESSION_ID")
    if not session_id:
        print("TIKTOK_SESSION_ID manquant")
        sys.exit(1)

    # Format Netscape cookie file (requis par tiktok-uploader)
    cookie_content = (
        "# Netscape HTTP Cookie File\n"
        ".tiktok.com\tTRUE\t/\tTRUE\t9999999999\tsessionid\t" + session_id + "\n"
    )
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(cookie_content)
        cookies_path = f.name

    caption = f"{title} {description}"[:2200]
    try:
        result = upload_video(
            video_path,
            description=caption,
            cookies=cookies_path,
            headless=True,
        )
        print(f"TikTok publie : {result}")
    finally:
        os.unlink(cookies_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    args = parser.parse_args()
    upload(args.video, args.title, args.description)

from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
import os
import subprocess
import uuid
import json
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for iPhone Shortcuts

# Configuration
# Windows-compatible paths
import tempfile

TEMP_DIR = tempfile.gettempdir()
UPLOAD_FOLDER = os.path.join(TEMP_DIR, "whatsapp_converter", "uploads")
OUTPUT_FOLDER = os.path.join(TEMP_DIR, "whatsapp_converter", "outputs")
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {"mp4", "mov", "avi", "mkv", "webm", "m4v"}

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# Check if FFmpeg is available
def check_ffmpeg():
    """Check if FFmpeg is installed and accessible"""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"], capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except:
        return False


FFMPEG_AVAILABLE = check_ffmpeg()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_video_info(filepath):
    """Get video metadata using ffprobe, including rotation detection."""
    if not os.path.exists(filepath):
        raise Exception("Video file not found")
    if os.path.getsize(filepath) == 0:
        raise Exception("Video file is empty")

    info = {"valid": True, "rotation": 0, "codec": None}

    try:
        # Probe stream-level metadata (codec, side_data for displaymatrix)
        probe_cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            "-show_entries",
            "stream=codec_name,codec_type:stream_side_data=rotation",
            filepath,
        ]
        probe_result = subprocess.run(
            probe_cmd, capture_output=True, text=True, timeout=15
        )
        if probe_result.returncode == 0:
            probe_data = json.loads(probe_result.stdout)
            for stream in probe_data.get("streams", []):
                if stream.get("codec_type") == "video":
                    info["codec"] = stream.get("codec_name")
                    # displaymatrix rotation is exposed as side_data
                    for sd in stream.get("side_data_list", []):
                        if "rotation" in sd:
                            info["rotation"] = int(sd["rotation"])
                    break
    except Exception as probe_err:
        # ffprobe failure is non-fatal; fall back to safe defaults
        print(f"Warning: ffprobe metadata check failed: {probe_err}")

    return info


def optimize_for_whatsapp(input_path, output_path):
    """
    Optimize video for WhatsApp status with these settings:
    - High quality H.264 encoding
    - 1080p max resolution (maintains aspect ratio)
    - High bitrate (5000k video, 192k audio)
    - 30 second max duration
    - MP4 container with proper flags for compatibility
    - Handles HEVC/H.265 input and Android rotation metadata
    """

    # Probe input for rotation and codec so we can handle Android HEVC videos
    try:
        video_meta = get_video_info(input_path)
    except Exception:
        video_meta = {"valid": True, "rotation": 0, "codec": None}

    rotation = video_meta.get("rotation", 0)
    input_codec = video_meta.get("codec") or ""

    # Build the video filter chain.
    # `transpose` corrects displaymatrix rotation that some decoders ignore.
    # After any transpose we scale so the longest edge stays ≤ 1080 px and
    # both dimensions remain divisible by 2 (required by yuv420p).
    transpose_map = {
        -90: "transpose=1",   # 90° clockwise  (Android portrait)
        270: "transpose=1",
        90:  "transpose=2",   # 90° counter-clockwise
        -270: "transpose=2",
        180: "transpose=2,transpose=2",
        -180: "transpose=2,transpose=2",
    }
    scale_filter = "scale='if(gte(iw,ih),min(1080,iw),-2)':'if(gte(iw,ih),-2,min(1080,ih))':flags=lanczos"

    if rotation in transpose_map:
        vf = f"{transpose_map[rotation]},{scale_filter}"
        print(f"→ Applying rotation correction for {rotation}°: {transpose_map[rotation]}")
    else:
        vf = scale_filter

    # For HEVC/H.265 input, explicitly set the decoder so FFmpeg does not
    # silently fall back to a slower or broken path.
    input_args = []
    if input_codec.lower() in ("hevc", "h265"):
        input_args = ["-c:v", "hevc"]
        print(f"→ HEVC input detected — using explicit hevc decoder")

    # FFmpeg command optimized for WhatsApp
    cmd = [
        "ffmpeg",
        *input_args,
        "-i",
        input_path,
        "-t",
        "30",  # Limit to 30 seconds for WhatsApp status
        "-c:v",
        "libx264",  # H.264 codec
        "-preset",
        "medium",  # Balanced speed/quality preset
        "-crf",
        "23",  # Good quality
        "-vf",
        vf,  # Scale + optional rotation correction
        "-b:v",
        "5000k",  # High video bitrate
        "-maxrate",
        "6000k",  # Max bitrate
        "-bufsize",
        "12000k",  # Buffer size
        "-pix_fmt",
        "yuv420p",  # Pixel format for compatibility
        "-threads",
        "4",  # Limit encoder threads to avoid resource contention
        "-c:a",
        "aac",  # AAC audio codec
        "-b:a",
        "192k",  # High audio bitrate
        "-ar",
        "48000",  # Audio sample rate
        "-movflags",
        "+faststart",  # Enable fast start for streaming
        "-y",  # Overwrite output file
        output_path,
    ]

    print(f"→ FFmpeg command: {' '.join(cmd)}")

    # Run FFmpeg with timeout
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120,  # 2 minute timeout
    )

    # Always log stderr so frame=0 / early-exit issues are visible in logs
    if result.stderr:
        print(f"FFmpeg stderr:\n{result.stderr[-3000:]}")

    if result.returncode != 0:
        raise Exception(f"FFmpeg error (exit {result.returncode}): {result.stderr[-2000:]}")

    # Detect silent failure: output exists but no frames were encoded
    if os.path.exists(output_path) and os.path.getsize(output_path) < 1024:
        raise Exception(
            "FFmpeg produced an unexpectedly small output file — "
            "encoding may have stalled (frame=0). "
            f"FFmpeg stderr: {result.stderr[-1000:]}"
        )

    return result


def cleanup_old_files():
    """Clean up files older than 1 hour"""
    current_time = time.time()
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath):
                if current_time - os.path.getmtime(filepath) > 3600:  # 1 hour
                    os.remove(filepath)


@app.route("/")
def index():
    """Render the main UI"""
    return render_template("index.html")


@app.route("/api")
def api_info():
    return jsonify(
        {
            "status": "online",
            "service": "WhatsApp HD Video Converter API",
            "version": "1.0",
            "ffmpeg_available": FFMPEG_AVAILABLE,
            "endpoints": {
                "/convert": "POST - Upload video for conversion",
                "/health": "GET - Check API health",
            },
            "usage": {
                "method": "POST",
                "endpoint": "/convert",
                "content_type": "multipart/form-data",
                "field_name": "video",
                "max_size": "100MB",
                "supported_formats": list(ALLOWED_EXTENSIONS),
                "output": "Optimized MP4 file",
            },
        }
    )


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "ffmpeg_available": FFMPEG_AVAILABLE,
        }
    )


@app.route("/convert", methods=["POST"])
def convert_video():
    """Convert video to WhatsApp-optimized format"""
    try:
        # Check if FFmpeg is available
        if not FFMPEG_AVAILABLE:
            return (
                jsonify(
                    {
                        "error": "FFmpeg not found. Please install FFmpeg to use this service."
                    }
                ),
                500,
            )

        # Check if file is present
        if "video" not in request.files:
            return jsonify({"error": "No video file provided"}), 400

        file = request.files["video"]

        # Check if file is selected
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        # Check file extension
        if not allowed_file(file.filename):
            return (
                jsonify(
                    {
                        "error": f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
                    }
                ),
                400,
            )

        # Generate unique file ID
        file_id = str(uuid.uuid4())
        file_extension = file.filename.rsplit(".", 1)[1].lower()
        input_filename = f"{file_id}.{file_extension}"
        output_filename = f"{file_id}_optimized.mp4"

        input_path = os.path.join(UPLOAD_FOLDER, input_filename)
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        # Save uploaded file
        file.save(input_path)

        # Get file size
        file_size = os.path.getsize(input_path)
        if file_size > MAX_FILE_SIZE:
            os.remove(input_path)
            return jsonify(
                {"error": f"File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB"}
            ), 400

        # Get video info
        try:
            video_info = get_video_info(input_path)
        except Exception as e:
            os.remove(input_path)
            return jsonify({"error": f"Invalid video file: {str(e)}"}), 400

        # Convert video
        try:
            optimize_for_whatsapp(input_path, output_path)

            # Get output file info
            output_size = os.path.getsize(output_path)

            # Clean up input file immediately after successful conversion
            try:
                if os.path.exists(input_path):
                    os.remove(input_path)
                    print(f"✓ Cleaned up input file: {input_filename}")
            except Exception as cleanup_error:
                print(f"Warning: Failed to cleanup input file: {cleanup_error}")

            # Return file info for download
            return jsonify(
                {
                    "success": True,
                    "file_id": file_id,
                    "output_filename": output_filename,
                    "output_size": output_size,
                    "download_url": f"/download/{file_id}",
                }
            )

        except Exception as e:
            # Cleanup both files on error
            try:
                if os.path.exists(input_path):
                    os.remove(input_path)
                    print(f"✓ Cleaned up input file after error: {input_filename}")
            except:
                pass
            try:
                if os.path.exists(output_path):
                    os.remove(output_path)
                    print(f"✓ Cleaned up output file after error: {output_filename}")
            except:
                pass
            return jsonify({"error": f"Conversion failed: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/download/<file_id>", methods=["GET"])
def download_video(file_id):
    """Download converted video"""
    try:
        output_filename = f"{file_id}_optimized.mp4"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        if not os.path.exists(output_path):
            return jsonify({"error": "File not found"}), 404

        print(f"→ Sending file: {output_filename}")

        response = send_file(
            output_path,
            mimetype="video/mp4",
            as_attachment=True,
            download_name=f"whatsapp_hd_{file_id}.mp4",
        )

        # Schedule cleanup of output file after sending
        @response.call_on_close
        def cleanup():
            try:
                # Wait a bit to ensure download completed
                time.sleep(2)
                if os.path.exists(output_path):
                    os.remove(output_path)
                    print(f"✓ Cleaned up output file: {output_filename}")
            except Exception as e:
                print(f"Warning: Failed to cleanup output file: {e}")

        return response

    except Exception as e:
        return jsonify({"error": f"Download error: {str(e)}"}), 500


@app.route("/cleanup", methods=["POST"])
def manual_cleanup():
    """Manual cleanup endpoint for testing"""
    try:
        cleaned_files = []

        # Cleanup upload folder
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            try:
                os.remove(filepath)
                cleaned_files.append(f"upload/{filename}")
            except:
                pass

        # Cleanup output folder
        for filename in os.listdir(OUTPUT_FOLDER):
            filepath = os.path.join(OUTPUT_FOLDER, filename)
            try:
                os.remove(filepath)
                cleaned_files.append(f"output/{filename}")
            except:
                pass

        return jsonify(
            {
                "success": True,
                "cleaned_files": cleaned_files,
                "count": len(cleaned_files),
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/storage", methods=["GET"])
def storage_info():
    """Get storage information"""
    try:
        upload_files = os.listdir(UPLOAD_FOLDER)
        output_files = os.listdir(OUTPUT_FOLDER)

        upload_size = sum(
            os.path.getsize(os.path.join(UPLOAD_FOLDER, f))
            for f in upload_files
            if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))
        )

        output_size = sum(
            os.path.getsize(os.path.join(OUTPUT_FOLDER, f))
            for f in output_files
            if os.path.isfile(os.path.join(OUTPUT_FOLDER, f))
        )

        return jsonify(
            {
                "upload_folder": {
                    "files": len(upload_files),
                    "size_bytes": upload_size,
                    "size_mb": round(upload_size / 1024 / 1024, 2),
                },
                "output_folder": {
                    "files": len(output_files),
                    "size_bytes": output_size,
                    "size_mb": round(output_size / 1024 / 1024, 2),
                },
                "total": {
                    "files": len(upload_files) + len(output_files),
                    "size_bytes": upload_size + output_size,
                    "size_mb": round((upload_size + output_size) / 1024 / 1024, 2),
                },
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)

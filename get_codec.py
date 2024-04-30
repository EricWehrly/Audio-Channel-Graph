import subprocess
import json
import sys

def get_codec(input_file):
    # Run ffprobe to get information about the input file
    ffprobe_cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', input_file]
    ffprobe_output = subprocess.check_output(ffprobe_cmd, stderr=subprocess.STDOUT)

    # Parse the JSON output
    info = json.loads(ffprobe_output)

    # Extract codec information from the first audio stream (assuming there is at least one)
    audio_streams = [stream for stream in info['streams'] if stream['codec_type'] == 'audio']
    if audio_streams:
        codec_name = audio_streams[0]['codec_name']
        codec_long_name = audio_streams[0]['codec_long_name']
        return codec_name, codec_long_name
    else:
        return None, None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_codec.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    codec_name, codec_long_name = get_codec(input_file)
    
    if codec_name:
        print(f"Codec Name: {codec_name}")
        print(f"Codec Long Name: {codec_long_name}")
    else:
        print("Error: No audio streams found in the input file.")

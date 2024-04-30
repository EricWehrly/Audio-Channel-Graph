import subprocess
import numpy as np
import matplotlib.pyplot as plt
import sys
import os.path

def analyze_audio(input_file, output_file):
    # Log input and output file paths
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)

    # Run ffprobe to get information about the input file
    ffprobe_cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_frames', input_file]
    ffprobe_output = subprocess.check_output(ffprobe_cmd, stderr=subprocess.STDOUT)
    info = json.loads(ffprobe_output)

    # Find the first audio stream
    audio_stream = next((stream for stream in info['streams'] if stream['codec_type'] == 'audio'), None)
    if audio_stream is None:
        print("Error: No audio streams found in the input file.")
        sys.exit(1)

    # Extract audio samples and calculate volume
    samples = []
    for frame in info['frames']:
        if frame['media_type'] == 'audio':
            if 'pkt_size' in frame:
                sample_size = int(frame['pkt_size'])
                samples.append(np.frombuffer(frame['coded_picture_buffer'], dtype=np.int16, count=sample_size//2))

    # Check if any audio samples were extracted
    if not samples:
        print("Error: No audio samples found in the input file.")
        sys.exit(1)

    # Calculate volume for each sample
    volumes = [np.mean(np.abs(sample)) for sample in samples]

    # Plot and save chart
    plt.plot(volumes)
    plt.xlabel('Sample')
    plt.ylabel('Volume')
    plt.savefig(output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python analyze_audio.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    analyze_audio(input_file, output_file)

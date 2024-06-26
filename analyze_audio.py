import subprocess
import numpy as np
import matplotlib.pyplot as plt
import sys
import os.path
import time
import json  # Add import statement for the json module

def analyze_audio(input_file, output_file, channel):
    start_time = time.time()

    try:
        # Log input and output file paths
        print(f"Input file: {input_file}")
        print(f"Output file: {output_file}")
        print(f"Channel: {channel}")

        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' does not exist.")
            sys.exit(1)

        # Run ffprobe to get information about the input file for the specified channel
        ffprobe_cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_frames', '-select_streams', f'a:{channel}', input_file]
        ffprobe_output = subprocess.check_output(ffprobe_cmd, stderr=subprocess.STDOUT)
        info = json.loads(ffprobe_output)

        # Extract audio samples and calculate volume
        samples = []
        for frame in info['frames']:
            if frame.get('media_type') == 'audio' and 'data' in frame:
                samples.append(np.frombuffer(frame['data'], dtype=np.int16))

        # Check if any audio samples were extracted
        if not samples:
            print("Error: No audio samples found in the input file for the specified channel.")
            sys.exit(1)

        # Calculate volume for each sample
        volumes = [np.mean(np.abs(sample)) for sample in samples]

        # Plot and save chart
        plt.plot(volumes)
        plt.xlabel('Sample')
        plt.ylabel('Volume')
        plt.savefig(output_file)

    except Exception as e:
        print(f"Error: An exception occurred: {e}")
        sys.exit(1)

    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_audio.py <input_file> [<output_file> [<channel>]]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) >= 3 else "/host/output.jpg"
    channel = int(sys.argv[3]) if len(sys.argv) == 4 else 0

    analyze_audio(input_file, output_file, channel)

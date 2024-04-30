import sys
import os.path
import ffmpeg
import numpy as np
import matplotlib.pyplot as plt

# Define the keys to exclude
EXCLUDED_KEYS = ['media_type', 'key_frame', 'pkt_pts', 'pkt_pts_time', 'pkt_dts', 'pkt_dts_time', 
                 'best_effort_timestamp', 'best_effort_timestamp_time', 'pkt_duration', 'pkt_duration_time', 
                 'pkt_pos', 'pkt_size']

unexpected_keys = set()

def analyze_audio(input_file, output_file):
    global unexpected_keys

    # Log input and output file paths
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)

    # Open the input file
    probe = ffmpeg.probe(input_file)

    # Find audio streams
    audio_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']

    # Initialize data dictionary to store volume data for each channel
    data = {f"Channel {i}": [] for i in range(len(audio_streams))}

    # Extract audio volume for each channel
    for stream in audio_streams:
        stream_index = stream['index']
        channel_count = int(stream['channels'])
        for channel in range(channel_count):
            for frame in ffmpeg.probe(input_file, select_streams=f'a:{stream_index}', show_frames=None)['frames']:
                if 'media_type' in frame and frame['media_type'] == 'audio':
                    if 'pkt_pts_time' in frame:
                        timestamp = float(frame['pkt_pts_time'])
                        volume = np.mean(np.abs(frame['channels'][channel]['data']))
                        data[f"Channel {channel}"].append((timestamp, volume))
                    else:
                        for key in frame.keys():
                            if key not in EXCLUDED_KEYS:
                                unexpected_keys.add(key)

    # Plot and save chart for each channel
    for channel, channel_data in data.items():
        timestamps, volumes = zip(*channel_data)
        plt.plot(timestamps, volumes, label=channel)

    # Add labels and legend
    plt.xlabel('Time (seconds)')
    plt.ylabel('Volume')
    plt.legend()

    # Save the plot as a JPEG file
    plt.savefig(output_file)

    # Check if there are unexpected keys
    if unexpected_keys:
        print("Warning: Unable to get timestamp. The following unexpected keys were found in the frame data:")
        for key in unexpected_keys:
            print(key)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python analyze_audio.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    analyze_audio(input_file, output_file)

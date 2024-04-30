import ffmpeg
import numpy as np

def analyze_audio(input_file, output_file):
    # Open the input file
    probe = ffmpeg.probe(input_file)

    # Find audio streams
    audio_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']

    # Open the output file for writing
    with open(output_file, 'w') as f:
        # Write header
        f.write("timestamp,channel,volume\n")

        # Extract audio volume for each channel and write to output file
        for stream in audio_streams:
            stream_index = stream['index']
            channel_count = int(stream['channels'])
            for channel in range(channel_count):
                for frame in ffmpeg.probe(input_file, select_streams=f'a:{stream_index}', show_frames=None)['frames']:
                    if 'media_type' in frame and frame['media_type'] == 'audio':
                        timestamp = float(frame['pkt_pts_time'])
                        volume = np.mean(np.abs(frame['channels'][channel]['data']))
                        f.write(f"{timestamp},{channel},{volume}\n")

# Example usage
input_file = 'input.mkv'
output_file = 'audio_analysis.csv'
analyze_audio(input_file, output_file)

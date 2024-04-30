`docker build -t audio_analysis .`

`docker run -v /path/to/input:/input -v /path/to/output:/output audio_analysis`

`docker run -v /path/to/input:/input -v /path/to/output:/output audio_analysis input.mkv audio_analysis.jpg`

`docker run -v $(pwd):/host audio_analysis /host/input.mkv /host/audio_analysis.jpg`

`docker run -v "$(pwd -W):/host" audio_analysis /host/input.mkv /host/audio_analysis.jpg`
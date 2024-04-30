# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Run analyze_audio.py when the container launches
#CMD ["python", "./analyze_audio.py"]

ENTRYPOINT [ "python",  "./analyze_audio.py" ]
CMD [ "/host/input.mkv", "output.jpg" ]

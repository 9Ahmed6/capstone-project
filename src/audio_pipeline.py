from __future__ import annotations
import ffmpeg # ffmpeg python wrapper
import os # file handling

# this function converts video audio into mono WAV at 16kHz
def extract_audio(video_path, output_audio_path):

    #create audio folder if missing
    os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)

    try:
        (
            ffmpeg

            #input video
            .input(video_path)

            #output settings:
            #pcm_s16le = wav
            #ac=1 =mono
            #ar=16000 = 16kHz
            .output(
                output_audio_path,
                format='wav',
                acodec='pcm_s16le',
                ac=1,
                ar='16000'
            )

            # overwrite existing file
            .run(overwrite_output=True)
        )

        return output_audio_path
    
    except FileNotFoundError:
        print("FFmpeg executable not found. Install FFmpeg and add it to PATH.")
        return None
    
    except ffmpeg.Error as e:

        #print error if extraction fails
        print("FFmpeg error:", e)
        return None
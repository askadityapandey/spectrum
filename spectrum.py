import os
from pydub import AudioSegment
import soundfile as sf
import librosa
import numpy as np

def read_audio(filepath):
    """
    This function reads an audio file from the specified path.

    Args:
        filepath (str): Path to the audio file.

    Returns:
        tuple: A tuple containing the audio data (numpy array) and sample rate (int),
             or None if the file cannot be read.
    """
    try:
        filepath = os.path.expanduser(filepath)  # Expand ~ to the user's home directory
        filepath = os.path.abspath(filepath)  # Convert to absolute path
        print(f"Reading audio file from: {filepath}")  # Debugging statement
        
        if filepath.lower().endswith('.m4a'):
            # Use pydub to read .m4a file and convert to .wav in memory
            audio = AudioSegment.from_file(filepath, format='m4a')
            audio = audio.set_channels(1)  # Ensure it's mono
            audio = audio.set_frame_rate(22050)  # Standard sampling rate for librosa
            samples = np.array(audio.get_array_of_samples())
            samples = samples.astype(np.float32) / np.iinfo(samples.dtype).max  # Normalize to -1 to 1
            sample_rate = audio.frame_rate
        else:
            # Use soundfile for other formats
            samples, sample_rate = sf.read(filepath)
        
        return samples, sample_rate
    except FileNotFoundError:
        print(f"Error: Audio file not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def process_audio(audio_data, sample_rate, options):
    """
    This function performs the audio processing based on user-specified options.

    Args:
        audio_data (numpy.ndarray): The audio data as a NumPy array.
        sample_rate (int): The sample rate of the audio data.
        options (dict): Dictionary containing user-selected processing options.

    Returns:
        numpy.ndarray: The processed audio output as a NumPy array.
    """
    # Noise reduction (optional)
    if options.get("noise_reduction"):
        pass  # Placeholder for noise reduction

    # Speech emphasis (optional)
    if options.get("speech_emphasis"):
        rolloff_freq = options.get("rolloff_freq", 0.1 * sample_rate)
        audio_data = librosa.effects.preemphasis(audio_data, coef=rolloff_freq/sample_rate)

    # Bass/treble boost (optional)
    if options.get("bass_boost"):
        pass  # Placeholder for bass boost
    elif options.get("treble_boost"):
        pass  # Placeholder for treble boost

    # Normalization (optional)
    if options.get("normalize"):
        audio_data = librosa.util.normalize(audio_data)

    # Compression (optional)
    if options.get("compress"):
        pass  # Placeholder for compression

    return audio_data

def write_audio(processed_data, sample_rate, output_path):
    """
    This function writes the processed audio data to a new file.

    Args:
        processed_data (numpy.ndarray): The processed audio data.
        sample_rate (int): The sample rate of the audio data.
        output_path (str): The path to save the output file.
    """
    sf.write(output_path, processed_data, sample_rate)

def get_user_input(prompt):
    """
    This function gets user input for a specified prompt.

    Args:
        prompt (str): The message to display to the user.

    Returns:
        str: The user's input as a string.
    """
    while True:
        user_input = input(prompt)
        if user_input:
            return user_input.strip()  # Remove leading/trailing whitespaces
        else:
            print("Please enter a value.")

def main():
    # Get audio file path from user
    audio_filepath = get_user_input("Enter the path to your audio file: ")
    
    # Read the audio file
    audio_data, sample_rate = read_audio(audio_filepath)
    if audio_data is None:
        return
    
    # Define processing options (these can be replaced with user input later)
    options = {
        "noise_reduction": True,  # Optional
        "speech_emphasis": True,  # Optional
        "rolloff_freq": 0.1 * sample_rate,  # Optional, adjust roll-off frequency
        "bass_boost": None,  # Optional, set value for bass boost
        "treble_boost": None,  # Optional, set value for treble boost
        "normalize": True,  # Optional
        "compress": False  # Optional
    }

    # Process the audio
    processed_audio = process_audio(audio_data, sample_rate, options)

    # Get output file path from user
    output_filepath = get_user_input("Enter the path to save the processed audio file: ")

    # Write the processed audio to a file
    write_audio(processed_audio, sample_rate, output_filepath)
    
    print("Audio processing complete!")

if __name__ == "__main__":
    main()

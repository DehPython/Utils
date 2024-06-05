import os
import wave
import numpy as np
import json
from tqdm import tqdm

def get_wav_files(directory):
    """Retorna uma lista de caminhos de arquivos .wav dentro do diretório e subdiretórios."""
    wav_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".wav"):
                wav_files.append(os.path.join(root, file))
    return wav_files

def concatenate_wav_files(files, max_duration, part_filename):
    """Concatena arquivos .wav até atingir a duração máxima, retorna áudio combinado, metadados e taxa de amostragem."""
    combined_audio = []
    metadata = []
    total_duration = 0
    sample_rate = None
    for file in tqdm(files, desc="Concatenating audio files", unit="file"):
        with wave.open(file, 'rb') as wav:
            if sample_rate is None:
                sample_rate = wav.getframerate()
            frames = wav.readframes(wav.getnframes())
            audio_data = np.frombuffer(frames, dtype=np.int16)
            duration = wav.getnframes() / float(wav.getframerate())
            if total_duration + duration > max_duration:
                break
            combined_audio.append(audio_data)
            metadata.append({
                'file': file,
                'duration': duration,
                'start_time': total_duration,
                'part': part_filename  # Adiciona o nome do arquivo concatenado ao metadata
            })
            total_duration += duration
    combined_audio = np.concatenate(combined_audio)
    return combined_audio, metadata, sample_rate

def save_combined_wav(combined_audio, output_path, framerate=44100):
    """Salva o áudio combinado em um arquivo .wav."""
    with wave.open(output_path, 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(framerate)
        wav.writeframes(combined_audio.tobytes())

def create_metadata_file(metadata, output_path):
    """Salva o arquivo de metadados contendo informações sobre cada áudio original."""
    with open(output_path, 'w') as json_file:
        json.dump(metadata, json_file, indent=4)

def create_file_paths_txt(output_dir):
    """Cria um arquivo txt com os caminhos completos de cada arquivo de áudio na pasta de saída."""
    file_paths = [os.path.abspath(os.path.join(output_dir, file)) for file in os.listdir(output_dir) if file.endswith(".wav")]
    with open(os.path.join(output_dir, "file_paths.txt"), 'w') as f:
        for path in file_paths:
            f.write(f"{path}\n")

def main(directory, output_dir, max_duration=29*60 + 40):
    os.makedirs(output_dir, exist_ok=True)
    wav_files = get_wav_files(directory)
    metadata = []
    part_number = 1
    while wav_files:
        part_filename = f"output_part_{part_number}.wav"
        combined_audio, part_metadata, framerate = concatenate_wav_files(wav_files, max_duration, part_filename)
        output_path = os.path.join(output_dir, part_filename)
        save_combined_wav(combined_audio, output_path, framerate)
        metadata.extend(part_metadata)
        part_number += 1
        # Remove arquivos processados da lista
        processed_files = [entry['file'] for entry in part_metadata]
        wav_files = [file for file in wav_files if file not in processed_files]
    # Criar um único arquivo de metadados
    create_metadata_file(metadata, os.path.join(output_dir, "metadata.json"))
    # Criar o arquivo file_paths.txt
    create_file_paths_txt(output_dir)

# Exemplo de uso
if __name__ == "__main__":
    directory = "cml_tts_dataset_polish_v0.1"
    output_dir = "output"
    main(directory, output_dir)

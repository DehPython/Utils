import json
from pydub import AudioSegment
import os
from tqdm import tqdm

def load_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def process_audio_segments(json_data, input_directory, output_base_path):
    # Cria um dicionário para armazenar os arquivos de áudio carregados
    audio_files = {}

    # Utiliza tqdm para mostrar a barra de progresso
    for segment_info in tqdm(json_data, desc="Processing audio segments"):
        part_file = segment_info["part"]  # Obtém o nome do arquivo de áudio a partir do JSON
        start_ms = segment_info["start_time"] * 1000  # Converte start_time de segundos para milissegundos
        end_ms = start_ms + segment_info["duration"] * 1000  # Calcula o fim do segmento em milissegundos
        
        # Carrega o arquivo de áudio se ainda não estiver carregado
        if part_file not in audio_files:
            audio_path = os.path.join(input_directory, part_file)
            audio_files[part_file] = AudioSegment.from_wav(audio_path)
        
        # Extrai o segmento do áudio
        audio = audio_files[part_file]
        segment = audio[start_ms:end_ms]
        
        output_path = os.path.join(output_base_path, segment_info["file"])  # Constrói o caminho de saída completo
        
        # Cria o diretório se ele não existir
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Exporta o segmento para o arquivo correspondente
        segment.export(output_path, format='wav')

def main():
    # Caminho para o JSON e o diretório de entrada
    json_path = 'output/metadata.json'  # Ajuste para o local correto do seu arquivo JSON
    input_directory = 'output'  # Diretório contendo os arquivos de áudio grandes
    output_base_path = 'saida'  # Caminho base para salvar os segmentos extraídos
    
    # Carregando os dados JSON
    json_data = load_json(json_path)
    
    # Processando os segmentos de áudio
    process_audio_segments(json_data, input_directory, output_base_path)

if __name__ == "__main__":
    main()

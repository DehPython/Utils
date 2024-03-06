import os
import argparse
from pydub import AudioSegment

def main():
    # Configuração do argparse
    parser = argparse.ArgumentParser(description='Converte arquivos de áudio de uma pasta de entrada para um formato especificado e os salva em uma pasta de saída, mantendo a estrutura de diretórios.')
    parser.add_argument('-i', '--input_folder', required=True, help='Nome da pasta de entrada onde estão os arquivos de áudio.')
    parser.add_argument('-o', '--output_folder', required=True, help='Nome da pasta de saída para os arquivos convertidos.')
    parser.add_argument('-f', '--format', required=True, choices=['mp3', 'wav', 'ogg', 'flac', 'aac', 'wma', 'mp4'], help='Formato de destino para a conversão dos arquivos de áudio.')
    args = parser.parse_args()

    # Verificar e criar as pastas de entrada e saída, se necessário
    if not os.path.exists(args.input_folder):
        print(f"A pasta de entrada especificada ({args.input_folder}) não existe.")
        exit()
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    # Função para converter os arquivos
    def converter_arquivo_audio(caminho_origem, caminho_destino, formato_destino):
        try:
            audio = AudioSegment.from_file(caminho_origem)
            audio.export(caminho_destino, format=formato_destino)
            print(f"Arquivo convertido e salvo em: {caminho_destino}")
        except Exception as e:
            print(f"Erro ao converter o arquivo {caminho_origem}: {e}")

    # Função para percorrer a pasta de entrada e converter os arquivos
    def percorrer_e_converter(diretorio, formato_destino, pasta_base_input, pasta_base_output):
        for root, dirs, files in os.walk(diretorio):
            for file in files:
                caminho_completo = os.path.join(root, file)
                caminho_destino = caminho_completo.replace(pasta_base_input, pasta_base_output, 1)
                caminho_destino = os.path.splitext(caminho_destino)[0] + '.' + formato_destino
                os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)
                converter_arquivo_audio(caminho_completo, caminho_destino, formato_destino)

    # Iniciar a conversão
    percorrer_e_converter(args.input_folder, args.format, args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()

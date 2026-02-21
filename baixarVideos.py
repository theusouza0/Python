from pytubefix import YouTube
from pytubefix.cli import on_progress

def baixar_video(url, caminho_destino):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download(caminho_destino)
        print(f"Vídeo '{yt.title}' baixado com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao baixar o vídeo: {e}")
        
if __name__ == "__main__":
    url_video = input("Digite a URL do vídeo do YouTube: ")
    caminho_destino = input("Digite o caminho de destino para salvar o vídeo: ")
    baixar_video(url_video, caminho_destino)
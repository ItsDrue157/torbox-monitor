import requests

def enviar_notificacao(evento):
    
    nome = evento["nome"]
    status = evento["tipo"]

    mensagem =  f'O torrent {nome}, está {status}'
    requests.post("https://ntfy.sh/carlos_alertatorbox", data=mensagem, headers={"Title":"Nova mensagem"})




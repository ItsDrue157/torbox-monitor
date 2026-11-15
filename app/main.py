from client.client import get_downloads
from repository.repository import criar_tabela_downloads
from service.service import processar_downloads
from notifications.ntfy import enviar_notificacao

import time

criar_tabela_downloads()

while True:
    lista_eventos = get_downloads()
    print(lista_eventos)
    download_processados = processar_downloads(lista_eventos)
    print(download_processados)
    for evento in download_processados:
        enviar_notificacao(evento)
        print(enviar_notificacao(evento))

    time.sleep(30)
    

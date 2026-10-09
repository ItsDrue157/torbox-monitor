from repository.repository import buscar_download,salvar_downloads,atualizar_download


def criar_evento(download, estado_antigo):
    state_download = download["download_state"]
    nome_download = download["name"]
    if state_download != estado_antigo:
        match state_download:
            case "completed":
                return {
                            "tipo":state_download,
                            "nome":nome_download
                        }
            case "downloading":
                pass

            case "error":
                return {
                            "tipo":state_download,
                            "nome":nome_download
                        }
            case "cached":
                return {
                    "tipo":state_download,
                    "nome":nome_download
                }
            case "checking":
                return {
                    "tipo":state_download,
                    "nome":nome_download
                }
                
                

def processar_downloads(downloads):
    lista_de_eventos = []
    for download in downloads:
        id_download = download["id"]
        resultado = buscar_download(id_download)
        if resultado is None:
            salvar_downloads(download)
        else:
            download_antigo = resultado
            download_novo = download["download_state"]
            if download_novo != download_antigo:
                atualizar_download(download)
                evento = criar_evento(download, estado_antigo=download_antigo)
                if evento is not None:
                    lista_de_eventos.append(evento)
            else:
                atualizar_download(download)
        
    return lista_de_eventos



        
    



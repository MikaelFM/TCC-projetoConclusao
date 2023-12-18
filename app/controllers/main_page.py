from flask import session
from app.models import *

def getDados():
    registros = EmailProgramado.getRegistros()
    arquivos = Arquivos.getArquivos()
    servidores = Servidor.getServidores()
    eventos = Eventos.getEventos()
    tipoServidores = TiposServidores.getTipoServidores()
    privacidadeTipos = PrivacidadeTipos.getPrivacidadeTipos()
    return {
        'registros': registros,
        'arquivos': arquivos,
        'servidores': servidores,
        'eventos': eventos,
        'tipoServidores': tipoServidores,
        'tiposPrivacidade':privacidadeTipos
    }
[app]

# Nome do seu aplicativo
title = Termoo

# Nome do pacote
package.name = termoo

# Domínio do pacote
package.domain = org.termoo
    
# Código fonte
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

# Lista de palavras personalizada
source.include_patterns = listaDePalavrasFinal_01_12_2024__22_28.py

# Versão do aplicativo
version = 0.1

# Requisitos (incluindo wordfreq)
requirements = python3,kivy,wordfreq,numpy

# Orientação da tela
orientation = portrait

# Permissões do Android
android.permissions = INTERNET

# Configurações do SDK do Android
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 23b

[buildozer]
# Pasta de log
log_level = 2
warn_on_root = 1

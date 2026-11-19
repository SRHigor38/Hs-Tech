# Instalação local

Veja os passos em [README.md](README.md). No Windows, ative o ambiente com `.venv\Scripts\Activate.ps1`; no Linux/macOS, use `source .venv/bin/activate`. Se a criação do ambiente falhar por restrições na pasta temporária do sistema, escolha uma pasta temporária gravável para `TEMP` e `TMP` e repita o processo. Não configure variáveis de produção para testes locais.

O comando de migração inicial é apenas para banco vazio ou banco com histórico Alembic compatível. Nunca remova ou recrie um banco existente para instalar.

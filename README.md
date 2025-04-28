# 📡 newDownDetector.py

Script Python para monitorar o status de serviços no site [istheservicedown.com.br](https://istheservicedown.com.br).

Ele retorna:
- `0` — Serviço funcionando normalmente
- `1` — Alguns problemas detectados (instabilidade parcial)
- `2` — Serviço fora do ar (problemas graves)
- `3` — Erro ao acessar ou status indefinido

---

## 🚀 Como Funciona

O script acessa a página de status de cada serviço em tempo real, faz scraping da informação e classifica automaticamente o estado.

**Exemplo de uso:**

```bash
./newDownDetector.py youtube
```

**Resposta esperada:**

```
0
```

**Outro exemplo:**

```bash
./newDownDetector.py netflix
```

**Resposta:**

```
1
```

---

## 🛠️ Requisitos

Antes de usar, instale as bibliotecas necessárias:

```bash
pip install cloudscraper beautifulsoup4
```

Essas bibliotecas são usadas para:
- **cloudscraper**: Permite acesso a sites protegidos por Cloudflare.
- **beautifulsoup4**: Faz o parsing do conteúdo HTML para extração dos dados.

---

## 🧩 Integração com Zabbix

1. Copie o script para o diretório de scripts externos do Zabbix (`/usr/lib/zabbix/externalscripts/`):

```bash
sudo chmod +x newDownDetector.py
sudo chown zabbix newDownDetector.py
```

2. No Zabbix, importe o arquivo **zbx_export_templates.yaml** para adicionar o template de coleta aos hosts.

3. Em seguida, importe o arquivo **zbx_export_hosts.yaml** para adicionar alguns hosts de teste:

- `youtube`
- `netflix`
- `vivo-brasil`
- `pix`
- `whatsapp-messenger`
- `discord`
- `nubank`
- `bradesco`
- `cloudflare`
- `correios`
- `copilot`
- `amazon-web-services-aws`
- `tim-brasil`
- `claro-brasil`
- `embratel`

**Importante:** Caso queira adicionar os hosts manualmente, basta criar o host exatamente com o nome do serviço monitorado em [Está Falhando?](https://istheservicedown.com.br/), dessa forma, adicionando o template importado, o host já estará configurado.

**Ps:** O nome do serviço fica no final do link. Exemplo:  
https://istheservicedown.com.br/status/**youtube**

---

## 🧩 Grafana

Importe o arquivo **Downdetector.json** no Grafana e ajuste o **Data Source** para iniciar o monitoramento.  
Ficará assim:

![Dashboard](downdetector.png)

---

## 🧠 Breve explicação do funcionamento do código

O script realiza as seguintes ações:

1. **Recebe um argumento via linha de comando** — o nome (slug) do serviço a ser consultado (ex.: `youtube`, `netflix`).
2. **Monta a URL** do serviço no site [istheservicedown.com.br](https://istheservicedown.com.br).
3. **Utiliza o `cloudscraper`** para fazer o download do conteúdo da página, contornando proteções como Cloudflare.
4. **Analisa o conteúdo HTML** usando `BeautifulSoup` e transforma todo o texto em minúsculo para simplificar a checagem.
5. **Busca palavras-chave específicas**:
    - `"nenhum problema detectado"` → retorna `0`
    - `"alguns problemas detectados"` → retorna `1`
    - `"problemas detectados"` ou `"enfrentando interrupções"` → retorna `2`
    - Qualquer outra situação ou erro → retorna `3`
6. **Imprime o código de status no console**, que o Zabbix coleta.

**Resumo do fluxo:**

- Se a página indicar que está tudo OK → `0`
- Se houver alguns problemas parciais → `1`
- Se houver problemas graves ou indisponibilidade → `2`
- Se ocorrer erro de acesso ou informação indefinida → `3`

---

### 📢 Observação final

Essa solução é uma alternativa ao Downdetector após os últimos bloqueios aplicados ao Cloudflare.  
Atualizações serão implementadas conforme novas descobertas.

---

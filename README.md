# 🌐 cf-dns

Registro de DNS no **Cloudflare** pela linha de comando — um arquivo Python, zero dependências.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/cf-dns/guia/**

## Instalar

```bash
git clone https://github.com/inematds/cf-dns
install -m 755 cf-dns/cf-dns.py ~/bin/cf-dns.py
export CLOUDFLARE_API_TOKEN=seu_token     # ou: export CF_ENV_FILE=~/.env
```

Requisitos: Python 3 (só a biblioteca padrão) e um **API Token** do Cloudflare com
permissão `Zone → DNS → Edit` nas zonas que você vai alterar
(painel → My Profile → API Tokens → Create Token → template *Edit zone DNS*).

O token vem da variável `CLOUDFLARE_API_TOKEN` ou da linha `CLOUDFLARE_API_TOKEN=` de um
arquivo `.env` apontado por `CF_ENV_FILE`. Nenhum segredo mora neste repositório.

## Usar

```bash
cf-dns.py list   inema.club              # a zona inteira
cf-dns.py list   inema.club dlp2         # só um nome
cf-dns.py add    inema.club A rede 192.168.2.99
cf-dns.py add    inema.club CNAME app destino.exemplo.com --ttl=300
cf-dns.py add    inema.club A site 203.0.113.10 --proxied
cf-dns.py delete inema.club <record_id>  # o id sai no `list`
```

### Subdomínio novo no Vercel

Cria o CNAME e o TXT de verificação de uma vez, com o proxy desligado (com o proxy
ligado a verificação não passa):

```bash
cf-dns.py vercel inema.club dlp2 \
  820ed52053a39f8f.vercel-dns-017.com \
  vc-domain-verify=dlp2.inema.club,5bc6ac41fe34ada1f4f9
```

Vários TXT em `_vercel` convivem — um por subdomínio. Depois que o domínio fica
verificado, o TXT daquele subdomínio pode ser removido.

## Convenções que evitam dor de cabeça

1. **Rode `list` antes de qualquer alteração** — é assim que se descobre um registro já
   ocupando o host.
2. **Um A e um CNAME não coexistem no mesmo nome.** Trocar um pelo outro derruba o que
   estava respondendo ali; anote o valor antigo antes de apagar.
3. **Proxy desligado** para Vercel e para IP privado — o Cloudflare não proxia endereço
   privado, e o proxy quebra a verificação do Vercel.
4. **TTL 60** enquanto algo está sendo verificado; suba depois, se quiser.

## Licença

Uso interno INEMA. Sem garantias — leia o script antes de rodar (são ~120 linhas).

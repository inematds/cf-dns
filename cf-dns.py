#!/usr/bin/env python3
"""
cf-dns — cadastro de DNS no Cloudflare pela API (o que eu faço à mão, em script).

Credencial: variável CLOUDFLARE_API_TOKEN, ou a linha CLOUDFLARE_API_TOKEN= de um
.env (padrão: ~/projetos/wifi/.env, ou o caminho em CF_ENV_FILE).

Uso:
  cf-dns.py list   <zona> [nome]
  cf-dns.py add    <zona> <tipo> <nome> <valor> [--ttl 60] [--proxied]
  cf-dns.py delete <zona> <id>
  cf-dns.py vercel <zona> <sub> <cname-alvo> <valor-do-txt>

Exemplos:
  cf-dns.py list   inema.club dlp2
  cf-dns.py add    inema.club A rede 192.168.2.99
  cf-dns.py vercel inema.club dlp2 820ed52053a39f8f.vercel-dns-017.com \\
                   vc-domain-verify=dlp2.inema.club,5bc6ac41fe34ada1f4f9

Só a biblioteca padrão do Python 3 — nada pra instalar.
"""
import json, os, sys, urllib.request, urllib.error

API = "https://api.cloudflare.com/client/v4"


def token():
    t = os.environ.get("CLOUDFLARE_API_TOKEN")
    if t:
        return t
    env = os.environ.get("CF_ENV_FILE", os.path.expanduser("~/projetos/wifi/.env"))
    try:
        for line in open(env):
            if line.startswith("CLOUDFLARE_API_TOKEN="):
                return line.split("=", 1)[1].strip().strip("\"'")
    except FileNotFoundError:
        pass
    sys.exit("Sem token: exporte CLOUDFLARE_API_TOKEN ou ponha no .env")


def api(path, data=None, method="GET"):
    req = urllib.request.Request(
        API + path,
        data=json.dumps(data).encode() if data is not None else None,
        method=method,
        headers={"Authorization": "Bearer " + token(),
                 "Content-Type": "application/json"},
    )
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:      # a API devolve o erro em JSON
        return json.load(e)


def zone_id(name):
    r = api("/zones?name=" + name)
    if not r.get("result"):
        sys.exit(f"Zona {name} não encontrada (token sem acesso a ela?)")
    return r["result"][0]["id"]


def show(r):
    print(f"  {r['id']}  {r['type']:6} {r['name']:36} -> {r['content'][:60]}"
          f"  proxied={r.get('proxied')} ttl={r.get('ttl')}")


def cmd_list(zona, nome=None):
    q = f"/zones/{zone_id(zona)}/dns_records?per_page=200"
    if nome:
        fqdn = nome if nome.endswith(zona) else f"{nome}.{zona}"
        q += "&name=" + fqdn
    for r in api(q)["result"]:
        show(r)


def cmd_add(zona, tipo, nome, valor, ttl=60, proxied=False):
    body = {"type": tipo.upper(), "name": nome, "content": valor,
            "ttl": int(ttl), "proxied": bool(proxied)}
    d = api(f"/zones/{zone_id(zona)}/dns_records", body, "POST")
    if not d.get("success"):
        print("ERRO:", json.dumps(d.get("errors"), ensure_ascii=False))
        return 1
    show(d["result"])
    return 0


def cmd_delete(zona, rid):
    d = api(f"/zones/{zone_id(zona)}/dns_records/{rid}", None, "DELETE")
    print("removido" if d.get("success") else d.get("errors"))


def cmd_vercel(zona, sub, alvo, txt):
    """CNAME do subdomínio + TXT de verificação, do jeito que o Vercel pede."""
    print("CNAME:")
    cmd_add(zona, "CNAME", sub, alvo, 60, False)     # proxy DESLIGADO, sempre
    print("TXT de verificação:")
    cmd_add(zona, "TXT", "_vercel", txt, 60, False)  # convive com os outros TXT


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    c = a[0]
    if c == "list":
        cmd_list(*a[1:])
    elif c == "add":
        pos = [x for x in a[1:] if not x.startswith("--")]
        ttl = next((x.split("=")[1] for x in a if x.startswith("--ttl=")), 60)
        cmd_add(*pos, ttl=ttl, proxied="--proxied" in a)
    elif c == "delete":
        cmd_delete(*a[1:])
    elif c == "vercel":
        cmd_vercel(*a[1:])
    else:
        sys.exit(__doc__)

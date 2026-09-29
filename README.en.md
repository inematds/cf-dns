# 🌐 cf-dns

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

Manage DNS records in **Cloudflare** from the command line — one Python file, zero dependencies.

## 📖 User guide

Full guide (landing page + walkthrough): **https://inematds.github.io/cf-dns/guia/en/**

## Install

```bash
git clone https://github.com/inematds/cf-dns
install -m 755 cf-dns/cf-dns.py ~/bin/cf-dns.py
export CLOUDFLARE_API_TOKEN=seu_token     # or: export CF_ENV_FILE=~/.env
```

Requirements: Python 3 (standard library only) and a Cloudflare **API Token** with
`Zone → DNS → Edit` permission for the zones you want to change
(dashboard → My Profile → API Tokens → Create Token → *Edit zone DNS* template).

The token comes from the `CLOUDFLARE_API_TOKEN` variable or the `CLOUDFLARE_API_TOKEN=` line in an
`.env` file specified by `CF_ENV_FILE`. No secrets are stored in this repository.

## Usage

```bash
cf-dns.py list   inema.club              # the entire zone
cf-dns.py list   inema.club dlp2         # just one name
cf-dns.py add    inema.club A rede 192.168.2.99
cf-dns.py add    inema.club CNAME app destino.exemplo.com --ttl=300
cf-dns.py add    inema.club A site 203.0.113.10 --proxied
cf-dns.py delete inema.club <record_id>  # the ID is shown by `list`
```

### New subdomain on Vercel

Creates the CNAME and verification TXT record at once, with the proxy disabled (verification
won't pass with the proxy enabled):

```bash
cf-dns.py vercel inema.club dlp2 \
  820ed52053a39f8f.vercel-dns-017.com \
  vc-domain-verify=dlp2.inema.club,5bc6ac41fe34ada1f4f9
```

Multiple TXT records can coexist under `_vercel` — one per subdomain. Once the domain is
verified, that subdomain's TXT record can be removed.

## Conventions that prevent headaches

1. **Run `list` before making any changes** — this is how you find out whether a record is already
   occupying the host.
2. **An A record and a CNAME cannot coexist under the same name.** Switching one for the other takes down what
   was responding there; note the old value before deleting it.
3. **Proxy disabled** for Vercel and private IPs — Cloudflare does not proxy private
   addresses, and the proxy breaks Vercel verification.
4. **TTL 60** while something is being verified; increase it afterward if you want.

## License

INEMA internal use. No warranties — read the script before running it (about 120 lines).

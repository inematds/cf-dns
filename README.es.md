# 🌐 cf-dns

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

Registro de DNS en **Cloudflare** desde la línea de comandos: un archivo Python, cero dependencias.

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://inematds.github.io/cf-dns/guia/es/**

## Instalar

```bash
git clone https://github.com/inematds/cf-dns
install -m 755 cf-dns/cf-dns.py ~/bin/cf-dns.py
export CLOUDFLARE_API_TOKEN=seu_token     # ou: export CF_ENV_FILE=~/.env
```

Requisitos: Python 3 (solo la biblioteca estándar) y un **API Token** de Cloudflare con
permiso `Zone → DNS → Edit` en las zonas que vas a modificar
(panel → My Profile → API Tokens → Create Token → plantilla *Edit zone DNS*).

El token se obtiene de la variable `CLOUDFLARE_API_TOKEN` o de la línea `CLOUDFLARE_API_TOKEN=` de un
archivo `.env` indicado por `CF_ENV_FILE`. Ningún secreto está en este repositorio.

## Usar

```bash
cf-dns.py list   inema.club              # toda la zona
cf-dns.py list   inema.club dlp2         # solo un nombre
cf-dns.py add    inema.club A rede 192.168.2.99
cf-dns.py add    inema.club CNAME app destino.exemplo.com --ttl=300
cf-dns.py add    inema.club A site 203.0.113.10 --proxied
cf-dns.py delete inema.club <record_id>  # el id aparece en `list`
```

### Nuevo subdominio en Vercel

Crea el CNAME y el TXT de verificación de una sola vez, con el proxy desactivado (con el proxy
activado, la verificación no funciona):

```bash
cf-dns.py vercel inema.club dlp2 \
  820ed52053a39f8f.vercel-dns-017.com \
  vc-domain-verify=dlp2.inema.club,5bc6ac41fe34ada1f4f9
```

Varios TXT en `_vercel` pueden coexistir: uno por subdominio. Después de verificar el dominio,
se puede eliminar el TXT de ese subdominio.

## Convenciones para evitar dolores de cabeza

1. **Ejecuta `list` antes de cualquier cambio**: así puedes detectar si ya hay un registro
   ocupando el host.
2. **Un A y un CNAME no pueden coexistir con el mismo nombre.** Cambiar uno por otro elimina lo que
   respondía allí; anota el valor anterior antes de borrarlo.
3. **Proxy desactivado** para Vercel y para IP privada: Cloudflare no proxifica direcciones
   privadas y el proxy impide la verificación de Vercel.
4. **TTL 60** mientras se verifica algo; auméntalo después, si quieres.

## Licencia

Uso interno de INEMA. Sin garantías: lee el script antes de ejecutarlo (son ~120 líneas).

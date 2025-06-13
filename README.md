# pyscript-cloudflare-ip-policy-updater for Home Assistant

These scripts are to automate the updating of Cloudflare Access Groups which can be used to secure external access to Home Assistant via Cloudflare's Zero Trust network.

This script currently supports updating a group which contains Google's IP ranges so Google Home can talk to Home Assistant.

## Installation

### `configuration.yaml`

```yaml
pyscript: !include pyscript/config.yaml
```

### `pyscript/config.yaml`

```yaml
allow_all_imports: true
apps:
  cloudflare-access-group-google-ip-updater:
    - account: !secret cloudflare_account_id
      token: !secret cloudflare_token
      group: !secret cloudflare_google_group_id
```

### `secrets.yaml`

```yaml
cloudflare_account_id: <cloudflare_account_id>
cloudflare_token: <cloudflare_token>
cloudflare_google_group_id: <cloudflare_google_group_id>
```

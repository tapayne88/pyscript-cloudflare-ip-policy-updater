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
  pyscript-cloudflare-ip-policy-updater:
    - account: !secret cloudflare_account_id
      token: !secret cloudflare_token
      google_policy: !secret cloudflare_google_policy_id
      home_policy: !secret cloudflare_home_policy_id
```

### `secrets.yaml`

```yaml
cloudflare_account_id: <cloudflare_account_id>
cloudflare_policy_token: <cloudflare_policy_token>
cloudflare_google_policy_id: <cloudflare_google_policy_id>
cloudflare_home_policy_id: <cloudflare_home_policy_id>
```

## Token

To generate the `<cloudflare_policy_token>` you need to visit [Cloudflare](https://dash.cloudflare.com/profile/api-tokens) and create a token. The token needs the following policies

- Account.Access: Apps and Policies:Edit
- Account.Access: Apps and Policies:Read

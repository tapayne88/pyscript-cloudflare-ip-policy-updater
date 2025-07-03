from cloudflare import Cloudflare
import requests


def get_home_address():
    log.info("Fetching home IP address")
    r = task.executor(requests.get, "https://api.ipify.org?format=json")
    r.raise_for_status()
    return [r.json()["ip"]]


def get_google_addresses():
    log.info("Fetching Google IP addresses")
    r = task.executor(requests.get, "https://www.gstatic.com/ipranges/goog.json")
    r.raise_for_status()
    ips = [
        entry["ipv4Prefix"] for entry in r.json()["prefixes"] if "ipv4Prefix" in entry
    ]
    ips = ips + [
        entry["ipv6Prefix"] for entry in r.json()["prefixes"] if "ipv6Prefix" in entry
    ]
    return ips


def update_access_policy(token, account_id, policy_id, ips):
    log.info(f"Updating Cloudflare Access Policy with IPs: {ips}")
    client = Cloudflare(api_token=token)
    # Fetch the current policy
    policy = task.executor(
        client.zero_trust.access.policies.get, policy_id, account_id=account_id
    )
    # Update the include list
    include = [{"ip": {"ip": ip}} for ip in ips]
    # Update the policy
    result = task.executor(
        client.zero_trust.access.policies.update, policy_id, account_id=account_id, include=include, name=policy["name"], decision=policy["decision"]
    )
    log.info("Successfully updated the IP policy")
    log.info("Result: %s", result)


@service
def cloudflare_access_policy_google_ip_updater():
    token = pyscript.app_config[0].get("token")
    account = pyscript.app_config[0].get("account")
    policy = pyscript.app_config[0].get("google_policy")
    log.info("Running Cloudflare Access Policy updater for Google IPs...")
    ips = get_google_addresses()
    update_access_policy(token, account, policy, ips)


@service
def cloudflare_access_policy_home_ip_updater():
    token = pyscript.app_config[0].get("token")
    account = pyscript.app_config[0].get("account")
    policy = pyscript.app_config[0].get("home_policy")
    log.info("Running Cloudflare Access Policy updater for Home IP...")
    ips = get_home_address()
    update_access_policy(token, account, policy, ips)

import CloudFlare
import requests


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


def update_access_policy(token, account_id, group_id, ips):
    log.info("Updating Cloudflare Policy with IPs: %s" % ips)
    client = CloudFlare.CloudFlare(token=token)

    data = {"include": [{"ip": {"ip": ip}} for ip in ips], "exclude": [], "require": []}

    task.executor(client.accounts.access.groups.put, account_id, group_id, data=data)
    log.info("Successfully updated Google IP group")
    log.info(
        "Result",
        task.executor(
            client.accounts.access.groups.get, account_id, group_id, data=data
        ),
    )


@service
def cloudflare_access_group_google_ip_updater():
    log.info("Updating Cloudflare Policy for Google IPs...")
    token = pyscript.app_config[0].get("token")
    account = pyscript.app_config[0].get("account")
    policy = pyscript.app_config[0].get("policy")
    ips = get_google_addresses()
    update_access_policy(token, account, policy, ips)

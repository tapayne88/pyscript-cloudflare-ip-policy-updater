import CloudFlare
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


def update_access_group(token, account_id, group_id, ips):
    log.info("Updating Cloudflare Access Group with IPs: %s" % ips)
    client = CloudFlare.CloudFlare(token=token)

    data = {"include": [{"ip": {"ip": ip}} for ip in ips], "exclude": [], "require": []}

    task.executor(client.accounts.access.groups.put, account_id, group_id, data=data)
    log.info("Successfully updated the IP group")
    log.info(
        "Result",
        task.executor(
            client.accounts.access.groups.get, account_id, group_id, data=data
        ),
    )


@service
def cloudflare_access_group_ip_updater():
    token = pyscript.app_config[0].get("token")
    account = pyscript.app_config[0].get("account")
    group = pyscript.app_config[0].get("group")
    mode = pyscript.app_config[0].get("mode")

    if mode == "home":
        log.info("Running Cloudflare Access Group updater for Home IP...")
        ips = get_home_address()
        update_access_group(token, account, group, ips)

    elif mode == "google":
        log.info("Running Cloudflare Access Group updater for Google IPs...")
        ips = get_google_addresses()
        update_access_group(token, account, group, ips)

    else:
        log.warn("Unrecognised mode, aborting: %s" % mode)

#!/usr/bin/env python3
import requests
import sys
import urllib3

# Disable warnings for insecure HTTPS requests.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_session(vcenter, username, password):
    url = f"https://{vcenter}/rest/com/vmware/cis/session"
    try:
        resp = requests.post(url, auth=(username, password), verify=False)
        resp.raise_for_status()
        session_id = resp.json()['value']
        return session_id
    except Exception as e:
        print(f"Failed to create session for {vcenter}: {e}")
        return None

def get_subscribed_libraries(vcenter, session_id):
    url = f"https://{vcenter}/rest/com/vmware/content/subscribed-library"
    headers = {"vmware-api-session-id": session_id}
    try:
        resp = requests.get(url, headers=headers, verify=False)
        resp.raise_for_status()
        libraries = resp.json().get('value', [])
        return libraries
    except Exception as e:
        print(f"Failed to retrieve libraries from {vcenter}: {e}")
        return []

def sync_library(vcenter, session_id, library_id):
    url = f"https://{vcenter}/rest/com/vmware/content/subscribed-library/{library_id}/sync"
    headers = {"vmware-api-session-id": session_id}
    try:
        resp = requests.post(url, headers=headers, verify=False)
        resp.raise_for_status()
        print(f"Successfully initiated sync for library {library_id} on {vcenter}")
    except Exception as e:
        print(f"Failed to sync library {library_id} on {vcenter}: {e}")

def delete_session(vcenter, session_id):
    url = f"https://{vcenter}/rest/com/vmware/cis/session"
    headers = {"vmware-api-session-id": session_id}
    try:
        requests.delete(url, headers=headers, verify=False)
    except Exception as e:
        print(f"Failed to delete session for {vcenter}: {e}")

def main():
    if len(sys.argv) != 4:
        print("Usage: sync_content_libraries.py <vSphereUSERNAME> <vSpherePASSWORD> <vcenterlist.txt>")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]
    vcenter_file = sys.argv[3]

    try:
        with open(vcenter_file, 'r') as f:
            vcenters = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading vCenter list file: {e}")
        sys.exit(1)

    for vcenter in vcenters:
        print(f"Processing vCenter: {vcenter}")
        session_id = get_session(vcenter, username, password)
        if not session_id:
            continue

        libraries = get_subscribed_libraries(vcenter, session_id)
        if libraries:
            for lib in libraries:
                # If each library is returned as a dictionary with a 'value' key, extract it.
                library_id = lib.get('value') if isinstance(lib, dict) else lib
                if library_id:
                    sync_library(vcenter, session_id, library_id)
        else:
            print(f"No subscribed libraries found on {vcenter}")

        delete_session(vcenter, session_id)

if __name__ == "__main__":
    main()

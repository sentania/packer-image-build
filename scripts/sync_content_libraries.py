#!/usr/bin/env python3
import requests
import sys
import os
import urllib3

# Disable warnings for insecure HTTPS requests.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_session(vcenter, username, password):
    """Creates a session against the vCenter REST API and returns the session ID."""
    url = f"https://{vcenter}/rest/com/vmware/cis/session"
    try:
        response = requests.post(url, auth=(username, password), verify=False)
        response.raise_for_status()
        session_id = response.json().get('value')
        if not session_id:
            raise Exception("No session ID returned")
        return session_id
    except Exception as e:
        print(f"[{vcenter}] Error creating session: {e}")
        return None

def list_subscribed_libraries(vcenter, session_id):
    """Retrieves the list of subscribed libraries from the vCenter."""
    url = f"https://{vcenter}/rest/com/vmware/content/subscribed-library"
    headers = {"vmware-api-session-id": session_id}
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        libraries = response.json().get('value', [])
        return libraries
    except Exception as e:
        print(f"[{vcenter}] Error retrieving libraries: {e}")
        return None

def sync_library(vcenter, session_id, library_id):
    """
    Initiates a sync for the given library on the vCenter.

    As per the API documentation, the sync endpoint is:
    POST /rest/com/vmware/content/subscribed-library/{library_id}__action=sync
    """
    url = f"https://{vcenter}/rest/com/vmware/content/subscribed-library/{library_id}__action=sync"
    headers = {"vmware-api-session-id": session_id}
    try:
        response = requests.post(url, headers=headers, verify=False)
        response.raise_for_status()
        print(f"[{vcenter}] Library '{library_id}' synchronized successfully.")
    except Exception as e:
        print(f"[{vcenter}] Error synchronizing library '{library_id}': {e}")

def delete_session(vcenter, session_id):
    """Deletes the session for the given vCenter."""
    url = f"https://{vcenter}/rest/com/vmware/cis/session"
    headers = {"vmware-api-session-id": session_id}
    try:
        response = requests.delete(url, headers=headers, verify=False)
        if response.status_code == 200:
            print(f"[{vcenter}] Session deleted successfully.")
    except Exception as e:
        print(f"[{vcenter}] Error deleting session: {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: sync_vsphere_libraries.py <vSphereUSERNAME> <vSpherePASSWORD>")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]
    # Hard-code the vCenter list file path
    vcenter_file = os.path.join("inputs", "vcenterlist.txt")

    try:
        with open(vcenter_file, 'r') as f:
            vcenters = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading vCenter list file '{vcenter_file}': {e}")
        sys.exit(1)

    for vcenter in vcenters:
        print(f"\nProcessing vCenter: {vcenter}")
        session_id = create_session(vcenter, username, password)
        if not session_id:
            print(f"Skipping {vcenter} due to session creation failure.")
            continue

        libraries = list_subscribed_libraries(vcenter, session_id)
        if libraries is None:
            print(f"Skipping library sync for {vcenter} due to error retrieving libraries.")
            delete_session(vcenter, session_id)
            continue

        if not libraries:
            print(f"[{vcenter}] No subscribed libraries found.")
        else:
            for lib in libraries:
                # Each library is expected to be a dict with a 'value' key containing the library ID.
                library_id = lib.get('value') if isinstance(lib, dict) else lib
                if library_id:
                    sync_library(vcenter, session_id, library_id)
                else:
                    print(f"[{vcenter}] Unexpected library format: {lib}")

        delete_session(vcenter, session_id)

if __name__ == "__main__":
    main()

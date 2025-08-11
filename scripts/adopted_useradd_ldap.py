import sys
sys.path.insert(0, '/o/opt/dev-py/incredible/libs')  # adjust if needed

from ldap3 import Server, Connection, ALL
import sys

LDAP_SERVER = 'ldap://localhost:8389'
ADMIN_DN = 'cn=admin,dc=myorg,dc=local'
ADMIN_PASSWORD = 'admin'

# New user info
<<<<<<< HEAD
USER_UID = 'brooks'
USER_CN = 'brooks'  # common name, can be full name or username
USER_GIVENNAME = 'brooks'  # example first name
USER_SN = 'brooks'         # example surname
USER_EMAIL = 'sergii@example.com'
=======
USER_UID = 'e2_b1'
USER_CN = 'e2_b1'
USER_GIVENNAME = 'Se'
USER_SN = 'Iv'
USER_EMAIL = 'se@example.com'
>>>>>>> 90d18e3 (Remove local LDAP config and data from repo)
USER_PASSWORD = '1qaz1'
USER_DN = f'uid={USER_UID},ou=users,dc=myorg,dc=local'
OU_DN = 'ou=users,dc=myorg,dc=local'

server = Server(LDAP_SERVER, get_info=ALL)
conn = Connection(server, ADMIN_DN, ADMIN_PASSWORD, auto_bind=True)

# Create OU if it doesn't exist
if not conn.search(OU_DN, '(objectClass=organizationalUnit)'):
    print("[!] OU 'users' not found. Creating it...")
    conn.add(OU_DN, ['top', 'organizationalUnit'], {'ou': 'users'})
    if conn.result['description'] != 'success':
        print(f"[✘] Failed to create OU: {conn.result['description']}")
        conn.unbind()
        sys.exit(1)
    print("[✔] OU 'users' created.")

# Create user
entry = {
    'objectClass': ['inetOrgPerson', 'simpleSecurityObject'],
    'cn': USER_CN,
    'givenName': USER_GIVENNAME,
    'sn': USER_SN,
    'uid': USER_UID,
    'mail': USER_EMAIL,
    'userPassword': USER_PASSWORD,
}

if conn.add(USER_DN, attributes=entry):
    print(f"[✔] User {USER_UID} created.")
else:
    print(f"[✘] Failed to create user: {conn.result['description']}")

conn.unbind()

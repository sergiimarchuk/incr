import sys
sys.path.insert(0, '/opt/dev-py/incredible/libs')
from ldap3 import Server, Connection, ALL

LDAP_SERVER = 'localhost'
BASE_DN = 'ou=users,dc=myorg,dc=local'

def authenticate_and_get_info(username, password):
    user_dn = f"uid={username},{BASE_DN}"
    server = Server(LDAP_SERVER, port=8389, get_info=ALL)

    try:
        # Bind using the user's credentials
        conn = Connection(server, user=user_dn, password=password, auto_bind=True)

        # Search only in the user's own DN
        conn.search(
            search_base=user_dn,
            search_filter='(objectClass=*)',
            attributes=["cn", "mail", "entryUUID"]
        )

        if not conn.entries:
            print("[ERROR] No entries found for user.", file=sys.stderr)
            return False

        user_entry = conn.entries[0]
        return {
            "uid": username,
            "cn": user_entry.cn.value,
            "email": user_entry.mail.value if 'mail' in user_entry else None,
            "entryUUID": user_entry.entryUUID.value
        }

    except Exception as e:
        print(f"LDAP auth error: {e}", file=sys.stderr)
        return False


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: uid_openldap_getting.py <username> <password>", file=sys.stderr)
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    user_info = authenticate_and_get_info(username, password)

    if user_info:
        print(user_info["uid"], user_info["cn"], user_info["email"], user_info["entryUUID"])
        sys.exit(0)
    else:
        sys.exit(1)


"""

## 🔐 `authenticate_and_get_info(username, password)`

**Main function. Steps:**

- **Builds full user DN:**  
  → `uid=<username>,<BASE_DN>`

- **Creates LDAP connection** (`Server` + `Connection`)  
  → Connects on port `8389`, binds using the given credentials

- **Attempts bind (auth):**  
  → If invalid DN or password — raises `Exception`

- **Searches user’s own DN**  
  → Filter: `(objectClass=*)`, returns `cn`, `mail`, `entryUUID`

- **Returns user info as a `dict`**  
  → If no entry found — logs error, returns `False`

---

## 🚀 `if __name__ == '__main__':`

**CLI entry point:**

- Takes `username` and `password` from command-line args
- Calls `authenticate_and_get_info`
- If successful — prints `uid`, `cn`, `email`, `entryUUID`
- If failed — exits with `1` (can be used in shell scripting)

---

## 🧯 Debug Tips — Where Things Might Break

| Section           | What to check                                                |
|-------------------|--------------------------------------------------------------|
| `auto_bind=True`  | Invalid DN or wrong password → triggers `Exception`          |
| `conn.search(...)`| User exists but no attributes? → Check schema or LDAP ACLs   |
| `entry.mail`      | Optional field — script safely handles if it's missing       |
| Port `8389`       | Ensure LDAP server is actually listening on this port        |


"""
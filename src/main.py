import subprocess
import json
import platform

def execute_query(query):
    print(f"Executing query: {query}")
    try:
        result = subprocess.run(['osqueryi', '--json', query], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing the query: {e}")
        print(f"Error output: {e.stderr}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return []

def check_disk_encryption():
    system = platform.system()
    if system == "Darwin":  # macOS
        query = "SELECT * FROM disk_encryption;"
    elif system == "Windows":
        query = "SELECT * FROM bitlocker_info;"
    else:  # Linux
        query = "SELECT * FROM disk_encryption;"
    
    result = execute_query(query)
    
    if system == "Darwin":
        if any(int(disk.get('encrypted', '0')) == 1 for disk in result):
            return "FileVault"
    elif system == "Windows":
        if any(int(disk.get('encryption_status', '0')) == 1 for disk in result):
            return "BitLocker"
    else:
        if any(int(disk.get('encrypted', '0')) == 1 for disk in result):
            return "LUKS"
    
    return None

def check_antivirus():
    system = platform.system()
    if system == "Darwin":  # macOS
        queries = [
            "SELECT * FROM xprotect_entries;",
            "SELECT * FROM xprotect_meta;",
            "SELECT * FROM launchd WHERE name LIKE '%com.apple.MRT%' OR name LIKE '%com.apple.XProtect%';",
            "SELECT * FROM processes WHERE name LIKE '%MRT%' OR name LIKE '%XProtect%';"
        ]
        for query in queries:
            result = execute_query(query)
            if result:
                return "XProtect/MRT (Built-in macOS protection)"
    elif system == "Windows":
        query = "SELECT * FROM windows_security_products;"
        result = execute_query(query)
        if result:
            return result[0].get('display_name', 'Windows Antivirus')
    else:  # Linux
        query = "SELECT name FROM processes WHERE name LIKE '%antivirus%' OR name LIKE '%anti-virus%';"
        result = execute_query(query)
        if result:
            return result[0].get('name', 'Unknown Antivirus')
    
    return None

def check_screen_lock():
    system = platform.system()
    if system == "Darwin":  # macOS
        query = "SELECT value FROM preferences WHERE domain = 'com.apple.screensaver' AND key = 'idleTime';"
    elif system == "Windows":
        query = "SELECT data FROM registry WHERE path = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\\InactivityTimeoutSecs';"
    else:  # Linux (assuming GNOME)
        query = "SELECT value FROM preferences WHERE domain = 'org.gnome.desktop.session' AND key = 'idle-delay';"
    
    result = execute_query(query)
    
    if result and 'value' in result[0]:
        time = int(result[0]['value'])
        if time > 0:
            if system == "Darwin":
                return time // 60  # Convert seconds to minutes
            elif system == "Windows":
                return time // 60  # Convert seconds to minutes
            else:
                return time  # Already in seconds
    return None

def main():
    print("Verifying system security...")
    
    encryption = check_disk_encryption()
    if encryption:
        print(f"✅ The disk is encrypted with {encryption}.")
    else:
        print("❌ The disk is not encrypted.")
    
    antivirus = check_antivirus()
    if antivirus:
        print(f"✅ Antivirus protection detected: {antivirus}")
    else:
        print("❌ No antivirus detected.")
    
    screen_lock_time = check_screen_lock()
    if screen_lock_time is not None:
        if platform.system() == "Darwin" or platform.system() == "Windows":
            print(f"✅ Screen lock is set to activate after {screen_lock_time} minutes of inactivity.")
        else:
            print(f"✅ Screen lock is set to activate after {screen_lock_time} seconds of inactivity.")
    else:
        print("❌ Screen lock is not configured or is disabled.")

if __name__ == "__main__":
    main()
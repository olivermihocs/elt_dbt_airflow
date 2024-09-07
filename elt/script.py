import subprocess
import time

#check db availability
def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host], check=True, capture_output=True, text=True)
            if "accepting connections" in result.stdout:
                print("Connected to PostgreSQL!")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to PostgreSQL: {e}")
            retries += 1
            print(
                f"Retrying in {delay_seconds} seconds... (Attempt {retries}/{max_retries})")
            time.sleep(delay_seconds)
    print("Max retries reached. Exiting.")
    return False


#safety check for db before running the script
if not wait_for_postgres(host="src_postgres"):
    exit(1)

print("Starting script...")

src_config = {
    'dbname': 'src_db',
    'user': 'postgres',
    'password': 'secret',
    'host': 'src_postgres' #host name
}

dest_config = {
    'dbname': 'dest_db',
    'user': 'postgres',
    'password': 'secret',
    'host': 'dest_postgres'
}

dump_cmd = [
    'pg_dump',
    '-h', src_config['host'],
    '-U', src_config['user'],
    '-d', src_config['dbname'],
    '-f', 'data_dump.sql',
    '-w'  # Do not prompt for password
]

#Setting PGPWD as an environment variable
subprocess_env = dict(PGPASSWORD=src_config['password'])

#execute dump
subprocess.run(dump_cmd, env=subprocess_env, check=True)

load_cmd = [
    'psql',
    '-h', dest_config['host'],
    '-U', dest_config['user'],
    '-d', dest_config['dbname'],
    '-a', '-f', 'data_dump.sql'
]

#Setting env variable for dest db
subprocess_env = dict(PGPASSWORD=dest_config['password'])

subprocess.run(load_cmd, env=subprocess_env, check=True)

print ("Ending script...")
import subprocess

def get_key_from_keychain(service, account):
    try:
        result = subprocess.check_output([
            'security', 'find-generic-password',
            '-s', service,
            '-a', account,
            '-w'
            ])
        return result.decode('utf-8').strip()
    except subprocess.CalledProcessError:
        raise RuntimeError('Secret not found.')

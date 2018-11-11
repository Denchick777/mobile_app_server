"""
Configuration info retriever for server application.
:author: Denis Chernikov
"""

configs = {}
failed = False

with open('private.config') as conf_file:
    for i, line in enumerate(conf_file.readlines()):
        if not line:
            continue
        try:
            name, value = map(str.strip, line.split('=', 1))
            configs[name] = value
        except ValueError:
            print(f'Error at line {i} while parsing config file!')
            failed = True
if failed:
    print(
        'Cannot read configuration info!\n'
        'Application terminating...'
    )
    exit(1)

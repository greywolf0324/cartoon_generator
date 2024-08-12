# OPENAI_API_KEY = 'tl.t1B2FRyVUMSJtL97VnKbU4CmclGKgNtpbpzRI2HKRxPT[LOq'
OPENAI_API_KEY = 'tl.hfzOu9{UK2oEvXl6j2JnU4CmclGKubtoG6ZPWwI8yeVCwfhp'
def encrypt(api_key):
    return ''.join(chr(ord(char) + 1) for char in api_key)

def decrypt(api_key):
    return ''.join(chr(ord(char) - 1) for char in api_key)

if __name__ == '__main__':
    print (encrypt(OPENAI_API_KEY))
# OPENAI_API_KEY = 'tl.t1B2FRyVUMSJtL97VnKbU4CmclGKgNtpbpzRI2HKRxPT[LOq'
# OPENAI_API_KEY = 'tl.hfzOu9{UK2oEvXl6j2JnU4CmclGKubtoG6ZPWwI8yeVCwfhp'
OPENAI_API_KEY = 'tl.qspk.ByFdkHX{z1sxnmYL.kisGsSrjP9km2F7:JzJv[lyBz.otp`hF6VFo:b48TU4CmclGKO7PTsUsMXX9JhHeiT:58X7yyn7Te:JyxK7hILHFO64CfsVnnHRPq3LQjlB'
def encrypt(api_key):
    return ''.join(chr(ord(char) + 1) for char in api_key)

def decrypt(api_key):
    return ''.join(chr(ord(char) - 1) for char in api_key)

if __name__ == '__main__':
    print (encrypt(OPENAI_API_KEY))
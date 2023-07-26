from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open("private_key.pem", "wb") as prifile:
        prifile.write(private_key_pem)

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open("public_key.pem", "wb") as pubfile:
        pubfile.write(public_key_pem)

def load_private_key():
    with open("private_key.pem", "rb") as prifile:
        private_key = serialization.load_pem_private_key(
            prifile.read(),
            password=None
        )
    return private_key

def load_public_key():
    with open("public_key.pem", "rb") as pubfile:
        public_key = serialization.load_pem_public_key(
            pubfile.read()
        )
    return public_key

def calculate_hash(file_path):
    
    hash_object = hashes.Hash(hashes.SHA256())

    # 打开文件并逐块读取数据进行哈希计算
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hash_object.update(chunk)

    # 返回哈希值的二进制表示
    return hash_object.finalize()

def sign_data(private_key, hash_value):
    signature = private_key.sign(
        hash_value,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    with open("signature.bin", "wb") as sigfile:
        sigfile.write(signature)

def load_signature():
    with open("signature.bin", "rb") as sigfile:
        signature = sigfile.read()
    return signature

def verify_signature(public_key, signature, hash_value):
    try:
        public_key.verify(
            signature,
            hash_value,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Signature is valid.")
    except InvalidSignature:
        print("Signature is invalid.")

if __name__ == '__main__':

# 发送方：

    # 生成RSA密钥对
    generate_rsa_key_pair()

    # 读取私钥
    private_key = load_private_key()

    # 计算数据的哈希值
    hash_value = calculate_hash("data.txt")

    # 使用私钥对哈希值进行签名
    sign_data(private_key, hash_value)

# 接收方：

    # 读取公钥
    public_key = load_public_key()

    # 读取签名
    signature = load_signature()

    # 使用公钥验证签名
    verify_signature(public_key, signature, hash_value)
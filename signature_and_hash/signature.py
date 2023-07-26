from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

# 生成RSA密钥对
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# 保存私钥到文件
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
with open("private_key.pem", "wb") as prifile:
    prifile.write(private_key_pem)

# 保存公钥到文件
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
with open("public_key.pem", "wb") as pubfile:
    pubfile.write(public_key_pem)

# 保存数据到文件
data = b"I love you"
with open("data.txt", "wb") as datafile:
    datafile.write(data)

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# 读取私钥
with open("private_key.pem", "rb") as prifile:
    private_key = serialization.load_pem_private_key(
        prifile.read(),
        password=None
    )

# 读取数据
with open("data.txt", "rb") as datafile:
    data = datafile.read()

# 计算数据的哈希值
digest = hashes.Hash(hashes.SHA256())
digest.update(data)
hash_value = digest.finalize()

# 使用私钥对哈希值进行签名
signature = private_key.sign(
    hash_value,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# 保存签名到文件
with open("signature.bin", "wb") as sigfile:
    sigfile.write(signature)

# 读取公钥
with open("public_key.pem", "rb") as pubfile:
    public_key = serialization.load_pem_public_key(
        pubfile.read()
    )

# 读取签名
with open("signature.bin", "rb") as sigfile:
    signature = sigfile.read()

# 使用公钥验证签名
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
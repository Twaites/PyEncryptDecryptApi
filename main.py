'''
Simple FastAPI script for encrypting and decrypting strings
'''

from cryptography.fernet import Fernet
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(root_path="/api/v1")

class EncryptMessage(BaseModel):
    message: str

class DecryptKeyToken(BaseModel):
    key: str
    token: str

@app.post("/decrypt")
def decrypt(decryptData: DecryptKeyToken):
    key = (decryptData.key).encode()
    token = (decryptData.token).encode()
    return {"message": Fernet(key).decrypt(token).decode()}

@app.post("/encrypt")
def enrypt(encryptData: EncryptMessage):
    key = Fernet.generate_key()
    token = Fernet(key).encrypt(encryptData.message.encode())
    return {"key": key.decode(), "token": token.decode()}
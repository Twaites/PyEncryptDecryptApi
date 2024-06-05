'''
Simple FastAPI script for encrypting and decrypting strings
'''

from cryptography.fernet import Fernet
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(root_path="/api/v1")

class EncryptMessage(BaseModel):
    message: str
    key: str = None

class DecryptKeyToken(BaseModel):
    key: str
    token: str

@app.post("/decrypt")
def decrypt(decryptData: DecryptKeyToken):
    key = (decryptData.key).encode()
    token = (decryptData.token).encode()
    return {"message": Fernet(key).decrypt(token).decode()}

@app.post("/encrypt")
def encrypt(encryptData: EncryptMessage):
    try:
        key = Fernet.generate_key() if not encryptData.key else Fernet(encryptData.key)
        token = Fernet(key).encrypt(encryptData.message.encode())
        return {"key": key.decode(), "token": token.decode()}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Encrypt Error")
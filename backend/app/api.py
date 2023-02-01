# pylint: disable=no-self-argument,no-self-use,broad-except
from typing import Any, List
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from . import vigenere, vigenere_auto, vigenere_extended, affine, hill, playfair, utils

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Cryptography Tucil 1 API"}


class VigenereEncryptRequest(BaseModel):
    plaintext: str
    key: str

    @validator('plaintext')
    def validate_plaintext(cls, plaintext):
        return utils.uppercase_and_filter_alphabets(plaintext)

    @validator('key')
    def validate_key(cls, key):
        return utils.uppercase_and_filter_alphabets(key)


class VigenereEncryptResponse(BaseModel):
    ciphertext: str


@app.post("/vigenere/encrypt", tags=["vigenere"], response_model=VigenereEncryptResponse)
async def vigenere_encrypt(body: VigenereEncryptRequest) -> dict:
    try:
        ciphertext = vigenere.encrypt(body.plaintext, body.key)
        return {"ciphertext": ciphertext}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


class VigenereDecryptRequest(BaseModel):
    ciphertext: str
    key: str

    @validator('ciphertext')
    def validate_ciphertext(cls, ciphertext):
        return utils.uppercase_and_filter_alphabets(ciphertext)

    @validator('key')
    def validate_key(cls, key):
        return utils.uppercase_and_filter_alphabets(key)


class VigenereDecryptResponse(BaseModel):
    plaintext: str


@app.post("/vigenere/decrypt", tags=["vigenere"], response_model=VigenereDecryptResponse)
async def vigenere_decrypt(body: VigenereDecryptRequest) -> dict:
    try:
        plaintext = vigenere.decrypt(body.ciphertext, body.key)
        return {"plaintext": plaintext}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/vigenere-auto/encrypt", tags=["vigenere"], response_model=VigenereEncryptResponse)
async def vigenere_auto_encrypt(body: VigenereEncryptRequest) -> dict:
    try:
        ciphertext = vigenere_auto.encrypt(body.plaintext, body.key)
        return {"ciphertext": ciphertext}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/vigenere-auto/decrypt", tags=["vigenere"], response_model=VigenereDecryptResponse)
async def vigenere_auto_decrypt(body: VigenereDecryptRequest) -> dict:
    try:
        plaintext = vigenere_auto.decrypt(body.ciphertext, body.key)
        return {"plaintext": plaintext}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


class VigenereExtendedEncryptRequest(BaseModel):
    plaintext: bytes
    key: str

    @validator('key')
    def validate_key(cls, key):
        return utils.uppercase_and_filter_alphabets(key)


@app.post("/vigenere-extended/encrypt", tags=["vigenere"])
async def vigenere_extended_encrypt(body: VigenereExtendedEncryptRequest) -> dict:
    try:
        ciphertext = vigenere_extended.encrypt_extended_vigenere(
            body.plaintext, body.key)
        return Response(
            status_code=200,
            content=ciphertext,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


class VigenereExtendedDecryptRequest(BaseModel):
    ciphertext: bytes
    key: str

    @validator('key')
    def validate_key(cls, key):
        return utils.uppercase_and_filter_alphabets(key)


@app.post("/vigenere-extended/decrypt", tags=["vigenere"])
async def vigenere_extended_decrypt(body: VigenereExtendedDecryptRequest) -> dict:
    try:
        plaintext = vigenere_extended.decrypt_extended_vigenere(
            body.ciphertext, body.key)
        return Response(
            status_code=200,
            content=str(plaintext),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


class AffineEncryptRequest(BaseModel):
    plaintext: str
    m: int
    b: int

    @validator('plaintext')
    def validate_plaintext(cls, plaintext):
        return utils.uppercase_and_filter_alphabets(plaintext)


class AffineEncryptResponse(BaseModel):
    ciphertext: str


@app.post("/affine/encrypt", tags=["affine"], response_model=AffineEncryptResponse)
async def affine_encrypt(body: AffineEncryptRequest) -> dict:
    try:
        ciphertext = affine.encrypt(body.plaintext, body.m, body.b)
        return {"ciphertext": ciphertext}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


class AffineDecryptRequest(BaseModel):
    ciphertext: str
    m: int
    b: int

    @validator('ciphertext')
    def validate_ciphertext(cls, ciphertext):
        return utils.uppercase_and_filter_alphabets(ciphertext)


class AffineDecryptResponse(BaseModel):
    plaintext: str


@app.post("/affine/decrypt", tags=["affine"], response_model=AffineDecryptResponse)
async def affine_decrypt(body: AffineDecryptRequest) -> dict:
    try:
        plaintext = affine.decrypt(body.ciphertext, body.m, body.b)
        return {"plaintext": plaintext}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


class HillEncryptRequest(BaseModel):
    plaintext: str
    key: List[List[int]]
    m: int

    @validator('plaintext')
    def validate_plaintext(cls, plaintext):
        return utils.uppercase_and_filter_alphabets(plaintext)


class HillEncryptResponse(BaseModel):
    ciphertext: str


@app.post("/hill/encrypt", tags=["hill"], response_model=HillEncryptResponse)
async def hill_encrypt(body: HillEncryptRequest) -> dict:
    try:
        ciphertext = hill.encrypt(body.plaintext, body.key, body.m)
        return {"ciphertext": ciphertext}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


class HillDecryptRequest(BaseModel):
    ciphertext: str
    key: List[List[int]]
    m: int

    @validator('ciphertext')
    def validate_ciphertext(cls, ciphertext):
        return utils.uppercase_and_filter_alphabets(ciphertext)


class HillDecryptResponse(BaseModel):
    plaintext: str


@app.post("/hill/decrypt", tags=["hill"], response_model=HillDecryptResponse)
async def hill_decrypt(body: HillDecryptRequest) -> dict:
    try:
        plaintext = hill.decrypt(body.ciphertext, body.key, body.m)
        return {"plaintext": plaintext}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


class PlayfairEncryptRequest(BaseModel):
    plaintext: str
    key: List[List[str]]

    @validator('plaintext')
    def validate_plaintext(cls, plaintext):
        return utils.uppercase_and_filter_alphabets(plaintext)

    @validator('key')
    def validate_key(cls, key):
        for row in key:
            for ch in row:
                if len(ch) > 1:
                    raise HTTPException(
                        status_code=400, detail='Key matrix is not a char matrix')
        return key


class PlayfairEncryptResponse(BaseModel):
    ciphertext: str


@app.post("/playfair/encrypt", tags=["playfair"], response_model=PlayfairEncryptResponse)
async def playfair_encrypt(body: PlayfairEncryptRequest) -> dict:
    try:
        ciphertext = playfair.encrypt(body.plaintext, body.key)
        return {"ciphertext": ciphertext}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


class PlayfairDecryptRequest(BaseModel):
    ciphertext: str
    key: List[List[str]]

    @validator('ciphertext')
    def validate_ciphertext(cls, ciphertext):
        return utils.uppercase_and_filter_alphabets(ciphertext)

    @validator('key')
    def validate_key(cls, key):
        for row in key:
            for ch in row:
                if len(ch) > 1:
                    raise HTTPException(
                        status_code=400, detail='Key matrix is not a char matrix')
        return key


class PlayfairDecryptResponse(BaseModel):
    plaintext: str


@app.post("/playfair/decrypt", tags=["playfair"], response_model=PlayfairDecryptResponse)
async def playfair_decrypt(body: PlayfairDecryptRequest) -> dict:
    try:
        plaintext = playfair.decrypt(body.ciphertext, body.key)
        return {"plaintext": plaintext}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


class PlayfairGenerateKeyRequest(BaseModel):
    sentence: str


class PlayfairGenerateKeyResponse(BaseModel):
    key: List[List[str]]


@app.post("/playfair/generate-key", tags=["playfair"], response_model=PlayfairGenerateKeyResponse)
async def playfair_generate_key(body: PlayfairGenerateKeyRequest) -> dict:
    try:
        key = playfair.generate_key(body.sentence)
        return {"key": key}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

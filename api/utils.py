from threading import Thread
from secrets import token_hex

from jwt import encode
from oauth2 import generate_nonce
from web3 import Web3
from eth_account.messages import encode_defunct


def get_new_nonce() -> str:
    return generate_nonce(10)


class MessageVerifier:
    def __init__(self, expected_account: str, message : str, signature : str) -> None:
        self.expected_account = expected_account
        self.message = message
        self.signature = signature
        self.recovered_account = None
        self.web3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/eb5bb169b7914b1fb87bae46ae8f4dda")) # this URL should be configured in env vars

    def recover_message(self) -> None:
        encoded_message = encode_defunct(text=self.message)
        self.recovered_account = self.web3.eth.account.recover_message(signable_message=encoded_message, signature=self.signature)

    def execute_message_verifier(self) -> bool:
        job = Thread(target=self.recover_message)
        job.start()
        job.join()

        if self.expected_account == self.recovered_account:
            return True
        else:
            return False


class JWTGenerator:
    def __init__(self, user_id : int, user_address : str) -> None:
        self.jwt_secret = token_hex(16)
        self.user_id = user_id
        self.user_address = user_address

    def get_jwt_token(self) -> str:
        # ADD EXPIRATION TO TOKEN?
        jwt_token = encode({"id": "{}".format(self.user_id), "public_address": "{}".format(self.user_address)}, 
            self.jwt_secret, algorithm="HS256")
        return jwt_token
        
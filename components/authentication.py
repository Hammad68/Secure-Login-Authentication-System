import pyotp
import qrcode
import base64
import time
import os

# Server Setup
def generate_totp_secret(username):
    """Generating the totp secret to verify the OTP"""

    # Generating a random base32 secret
    secret = pyotp.random_base32()
    # Creating a TOTP object based on that secret
    totp = pyotp.TOTP(secret)

    # URI encodes the secret, issuer and account info
    uri = totp.provisioning_uri(
        name = username,
        issuer_name = 'Secure-Authenticar'
    )

    # Making a new directory if it does not exists
    save_dir = "qrcodes"
    os.makedirs(save_dir, exist_ok=True)

    # Generating the qrcode & saving that image into specified directory
    img = qrcode.make(uri)
    img.save(f'{save_dir}/{username}_totp_setup.png')

    return secret


# verification phase
def verifytotp(secret, user_otp):
    """Verifying the OTP by using generated totp"""

    # Generarting TOTP object from shared code
    totp = pyotp.TOTP(secret)
    # Verifying the OTP against the TOTP generated from the shared secret
    return totp.verify(user_otp)
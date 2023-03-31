import hashlib
import hmac
import os


def authorize(body, timestamp, sign):
    # Form the basestring as stated in the Slack API docs. We need to make a bytestring.
    base_string = f'v0:{timestamp}:{body}'.encode('utf-8')

    # Make the Signing Secret a bytestring too.
    slack_signing_secret = os.getenv("SIGNING_SECRET")
    slack_signing_secret = bytes(slack_signing_secret, 'utf-8')

    # Create a new HMAC "signature", and return the string presentation.
    my_signature = 'v0=' + hmac.new(
        slack_signing_secret, base_string, hashlib.sha256
    ).hexdigest()

    # Compare the the Slack provided signature to ours
    result = hmac.compare_digest(my_signature, sign)
    if not result:
        print('Verification failed. my_signature: ')
        print(f'{my_signature} != {sign}')

    return result

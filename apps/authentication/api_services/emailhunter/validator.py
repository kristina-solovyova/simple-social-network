from django.core.exceptions import ValidationError
from .verifier import EmailHunterVerifier
from social_net import settings

# Dict with verification result types in format "email type: is_valid"
RESULT_TYPES = {
    'deliverable': True,  # the email verification is successful and the email address is valid
    'undeliverable': False,  # the email address is not valid
    'risky': True  # the verification can't be validated
}


class EmailHunterValidator:
    def __init__(self):
        self.verifier = EmailHunterVerifier(api_key=settings.EMAIL_HUNTER_API_KEY)

    def __call__(self, value):
        self.verify(value)

    def verify(self, email):
        data = self.verifier.email_verifier(email)

        status = data['result']
        disposable = data['disposable']
        gibberish = data['gibberish']

        if status not in RESULT_TYPES.keys():
            raise ValidationError('Error during verification of this email.')
        if not RESULT_TYPES[status]:
            raise ValidationError('This is {} email. Please use another one.'.format(status))
        if disposable:
            raise ValidationError('This is an email address from a disposable email service.')
        if gibberish:
            raise ValidationError('This is an automatically generated email address.')


validate_email = EmailHunterValidator()

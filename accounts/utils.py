import secrets

from django.contrib.auth.hashers import make_password
from django.db import transaction

from .models import RecoveryCode


RECOVERY_CODE_COUNT = 10


def generate_recovery_codes(user):
    """
    Generate a fresh set of recovery codes for a user.

    Existing recovery codes are removed first.
    Plaintext codes are returned once to the caller.
    Only hashes are stored in the database.
    """

    plain_codes = []

    with transaction.atomic():

        RecoveryCode.objects.filter(
            user=user,
        ).delete()

        for _ in range(RECOVERY_CODE_COUNT):

            plain_code = (
                f"{secrets.token_hex(2).upper()}-"
                f"{secrets.token_hex(2).upper()}-"
                f"{secrets.token_hex(2).upper()}"
            )

            RecoveryCode.objects.create(
                user=user,
                code_hash=make_password(
                    plain_code
                ),
            )

            plain_codes.append(
                plain_code
            )

    return plain_codes


def verify_recovery_code(user, submitted_code):
    """
    Verify a recovery code for a user.

    A valid recovery code can only be used once.
    """

    if not submitted_code:
        return False

    submitted_code = submitted_code.strip().upper()

    recovery_codes = RecoveryCode.objects.filter(
        user=user,
        used_at__isnull=True,
    )

    for recovery_code in recovery_codes:

        if recovery_code.verify_code(
            submitted_code
        ):
            recovery_code.mark_used()
            return True

    return False
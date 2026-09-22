importsecrets

fromdjango.contrib.auth.hashersimportmake_password
fromdjango.dbimporttransaction

from.modelsimportRecoveryCode


RECOVERY_CODE_COUNT=10


defgenerate_recovery_codes(user):
    """
    Generate a fresh set of recovery codes for a user.

    Existing recovery codes are removed first.
    Plaintext codes are returned once to the caller.
    Only hashes are stored in the database.
    """

plain_codes=[]

withtransaction.atomic():

        RecoveryCode.objects.filter(
user=user,
).delete()

for_inrange(RECOVERY_CODE_COUNT):

            plain_code=(
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

returnplain_codes


defverify_recovery_code(user,submitted_code):
    """
    Verify a recovery code for a user.

    A valid recovery code can only be used once.
    """

ifnotsubmitted_code:
        returnFalse

submitted_code=submitted_code.strip().upper()

recovery_codes=RecoveryCode.objects.filter(
user=user,
used_at__isnull=True,
)

forrecovery_codeinrecovery_codes:

        ifrecovery_code.verify_code(
submitted_code
):
            recovery_code.mark_used()
returnTrue

returnFalse
import os
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from pathlib import Path


class MyValidator():
    message = _(
        "File extension “%(extension)s” is not allowed. "
        "Allowed extensions are: %(allowed_extensions)s."
        "File too large. Size should not exceed %(allowed_size)s MiB."
    )
    code = "invalid_extension"
    allowed_size = 3

    def __init__(self, allowed_extensions=None, allowed_size=None, message=None, code=None):
        if allowed_extensions is not None:
            allowed_extensions = [
                allowed_extension.lower() for allowed_extension in allowed_extensions
            ]
        self.allowed_extensions = allowed_extensions
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if allowed_size is not None:
            self.allowed_size = allowed_size

    def __call__(self, value):
        extension = Path(value.name).suffix[1:].lower()
        # print(extension)
        if (
            self.allowed_extensions is not None
            and extension not in self.allowed_extensions
            or value.size > self.allowed_size * 1024**2
        ):
            raise ValidationError(
                self.message,
                code=self.code,
                params={
                    "extension": extension,
                    "allowed_extensions": ", ".join(self.allowed_extensions),
                    "value": value,
                    "allowed_size": self.allowed_size,
                },
            )


def image_validator(value): # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpeg', '.jpg', '.png', '.gif']
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')
    if not ext.lower() in valid_extensions:
        raise ValidationError(f'Unsupported file extension. support only: {valid_extensions}')
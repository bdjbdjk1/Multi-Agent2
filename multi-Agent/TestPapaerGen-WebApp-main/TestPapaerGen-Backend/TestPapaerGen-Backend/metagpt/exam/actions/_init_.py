# exam/actions/__init__.py

from .ChecktTest import CheckDuplicate
from .pdfchange import Summarize
from .generate import GenerateQuestion
from .CreatChoose import Choose
from .CreatFill import Fill

__all__ = [
    'CheckDuplicate',
    'Summarize',
    'GenerateQuestion',
    'Choose',
    'Fill'
]

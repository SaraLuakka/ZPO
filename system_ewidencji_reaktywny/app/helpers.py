from flask import flash
from enum import Enum, auto


def flash_bootstrap_danger(text):
    flash(f'<div class="alert alert-danger" role="alert">{text}</div>')

def flash_bootstrap_success(text):
    flash(f'<div class="alert alert-success" role="alert">{text}</div>')


class AchievementState(str, Enum):
    NEW = "NEW"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
    TO_BE_FIXED = "TO_BE_FIXED"
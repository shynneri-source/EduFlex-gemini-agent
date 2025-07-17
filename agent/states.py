from typing_extensions import TypedDict


class overall_state(TypedDict):
    messages: str
    analytics: str
    plan: str
    lesson: str
    practice: str
    user_response: str
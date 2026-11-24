from types import SimpleNamespace
from uuid import uuid4

import pytest

from core.errors import AppError
from services.sessions import require_candidate_session


def test_anonymous_session_is_rejected() -> None:
    session = SimpleNamespace(candidate_id=None)

    with pytest.raises(AppError) as exc_info:
        require_candidate_session(session)

    assert exc_info.value.status_code == 403
    assert exc_info.value.code == "candidate_required"


def test_candidate_session_is_accepted() -> None:
    session = SimpleNamespace(candidate_id=uuid4())

    assert require_candidate_session(session) is session
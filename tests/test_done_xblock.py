"""
Basic unit tests for the Done XBlock.
"""

from mock import Mock
import pytest


def test_student_view(done_xblock):
    """ Test content of DoneXBlock's student view """
    student_fragment = done_xblock.render('student_view', Mock())
    assert 'done' in student_fragment.content


def test_studio_view(done_xblock):
    """ Test the DoneXBlock's studio view """
    request_body = b"""{
        "display_name": "foo"
    }"""
    request = Mock(method='POST', body=request_body)
    studio_fragment = done_xblock.studio_view(request)
    assert 'This is a very simple component' in studio_fragment.content


def test_workbench_scenarios(done_xblock):
    """ Test the DoneXBlock's workbench scenarios """
    first_scenario = done_xblock.workbench_scenarios()[0]
    assert first_scenario[0] == 'DoneXBlock'


def test_methods_methods(done_xblock):
    """Tests for basic methods """
    assert not done_xblock.has_dynamic_children()
    assert done_xblock.max_score() == 1


@pytest.mark.parametrize('is_done', [False, True])
def test_toggle_button(done_xblock, is_done):
    """Toggle the done button"""
    request_body = """{
        "display_name": "foo",
        "done": %s
    }""" % str(is_done).lower()
    request = Mock(method='POST', body=request_body.encode('utf-8'))
    response = done_xblock.toggle_button(request)
    assert response.json == {'state': is_done}

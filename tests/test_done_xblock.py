"""
Tests for the Feedback XBlock with heavy mocking.
"""


def test_something(done_xblock):
    pass


# def test_template_content(feedback_xblock):
#     """ Test content of FeedbackXBlock's student view """
#     student_fragment = feedback_xblock.render('student_view', Mock())
#     assert 'feedback' in student_fragment.content
#
#
# def test_studio_view(feedback_xblock):
#     """ Test content of FeedbackXBlock's author view """
#     student_fragment = feedback_xblock.render('studio_view', Mock())
#     assert 'feedback' in student_fragment.content
#
#
# def test_studio_submit(feedback_xblock):
#     """ Test the FeedbackXBlock's save action """
#     request_body = b"""{
#         "display_name": "foo"
#     }"""
#     request = Mock(method='POST', body=request_body)
#     response = feedback_xblock.studio_submit(request)
#     assert response.status_code == 200 and {'result': 'success'} == response.json, response.json
#
#
# def test_vote(feedback_xblock):
#     """ Test content of FeedbackXBlock's vote() method """
#     feedback_xblock.vote({'vote': 1})
#
#
# def test_feedback_method(feedback_xblock):
#     """ Test content of FeedbackXBlock's feedback() method """
#     request_body = b"""{
#         "freeform": "yes",
#         "vote": 1
#     }"""
#     request = Mock(method='POST', body=request_body)
#     response = feedback_xblock.feedback(request)
#
#     expected_response_json = {
#         "aggregate": [0, 1, 0, 0, 0],
#         "freeform": "yes",
#         "response": "Thank you for your feedback!",
#         "success": True,
#         "vote": 1,
#     }
#
#     assert response.status_code == 200 and response.json == expected_response_json, response.json

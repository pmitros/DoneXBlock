""" Show a toggle which lets students mark things as done."""

import pkg_resources
import re
import uuid

from django.utils.translation import ugettext as _

from xblock.core import XBlock
from xblock.fields import Scope, String, Boolean, DateTime, Float
from xblock.fragment import Fragment

from xblockutils.studio_editable import StudioEditableXBlockMixin


def resource_string(path):
    """Handy helper for getting resources from our kit."""
    data = pkg_resources.resource_string(__name__, path)
    return data.decode("utf8")


@XBlock.needs("i18n")
class DoneXBlock(StudioEditableXBlockMixin, XBlock):
    """
    Show a toggle which lets students mark things as done.
    """

    done = Boolean(
        scope=Scope.user_state,
        help="Is the student done?",
        default=False
    )

    align = String(
        display_name=_("Alignment"),
        scope=Scope.content,
        help="Align left/right/center",
        default="left"
    )

    button_text_before = String(
        display_name=_("Button text (incomplete)"),
        scope=Scope.content,
        help="Text displayed on the button before completion",
        default="Mark as complete"
    )

    button_text_after = String(
        display_name=_("Button text (complete)"),
        scope=Scope.content,
        help="Text displayed on the button after completion",
        default="Mark as incomplete"
    )

    editable_fields = ['align', 'button_text_before', 'button_text_after']
    has_score = True

    # pylint: disable=unused-argument
    @XBlock.json_handler
    def toggle_button(self, data, suffix=''):
        """
        Ajax call when the button is clicked. Input is a JSON dictionary
        with one boolean field: `done`. This will save this in the
        XBlock field, and then issue an appropriate grade.
        """
        if 'done' in data:
            self.done = data['done']
            if data['done']:
                grade = 1
            else:
                grade = 0
            grade_event = {'value': grade, 'max_value': 1}
            self.runtime.publish(self, 'grade', grade_event)
            # This should move to self.runtime.publish, once that pipeline
            # is finished for XBlocks.
            self.runtime.publish(self, "edx.done.toggled", {'done': self.done})

        return {'state': self.done}

    def student_view(self, context=None):  # pylint: disable=unused-argument
        """
        The primary view of the DoneXBlock, shown to students
        when viewing courses.
        """

        def css_content_escape(inputstr):
            """
            escape strings for CSS content attribute
            """
            # https://stackoverflow.com/a/25699953
            css_content_re = r'''['"\n\\]'''
            return re.sub(css_content_re, lambda m: '\\{:X} '.format(ord(m.group())), inputstr)

        button_text_before = css_content_escape(self.button_text_before)
        button_text_after = css_content_escape(self.button_text_after)
        status_button_text = self.button_text_before if self.done else self.button_text_after

        html_resource = resource_string("static/html/done.html")
        html = html_resource.format(done=self.done,
                                    id=uuid.uuid1(0),
                                    button_text_before=button_text_before,
                                    button_text_after=button_text_after,
                                    button_text=status_button_text,
                                    )

        (unchecked_png, checked_png) = (
            self.runtime.local_resource_url(self, x) for x in
            ('public/check-empty.png', 'public/check-full.png')
        )

        frag = Fragment(html)
        frag.add_css(resource_string("static/css/done.css"))
        frag.add_javascript(resource_string("static/js/src/done.js"))
        frag.initialize_js("DoneXBlock", {'state': self.done,
                                          'unchecked': unchecked_png,
                                          'checked': checked_png,
                                          'align': self.align.lower(),
                                          })
        return frag

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("DoneXBlock",
             """<vertical_demo>
                  <done align="left"> </done>
                  <done align="right"> </done>
                  <done align="center"> </done>
                </vertical_demo>
             """),
        ]

    # Everything below is stolen from
    # https://github.com/edx/edx-ora2/blob/master/apps/openassessment/
    #        xblock/lms_mixin.py
    # It's needed to keep the LMS+Studio happy.
    # It should be included as a mixin.

    display_name = String(
        default="Completion", scope=Scope.content,
        help="Display name"
    )

    start = DateTime(
        default=None, scope=Scope.content,
        help="ISO-8601 formatted string representing the start date "
             "of this assignment. We ignore this."
    )

    due = DateTime(
        default=None, scope=Scope.content,
        help="ISO-8601 formatted string representing the due date "
             "of this assignment. We ignore this."
    )

    weight = Float(
        display_name="Problem Weight",
        help=("Defines the number of points each problem is worth. "
              "If the value is not set, the problem is worth the sum of the "
              "option point values."),
        values={"min": 0, "step": .1},
        scope=Scope.content
    )

    def has_dynamic_children(self):
        """Do we dynamically determine our children? No, we don't have any.
        """
        return False

    def max_score(self):
        """The maximum raw score of our problem.
        """
        return 1

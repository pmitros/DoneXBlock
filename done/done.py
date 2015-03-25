"""TO-DO: Show a toggle which lets students mark things as done."""

import pkg_resources
import uuid

from xblock.core import XBlock
from xblock.fields import Scope, String, Boolean, DateTime, Float
from xblock.fragment import Fragment


class DoneXBlock(XBlock):
    """
    Show a toggle which lets students mark things as done.
    """

    done = Boolean(
           scope=Scope.user_state,
           help="Is the student done?",
           default=False
        )

    align = String(
           scope=Scope.settings,
           help="Align left/right/center",
           default="left"
        )

    has_score = True

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    @XBlock.json_handler
    def toggle_button(self, data, suffix=''):
        """
        Ajax call when the button is clicked. Input is a JSON dictionary
        with one boolean field: `done`. This will save this in the
        XBlock field, and then issue an appropriate grade. 
        """
        self.done = data['done']
        if data['done']:
            grade = 1
        else:
            grade = 0

        self.runtime.publish(self, 'grade', {'value': grade, 'max_value': 1})
        return {}

    def student_view(self, context=None):
        """
        The primary view of the DoneXBlock, shown to students
        when viewing courses.
        """
        html_resource = self.resource_string("static/html/done.html")
        html = html_resource.format(done=self.done,
                                    id=uuid.uuid1(0))
        unchecked_png = self.runtime.local_resource_url(self, 'public/check-empty.png')
        checked_png = self.runtime.local_resource_url(self, 'public/check-full.png')
        frag = Fragment(html)
        frag.add_css(self.resource_string("static/css/done.css"))
        frag.add_javascript(self.resource_string("static/js/src/done.js"))
        frag.initialize_js("DoneXBlock", {'state': self.done,
                                          'unchecked': unchecked_png,
                                          'checked': checked_png,
                                          'align': self.align.lower()})
        return frag

    def studio_view(self, _context=None):  # pylint: disable=unused-argument
        frag = Fragment(pkg_resources.resource_string("static/html/studioview.html"))
        return frag

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("DoneXBlock",
             """<vertical_demo>
                  <done align="left"> </done>
                  <done align="right"> </done>
                </vertical_demo>
             """),
        ]

    ## Everything below is stolen from https://github.com/edx/edx-ora2/blob/master/apps/openassessment/xblock/lms_mixin.py
    ## It's needed to keep the LMS+Studio happy.
    ## It should be included as a mixin.

    display_name = String(
        default="Completion", scope=Scope.settings,
        help="Display name"
    )

    start = DateTime(
        default=None, scope=Scope.settings,
        help="ISO-8601 formatted string representing the start date of this assignment. We ignore this."
    )

    due = DateTime(
        default=None, scope=Scope.settings,
        help="ISO-8601 formatted string representing the due date of this assignment. We ignore this."
    )

    weight = Float(
        display_name="Problem Weight",
        help=("Defines the number of points each problem is worth. "
              "If the value is not set, the problem is worth the sum of the "
              "option point values."),
        values={"min": 0, "step": .1},
        scope=Scope.settings
    )

    def has_dynamic_children(self):
        """Do we dynamically determine our children? No, we don't have any.
        """
        return False

    def max_score(self):
        """The maximum raw score of our problem.
        """
        return 1

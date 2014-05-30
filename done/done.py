"""TO-DO: Show a toggle which lets students mark things as done."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean, DateTime, Float
from xblock.fragment import Fragment


class DoneXBlock(XBlock):
    """
    Show a toggle which lets students mark things as done.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    done = Boolean(
           scope = Scope.user_state, 
           help = "Is the student done?",
           default = False
        )

    align = String(
           scope = Scope.settings, 
           help = "Align left/right/center",
           default = "left"
        )

    has_score = True

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    @XBlock.json_handler
    def toggle_button(self, data, suffix=''):
        self.done = data['done']
        if data['done']:
            grade = 1
        else:
            grade = 0

        self.runtime.publish(self, 'grade', {'value':grade, 'max_value': 1})
        return {}


    def student_view(self, context=None):
        """
        The primary view of the DoneXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/done.html")
        frag = Fragment(html)#.format(uid=self.scope_ids.usage_id))
        frag.add_css_url("//ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/themes/smoothness/jquery-ui.css")
        #frag.add_javascript_url("//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js")
        frag.add_javascript_url("//ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/jquery-ui.min.js")
        frag.add_css(self.resource_string("static/css/done.css"))
        grow_left = 1
        grow_right = 1
        if self.align.lower() == "left":
            grow_left = 0
        if self.align.lower() == "right":
            grow_right = 0
        frag.add_css(".done_left_spacer {{ flex-grow:{l}; }} .done_right_spacer {{ flex-grow:{r}; }}".format(r=grow_right, l=grow_left))
        frag.add_javascript(self.resource_string("static/js/src/done.js"))
        if self.done:
            frag.initialize_js("DoneXBlockOn")
        else:
            frag.initialize_js("DoneXBlockOff")
        return frag

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("DoneXBlock",
             """<vertical_demo>
                  <done align="left"> </done>
                  <done align="left"> </done>
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

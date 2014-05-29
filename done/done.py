"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean
from xblock.fragment import Fragment


class DoneXBlock(XBlock):
    """
    This XBlock will play an MP3 file as an HTML5 audio element. 
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    done = Boolean(
           scope = Scope.user_state, 
           help = "Is the student done?",
           default = False
        )

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
        frag.add_javascript("var done_done = "+("true" if self.done else "false")+";")
        frag.add_javascript(self.resource_string("static/js/src/done.js"))
        frag.initialize_js('DoneXBlock')
        return frag

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("DoneXBlock",
             """<vertical_demo>
                  <done> </done>
                </vertical_demo>
             """),
        ]

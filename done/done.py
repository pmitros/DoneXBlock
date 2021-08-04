""" Show a toggle which lets students mark things as done."""

import pkg_resources
import os
import uuid

from django.template import Context
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Scope, String, Boolean, DateTime, Float, Set
from xblockutils.resources import ResourceLoader

try:
    from xblock.completable import CompletableXBlockMixin
except ImportError:
    class CompletableXBlockMixin:
        """ No-op mixin for pre-Hawthorn Open edX versions """
        def emit_completion(self, completion_percent):
            pass


def _(str):
    """
    Dummy ugettext.
    """
    return str


def resource_string(path):
    """Handy helper for getting resources from our kit."""
    data = pkg_resources.resource_string(__name__, path)
    return data.decode("utf8")


@XBlock.needs("i18n")
class DoneXBlock(XBlock, CompletableXBlockMixin):
    """
    Show a toggle which lets students mark things as done.
    """
    loader = ResourceLoader(__name__)

    done = Boolean(
        scope=Scope.user_state,
        help=_("Is the student done?"),
        default=False
    )

    align = String(
        scope=Scope.settings,
        help=_("Align left/right/center"),
        default="left"
    )

    emoji_set = Set(scope=Scope.user_state, help=_("The set of emoji a student can react to"),
                    default={'like', 'love', 'confused', 'none'})

    emoji_selected = String(scope=Scope.user_state, help=_("Student selection"), default="none")

    has_score = True

    def render_template(self, path, context=None):
        return self.loader.render_django_template(
            os.path.join("static/html", path),
            context=Context(context or {}),
            i18n_service=self.runtime.service(self, "i18n"),
        )

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
            self.emit_completion(grade)

        return {'state': self.done}
        
# Don't touch anything up 
    @XBlock.json_handler
    def react_emoji(self, data, suffix=''):
        """
        Ajax call when one of the emoji, is selected. Input is a JSON dictionary
        with one string field: `selected`, which should be one of the emoji set defined above 
        """
        if data['selected'] in self.emoji_set:
            self.emoji_selected = data['selected']

            react_event = {'value': self.emoji_selected}
            self.runtime.publish(self, 'emoji', react_event)
            # This should move to self.runtime.publish, once that pipeline
            # is finished for XBlocks.
            self.runtime.publish(self, "edx.done.react", {'selected_emoji': self.emoji_selected})

        return {'selected': self.emoji_selected}

    @XBlock.supports("multi_device")
    def student_view(self, context=None):  # pylint: disable=unused-argument
        """
        The primary view of the DoneXBlock, shown to students
        when viewing courses.
        """
        html = self.render_template("done.html", {
            'done': self.done,
            'id': uuid.uuid1(0),
            'selected':self.emoji_selected
        })

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
                                          'align': self.align.lower()})
        frag.initialize_js("ReactXBlock",{'selected':self.emoji_selected})
                                        
        return frag

    def studio_view(self, _context=None):  # pylint: disable=unused-argument
        '''
        Minimal view with no configuration options giving some help text.
        '''
        html = self.render_template("studioview.html")
        frag = Fragment(html)
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
        default=_("Completion"), scope=Scope.settings,
        help=_("Display name")
    )

    start = DateTime(
        default=None, scope=Scope.settings,
        help=_("ISO-8601 formatted string representing the start date "
               "of this assignment. We ignore this.")
    )

    due = DateTime(
        default=None, scope=Scope.settings,
        help=_("ISO-8601 formatted string representing the due date "
               "of this assignment. We ignore this.")
    )

    weight = Float(
        display_name=_("Problem Weight"),
        help=_("Defines the number of points each problem is worth. "
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

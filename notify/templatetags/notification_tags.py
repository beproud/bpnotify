#:coding=utf8:

from django.template import Node, Library, TemplateDoesNotExist, TemplateSyntaxError, Variable
from django.template.loader import render_to_string

from notify.engine import render_notification

register = Library()

class NotificationNode(Node):
    def __init__(self, notification_var, template_name_var):
        self.notification_var = Variable(notification_var)
        self.template_name_var = Variable(template_name_var) if template_name_var else None

    def render(self, context):
        try:
            notification = self.notification_var.resolve(context)
            template_name = self.template_name_var.resolve(context) if self.template_name_var else None
            if not template_name:
                template_name = "%s.html" % notification.media.lower()
            context_dict = {}
            for c in context.dicts:
                context_dict.update(c)

            return render_notification(notification, template_name,extra_context=context_dict)
        except TemplateDoesNotExist,e:
            return ''

@register.tag
def display_notification(parser, token):
    bits = token.split_contents()
    if len(bits) != 2 and len(bits) != 3:
        raise TemplateSyntaxError("%r takes at least one argument." % bits[0])
    template_name = bits[2] if len(bits) == 3 else None 
    return NotificationNode(bits[1], template_name)

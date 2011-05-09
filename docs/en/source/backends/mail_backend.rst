=======================
Email Backend
=======================

.. module:: beproud.django.notify.backends.mail

.. class:: beproud.django.notify.backends.mail.EmailBackend

The email backend sends notifications via email messages. The content of email
is rendered from a django template and given a context including relavent
information about the notification.  The body templates can contain both html
and text, only html, or only text.

Email Templates
-------------------------

The email content is rendered from a template found in the following templates:

.. list-table::
    :header-rows: 1

    * - Content
      - Template Path
    * - Subject
      - notify/<notify_type>/<media>/mail_subject.txt
    * - HTML Body
      - notify/<notify_type>/<media>/mail_body.html
    * - Text Body
      - notify/<notify_type>/<media>/mail_body.txt

The subject template is required. One of the html body template or text body
template is required.  If only a text template is found then the email is sent
as text.  If only a html template is found then the email is send as multipart
with a text body created by stripping html tags from the html body.  If both
html and a text template are found then the email is sent as multipart with the
rendered content.

.. note::

    If no subject template is found or if neither the html body or text
    body template could be found then the email is not sent.

The context given to the template contains the following data as well as all
data passed in the extra_context:

.. list-table::
    :header-rows: 1

    * - Key
      - Description
    * - target
      - The target object of the notification.
    * - notify_type
      - The notify type of the notification
    * - media
      - The media type of the notification

Recipient
----------------------

The email recipient is retrieved from each target object by searching for a
"email" or "mail" property. If none is found the extra_data dictionary is
searched for a "email" or "mail" key.

.. note::

    If no recipient email could be retrieved then the mail is not sent.

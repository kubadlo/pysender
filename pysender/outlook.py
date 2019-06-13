import win32com.client as win32


class OutlookClient:
    def __init__(self):
        self.outlook = win32.Dispatch('outlook.application')

    def send_email(self, address_to, subject, body_plain, body_html):
        mail = self.outlook.CreateItem(0)
        mail.BCC = address_to
        mail.Subject = subject
        mail.Body = body_plain
        mail.HTMLBody = body_html

        mail.Send()

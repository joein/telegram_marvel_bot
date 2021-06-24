class FetcherException(Exception):
    def __init__(self, status_code, text):
        self.text = text
        self.status_code = status_code

    def __str__(self):
        if self.status_code or self.text:
            return f"""Fetcher Exception:
Response ended with status code {self.status_code},
response.text is {self.text}
"""
        else:
            return "Fetcher Exception has been raised"

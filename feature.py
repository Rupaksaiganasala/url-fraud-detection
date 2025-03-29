# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
import ipaddress
import re
import urllib.request
from bs4 import BeautifulSoup
import socket
import requests
from googlesearch import search
import whois
from datetime import date, datetime
import os
import ssl
from urllib.parse import urlparse

class FeatureExtraction:
    def __init__(self, url):
        self.features = []
        self.url = url
        self.domain = ""
        self.whois_response = ""
        self.urlparse = ""
        self.response = ""
        self.soup = ""

        try:
            self.response = requests.get(url)
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
        except:
            pass

        try:
            self.urlparse = urlparse(url)
            self.domain = self.urlparse.netloc
        except:
            pass

        try:
            self.whois_response = whois.whois(self.domain)
        except:
            pass

        self.extract_features()

    def extract_features(self):
        self.features.append(self.length_url())
        self.features.append(self.qty_dot_url())
        self.features.append(self.qty_hyphen_url())
        self.features.append(self.qty_slash_url())
        self.features.append(self.qty_questionmark_url())
        self.features.append(self.qty_equal_url())
        self.features.append(self.qty_at_url())
        self.features.append(self.email_in_url())
        self.features.append(self.domain_length())
        self.features.append(self.domain_in_ip())
        self.features.append(self.qty_dot_domain())
        self.features.append(self.qty_hyphen_domain())
        self.features.append(self.directory_length())
        self.features.append(self.qty_slash_directory())
        self.features.append(self.file_length())
        self.features.append(self.qty_dot_file())
        self.features.append(self.qty_hyphen_file())
        self.features.append(self.params_length())
        self.features.append(self.qty_params())
        self.features.append(self.url_google_index())
        self.features.append(self.tls_ssl_certificate())
        self.features.append(self.qty_redirects())
        self.features.append(self.url_shortened())

    def length_url(self):
        return len(self.url)

    def qty_dot_url(self):
        return self.url.count('.')

    def qty_hyphen_url(self):
        return self.url.count('-')

    def qty_slash_url(self):
        return self.url.count('/')

    def qty_questionmark_url(self):
        return self.url.count('?')

    def qty_equal_url(self):
        return self.url.count('=')

    def qty_at_url(self):
        return self.url.count('@')

    def email_in_url(self):
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        return 0 if re.search(email_pattern, self.url) else 1

    def domain_length(self):
        return len(self.domain)

    def domain_in_ip(self):
        ipv4_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
        ipv6_pattern = r"^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$"
        return 1 if re.match(ipv4_pattern, self.domain) or re.match(ipv6_pattern, self.domain) else 0

    def qty_dot_domain(self):
        return self.domain.count('.')

    def qty_hyphen_domain(self):
        return self.domain.count('-')

    def directory_length(self):
        return len(self.urlparse.path)

    def qty_slash_directory(self):
        return self.urlparse.path.count('/')

    def file_length(self):
        file_name = os.path.basename(self.urlparse.path)
        return len(file_name)

    def qty_dot_file(self):
        file_name = os.path.basename(self.urlparse.path)
        return file_name.count('.')

    def qty_hyphen_file(self):
        file_name = os.path.basename(self.urlparse.path)
        return file_name.count('-')

    def params_length(self):
        return len(self.urlparse.query)

    def qty_params(self):
        return len(self.urlparse.query.split('&')) if self.urlparse.query else -1

    def url_google_index(self):
        try:
            query = f"site:{self.url}"
            search_results = list(search(query, num=1, stop=1))
            return 1 if search_results else 0
        except Exception:
            return 0

    def tls_ssl_certificate(self):
        try:
            parsed_url = urlparse(self.url)
            if parsed_url.scheme != 'https':
                return 0
            context = ssl.create_default_context()
            with socket.create_connection((parsed_url.hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=parsed_url.hostname) as ssock:
                    return 1
        except ssl.SSLError:
            return 0
        except Exception:
            return 0

    def qty_redirects(self):
        try:
            response = requests.get(self.url, allow_redirects=True)
            return 1 if len(response.history) > 0 else 0
        except Exception:
            return 0

    def url_shortened(self):
        pattern = r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|' \
                  r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|' \
                  r'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|' \
                  r'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|lnkd\.in|db\.tt|' \
                  r'qr\.ae|adf\.ly|cur\.lv|ow\.ly|ity\.im|q\.gs|po\.st|bc\.vc|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|' \
                  r'1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net'
        return -1 if re.search(pattern, self.url) else 1

    def get_features_list(self):
        return self.features
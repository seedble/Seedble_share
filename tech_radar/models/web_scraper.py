from odoo import fields, models, api
import spacy
import urllib3
from bs4 import BeautifulSoup


class WebScraper(models.Model):
    _name = "web.scraper"
    _description = "Scans websites for keywords"

    url_field = fields.Char(string="Paste URL Here", required=True)

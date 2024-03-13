from odoo import fields, models, api
from openai import OpenAI, RateLimitError

client = OpenAI()
class EntriesList(models.Model):
    _name = "entries.list"
    _description = "Tracks entries"

    query = fields.Char(string="Enter question", required=True)
    response = fields.Text(string="Recommended answer", compute="_compute_answer", store=True)

    @api.depends('query')
    def _compute_answer(self):
        for rec in self:
            if rec.query:
                try:
                    rec.response = rec.answer_question()
                except RateLimitError:
                    rec.response = "Not enough tokens"
            else:
                rec.response = ""
    def answer_question(self):
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"system", "content":"You are a helpful consulting assistant"},
                {"role":"user", "content":self.query}
            ]
        )
        return completion

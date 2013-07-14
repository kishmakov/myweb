import HTMLParser
from django.db import models

class Notes(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    section = models.CharField(db_column='Section', max_length=30)

    title = models.TextField(db_column='Title')
    author = models.TextField(db_column='Author')
    teaser = models.TextField(db_column='Teaser')
    body = models.TextField(db_column='Body')
    original = models.TextField(db_column='Original')

# def get_absolute_url(self):
    #     return {'simple_fluid', [self.id]}

    def __unicode__(self):
        h = HTMLParser.HTMLParser()
        unescaped = h.unescape(self.title)
        return u'{0} - {1}: {2}'.format(self.id, self.section, unescaped)

    class Meta:
        db_table = u'notes'


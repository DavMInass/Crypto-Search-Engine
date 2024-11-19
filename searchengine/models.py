from django.db import models

# Create your models here.

# Represents a document
class Document(models.Model):
    # Doc num/id
    # db_index means we can quickly find docs by id
    doc_no = models.IntegerField(db_index=True)
    # Document text
    text = models.TextField()

    title = models.TextField()
    views_count = models.IntegerField(default=0)

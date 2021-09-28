from django.db import models
from users_app.models.models_user import User
from django.db.models.base import ObjectDoesNotExist

# Managers
class DocumentClassificationManger(models.Manager):
    def create_document_classification(self, name):
        if self.filter(name=name).exists():
            return
        self.create(name=name) 


class DocumentTypeManager(models.Manager):
    def create_document_type(self, classification_name, type_name):
        if self.filter(name=type_name).exists():
            return
        try:
            classification = DocumentClassification.objects.get(name=classification_name)
            self.create(classification_id=classification, name=type_name)
        except ObjectDoesNotExist: 
            msg = "couldn't find classification"
            return


# Models
class DocumentClassification(models.Model):
    name = models.CharField(max_length=100, unique=True)
    objects = DocumentClassificationManger()

    def __str__(self):
        return self.name



class DocumentType(models.Model):
    classification_id = models.ForeignKey(DocumentClassification, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    objects = DocumentTypeManager()

    def __str__(self):
        return self.name


def content_file_name(instance, filename):
    return f"{instance.user_id.email}/{instance.document_type_id.name}/{filename}"


class Document(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    document_type_id = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=100)
    document = models.FileField(upload_to=content_file_name)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.document_name

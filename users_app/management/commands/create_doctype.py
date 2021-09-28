from django.core.management.base import BaseCommand, CommandError
from users_app.models.models_documents import DocumentClassification, DocumentType


class Command(BaseCommand):
    help = "Adds basic document types"

    def handle(self, *args, **options):
        DocumentClassification.objects.create_document_classification("Personal")
        DocumentClassification.objects.create_document_classification("Formal")
        DocumentClassification.objects.create_document_classification("Official")
        DocumentClassification.objects.create_document_classification("Payslips")
        DocumentClassification.objects.create_document_classification("Resume")
        DocumentClassification.objects.create_document_classification("Recruiter Access")


        DocumentType.objects.create_document_type("Personal", "PAN")
        DocumentType.objects.create_document_type("Personal", "Aadhar")
        DocumentType.objects.create_document_type("Formal", "Joining Letter")
        DocumentType.objects.create_document_type("Formal", "Relieving Letter")
        DocumentType.objects.create_document_type("Formal", "Backgroung Verification Form")
        DocumentType.objects.create_document_type("Official", "Laptop Agreement")
        DocumentType.objects.create_document_type("Payslips", "Payslip")
        DocumentType.objects.create_document_type("Resume", "Original Resume")
        DocumentType.objects.create_document_type("Recruiter Access", "Company Resume")

        self.stdout.write("Created basic document types")

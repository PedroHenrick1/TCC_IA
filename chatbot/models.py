from django.db import models
import hashlib

class ConversationHistory(models.Model):
    session_id = models.CharField(max_length=100, db_index=True)
    human_message = models.TextField()
    ai_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sessão: {self.session_id} - Humano: {self.human_message[:50]}"

class ProcessedDocument(models.Model):
    file_path = models.CharField(max_length=500, unique=True)
    file_hash = models.CharField(max_length=64)
    content = models.TextField() 
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_path

    @staticmethod
    def calculate_hash(file_path):
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

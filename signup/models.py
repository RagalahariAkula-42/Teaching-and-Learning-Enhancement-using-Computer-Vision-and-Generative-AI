# Import djongo's models to use MongoDB features
from django.contrib.auth.models import User
from django.utils.timezone import now
from djongo import models
from bson import ObjectId


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(
        max_length=50, 
        choices=[("student", "Student"), ("teacher", "Teacher")]
    )
    created_at = models.DateTimeField(default=now)
    is_resolved = models.BooleanField(default=False)
    id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)  # MongoDB ObjectId as primary key

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Test(models.Model):
    #id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)  # MongoDB ObjectId as primary key
    test_name = models.CharField(max_length=100)
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()
    duration = models.PositiveIntegerField()  # Duration in minutes
    num_questions = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tests_created")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.test_name

    class Meta:
        ordering = ["-created_at"]


class TestQuestion(models.Model):
    #id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)  # MongoDB ObjectId as primary key
    test = models.ForeignKey(Test, related_name="questions", on_delete=models.CASCADE)  # ForeignKey to Test
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(
        max_length=1, 
        choices=[("A", "Option A"), ("B", "Option B"), ("C", "Option C"), ("D", "Option D")]
    )

    def __str__(self):
        return f"Question {self.id} for Test: {self.test.test_name}"

    class Meta:
        ordering = ["id"]



class StudentMarks(models.Model):
    #id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)  # MongoDB ObjectId as primary key
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="marks")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="marks")
    marks_obtained = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.student.username} - {self.test.test_name}: {self.marks_obtained}"

    class Meta:
        unique_together = ("test", "student")
        ordering = ["-marks_obtained"]


class StudentTestAttempt(models.Model):
    #id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)  # MongoDB ObjectId as primary key
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test_attempts")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="attempts")
    correct_answers = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.test.test_name}"

    class Meta:
        unique_together = ("student", "test")
        ordering = ["-submitted_at"]


class Notes(models.Model):
    note_name = models.CharField(max_length=250)
    note_link = models.URLField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes_created")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.note_link

    class Meta:
        ordering = ["-created_at"]

class Classes(models.Model):
    class_name = models.CharField(max_length=250)
    class_link = models.URLField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="classes_created")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.class_link

    class Meta:
        ordering = ["-created_at"]

class Doubts(models.Model):
    doubt = models.TextField()
    posted_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doubt_posted_to")
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doubt_posted_by")
    posted_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.title} by {self.posted_by.username}"

    class Meta:
        ordering = ["-posted_at"]

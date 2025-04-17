from django.contrib import admin
from .models import Profile, Test, TestQuestion, StudentMarks, StudentTestAttempt, Notes, Classes, Doubts

# Admin configuration for Profile model
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at', 'is_resolved')

# Admin configuration for Test model
class TestAdmin(admin.ModelAdmin):
    list_display = ('id_str', 'test_name', 'open_time', 'close_time', 'duration', 'num_questions', 'created_by', 'created_at')

    def id_str(self, obj):
        return str(obj.id)  # Convert ObjectId to string for display
    id_str.short_description = "ID"  # Label for the column

# Admin configuration for TestQuestion model
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ('id_str', 'test_id_str', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer')

    def id_str(self, obj):
        return str(obj.id)  # Convert ObjectId to string for display
    id_str.short_description = "ID"  # Label for the column

    # Explicitly display the hexadecimal ObjectId for the test field
    def test_id_str(self, obj):
        return str(obj.test.id)  # Convert the related Test's ObjectId to string for display
    test_id_str.short_description = "Test ID"  # Label for the column

# Admin configuration for StudentMarks model
class StudentMarksAdmin(admin.ModelAdmin):
    list_display = ('id_str', 'test', 'student', 'marks_obtained')

    def id_str(self, obj):
        return str(obj.id)  # Convert ObjectId to string for display
    id_str.short_description = "ID"  # Label for the column

# Admin configuration for StudentTestAttempt model
class StudentTestAttemptAdmin(admin.ModelAdmin):
    list_display = ('id_str', 'student', 'test', 'correct_answers', 'total_questions', 'submitted_at')

    def id_str(self, obj):
        return str(obj.id)  # Convert ObjectId to string for display
    id_str.short_description = "ID"  # Label for the column

# Admin configuration for Notes model
class NotesAdmin(admin.ModelAdmin):
    list_display = ('note_name', 'note_link', 'created_by', 'created_at')

# Admin configuration for Classes model
class ClassesAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'class_link', 'created_by', 'created_at')

# Admin configuration for Doubts model
class DoubtsAdmin(admin.ModelAdmin):
    list_display = ('doubt', 'posted_to', 'posted_by', 'posted_at')


# Register all models with Django Admin
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(TestQuestion, TestQuestionAdmin)
admin.site.register(StudentMarks, StudentMarksAdmin)
admin.site.register(StudentTestAttempt, StudentTestAttemptAdmin)
admin.site.register(Notes, NotesAdmin)
admin.site.register(Classes, ClassesAdmin)
admin.site.register(Doubts, DoubtsAdmin)

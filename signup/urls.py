from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    signup,
    login_user,
    logout_user,
    teacher_home,
    create_test,
    tests_created,
    download_questions,
    download_marks,
    student_home,
    attempt_test,
    test,
    submit_test,
    tests_attempted,
    preperation,
    purpose,
    board,
    upload,
    uploads,
    notes_classes,
    post_doubt,
    doubts_posted,
    doubts_recieved,
    translate,
    summary,
)

urlpatterns = [
    # Authentication URLs
    path('', purpose, name="purpose"),
    path('board', board, name="board"),
    path('signup/', signup, name="signup"),
    path('login/', login_user, name="login"),  
    path('logout/', logout_user, name="logout"),
    path('translate/', translate, name='translate'),
    path('summary/', summary, name='summary'),


    # Teacher URLs
    path('teacher_home/', teacher_home, name='teacher_home'),
    path('create_test/', create_test, name='create_test'),
    path('tests_created/', tests_created, name='tests_created'),
    path('download_questions/<str:test_id>/', download_questions, name='download_questions'),
    path('download_marks/<str:test_id>/', download_marks, name='download_marks'),
    path('upload/', upload, name="upload"),
    path('uploads/', uploads, name="uploads"),
    path('doubts_recieved/', doubts_recieved, name="doubts_recieved"),

    # Student URLs
    path('student_home/', student_home, name='student_home'),
    path('attempt_test/', attempt_test, name='attempt_test'),
    path('test/<str:test_id>/', test, name='test'),
    path('submit_test/<str:test_id>/', submit_test, name='submit_test'),
    path('tests_attempted/', tests_attempted, name='tests_attempted'),
    path('preperation/', preperation, name='preperation'),
    path('notes_classes/', notes_classes, name='notes_classes'),
    path('post_doubt/', post_doubt, name="post_doubt"),
    path('doubts_posted/', doubts_posted, name="doubts_posted"),
]


# Serve static files in development (only needed when DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

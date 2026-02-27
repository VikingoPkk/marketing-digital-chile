import io
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm

# Modelos del sistema
from .models import Course, Certificate, LessonProgress, Lesson, Enrollment, Quiz
from agency.models import Service 

# 1. VISTAS DE NAVEGACIÓN Y AGENCIA
def home(request):
    """Página de inicio de la plataforma."""
    return render(request, 'home.html')

def services_list(request):
    """Muestra tus servicios reales desde la app Agency."""
    servicios_db = Service.objects.filter(is_active=True).order_by('order')
    return render(request, 'services.html', {'servicios': servicios_db})

@login_required
def dashboard(request):
    """Panel del alumno con progreso real de cursos."""
    inscripciones = Enrollment.objects.filter(user=request.user)
    cursos_inscritos = []

    for inscripcion in inscripciones:
        curso = inscripcion.course
        total = curso.total_lessons
        completadas = LessonProgress.objects.filter(
            user=request.user, 
            lesson__module__course=curso, 
            is_completed=True
        ).count()
        
        progreso = int((completadas / total) * 100) if total > 0 else 0
        cursos_inscritos.append({
            'curso': curso,
            'progreso': progreso
        })

    otros_cursos = Course.objects.exclude(enrollment__user=request.user).filter(is_published=True)

    return render(request, 'dashboard.html', {
        'cursos_inscritos': cursos_inscritos,
        'otros_cursos': otros_cursos
    })

# 2. LÓGICA DE CURSOS Y CLASES
@login_required
def course_detail(request, course_id):
    """Carga la lección actual y evita errores de ID."""
    course = get_object_or_404(Course, id=course_id)
    
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        return redirect('checkout', course_id=course.id)

    lessons = Lesson.objects.filter(module__course=course).order_by('module__order', 'order')
    
    if not lessons.exists():
        messages.warning(request, f"El curso '{course.title}' aún no tiene lecciones cargadas.")
        return redirect('dashboard')

    lesson_id = request.GET.get('lesson')
    if lesson_id:
        current_lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    else:
        current_lesson = lessons.first()

    total = lessons.count()
    completas = LessonProgress.objects.filter(user=request.user, lesson__module__course=course, is_completed=True).count()
    progreso = int((completas / total) * 100) if total > 0 else 0

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'current_lesson': current_lesson,
        'progreso_curso': progreso
    })

@login_required
def toggle_lesson_completion(request, lesson_id):
    """Marca lección como completada."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, created = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.is_completed = not progress.is_completed
    progress.save()
    return redirect(f"/course/{lesson.module.course.id}/?lesson={lesson.id}")

@login_required
def enroll_trial(request, course_id):
    """Inscripción rápida."""
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('dashboard')

@login_required
def checkout(request, course_id):
    """Página de preventa."""
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/checkout.html', {'course': course})

# --- SISTEMA DE EXÁMENES ---
@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        score = 0
        review_data = []
        total_questions = questions.count()
        
        for q in questions:
            ans = request.POST.get(f'question_{q.id}')
            is_correct = (int(ans) == q.correct_option) if ans else False
            if is_correct: score += 1

            review_data.append({
                'question_text': q.text,
                'user_answer_text': getattr(q, f'option{ans}') if ans else "Sin respuesta",
                'correct_answer_text': getattr(q, f'option{q.correct_option}'),
                'is_correct': is_correct
            })

        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        request.session['quiz_result'] = {
            'quiz_title': quiz.title,
            'quiz_id': quiz.id,
            'percentage': round(percentage, 1),
            'course_id': quiz.module.course.id,
            'review_data': review_data
        }
        return render(request, 'courses/quiz_result.html')

    return render(request, 'courses/quiz.html', {'quiz': quiz, 'questions': questions})

# --- EDICIÓN DE PERFIL CORREGIDA ---
@login_required
def edit_profile(request):
    """Procesa los cambios del perfil, incluyendo la foto."""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        
        # Guardar RUT y BIO solo si existen en tu modelo
        if hasattr(user, 'rut'): user.rut = request.POST.get('rut')
        if hasattr(user, 'bio'): user.bio = request.POST.get('bio')
        
        # Procesar la foto (buscamos 'avatar' para coincidir con tu HTML)
        if 'avatar' in request.FILES:
            user.profile_picture = request.FILES['avatar']
            
        user.save()
        messages.success(request, "Perfil actualizado correctamente.")
        return redirect('dashboard')
        
    return render(request, 'account/edit_profile.html')

# 3. SISTEMA DE DIPLOMAS
@login_required
def check_certificate(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    total_lessons = course.total_lessons
    completed_lessons = LessonProgress.objects.filter(
        user=request.user, 
        lesson__module__course=course, 
        is_completed=True
    ).count()

    if total_lessons > 0 and completed_lessons >= total_lessons:
        cert, created = Certificate.objects.get_or_create(user=request.user, course=course)
        return redirect('generate_diploma_pdf', certificate_id=cert.id)
    
    messages.warning(request, "Aún no has completado todas las lecciones.")
    return redirect('dashboard')

@login_required
def generate_diploma_pdf(request, certificate_id):
    cert = get_object_or_404(Certificate, id=certificate_id, user=request.user)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)
    c.setStrokeColorRGB(0.1, 0.3, 0.8) 
    c.setLineWidth(8)
    c.rect(1*cm, 1*cm, width-2*cm, height-2*cm)
    c.setStrokeColorRGB(0.8, 0.6, 0.2) 
    c.setLineWidth(2)
    c.rect(1.4*cm, 1.4*cm, width-2.8*cm, height-2.8*cm)
    c.setFont("Helvetica-Bold", 45)
    c.drawCentredString(width/2, height - 5*cm, "DIPLOMA DE FINALIZACIÓN")
    c.setFont("Helvetica", 18)
    c.drawCentredString(width/2, height - 7*cm, "ESTE CERTIFICADO SE OTORGA CON EXCELENCIA A:")
    c.setFont("Helvetica-Bold", 35)
    nombre = f"{request.user.first_name} {request.user.last_name}".upper()
    if not request.user.first_name: nombre = request.user.username.upper()
    c.drawCentredString(width/2, height/2 + 0.5*cm, nombre)
    c.setFont("Helvetica", 16)
    c.drawCentredString(width/2, height/2 - 2*cm, "Por haber cumplido con todos los requisitos académicos del curso:")
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, height/2 - 3.5*cm, cert.course.title.upper())
    c.setFont("Helvetica", 10)
    c.drawString(2*cm, 3*cm, f"Fecha de emisión: {cert.issue_date.strftime('%d/%m/%Y')}")
    c.drawRightString(width-2*cm, 3*cm, f"Código de Verificación: {cert.certificate_code}")
    c.setFont("Times-BoldItalic", 15)
    c.drawCentredString(width/2, 3.5*cm, "Angelo Vilche Huerta") 
    c.line(width/2 - 3*cm, 3.8*cm, width/2 + 3*cm, 3.8*cm)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, 3*cm, "Director Académico MD Chile")
    c.showPage()
    c.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'Diploma_{cert.course.slug}.pdf')
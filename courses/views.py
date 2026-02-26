import io
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from .models import Course, Certificate, LessonProgress, Lesson, Enrollment, Quiz

# 1. VISTAS PRINCIPALES
def home(request):
    """Página de inicio de la plataforma."""
    return render(request, 'home.html')

@login_required
def dashboard(request):
    """Panel del alumno con progreso de cursos."""
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

    # Cursos disponibles para inscribirse
    otros_cursos = Course.objects.exclude(enrollment__user=request.user).filter(is_published=True)

    return render(request, 'dashboard.html', {
        'cursos_inscritos': cursos_inscritos,
        'otros_cursos': otros_cursos
    })

@login_required
def course_detail(request, course_id):
    """Vista de las lecciones del curso."""
    course = get_object_or_404(Course, id=course_id)
    # Verifica si el usuario está inscrito
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        return redirect('checkout', course_id=course.id)
    return render(request, 'courses/course_detail.html', {'course': course})

# 2. LÓGICA DE PROGRESO Y CLASES
@login_required
def toggle_lesson_completion(request, lesson_id):
    """Marca una lección como completada o pendiente."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, created = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.is_completed = not progress.is_completed
    progress.save()
    return redirect('course_detail', course_id=lesson.module.course.id)

@login_required
def enroll_trial(request, course_id):
    """Inscripción rápida/gratuita."""
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('dashboard')

@login_required
def checkout(request, course_id):
    """Página de preventa/pago del curso."""
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/checkout.html', {'course': course})

@login_required
def take_quiz(request, quiz_id):
    """Vista para realizar exámenes."""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'courses/quiz.html', {'quiz': quiz})

@login_required
def edit_profile(request):
    """Edición de perfil de usuario."""
    # Aquí iría tu lógica de formulario de perfil
    return render(request, 'account/edit_profile.html')

# 3. SISTEMA DE DIPLOMAS
@login_required
def check_certificate(request, course_id):
    """Verifica progreso y redirige a la generación del diploma."""
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
    """Dibuja y descarga el diploma en PDF."""
    cert = get_object_or_404(Certificate, id=certificate_id, user=request.user)
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

    # --- DISEÑO ---
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
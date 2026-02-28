import io
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string # <-- NUEVO: Para diseño HTML
from django.utils.html import strip_tags           # <-- NUEVO: Para versión texto plano
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm

# Modelos del sistema
from .models import Course, Certificate, LessonProgress, Lesson, Enrollment, Quiz, CourseQuery
from agency.models import Service, ContactMessage 

# 1. VISTAS DE NAVEGACIÓN Y AGENCIA
def home(request):
    """Página de inicio de la plataforma."""
    return render(request, 'home.html')

def contact_page(request):
    """Muestra la página de contacto oficial de MD Chile."""
    return render(request, 'contact.html')

def services_list(request):
    """Muestra la vitrina de servicios dinámicos."""
    servicios_reales = Service.objects.filter(is_active=True).order_by('order')
    return render(request, 'servicios_academia.html', {'servicios': servicios_reales})

# --- LANDING PAGE CON CORREO HTML PROFESIONAL ---
def service_detail(request, slug):
    """Landing page individual con captura de lead y envío de regalo con diseño HTML."""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    if request.method == 'POST':
        nombre = request.POST.get('name')
        email = request.POST.get('email')
        mensaje = request.POST.get('message')
        
        if nombre and email:
            # 1. Guardar el Lead en la base de datos
            ContactMessage.objects.create(
                name=nombre,
                email=email,
                message=mensaje,
                servicio_interes=service,
                lead_source=f"Landing_{service.slug}"
            )
            
            # 2. Construir link del regalo (PDF o Video)
            regalo_url = request.build_absolute_uri(service.regalo_pdf.url) if service.regalo_pdf else service.regalo_video_privado
            
            # 3. Preparar el Correo con Diseño HTML
            asunto = f"🎁 ¡Aquí tienes tu regalo de MD Chile: {service.title}!"
            context = {
                'nombre': nombre,
                'servicio': service,
                'regalo_url': regalo_url
            }
            
            # Renderizamos el template HTML que crearemos luego
            html_message = render_to_string('emails/welcome_lead.html', context)
            plain_message = strip_tags(html_message) # Versión alternativa para apps viejas
            
            try:
                send_mail(
                    asunto,
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    html_message=html_message, # <--- DISPARO CON DISEÑO
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error enviando correo profesional: {e}")
            
            # 4. Redirigir a la página de Gracias
            return render(request, 'agency/thanks_gift.html', {
                'service': service,
                'nombre_cliente': nombre
            })

    return render(request, 'agency/service_landing.html', {'service': service})

# --- NUEVO: DASHBOARD DE LEADS PARA ANGELO ---
@login_required
def leads_dashboard(request):
    """Vista exclusiva para que Angelo vea los prospectos capturados."""
    # Seguridad: Solo staff (Angelo) puede entrar
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos de Capitán para ver esta zona.")
        return redirect('dashboard')
        
    leads = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'agency/leads_admin.html', {'leads': leads})


# 2. DASHBOARD Y PROGRESO DEL ALUMNO
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

@login_required
def course_detail(request, course_id):
    """Carga la lección actual y duda académica."""
    course = get_object_or_404(Course, id=course_id)
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        return redirect('checkout', course_id=course.id)

    lessons = Lesson.objects.filter(module__course=course).order_by('module__order', 'order')
    if not lessons.exists():
        messages.warning(request, f"El curso '{course.title}' aún no tiene lecciones.")
        return redirect('dashboard')

    lesson_id = request.GET.get('lesson')
    current_lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course) if lesson_id else lessons.first()

    if request.method == 'POST' and 'submit_query' in request.POST:
        question_text = request.POST.get('question')
        if question_text:
            CourseQuery.objects.create(
                user=request.user, course=course, lesson=current_lesson, question=question_text
            )
            messages.success(request, "¡Tu duda ha sido enviada!")
            return redirect(f"/course/{course.id}/?lesson={current_lesson.id}")

    mis_dudas = CourseQuery.objects.filter(user=request.user, lesson=current_lesson).order_by('-created_at')
    total = lessons.count()
    completas = LessonProgress.objects.filter(user=request.user, lesson__module__course=course, is_completed=True).count()
    progreso = int((completas / total) * 100) if total > 0 else 0

    return render(request, 'courses/course_detail.html', {
        'course': course, 'lessons': lessons, 'current_lesson': current_lesson,
        'progreso_curso': progreso, 'mis_dudas': mis_dudas,
    })

@login_required
def toggle_lesson_completion(request, lesson_id):
    """Marca lección como completada."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.is_completed = not progress.is_completed
    progress.save()
    return redirect(f"/course/{lesson.module.course.id}/?lesson={lesson.id}")

@login_required
def enroll_trial(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('dashboard')

@login_required
def checkout(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/checkout.html', {'course': course})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    if request.method == 'POST':
        score = 0
        review_data = []
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
        request.session['quiz_result'] = {
            'quiz_title': quiz.title, 'quiz_id': quiz.id,
            'percentage': round((score / questions.count()) * 100, 1) if questions.count() > 0 else 0,
            'course_id': quiz.module.course.id, 'review_data': review_data
        }
        return render(request, 'courses/quiz_result.html')
    return render(request, 'courses/quiz.html', {'quiz': quiz, 'questions': questions})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        if hasattr(request.user, 'rut'): request.user.rut = request.POST.get('rut')
        if hasattr(request.user, 'bio'): request.user.bio = request.POST.get('bio')
        if 'avatar' in request.FILES: request.user.profile_picture = request.FILES['avatar']
        request.user.save()
        messages.success(request, "Perfil actualizado.")
        return redirect('dashboard')
    return render(request, 'account/edit_profile.html')

@login_required
def check_certificate(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    total_lessons = course.total_lessons
    completadas = LessonProgress.objects.filter(user=request.user, lesson__module__course=course, is_completed=True).count()
    if total_lessons > 0 and completadas >= total_lessons:
        cert, _ = Certificate.objects.get_or_create(user=request.user, course=course)
        return redirect('generate_diploma_pdf', certificate_id=cert.id)
    messages.warning(request, "Aún no terminas el curso.")
    return redirect('dashboard')

@login_required
def generate_diploma_pdf(request, certificate_id):
    cert = get_object_or_404(Certificate, id=certificate_id, user=request.user)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)
    c.setStrokeColorRGB(0.1, 0.3, 0.8); c.setLineWidth(8); c.rect(1*cm, 1*cm, width-2*cm, height-2*cm)
    c.setFont("Helvetica-Bold", 45); c.drawCentredString(width/2, height - 5*cm, "DIPLOMA DE FINALIZACIÓN")
    nombre = f"{request.user.first_name} {request.user.last_name}".upper() if request.user.first_name else request.user.username.upper()
    c.setFont("Helvetica-Bold", 35); c.drawCentredString(width/2, height/2 + 0.5*cm, nombre)
    c.setFont("Helvetica-Bold", 22); c.drawCentredString(width/2, height/2 - 3.5*cm, cert.course.title.upper())
    c.save(); buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'Diploma_{cert.course.slug}.pdf')
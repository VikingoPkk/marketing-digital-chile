import io
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse, JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm

# Importación de IA
from marketing.servicios_ia import generar_respuesta_experto_ia

# API y REST Framework
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CursoSerializer, LessonSerializer 

# Modelos
from .models import Course, Certificate, LessonProgress, Lesson, Enrollment, Quiz, CourseQuery
from agency.models import Service, ContactMessage, Project, HomeSection, ClientLogo, UserTestimonial, HomeReel, Post
from agency.forms import TestimonialForm 

# ==========================================
# 1. VISTAS DE NAVEGACIÓN Y AGENCIA
# ==========================================

def home(request):
    secciones = HomeSection.objects.filter(is_active=True).order_by('order')
    reels = HomeReel.objects.filter(is_active=True)[:4]
    logos = ClientLogo.objects.all()
    testimonios = UserTestimonial.objects.filter(is_approved=True).order_by('-created_at')
    servicios = Service.objects.filter(is_active=True).order_by('order')[:3]
    proyectos = Project.objects.all().order_by('order')[:3]
    return render(request, 'home.html', {
        'secciones': secciones, 'reels': reels, 'logos': logos, 
        'testimonios': testimonios, 'servicios': servicios, 'proyectos': proyectos
    })

def contact_page(request): return render(request, 'contact.html')
def services_list(request):
    servicios_reales = Service.objects.filter(is_active=True).order_by('order')
    return render(request, 'servicios_academia.html', {'servicios': servicios_reales})
def projects_list(request):
    proyectos = Project.objects.all().order_by('order') 
    return render(request, 'agency/projects_list.html', {'proyectos': proyectos})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    if request.method == 'POST':
        nombre = request.POST.get('name'); email = request.POST.get('email'); mensaje = request.POST.get('message')
        if nombre and email:
            ContactMessage.objects.create(name=nombre, email=email, message=mensaje, servicio_interes=service, lead_source=f"Landing_{service.slug}")
            regalo_url = request.build_absolute_uri(service.regalo_pdf.url) if service.regalo_pdf else service.regalo_video_privado
            context = {'nombre': nombre, 'servicio': service, 'regalo_url': regalo_url}
            html_message = render_to_string('emails/welcome_lead.html', context)
            send_mail(f"🎁 Regalo de MD Chile: {service.title}!", strip_tags(html_message), settings.EMAIL_HOST_USER, [email], html_message=html_message)
            return render(request, 'agency/thanks_gift.html', {'service': service, 'nombre_cliente': nombre})
    return render(request, 'agency/service_landing.html', {'service': service})

@login_required
def leads_dashboard(request):
    if not request.user.is_staff: return redirect('dashboard')
    leads = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'agency/leads_admin.html', {'leads': leads})

# ==========================================
# 2. DASHBOARD Y PROGRESO DEL ALUMNO
# ==========================================

@login_required
def dashboard(request):
    inscripciones = Enrollment.objects.filter(user=request.user)
    cursos_inscritos = []
    for inscripcion in inscripciones:
        curso = inscripcion.course; total = curso.total_lessons
        completadas = LessonProgress.objects.filter(user=request.user, lesson__module__course=curso, is_completed=True).count()
        progreso = int((completadas / total) * 100) if total > 0 else 0
        cursos_inscritos.append({'curso': curso, 'progreso': progreso})
    otros_cursos = Course.objects.exclude(enrollment__user=request.user).filter(is_published=True)
    return render(request, 'dashboard.html', {'cursos_inscritos': cursos_inscritos, 'otros_cursos': otros_cursos, 'testimonial_form': TestimonialForm()})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        return redirect('checkout', course_id=course.id)
    lessons = Lesson.objects.filter(module__course=course).order_by('module__order', 'order')
    if not lessons.exists(): return redirect('dashboard')
    
    lesson_id = request.GET.get('lesson')
    current_lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course) if lesson_id else lessons.first()
    
    # PROCESAMIENTO DE PREGUNTA AL EXPERTO CON IA
    if request.method == 'POST' and 'submit_query' in request.POST:
        pregunta_txt = request.POST.get('question')
        
        # 1. Crear la duda
        nueva_duda = CourseQuery.objects.create(
            user=request.user, 
            course=course, 
            lesson=current_lesson, 
            question=pregunta_txt
        )
        
        # 2. Consultar Gemini Pro (A prueba de fallos)
        try:
            sugerencia = generar_respuesta_experto_ia(pregunta_txt, clase_contexto=current_lesson.title)
            nueva_duda.respuesta_ia = sugerencia
            nueva_duda.save()
        except:
            pass # Si la IA falla, la duda se guarda igual para el humano

        messages.success(request, "Tu duda ha sido enviada al experto.")
        return redirect(f"/course/{course.id}/?lesson={current_lesson.id}")

    completas = LessonProgress.objects.filter(user=request.user, lesson__module__course=course, is_completed=True).count()
    progreso = int((completas / lessons.count()) * 100) if lessons.count() > 0 else 0
    return render(request, 'courses/course_detail.html', {
        'course': course, 'lessons': lessons, 'current_lesson': current_lesson, 
        'progreso_curso': progreso, 
        'mis_dudas': CourseQuery.objects.filter(user=request.user, lesson=current_lesson)
    })

@login_required
def toggle_lesson_completion(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.is_completed = not progress.is_completed; progress.save()
    return redirect(f"/course/{lesson.module.course.id}/?lesson={lesson.id}")

@login_required
def enroll_trial(request, course_id):
    Enrollment.objects.get_or_create(user=request.user, course=get_object_or_404(Course, id=course_id))
    return redirect('dashboard')

@login_required
def checkout(request, course_id): return render(request, 'courses/checkout.html', {'course': get_object_or_404(Course, id=course_id)})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    course_id = quiz.module.course.id 

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
            'quiz_title': quiz.title, 
            'quiz_id': quiz.id, 
            'percentage': round((score / questions.count()) * 100, 1) if questions.count() > 0 else 0, 
            'course_id': course_id, 
            'review_data': review_data
        }
        return render(request, 'courses/quiz_result.html', {'course_id': course_id})
        
    return render(request, 'courses/quiz.html', {'quiz': quiz, 'questions': questions})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name'); request.user.save()
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
    messages.warning(request, "Aún no terminas todas las lecciones.")
    return redirect('dashboard')

@login_required
def generate_diploma_pdf(request, certificate_id):
    cert = get_object_or_404(Certificate, id=certificate_id, user=request.user)
    buffer = io.BytesIO(); c = canvas.Canvas(buffer, pagesize=landscape(A4)); width, height = landscape(A4)
    c.setStrokeColorRGB(0.1, 0.3, 0.8); c.rect(1*cm, 1*cm, width-2*cm, height-2*cm)
    c.setFont("Helvetica-Bold", 45); c.drawCentredString(width/2, height - 5*cm, "DIPLOMA DE FINALIZACIÓN")
    nombre = f"{request.user.first_name} {request.user.last_name}".upper() if request.user.first_name else request.user.username.upper()
    c.setFont("Helvetica-Bold", 35); c.drawCentredString(width/2, height/2, nombre)
    c.setFont("Helvetica-Bold", 22); c.drawCentredString(width/2, height/2 - 3.5*cm, cert.course.title.upper())
    c.save(); buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'Diploma_{cert.course.slug}.pdf')

# ==========================================
# 3. VISTAS DEL BLOG
# ==========================================
def blog_list(request): return render(request, 'agency/blog_list.html', {'posts': Post.objects.filter(is_published=True)})
def blog_detail(request, slug): return render(request, 'agency/blog_detail.html', {'post': get_object_or_404(Post, slug=slug, is_published=True)})
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id); post.likes_count += 1; post.save()
    return redirect('blog_detail', slug=post.slug)

def privacidad(request): return render(request, 'legal/privacidad.html')
def terminos(request): return render(request, 'legal/terminos.html')

# ==========================================
# 4. API ENDPOINTS
# ==========================================
class CursoListAPI(generics.ListAPIView):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = CursoSerializer

class LessonListAPI(generics.ListAPIView):
    serializer_class = LessonSerializer 
    def get_queryset(self): return Lesson.objects.filter(module__course_id=self.kwargs['course_id']).order_by('order')

class ToggleCompleteAPI(APIView):
    def post(self, request, lesson_id):
        from django.contrib.auth.models import User
        user = User.objects.first() 
        progress, _ = LessonProgress.objects.get_or_create(user=user, lesson=get_object_or_404(Lesson, id=lesson_id))
        progress.is_completed = not progress.is_completed; progress.save()
        return Response({"status": "ok", "is_completed": progress.is_completed})

class CreatePaymentPreference(APIView):
    def post(self, request, course_id):
        payment_url = "https://www.mercadopago.com.cl/checkout/v1/redirect?pref_id=TEST_MODE"
        return Response({"checkout_url": payment_url})

class MisCursosAPI(generics.ListAPIView):
    serializer_class = CursoSerializer
    def get_queryset(self):
        user = self.request.user 
        return Course.objects.filter(enrollment__user=user, is_published=True)

class TiendaCursosAPI(generics.ListAPIView):
    serializer_class = CursoSerializer
    def get_queryset(self):
        user = self.request.user
        return Course.objects.exclude(enrollment__user=user).filter(is_published=True)
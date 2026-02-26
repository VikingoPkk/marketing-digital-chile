from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Lesson, Enrollment, LessonProgress, Quiz

# 1. Dashboard Principal: Gestiona "Mis Cursos" con barra de progreso y "Explorar"
@login_required
def dashboard(request):
    inscripciones = Enrollment.objects.filter(user=request.user)
    inscritos_ids = inscripciones.values_list('course_id', flat=True)
    
    cursos_inscritos_data = []
    for enr in inscripciones:
        total = enr.course.total_lessons
        completadas = LessonProgress.objects.filter(
            user=request.user, 
            lesson__module__course=enr.course, 
            is_completed=True
        ).count()
        # Progreso real para la barra de colores del diseño profesional
        progreso = (completadas / total * 100) if total > 0 else 0
        cursos_inscritos_data.append({
            'curso': enr.course, 
            'progreso': int(progreso)
        })

    # Cursos que el usuario aún no tiene para la sección de abajo
    otros_cursos = Course.objects.filter(is_published=True).exclude(id__in=inscritos_ids)

    return render(request, 'dashboard.html', {
        'cursos_inscritos': cursos_inscritos_data,
        'otros_cursos': otros_cursos
    })

# 2. Vista de Detalles / Compra (Checkout)
@login_required
def checkout(request, course_id):
    curso = get_object_or_404(Course, id=course_id)
    # Si ya está inscrito, lo mandamos directo al contenido
    if Enrollment.objects.filter(user=request.user, course=curso).exists():
        return redirect('course_detail', course_id=curso.id)
    return render(request, 'checkout.html', {'curso': curso})

# 3. Proceso de Inscripción
@login_required
def enroll_trial(request, course_id):
    curso = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=curso)
    return redirect('course_detail', course_id=course_id)

# 4. Reproductor de Clases con Limpieza de URL de YouTube
@login_required
def course_detail(request, course_id):
    curso = get_object_or_404(Course, id=course_id)
    
    # Seguridad: Si no está inscrito, lo mandamos a checkout
    if not Enrollment.objects.filter(user=request.user, course=curso).exists():
        return redirect('checkout', course_id=course_id)

    modulos = curso.modules.all().prefetch_related('lessons')
    leccion_id = request.GET.get('leccion')
    leccion_actual = Lesson.objects.filter(id=leccion_id).first() if leccion_id else None
    
    if not leccion_actual and modulos.exists():
        leccion_actual = modulos.first().lessons.first()

    # --- LIMPIEZA AUTOMÁTICA DE URL PARA EVITAR BLOQUEOS DE YOUTUBE ---
    if leccion_actual and leccion_actual.video_url:
        url = leccion_actual.video_url
        video_id = ""
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("/")[-1].split("?")[0]
        elif "embed/" in url:
            video_id = url.split("embed/")[1].split("?")[0]
            
        if video_id:
            leccion_actual.video_url = f"https://www.youtube.com/embed/{video_id}?rel=0"

    progreso_ids = list(LessonProgress.objects.filter(
        user=request.user, 
        lesson__module__course=curso, 
        is_completed=True
    ).values_list('lesson_id', flat=True))

    leccion_completada = False
    if leccion_actual:
        leccion_completada = leccion_actual.id in progreso_ids

    return render(request, 'course_detail.html', {
        'curso': curso, 
        'modulos': modulos, 
        'leccion_actual': leccion_actual,
        'leccion_completada': leccion_completada,
        'lecciones_completadas_ids': progreso_ids
    })

# 5. Marcar lección como completada (Botón de progreso)
@login_required
def toggle_lesson_completion(request, lesson_id):
    leccion = get_object_or_404(Lesson, id=lesson_id)
    prog, created = LessonProgress.objects.get_or_create(user=request.user, lesson=leccion)
    prog.is_completed = not prog.is_completed if not created else True
    prog.save()
    return redirect(f"/course/{leccion.module.course.id}/?leccion={leccion.id}")

# 6. Lógica de Exámenes (Take Quiz)
@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == "POST":
        puntos = 0
        total_preguntas = quiz.questions.count()
        
        for question in quiz.questions.all():
            respuesta_usuario = request.POST.get(f"question_{question.id}")
            if respuesta_usuario and int(respuesta_usuario) == question.correct_option:
                puntos += 1
        
        return render(request, 'quiz_result.html', {
            'quiz': quiz,
            'puntos': puntos,
            'total': total_preguntas
        })
        
    return render(request, 'quiz_form.html', {'quiz': quiz})

# 7. NUEVA: Editar Perfil (Vinculado a tu modelo de usuario con RUT y Bio)
@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        # Obtenemos los datos del formulario
        avatar = request.FILES.get('avatar')
        nombre = request.POST.get('first_name')
        biografia = request.POST.get('bio')
        rut_cl = request.POST.get('rut')

        # Guardamos directamente en el objeto User personalizado
        user.first_name = nombre
        user.bio = biografia
        user.rut = rut_cl
        
        if avatar:
            user.profile_picture = avatar
        
        user.save()
        messages.success(request, "¡Tu perfil de MD Chile ha sido actualizado!")
        return redirect('dashboard')
    
    return render(request, 'profile_edit.html', {'user': user})

# 8. Landing Page
def home(request):
    return render(request, 'home.html', {'cursos': Course.objects.filter(is_published=True)[:3]})
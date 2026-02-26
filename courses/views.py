from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Lesson, Enrollment

# 1. Vista de la página de inicio (Landing Page)
def home(request):
    # Traemos solo los primeros 3 cursos que estén marcados como publicados
    cursos_destacados = Course.objects.filter(is_published=True)[:3]
    return render(request, 'home.html', {
        'cursos': cursos_destacados
    })

# 2. Vista del Panel del Alumno (Dashboard)
@login_required
def dashboard(request):
    # Traemos todos los cursos publicados
    todos_los_cursos = Course.objects.filter(is_published=True)
    
    # Obtenemos los IDs de los cursos donde el alumno ya está matriculado
    mis_matriculas_ids = Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True)
    
    return render(request, 'dashboard.html', {
        'cursos': todos_los_cursos,
        'mis_matriculas_ids': mis_matriculas_ids
    })

# 3. Vista del detalle del curso y reproductor de video (CON SEGURIDAD)
@login_required
def course_detail(request, course_id):
    # Buscamos el curso o devolvemos error 404
    curso = get_object_or_404(Course, id=course_id)
    
    # --- FILTRO DE SEGURIDAD ---
    # Verificamos si existe una matrícula para este usuario y este curso
    esta_matriculado = Enrollment.objects.filter(user=request.user, course=curso).exists()
    
    if not esta_matriculado:
        # Si no ha pagado/matriculado, mensaje de alerta y fuera
        messages.warning(request, f"No tienes acceso a {curso.title}. ¡Inscríbete para comenzar a aprender!")
        return redirect('dashboard')
    # ---------------------------

    # Si pasa la seguridad, cargamos el contenido
    modulos = curso.modules.all().prefetch_related('lessons')
    
    leccion_id = request.GET.get('leccion')
    leccion_actual = None
    
    if leccion_id:
        leccion_actual = get_object_or_404(Lesson, id=leccion_id)
    elif modulos.exists():
        primer_modulo = modulos.first()
        if primer_modulo.lessons.exists():
            leccion_actual = primer_modulo.lessons.first()

    return render(request, 'course_detail.html', {
        'curso': curso,
        'modulos': modulos,
        'leccion_actual': leccion_actual
    })

# 4. Vista de Checkout (Resumen de Compra)
@login_required
def checkout(request, course_id):
    curso = get_object_or_404(Course, id=course_id)
    
    # Si ya tiene el curso, lo mandamos directo a estudiar
    if Enrollment.objects.filter(user=request.user, course=curso).exists():
        return redirect('course_detail', course_id=curso.id)
        
    return render(request, 'checkout.html', {'curso': curso})

# 5. Simulación de Pago Exitoso (Matrícula automática)
@login_required
def enroll_trial(request, course_id):
    curso = get_object_or_404(Course, id=course_id)
    
    # Creamos la matrícula (o la obtenemos si ya existe para evitar duplicados)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=curso
    )
    
    if created:
        messages.success(request, f"¡Felicidades! Te has inscrito exitosamente en {curso.title}.")
    
    return redirect('course_detail', course_id=curso.id)
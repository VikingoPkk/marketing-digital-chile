from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment

def academia_publica(request):
    """Listado de cursos bloqueados"""
    cursos = Course.objects.filter(is_published=True)
    return render(request, 'courses/academia_publica.html', {'cursos': cursos})

def curso_detalle_publico(request, slug):
    """Landing de pre-venta estilo Platzi"""
    course = get_object_or_404(Course, slug=slug)
    # Si ya tiene acceso, lo mandamos al real
    if request.user.is_authenticated:
        if Enrollment.objects.filter(user=request.user, course=course).exists():
            return redirect('course_detail', course_id=course.id)
    return render(request, 'courses/curso_detalle_publico.html', {'course': course})
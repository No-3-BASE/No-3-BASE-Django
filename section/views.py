from django.shortcuts import render, get_object_or_404
from board.models import Section

def section_view(request, section_id):
    detail = get_object_or_404(Section, id=section_id)

    return render(request, 'section/section.html', {'detail': detail})

from models import Magazine
def show_magazine(request):
  return {
      'magazine':Magazine.objects.filter(index=True).order_by('-date_added'),
  }

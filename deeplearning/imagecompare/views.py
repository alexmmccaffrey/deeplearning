from rest_framework.views import APIView
from django.shortcuts import render, redirect
from .forms import ImageForm

class ImageView(APIView):
    def upload(request):
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('upload')
        else:
            form = ImageForm()
        return render(request, 'imagecompare/upload.html', {
            'form': form
        })
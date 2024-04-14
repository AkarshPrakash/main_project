# views.py
from django.shortcuts import render
from .forms import ImageUploadForm
from .predict import predict_image
'''
def predict(request):
    prediction = None
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            image_path = instance.image.path
            class_names = ['adenocarcinoma', 'large.cell.carcinoma', 'normal/invalid input', 'squamous.cell.carcinoma']
            prediction = predict_image(image_path, class_names)
    else:
        form = ImageUploadForm()
    
    return render(request, 'predict.html', {'form': form, 'prediction': prediction})
'''
def predict(request):
    prediction = None
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            image_url = instance.image.url  # Get the URL of the uploaded image
            class_names = ['adenocarcinoma', 'large.cell.carcinoma', 'normal', 'squamous.cell.carcinoma']
            prediction = predict_image(image_url, class_names)
    else:
        form = ImageUploadForm()
    
    return render(request, 'predict.html', {'form': form, 'prediction': prediction})

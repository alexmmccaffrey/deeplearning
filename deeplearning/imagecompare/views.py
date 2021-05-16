from rest_framework.views import APIView
from django.shortcuts import render, redirect
from .forms import ImageForm

# PYTORCH GARBAGE
from torchvision import models
import torch
from torchvision import transforms
from PIL import Image
import torch.nn.functional



class MLModelCheck:

    def image_transformation(image_path):
        transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )])
        image = Image.open(image_path)
        image_transform = transform(image)
        image_batch = torch.unsqueeze(image_transform, 0)
        return image_batch

    def image_evaluate(image_batch):
        alexnet = models.alexnet(pretrained=True)
        alexnet.eval()
        output = alexnet(image_batch)
        return output

    def image_classification(image_evaluation):
        with open('image_classifcation_names.txt') as classifications:
            classes = [i.strip() for i in classifications.readlines()]
        sorted, indices = torch.sort(image_evaluation, descending=True)
        percentage = torch.nn.functional.softmax(image_evaluation, dim=1)[0] * 100.0
        results = [(classes[i], percentage[i].item) for i in indices[0][:5]]
        print("Top 5 classifications:")
        for i in range(5):
            print('{}: {:.4f}%'.format(results[i][0], results[i][1]))


class ImageView(APIView):
    def upload(request):
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                transformed_image = MLModelCheck.image_transformation(form.instance.image.path)
                image_evaluation = MLModelCheck.image_evaluate(transformed_image)
                image_classifications = MLModelCheck.image_classification(image_evaluation)
                return redirect('upload')
        else:
            form = ImageForm()
        return render(request, 'imagecompare/upload.html', {
            'form': form
        })
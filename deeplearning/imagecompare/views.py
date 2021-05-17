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
        results = [(classes[i], percentage[i].item()) for i in indices[0][:5]]
        image_classification = results[0][0]
        return image_classification

    def cat_check(image_classification):
        th_list = ["tabby, tabby cat", "tiger cat", "Persian cat", "Siamese cat, Siamese", "Egyptian cat", "cougar, puma, catamount, mountain lion, painter, panther, Felis concolor", "lynx, catamount", "leopard, Panthera pardus", "snow leopard, ounce, Panthera uncia", "jaguar, panther, Panthera onca, Felis onca", "lion, king of beasts, Panthera leo", "tiger, Panthera tigris", "cheetah, chetah, Acinonyx jubatus"]
        for i in th_list:
            if i == image_classification:
                return True
        return False

# "tabby, tabby cat" or "tiger cat" or "Persian cat" or "Siamese cat, Siamese" or "Egyptian cat" or "cougar, puma, catamount, mountain lion, painter, panther, Felis concolor" or "lynx, catamount" or "leopard, Panthera pardus" or "snow leopard, ounce, Panthera uncia" or "jaguar, panther, Panthera onca, Felis onca" or "lion, king of beasts, Panthera leo" or "tiger, Panthera tigris" or "cheetah, chetah, Acinonyx jubatus":

class ImageView(APIView):
    def upload(request):
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                transformed_image = MLModelCheck.image_transformation(form.instance.image.path)
                image_evaluation = MLModelCheck.image_evaluate(transformed_image)
                image_classification = MLModelCheck.image_classification(image_evaluation)
                cat_check = MLModelCheck.cat_check(image_classification)
                return render(request, 'imagecompare/upload.html', {
                    'cat_check': cat_check,
                    'form': form
                })
        else:
            form = ImageForm()
        return render(request, 'imagecompare/upload.html', {
            'form': form
        })
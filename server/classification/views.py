from .serializers import ClassificationImageSerializer
from .models import ClassificationImage
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import pickle
import os
import torch
from torchvision import models, transforms, datasets
import torch.nn as nn
import torch
import torchvision
import glob as glob
from torch.autograd import Variable
from PIL import Image

def predict_image(model, image):
    with torch.no_grad():
        test_transforms = transforms.Compose([
            transforms.Resize((150, 150)),
            transforms.ToTensor(),
            transforms.Normalize([0.5,0.5,0.5], [0.5,0.5,0.5])
        ])
        image_tensor = test_transforms(image).float()
        image_tensor = image_tensor.unsqueeze_(0)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")    
        input = image_tensor.to(device)
        output = model.forward(input)
        return output.argmax().item()

class ClassificationView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    # def get(self, request, *args, **kwargs):
    #     posts = ClassificationImage.objects.all()
    #     serializer = ClassificationImageSerializer(posts, many=True)
    #     return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        posts_serializer = ClassificationImageSerializer(data=request.data)
        if posts_serializer.is_valid():
            instance = posts_serializer.save()
            classes_decoder = {}
            model_dir = os.path.join(os.pardir, 'model')
            with open(os.path.join(model_dir, 'classesDecoder.pkl'), 'rb') as decoder:
                classes_decoder = pickle.load(decoder)
            model = models.resnet50()
            model.fc = nn.Linear(in_features=2048, out_features=120, bias=True)
            checkpoint = torch.load(os.path.join(model_dir, 'model.pth'))
            try:
                checkpoint.eval()
            except AttributeError as error:
                print(error)
            ### 'dict' object has no attribute 'eval'
            model.load_state_dict(checkpoint)
            ### now you can evaluate it
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)
            for infile in glob.glob("./media/post_images/*"):
                im = Image.open(infile)
                print(infile)
                print(classes_decoder[predict_image(model, im)])
            instance.delete()
            return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# predict.py
import os
import torch
from torchvision import transforms as transform
from PIL import Image
import torchvision.models as models
from efficientnet_pytorch import EfficientNet
import torch.nn as nn
import requests
from io import BytesIO
import boto3

class Efficient(nn.Module):
    def __init__(self, num_classes=1):
        super(Efficient, self).__init__()
        self.model = EfficientNet.from_pretrained("efficientnet-b3")
        self.pool = nn.AdaptiveAvgPool2d((1,1))
        self.fc = nn.Linear(1536, 256)
        
        self.reg_model = nn.Sequential(
            nn.BatchNorm1d(256),
            nn.Linear(256, 500),
            nn.BatchNorm1d(500),
            nn.Tanh(),
            nn.Dropout(0.2),
            nn.Linear(500, 100),
            nn.BatchNorm1d(100),
            nn.Tanh(),
            nn.Dropout(0.2),
            nn.Linear(100, num_classes),
        )
        
    def forward(self, x):
        x = self.model.extract_features(x)
        x = self.pool(x)
        x = x.view(-1, 1536)
        x = self.fc(x)
        x = self.reg_model(x)
        return x

def predict_image(image_url, class_names):
    app_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(app_dir, 'models', 'EfficientNet_CT_Scans.pth.tar')

    model = Efficient(num_classes=len(class_names))
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content)).convert('RGB')
    preprocess = transform.Compose([transform.Resize(size=(224, 224)),
                                    transform.ToTensor(),
                                    transform.Normalize(mean=[0.485, 0.456, 0.406],
                                                         std=[0.229, 0.224, 0.225])])
    img_tensor = preprocess(img)
    img_tensor = img_tensor.unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_tensor)
        _, predicted = torch.max(outputs, 1)
        predicted_class = class_names[predicted.item()]

    return predicted_class
'''
import requests
from io import BytesIO
import boto3

def predict_image(image_url, class_names):
    # Initialize S3 client
    s3 = boto3.client('s3')

    # S3 bucket and model path
    bucket_name = 'ehrstorage'
    model_key = 'models/EfficientNet_CT_Scans.pth.tar'  # Adjust this according to your S3 folder structure

    # Download model file from S3
    model_object = s3.get_object(Bucket=bucket_name, Key=model_key)
    model_bytes = model_object['Body'].read()

    # Load model
    model = Efficient(num_classes=len(class_names))
    model.load_state_dict(torch.load(BytesIO(model_bytes), map_location=torch.device('cpu')))
    model.eval()

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content)).convert('RGB')
    preprocess = transform.Compose([
        transform.Resize(size=(224, 224)),
        transform.ToTensor(),
        transform.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    img_tensor = preprocess(img)
    img_tensor = img_tensor.unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_tensor)
        _, predicted = torch.max(outputs, 1)
        predicted_class = class_names[predicted.item()]

    return predicted_class
'''

from django.shortcuts import render
import requests

from material import GetMaterialBase
# Create your views here.

def load_material_from_url():
    mtl = GetMaterialBase("https://www.homedepot.com/p/Nashua-Tape-1-89-in-x-30-yd-Dryer-Vent-Installation-Duct-Tape-1529836/207203955")
    print("pause")


if __name__ == "__main__":
    load_material_from_url()
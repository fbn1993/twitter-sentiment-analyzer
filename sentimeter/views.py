from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import base64
import urllib
from .forms import userinput
import matplotlib.pyplot as plt
import io
from .sentimeter import primary, secondary


def index(request):
    user_input = userinput()
    return render(request, "index.html", {'input_hastag': user_input})

def analyse(request):
    user_input = userinput(request.GET or None)
    if request.GET and user_input.is_valid():
        input_hastag = user_input.cleaned_data['q']
        data = primary(input_hastag)
        return render(request, "analyse.html", {'data': data})
    return render(request, "index.html", {'input_hastag': user_input})

def polarity(request):
    user_input = userinput(request.GET or None)
    if request.GET and user_input.is_valid():
        input_hastag = user_input.cleaned_data['q']
        sentiment_df = secondary(input_hastag)
        fig, ax = plt.subplots(figsize=(8, 6))

        # Plot histogram of the polarity values
        sentiment_df.hist(bins=[-1, -0.75, -0.5, -0.25, 0.25, 0.5, 0.75, 1],
                ax=ax,
                color="blue")

        plt.title("Sentiments from Tweets on searched hashtag")
        buf = io.BytesIO()
        fig.savefig(buf,format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        return render(request, "polarity.html", {'data': uri})
    return render(request, "index.html", {'input_hastag': user_input})


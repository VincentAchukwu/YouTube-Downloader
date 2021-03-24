from flask import Flask, render_template, url_for, request, redirect, send_file
from pytube import YouTube
import os, datetime

app = Flask(__name__)

# initiating global string for download path
vidDownload = ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["GET", "POST"])
def result():

    if request.method == "POST":
        vidURL = request.form.get("videoURL")
        try:
            # (attempt to save memory)
            # delete any previously requested videos before receiving another one 
            # os.chdir("./downloads")
            # currDir = "./"
            # listDir = os.listdir(currDir)
            # for file in listDir:
            #     if file.endswith(".mp4"):
            #         os.remove(file)

            # obtain video data
            ytd = YouTube(vidURL)
            vidTitle = ytd.title
            vidViews =  ytd.views
            vidLength = str(datetime.timedelta(seconds=ytd.length))
            vidRating = str("{:.1f}".format(ytd.rating))
            vidThumb = ytd.thumbnail_url
            # then using global variable for later use in /download route
            global vidDownload
            vidDownload = ytd.streams.get_highest_resolution().download()
            
            # then go back to root dir
            # os.chdir("../")

            return render_template("result.html", msg=[vidTitle, vidViews, vidLength, vidRating, vidThumb, vidDownload])

        except Exception as e:
            print("Invalid Video URL {}".format(e))
            return render_template("index.html", msg="Invalid URL")


    # return render_template("index.html", msg="Invalid URL")

# download the video via send_file and using global path (vidDownload)
@app.route("/download")
def download_file():
    global vidDownload
    return send_file(vidDownload, as_attachment=True)

@app.route("/contactus", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        query = request.form.get("userContent")
        if query:
            return render_template("contactus.html", msg="Thank you, your response has been recorded.")
        else:
            redirect("/contactus")

    return render_template("contactus.html")



if __name__ == '__main__':
    app.run(debug=True)
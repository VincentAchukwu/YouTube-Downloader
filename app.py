from flask import Flask, render_template, url_for, request, redirect, send_file
from pytube import YouTube
import os, datetime

app = Flask(__name__)

# yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution")[-1].download()

# initiating global string for download path
fileDownload = ""

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
            global fileDownload

            # testing how to download mp3/mp4 files (Pytube doesn't seem to support mp3)
            # if request.form["options"] == "mp3":
            #     print("mp3 pressed")
            #     fileType = "mp3"
            #     fileDownload = ytd.streams.get_by_itag(251).download()
            # if request.form["options"] == "mp4":
            #     print("mp4 pressed")
            #     fileType = "mp4"
            #     fileDownload = ytd.streams.get_highest_resolution().download()

            # but for now, we're just downloading via mp4
            fileDownload = ytd.streams.get_highest_resolution().download()
            # then go back to root dir
            # os.chdir("../")

            return render_template("result.html", msg=[vidTitle, vidViews, vidLength, vidRating, vidThumb, fileDownload])

        except Exception as e:
            print("Invalid Video URL {}".format(e))
            return render_template("index.html", msg="Invalid URL")


    # return render_template("index.html", msg="Invalid URL")

# download the video via send_file and using global path (fileDownload)
@app.route("/download")
def download_file():
    global fileDownload
    return send_file(fileDownload, as_attachment=True)

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
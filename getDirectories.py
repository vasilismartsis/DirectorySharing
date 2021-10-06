from flask import Flask, redirect, url_for, render_template, request, jsonify, make_response, Blueprint, send_from_directory, session
import os
from PIL import Image
from moviepy.editor import *
import atexit
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

thumbnailPath = "thumbnails"
quality = 1.5
scheduler = BackgroundScheduler()


def getDirectories(content="", status=""):
    scheduler.remove_all_jobs()

    allLists = {}
    directoryList = []
    fileList = []

    previousName = ""
    if "username" in session and session["username"] == "vasilismartsis":
        previousPath = "E:/Photos"
    else:
        previousPath = "E:/Photos/Κοινοποιημένες Φωτογραφίες"

    if request.args.get('previousName') != None:
        previousName = request.args.get('previousName')
    if request.args.get('previousPath') != None:
        previousPath = request.args.get('previousPath')

    path = previousPath + "/" + previousName

    directories = os.listdir(path)
    for file in directories:
        if not file.startswith('.') and file != "desktop.ini" and os.path.isdir(os.path.join(path, file)):
            directoryList.append(file)
        elif not os.path.isdir(os.path.join(path, file)) and file != "desktop.ini":
            if file.lower().endswith('jpg') or file.lower().endswith('jpeg'):
                createThumbnailImage(path, file)
                fileList.append(file)
            elif file.lower().endswith('vob') or file.lower().endswith('mp4') or file.lower().endswith('avi'):
                createThumbnailVideo(path, file)
                fileList.append(file)

    allLists["directoryList"] = directoryList
    allLists["fileList"] = fileList

    if not scheduler.get_job('startDeletingAgain'):
        scheduler.add_job(deleteThumbnailFiles, trigger='interval',
                          hours=1, id="startDeletingAgain")

    if "username" in session:
        return render_template("index.html", allLists=allLists, newPath=path, thumbnailPath=thumbnailPath, content=content, status=status)
    else:
        return render_template("index.html")


def createThumbnailImage(path, file):
    print(path)
    print(file)
    image = Image.open(path + "/" + file)
    MAX_SIZE = (quality * 100, quality * 100)
    image.thumbnail(MAX_SIZE)
    image.save(thumbnailPath + "/" + file)


def createThumbnailVideo(path, file):
    if not os.path.exists(thumbnailPath + os.path.splitext(file)[0] + ".gif"):
        clip = VideoFileClip(path + "/" + file)
        if clip.duration > 5:
            clip = clip.subclip(0, 5)
        else:
            clip = clip.subclip()
        clip = clip.resize(quality/10)
        clip.write_gif(
            thumbnailPath + "/" + os.path.splitext(file)[0] + ".gif", fps=3)


def deleteThumbnailFiles():
    directory = os.listdir(thumbnailPath)
    for file in directory:
        timeFormat = "%H:%M:%S"
        nowTime = datetime.now().strftime(timeFormat)
        lastModifiedTime = datetime.fromtimestamp(
            os.path.getmtime(thumbnailPath + file)).strftime(timeFormat)
        timeDifference = datetime.strptime(
            nowTime, timeFormat) - datetime.strptime(lastModifiedTime, timeFormat)
        if datetime.strptime(str(timeDifference), timeFormat) > datetime.strptime("1:00:00", timeFormat):
            os.remove(thumbnailPath + file)


def startDeletingAgain():
    if not scheduler.get_job('deleteThumbnailFiles'):
        scheduler.add_job(deleteThumbnailFiles, trigger='interval',
                          hours=1, id="deleteThumbnailFiles")


startDeletingAgain()

scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

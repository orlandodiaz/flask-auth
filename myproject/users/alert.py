from flask import flash

def error(msg):
    flash(msg, category="danger")

def info(msg):
    flash(msg, category="info")
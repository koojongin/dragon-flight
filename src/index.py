import asyncio
import sys

import pygame

from src.application import Application


def run_application():
    app = Application("Dragon Flight", (384, 700))
    app.run()

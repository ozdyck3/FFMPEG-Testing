#!/usr/bin/env python
from __future__ import unicode_literals, print_function
import argparse
import ffmpeg
import sys
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import pygame

probe = ffmpeg.probe("testvideo.mp4")
video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

WINDOW_SURFACE = pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE

width = int(video_stream['width'])
height = int(video_stream['height'])
num_frames = int(video_stream['nb_frames'])
print('width: {}'.format(width))
print('height: {}'.format(height))
print('num_frames: {}'.format(num_frames))

pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((1280,720), WINDOW_SURFACE)

process = (
    ffmpeg
    .input("testvideo.mp4")
    .output('pipe:', format="rawvideo", pix_fmt="rgb24")
    .run_async(pipe_stdout=True)
)




while True:
    clock = pygame.time.Clock()
    in_bytes = process.stdout.read(width*height*3)
    if not in_bytes:
        break
    in_frame = (
        np
        .frombuffer(in_bytes, np.uint8)
        .reshape([1280,720,3])
    )

    frame = pygame.image.frombuffer(in_frame, (1280, 720), 'RGB')
    window.blit(frame, (0,0))
    pygame.display.flip()
    clock.tick_busy_loop(25)

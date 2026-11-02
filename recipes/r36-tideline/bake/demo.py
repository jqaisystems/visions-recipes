"""A demo clip so the recipe runs out of the box: two minutes of drifting colour at the film's source size, with a
tone whose loudness rises and falls, so the strip, the strongest minute and every time effect have something to show.
Writes assets/demo/demo.mp4 and assets/demo/demo.wav (not committed). Use your own clip instead for the real thing.
Usage: python bake/demo.py"""
import os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "demo")
os.makedirs(OUT, exist_ok=True)
DUR, W, H = 120, 1608, 1080
run = lambda *a: subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
# colour that drifts and turns, with bands of light rolling down it like waves
run("-f", "lavfi", "-i", f"gradients=s={W}x{H}:r=30:d={DUR}:speed=0.012:type=radial:c0=0x0A1418:c1=0xff8a6a:c2=0x3fd6c0:c3=0xf6c27a:x0=200:y0=180:x1=1400:y1=900",
    "-vf", "geq=r='r(X,Y)*(0.82+0.18*sin(Y/38-T*2.2))':g='g(X,Y)*(0.82+0.18*sin(Y/38-T*2.2))':b='b(X,Y)*(0.82+0.18*sin(Y/38-T*2.2))',format=yuv420p",
    "-c:v", "libx264", "-crf", "20", "-preset", "fast", os.path.join(OUT, "demo.mp4"))
# a soft chord whose loudness swells, loudest a little after the first minute
run("-f", "lavfi", "-i", f"aevalsrc='(0.12*sin(2*PI*220*t)+0.08*sin(2*PI*277.2*t)+0.06*sin(2*PI*329.6*t))*(0.35+0.65*exp(-pow((t-80)/28,2)))*(0.8+0.2*sin(2*PI*t/2.5))':s=48000:d={DUR}",
    os.path.join(OUT, "demo.wav"))
print("demo clip:", os.path.join(OUT, "demo.mp4"))

Manim install
sudo apt update && sudo apt install -y \
  libcairo2-dev \
  libpango1.0-dev \
  pkg-config \
  python3-dev \
  ffmpeg \
  texlive-latex-base \
  texlive-fonts-recommended \
  texlive-latex-extra \
  cm-super


then

pip install manim

for render of the project

manim -pql "projects/Symmetry/scene 3.py" Transformations

Use -pqh for 1080p.

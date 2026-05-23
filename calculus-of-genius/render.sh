#!/usr/bin/env bash
set -euo pipefail

QUALITY="${QUALITY:-qh}"
FPS="${FPS:-60}"

manim "-${QUALITY}" --fps "$FPS" scenes/scene_00_title.py TitleScene
manim "-${QUALITY}" --fps "$FPS" scenes/scene_01_hook.py HookScene
manim "-${QUALITY}" --fps "$FPS" scenes/scene_02_probability.py ProbabilityScene
manim "-${QUALITY}" --fps "$FPS" scenes/scene_03_zipf.py ZipfScene
manim "-${QUALITY}" --fps "$FPS" scenes/scene_04_combinatorial.py CombinatorialScene
manim "-${QUALITY}" --fps "$FPS" scenes/scene_05_compound_time.py CompoundTimeScene
manim "-${QUALITY}" --fps "$FPS" scenes/scene_06_edge_of_chaos.py EdgeOfChaosScene
manim "-${QUALITY}" --fps "$FPS" scenes/scene_07_diminishing_returns.py DiminishingReturnsScene
manim "-${QUALITY}" --fps "$FPS" scenes/scene_08_final_formula.py FinalFormulaScene


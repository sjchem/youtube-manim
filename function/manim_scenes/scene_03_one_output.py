"""Scene 03: isolate a split, then contrast it with a shared output."""
from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import begin_scene, clear_background, end_scene


class Scene03OneOutput(Scene):
    def construct(self) -> None:
        play_scene(self)


def _text(words, size=32, color=cfg.WHITE):
    return Text(words, font='DejaVu Sans', font_size=size, color=color, weight=MEDIUM)


def _value(value, x, y, color):
    return MathTex(value, font_size=72, color=color).move_to([x, y, 0])


def _link(source, target, color=cfg.RULE_COLOR):
    return Arrow(source.get_right() + RIGHT*.24, target.get_left() + LEFT*.24,
                 color=color, buff=0, stroke_width=2.4, tip_length=.18,
                 max_tip_length_to_length_ratio=.06)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, '03')
    # A quiet, flat field keeps the relation itself in focus. Remove the reused
    # bubble/grid background when this chapter runs inside FullVideo as well.
    clear_background(scene)

    def until(seconds):
        remaining = seconds - (float(scene.time) - started)
        if remaining < -.14:
            raise ValueError(f'Scene 03 cue {seconds}s overrun by {-remaining:.3f}s')
        if remaining > 1e-6:
            scene.wait(remaining)

    def checkpoint(name):
        callback = getattr(scene, '_scene03_review', None)
        if callback:
            callback(scene, name, float(scene.time) - started)

    title = _text('One input. One answer.', 42).move_to([0, 3.15, 0])
    headings = VGroup(_text('INPUT', 24, cfg.INPUT_COLOR).move_to([-3.5, 2.15, 0]),
                      _text('OUTPUT', 24, cfg.OUTPUT_COLOR).move_to([3.5, 2.15, 0]))
    scene.play(FadeIn(title), FadeIn(headings), run_time=1)

    # 0–20: equal rows make every pairing easy to scan; no enclosing ovals.
    rows = []
    for inp, out, y in [('1', '2', 1.15), ('2', '4', -.25), ('3', '6', -1.65)]:
        left = _value(inp, -3.5, y, cfg.INPUT_COLOR)
        right = _value(out, 3.5, y, cfg.OUTPUT_COLOR)
        arrow = _link(left, right)
        rows.append((left, arrow, right))
    for row, cue in zip(rows, [6, 11, 16]):
        left, arrow, right = row
        scene.play(FadeIn(left), run_time=.4)
        scene.play(GrowArrow(arrow), FadeIn(right), run_time=.8)
        until(cue)
    verdict = _text('A function', 30, cfg.GREEN).move_to([0, -2.95, 0])
    scene.play(FadeIn(verdict), run_time=.6)
    checkpoint('01_aligned_pairs')
    until(20)

    # 20–24: remove unrelated examples before introducing the conflict.
    two, four_arrow, four = rows[1]
    focus_title = _text('What if one input gives two answers?', 38).move_to(title)
    scene.play(FadeOut(*rows[0], *rows[2], verdict),
               ReplacementTransform(title, focus_title), run_time=1)
    title = focus_title
    two_target, four_target = two.copy().set_y(0), four.copy().set_y(0)
    scene.play(two.animate.set_y(0), four.animate.set_y(0),
               Transform(four_arrow, _link(two_target, four_target)), run_time=1)
    until(24)

    # 24–32: a single, spacious fork. There are no other arrows to cross.
    upper = four.copy().set_y(.95)
    scene.play(four.animate.set_y(.95),
               Transform(four_arrow, _link(two, upper)), run_time=.8)
    seven = _value('7', 3.5, -.95, cfg.OUTPUT_COLOR)
    seven_arrow = _link(two, seven, cfg.RED)
    scene.play(GrowArrow(seven_arrow), FadeIn(seven), run_time=1.2)
    scene.play(four_arrow.animate.set_color(cfg.RED), run_time=.6)
    until(29)
    verdict = _text('Not a function', 30, cfg.RED).move_to([0, -2.75, 0])
    scene.play(FadeIn(verdict), run_time=.6)
    checkpoint('02_isolated_split')
    until(36)

    # 36–45: keep one statement beneath the diagram, rather than stacking
    # a question, a warning, a cross, and a second caption in the same space.
    definition = _text('Each allowed input must determine exactly one output.', 27)
    definition.move_to([0, -2.75, 0])
    scene.play(FadeOut(verdict), FadeIn(definition), run_time=.8)
    until(45)

    # 45–66: reverse the visual pattern, not the rule. Squaring is a new
    # example: -2 and 2 independently reach 4. Neither input branches.
    shared_title = _text('Two inputs. One answer.', 42).move_to(title)
    square_tag = MathTex(r'x\mapsto x^2', font_size=32, color=cfg.MUTED).move_to([0, 1.85, 0])
    scene.play(FadeOut(seven_arrow, seven, four_arrow, definition),
               ReplacementTransform(title, shared_title),
               two.animate.set_y(-.95), four.animate.set_y(0),
               FadeIn(square_tag), run_time=1)
    title = shared_title
    negative = _value('-2', -3.5, .95, cfg.INPUT_COLOR)
    negative_arrow = _link(negative, four)
    positive_arrow = _link(two, four)
    scene.play(FadeIn(negative), GrowArrow(negative_arrow), run_time=1)
    until(53)
    scene.play(GrowArrow(positive_arrow), run_time=1)
    until(60)
    verdict = _text('Still a function', 30, cfg.GREEN).move_to([0, -2.75, 0])
    scene.play(FadeIn(verdict), run_time=.6)
    checkpoint('03_shared_output')
    until(70)

    # 70–88: leave the viewer with one precise promise and a quiet handoff.
    scene.play(FadeOut(title, headings, two, four, negative, negative_arrow,
                       positive_arrow, square_tag, verdict), run_time=1)
    promise = _text('Each allowed input determines\nexactly one output.', 42)
    promise.move_to([0, .4, 0])
    scene.play(FadeIn(promise, shift=UP*.12), run_time=1)
    until(81)
    next_question = _text('Which inputs are allowed?', 28, cfg.MUTED).move_to([0, -2.1, 0])
    scene.play(FadeIn(next_question), run_time=.6)
    checkpoint('04_promise')
    until(87.3)
    end_scene(scene, started, cfg.SCENE_DURATIONS['03'])

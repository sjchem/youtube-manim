from __future__ import annotations

from manim import *

from utils.style import BLUE_GLOW, GOLD_GLOW, GREEN_GLOW, PURPLE_GLOW, RED_GLOW, TEXT_COLOR


def probability_success_equation(font_size: int = 42) -> MathTex:
    return MathTex(
        r"P(\mathrm{breakthrough}) = 1 - (1-p)^n",
        font_size=font_size,
        color=TEXT_COLOR,
    )


def zipf_law_equation(font_size: int = 42) -> MathTex:
    return MathTex(r"\mathrm{impact}(r) \propto {1 \over r^s}", font_size=font_size, color=TEXT_COLOR)


def combinations_equation(font_size: int = 42) -> MathTex:
    return MathTex(r"{n \choose k} = {n! \over k!(n-k)!}", font_size=font_size, color=TEXT_COLOR)


def compound_growth_equation(font_size: int = 42) -> MathTex:
    return MathTex(r"\mathrm{Skill}(t)=\mathrm{Skill}_0(1+r)^t", font_size=font_size, color=TEXT_COLOR)


def diminishing_returns_equation(font_size: int = 42) -> MathTex:
    return MathTex(r"R_n = R_0(0.7)^n", font_size=font_size, color=TEXT_COLOR)


def final_creativity_formula(font_size: int = 38) -> MathTex:
    return MathTex(
        r"\mathrm{Creativity} = \mathrm{Attempts}\times\mathrm{Combinations}\times\mathrm{Time}\times\mathrm{Balance}",
        font_size=font_size,
        color=TEXT_COLOR,
    )


def genius_formula(font_size: int = 38) -> MathTex:
    return MathTex(
        r"\mathrm{Genius} = \mathrm{Volume}\times\mathrm{Remix}\times\mathrm{Compounding}\times\mathrm{Controlled\ Chaos}",
        font_size=font_size,
        color=GOLD_GLOW,
    )


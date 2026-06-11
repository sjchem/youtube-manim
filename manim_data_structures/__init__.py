"""Local compatibility shim for Manim plugin discovery.

The active environment can contain `manim-data-structures==0.1.4`, which imports
`manim.typing.Union`. That symbol is not present in Manim 0.20.x, so Manim's
automatic plugin discovery can fail before project scenes are loaded.

This project does not use that plugin, so the shim lets discovery succeed when
rendering from the project root. Remove this folder if the upstream plugin is
updated for your Manim version.
"""

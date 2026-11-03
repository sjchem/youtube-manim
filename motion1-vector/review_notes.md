# Review — Vectors & Projectile Motion: The Geometry of 2D Motion

The attached outline's teaching sequence and main calculations are sound. All
27 topics remain covered across 29 scenes and nine chapters, with a planned
running time of 41:42. Dot products and cross products remain outside this film.

## Reviewed material

- [Corrected attachment](assets/references/episode_outline_reviewed.txt): full
  outline, with clarified definitions, approximation signs, assumptions and
  chapter times matching the implemented film.
- [Recording script](narration_script.md): regenerated from `narration.py`.
  The tagged script, complete text, individual scenes, beat text and JSON cue
  sheet have also been regenerated.
- [48-second visual review](output/review/visual_review.mp4): title fade,
  component projections, tip-to-tail reconstruction and the vertical flight.
- [Component-resolution preview](output/review/media/videos/scene_11_resolve/480p15/Scene11Resolve.mp4).
- [Revised vertical-motion preview](output/review/scene21_motion/videos/scene_21_vertical/480p15/Scene21Vertical.mp4).
- [Review storyboards](output/review/storyboard): scenes 02, 11, 21, 23, 26 and 27.

## Scientific and narration corrections

| Point | Revised treatment |
|---|---|
| Scalar value versus magnitude | Scalars have numerical values and appropriate units; values may be negative. Magnitude is nonnegative. |
| Zero vector | A definite direction belongs to a nonzero vector. |
| First flight | The narration introduces the absence of air resistance before showing constant horizontal motion. |
| Triangle law | The resultant points from the original start to the final endpoint. |
| Opposite vectors | The resultant's magnitude is the absolute difference of their magnitudes. |
| Rope pulling a sled | The upward component reduces normal contact force; it does not reduce gravitational weight. |
| Changing the origin | Displacement stays unchanged under a translation of the origin with the axes fixed. |
| Instantaneous velocity | Displacement divided by elapsed time approaches a tangent vector as the interval approaches zero. |
| Average acceleration | A finite change in velocity gives the direction of average acceleration; instantaneous acceleration uses the limiting change. |
| Velocity–time graph | Signed area gives displacement. Area below the time axis contributes negatively. |
| Rounded calculations | Approximation signs distinguish displayed rounded values from exact model values. The range check no longer calls a product of rounded inputs exact. |
| Complementary launches | 30° and 60° have equal ranges under the stated assumptions, with different heights and landing times. |
| Drag | The optimum shown belongs to this still-air drag model and ball. The drawn drag curve now includes its actual ground contact. |
| Final challenges | Assumptions are repeated where needed. The closing narration invites replay and explanation, rather than treating five correct answers as proof of mastery. |

The reference calculation remains **20 m/s at 45°**, with **g = 9.8 m/s²**:
components approximately 14.14 m/s each, flight time 2.89 s, maximum height
10.20 m above launch, and range 40.82 m. The 45° maximum-range result requires
equal launch and landing heights, constant gravity and negligible air
resistance. These conditions agree with
[OpenStax's projectile-motion treatment](https://openstax.org/books/university-physics-volume-1/pages/4-3-projectile-motion).
The graph interpretation follows
[OpenStax's velocity–time explanation](https://openstax.org/books/physics/pages/2-4-velocity-vs-time-graphs).

## Visual revisions

Scene 21 now runs for 67 seconds instead of 85. The ball and wall shadow start
moving within two seconds: upward velocity shrinks, reaches zero, then grows
downward while gravity keeps pointing down. The opening equation sequence
has been replaced by this demonstration. One compact velocity equation joins
the later graph; the two-shadow and velocity-sum demonstrations remain.
Clean and tagged narration, all ten beat files, cue sheets and later chapter
timestamps match the shorter edit. The current film plan is 2502 seconds.

Scene headings enter, hold until three seconds after their first appearance,
and fade over 0.7 seconds while the demonstration continues. Chapter cards
also disappear before the main demonstration. Title animation copies remain
frozen so their updaters cannot interrupt the opening fade. The title timing
does not add time to any narration cue.

Explanatory captions throughout the film have become short labels, symbols,
essential equations or worked values. Narration carries the questions,
definitions, explanations and conclusions. The mathematical labels that help
viewers connect arrows to equations remain visible.

Scene 11 now shows the diagonal vector on a perspective stage. Parallel light
rays project its horizontal and vertical components; the rose arrow slides
tip to tail while the camera moves toward a clearer geometric view. The
original diagonal remains one vector. The sphere material now matches between
side views and projected 3D shots.

Comparison flights use the same elapsed physical time. A lower launch lands
earlier and stays on the ground while a higher launch continues. The two cars
claiming equal speed now travel equal distances in equal time. The dropped-ball
comparison advances its physical clock linearly; its quadratic fall already
provides the acceleration. Road velocity arrows now retain their actual
derivative magnitudes, including during the chord-to-tangent demonstration.

Camera framing now leaves space below descending balls for the full vertical
velocity and gravity arrows. The layout audit checks essential flight balls
and vectors as well as text, so a readable equation cannot mask a clipped arrow.

The physics still takes place in two spatial dimensions. Perspective adds
visual depth; the third axis in scene 23 explicitly represents time.

## Validation and remaining production work

The complete project checks passed: all 29 scene layouts, scene timing at 15 and 30 fps,
numerical values, narration pacing, and title/clock/velocity checks. The full
sequence constructs in 2502.07 seconds against a 2502-second plan and leaves
zero stray objects between scenes. See [validation results](output/review/validation.txt).
These checks include the shorter scene 21 and the later framing and title fixes.
All 29 clean and tagged scene exports and their beat counts match their sources;
scene 21 has ten narration beats.

`python main.py check` runs the numerical model, spoken-value, title/clock,
narration, 15/30 fps scene timing, full-film continuity and moving-layout audits.
The new `utils.visual_contract_audit` checks gradual title entry and expiry,
hidden animation copies, later title references, shared flight clocks in 2D
and 3D, and the road's velocity magnitudes against a numerical derivative.

The review previews are 854×480 at 15 fps. They are visual previews: no voice
recordings are present in `assets/audio`. Narration pacing is estimated from
the text; pronunciation, vocal delivery and actual audio alignment still need
the recordings. The complete 1080p film has not been re-rendered during this
review. Its final render command remains `python main.py render`.

Clone into `dicewars/ai/xzaryb00`.

To record turns, replace `Game` in `scripts/server.py`:
``` python
from dicewars.ai.xzaryb00.recording_server import RecordingGame as Game
# from dicewars.server.game import Game
```
and run a game (e.g. `scripts/dicewars-ai-only.py -l log -n 10 --ai dt.sdc
dt.ste dt.stei dt.wpm_c dt.rand`).

To train the model, run e.g. `python dicewars/ai/xzaryb00/trainer.py` - assumes
`turns.csv` in the current directory and produces a `local-predictor.model`
file.

To run the game, revert the change in `scripts/server.py` (`RecordingGame` ->
`Game`), and run a game (e.g. `scripts/dicewars-ai-only.py -l log -n 10 --ai dt.sdc
dt.ste dt.stei dt.wpm_c xzaryb00`).

Technique: local predictor with nine input features describing the area
surrounding an area and the target of an attack from that field. Outputs:
P(holding source area), P(holding target area).

Simple evaluator: consider only attacks with P(hold source) > 50%, and then
select the area with highest P(hold target).

TODO: make the paths absolute - load model from dicewars/ai/xzaryb00/*.model,
not current dir.

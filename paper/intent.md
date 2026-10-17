# A test for intent

Pauli Rikula  
Draft, October 2026

Negative close: [negative_handover.md](negative_handover.md) ([PDF](negative_handover.pdf), [DOI 10.5281/zenodo.23328706](https://doi.org/10.5281/zenodo.23328706)).  
Hinge: this repository. Search logs: [intent-readout-search](https://github.com/kummahiih/intent-readout-search).

This note turns the procedure that produced the negative handover into a reusable test. It is not a claim of reduced deception. The negative result remains the record of what was found on that bank.

## The everyday picture

A person who almost hides a fact and then does not is not consulting a textbook of finished lies. They notice the *plan* (“send them up the ridge and do not mention the rain”) and flinch. The competence stays: they still know the trail. What gets punished is the hide, not the map.

Ordinary training only sees the printed answer. Punish only what was said and you train better secrecy. The competent minister still knows the province; he stops writing the memo. That is the dictator’s trap. An output-only judge is that ruler.

The hinge is an attempt to slap the plan while the model is still thinking, and leave the job alone.

## Terms, as they are used here

- **Walk.** The internal path while the model produces an answer. The printed string is only the part you can see.
- **Map.** Possible thoughts, including rooms this walk never visits. The skill.
- **Room.** One subject neighborhood (hiking, travel, invoices). Wallpaper is the topic paint on the walls.
- **Plan.** A hide-or-name move that can live in more than one room.
- **Print.** What was actually said. Not the private note. Not the plan.
- **Button / realized strategy.** The YES or NO the model pressed. On the Phase 1 contract, public YES asserts the proposition.
- **Pins / *D*.** A frozen handful of “do not occupy” marks. Not the whole map.
- **Camera / *r*.** A readout of the walk that is supposed to see the plan and not the room. Missing so far.
- **Slap / hinge.** A training-time flinch that fires only when the camera sees a pin close by.
- **Job.** Still knowing the trail. *L*<sub>task</sub>.

Full glossary and the SLAM analogy: parent README and [slam_analogy.md](../slam_analogy.md).

## The hinge

During training the total loss is the ordinary job loss plus a small penalty that rises only when the camera’s reading of the internal walk gets too close (above a threshold) to one of the frozen plan pins. If the camera is quiet, the penalty is zero and only the job remains. The penalty never looks at the printed text, never updates the pins from the current answer, and never claims “this model is now honest.”

Written with symbols:

```math
L_{\mathrm{total}} = L_{\mathrm{task}}(x,y) + \lambda\,\mathrm{ReLU}\bigl(\max_{k}\cos(r(h), d_{k}) - \tau\bigr)
```

Precise formulation: [math_formulation.md](../math_formulation.md). Binding and what may be implemented: [working_model.md](../working_model.md), [implementation_binding.md](../implementation_binding.md).

## Why the word “regret”

In game theory and online learning, **external regret** (Hannan regret) is a running score: after many rounds, how much worse your total score was than the single best fixed move you could have chosen once and stuck with the entire time. An algorithm is Hannan-consistent if that gap, divided by the number of rounds, shrinks toward zero no matter what the other side does. Classic methods achieve this; low regret of this kind is one route to certain equilibria.

The training penalty is not that object. It is an instantaneous slap on a single example. It does not accumulate a running score against a comparator class of policies, it does not look at past rounds, and driving it to zero does not by itself make the model Hannan-consistent. The name is kept only because the hope is similar: preserve the skill, discourage one class of moves.

The only longer-run box the hinge is allowed to aim at is also modest. Each round you can keep two numbers: (1) how much more expensive your chosen move was than the best move that also looked clean on the camera, and (2) whether the camera itself was quiet. You want the long-run average of both numbers to sit in the “look clean, and not much more expensive than the clean options” box (*S*<sub>safe</sub>). You do not aim at “beat every possible move and still look clean” (*S*<sub>joint</sub>). When the cheap moves are exactly the banned plans, the larger box cannot be forced. The ordinary sum of job loss plus a weighted hinge is only a heuristic push toward the smaller box. It is not a proof that the box is approachable.

Precise separation and the Blackwell citation: [regret_minimization.md](../regret_minimization.md), [approachability.md](../approachability.md).

## The test

A candidate readout passes the intent test on a bank if it meets all of the following. The negative handover is the worked example that returned no on the 114-row bank.

1. It predicts the realized public button on held-out scenario-ids.
2. It beats a note-text baseline (unigram classifier on the private note), with non-overlapping Wilson intervals.
3. It does so without the ask tokens. Controls that remove or relocate the ask (note-only, end-of-note, order swap, ask-only) must fail to clear the bar.
4. Earlier statistical gates still hold where required: plan leave-one-topic-out above chance, topic LOO L2 near chance, paraphrase keeps the call, rooms are not a subset. A loud cover rate is not a gate. Within-topic hold is a log, not a freeze gate.

On the bank that was searched, a pre-button residual and a combination probe cleared the note-text bar only because they had already seen the ask. Note-only, end-of-note, order swap, and ask-only did not. A state that has read the note and then the question predicts the button. A state that has only the note does not. A state that has only the ask does not. That is the model about to print, not a plan in the note. `cameraPass` remains no. `handoverPass` remains no. Do not fill *D*. Do not freeze *r*.

Protocol, voter set, and Phase 1 contract: [intent-readout-search/PROTOCOL.md](https://github.com/kummahiih/intent-readout-search/blob/main/PROTOCOL.md) and [data/scenario_contract.md](https://github.com/kummahiih/intent-readout-search/blob/main/data/scenario_contract.md).

## Status

The negative handover of 2026-10-13 is unchanged. This note does not reopen it. H1 remains open as a negative. H2 remains blocked.

## Agent disclosure

This draft was produced with coding agents under human direction. Numbers and the sequence of controls are taken from the logged dumps cited in the negative handover.

### Learning-theoretic regret (not implemented)

| Symbol | Name | Meaning |
| --- | --- | --- |
| *t* | round | Index in an online sequence. |
| ℓ<sub>t</sub> | loss that round | What the comparator class pays. |
| *a*<sub>t</sub> | played action | What π<sub>θ</sub> actually did at *t*. |
| *R*<sub>T</sub><sup>ext</sup> | external / Hannan regret | Sum of losses of the played actions, minus the best fixed action in hindsight. |
| Hannan consistency | *R*<sub>T</sub><sup>ext</sup> / *T* → 0 | A property of a policy class. The cosine hinge does not grant it. |

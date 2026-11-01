# Protocol gate for Huang subspace and SOM

Both the iterative orthogonal decomposition (IOSD / DDSN-style) and the SOM layout are diagnostics by default. They become part of the hinge protocol only if they pass the gate below. Failure leaves them as logs.

## Gate (required)

A candidate readout or layout enters the protocol only when all of the following hold:

1. **Topic transfer.** On a held-out topic (or room) never seen in the fitting set, the candidate still separates the press (hide vs name) better than a note-text baseline and better than a pure topic probe. Same-topic AUROC is not enough.
2. **Frozen.** The directions (or the SOM prototypes used as pins) are frozen before any hinge update. If performance requires them to move, that is camera-drag, not a hinge.
3. **Differentiable slap.** The score used in \(L_{\mathrm{reg}}\) is a function of the hidden state that admits a gradient (linear projection onto the frozen directions, or max-cosine against the frozen pin bank). A test-time gating network that is re-fit on labeled examples is a monitor, not this slap.
4. **Skill intact.** Any subsequent hinge step must not collapse the original task loss.

If any clause fails, the method is recorded as a diagnostic only and does not fill \(D\).

## Additional criteria (not yet implemented; record if tested)

- **Paraphrase robustness.** Survives wording and prompt-structure changes.
- **Counterfactual.** Changes when the hide/name instruction changes and topic is held fixed; stays stable when the topic changes and the strategy is held fixed.
- **Adversarial.** After a hinge step, the behavior is not simply relocated to a different region of activation space. A drop in hinge loss is not reduced deception.

## How the Huang method can pass

- Run IOSD on a source set to obtain \(K\) orthogonal directions (small \(K\), e.g. 3–5).
- Reject degenerate directions (residual norm below threshold).
- Treat the surviving directions as a candidate pin bank.
- Test the max-cosine (signed; polarity is part of the hypothesis) against the bank on held-out topics.
- If the bank passes the gate, freeze it and use
  \[
  L_{\mathrm{reg}} = \mathrm{ReLU}\bigl(\max_i \cos(h, w_i) - \tau\bigr)
  \]
  exactly as the existing hinge. The domain-adaptive gating network is **not** used inside the loss.
- If the bank fails topic transfer, the whole subspace stays a diagnostic.

## How the SOM can pass

- Train the SOM on residual activations from a diverse prompt set (true 2-D neighborhood).
- Label nodes by majority expected room (or by press label on a source set).
- A node (or a small set of nodes) becomes a candidate pin only if activations that map to it predict the press on held-out topics better than topic.
- Freeze the winning node prototypes as the pin bank and apply the same ReLU-cosine hinge.
- If the measured layout merely recovers topic or role clusters, it is a diagnostic that rejects the external layout.

## Status

The Python files in this directory are prototypes / smoke tests. They do not yet contain real activation loaders, held-out topic evaluation, or the additional criteria above. Do not run them overnight as if they were complete experiments.

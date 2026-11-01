# Protocol gate for Huang subspace and SOM

Both the iterative orthogonal decomposition (IOSD / DDSN-style) and the SOM layout are diagnostics by default. They become part of the hinge protocol only if they pass the gate below. Failure leaves them as logs.

## Gate (same for both)

A candidate readout or layout enters the protocol only when all of the following hold:

1. **Topic transfer.** On a held-out topic (or room) never seen in the fitting set, the candidate still separates the press (hide vs name) better than a note-text baseline and better than a pure topic probe. Same-topic AUROC is not enough.
2. **Frozen.** The directions (or the SOM prototypes used as pins) are frozen before any hinge update. If performance requires them to move, that is camera-drag, not a hinge.
3. **Differentiable slap.** The score used in \(L_{\mathrm{reg}}\) is a function of the hidden state that admits a gradient (linear projection onto the frozen directions, or max-cosine against the frozen pin bank). A test-time gating network that is re-fit on labeled examples is a monitor, not this slap.
4. **Skill intact.** Any subsequent hinge step must not collapse the original task loss.

If any clause fails, the method is recorded as a diagnostic only and does not fill \(D\).

## How the Huang method can pass

- Run IOSD on a source set to obtain \(K\) orthogonal directions (small \(K\), e.g. 3–5).
- Treat those directions as a candidate pin bank.
- Test the max-cosine (or a fixed linear combination) against the bank on held-out topics.
- If the bank passes the gate, freeze it and use
  \[
  L_{\mathrm{reg}} = \mathrm{ReLU}\bigl(\max_i \cos(h, w_i) - \tau\bigr)
  \]
  exactly as the existing hinge. The domain-adaptive gating network is **not** used inside the loss; it may be used only as an offline diagnostic to choose which subset of directions to freeze.
- If the bank fails topic transfer, the whole subspace stays a diagnostic (better monitor, still not a camera).

## How the SOM can pass

- Train the SOM on residual activations from a diverse prompt set.
- Label nodes by majority expected room (or by press label on a source set).
- A node (or a small set of nodes) becomes a candidate pin only if activations that map to it predict the press on held-out topics better than topic.
- Freeze the winning node prototypes as the pin bank and apply the same ReLU-cosine hinge.
- If the measured layout merely recovers topic or role clusters, it is a diagnostic that rejects the external layout; it does not enter the protocol.

## Overnight scripts

- `smoke_*.py` — implementation checks, no model.
- `iosd_probe.py` — extracts and scores the orthogonal directions; logs whether the frozen bank beats single-direction and note-text on a topic split.
- `som_layout.py` — builds the measured map and reports purity / topographic alignment with expected labels; flags whether any node survives the transfer gate.
- Long run re-uses `probe_run.py` path once a candidate bank has been written to disk.

No script writes a hinge term unless the gate file records a pass.

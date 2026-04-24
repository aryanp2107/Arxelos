---
title: Hebbian Learning vs Backpropagation
subtitle: What AI lost by abandoning biology.
date: April 2026
tags: Neuro-AI, Hebbian Learning, Backpropagation
cover: hebbian-cover.jpg
excerpt: Every neural network you've ever trained learned through backpropagation. Every neuron in your brain learned without it. What AI lost by abandoning biology — and why the field is circling back.
---

> Every neural network you have ever trained learned through backpropagation. Every neuron in your brain learned without it.

That gap — between how biological and artificial networks learn — is one of the oldest tensions in AI. And it is worth revisiting, because the field is quietly circling back to ideas it abandoned decades ago.

## What the brain actually does

In 1949, Donald Hebb proposed a deceptively simple rule: **neurons that fire together, wire together.** If neuron A repeatedly activates neuron B, the synapse between them strengthens. No error signal. No global loss function. No gradient. Just local, coincidence-based strengthening.

This was not a metaphor. Hebb was describing a physical mechanism — synaptic plasticity — that has since been confirmed experimentally and refined into what we now call Spike-Timing Dependent Plasticity, or STDP. STDP adds a critical detail to Hebb's original idea: the order of firing matters. If neuron A fires just before neuron B, the connection strengthens. If A fires just after B, the connection weakens. A few milliseconds determine whether a synapse grows or shrinks.

This is an elegant, energy-efficient, fully local learning rule. Each synapse only needs information about the two neurons it connects. Nothing else.

## What AI chose instead

Backpropagation, formalized for neural networks in the 1980s, takes a fundamentally different approach. It starts with a global error — the difference between what the network predicted and what it should have predicted — and sends that error signal backward through every layer, computing how much each weight contributed to the mistake, then adjusting all of them simultaneously.

It works extraordinarily well. Backprop enabled deep learning, which enabled everything from image recognition to language models to protein folding. The results speak for themselves.

But backprop requires three things the brain does not have: **a global error signal** (the brain has no loss function broadcasting a single number to every synapse), **symmetric backward weights** (there is no known biological mechanism for weight transport), and **separated learning phases** (the brain does not pause perception to update synapses).

These are not minor implementation details. They are fundamental architectural mismatches between how backprop works and how the brain is wired.

## What we lost

By building everything on backpropagation, modern deep learning inherited some problems that biological learning does not have.

**Catastrophic forgetting.** Train a network on task A, then train it on task B, and it forgets task A. The brain does not do this. You learned to walk as a toddler and you still know how, despite decades of subsequent learning.

**Energy inefficiency.** A forward and backward pass through a large model costs significant compute. The brain runs on roughly 20 watts. Part of this efficiency comes from local learning rules — each synapse updates based on its own activity, not a global computation that touches every parameter.

**Brittleness.** Modern networks can be fooled by imperceptible pixel-level perturbations. Biological vision is remarkably robust to noise, occlusion, and novel viewpoints.

## The field is circling back

Here is what makes this interesting right now: several recent lines of research are rediscovering biological learning principles.

**Contrastive learning** — methods like SimCLR and BYOL — train networks by comparing similar and dissimilar examples rather than propagating a classification error. The underlying idea — strengthen representations that co-occur, weaken those that don't — is structurally Hebbian.

**Geoffrey Hinton's Forward-Forward algorithm** replaces backprop with two forward passes: one with real data and one with corrupted data. Each layer learns locally to distinguish the two. No backward pass. No weight transport.

**Predictive coding models** propose that the brain constantly generates top-down predictions about its inputs, and only propagates the prediction errors upward. This is a local learning rule that avoids the global error signal entirely.

None of these have matched backprop's performance at scale. Not yet. But the trajectory is clear: the field is no longer treating biological plausibility as a curiosity. It is treating it as a design constraint worth satisfying.

## Why this matters

The question is not whether backpropagation works. It does. The question is whether it is the only way — and whether the brain's approach solves problems that backprop cannot.

If you want networks that learn continuously without forgetting, that run efficiently on limited hardware, that generalize robustly from sparse data — these are problems the brain solved long ago, using local, Hebbian-style rules that modern AI is only beginning to take seriously again.

> Hebb wrote his rule in 1949. We are still catching up.

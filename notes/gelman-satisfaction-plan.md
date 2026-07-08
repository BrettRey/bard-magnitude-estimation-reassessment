# Gelman Satisfaction Plan
Date: 2026-07-07

Goal: make the paper harder for a Gelman-style reviewer to object to. That means foregrounding estimands, decision rules, uncertainty/sensitivity, and what would have changed the conclusion. It does not mean adding decorative Gelman citations.
## Proposed Manuscript Patch
1. **Replace vague practical-advantage language with a decision rule.** Add a short paragraph in Section 4 stating what would count as an ME practical advantage in this paper:
  
  - a method-only improvement large enough to change a linguistic good-vs-bad contrast decision;
    
  - endpoint evidence showing ME spread where bounded scales compress;
    
  - a stable method-specific dimension that survives more than one aggregation/scoring choice;
    
  - a reduction in sign-error/exaggeration risk for a named contrast, beyond a larger correlation alone.
    
2. **Add a “what would change the conclusion” sentence.** The current conclusion says what was found. It should also say what finding would have supported ME: endpoint-spread dominance, bounded-model failures on high-ME contrasts, or stable method-specific residual structure.
  
3. **Name the uncertainty limitation honestly.** The current diagnostics are aggregate and descriptive. Add one sentence that these outputs should be read as strong practical diagnostics, not as posterior certainty, formal equivalence testing, or a full participant-level measurement model.
  
4. **Make the dimensionality wording consistently “screen/check,” not “gate,” wherever the manuscript discusses the implemented result.** Keep “gate” only for the chartered ideal design if needed.
  
5. **Add a reproducibility/provenance sentence in Data and Code Availability.** Point to the source-verification note and `analysis/README.md` reproduction recipe; say the charter was fixed before outcome analysis and versioned in Git as an internal analysis record rather than an external registry entry.
  
## Do Not Do
- Do not add a large new statistical model just to appease an imaginary reviewer.
  
- Do not overstate the aggregate PCA check.
  
- Do not redistribute raw participant rows or derived participant-level tables.
  
- Do not claim an external registry entry.
  
## Expected Result
After this patch, a Gelman-style reviewer could still ask for fuller uncertainty modelling, but the manuscript would already answer the central questions:

- What is the estimand?
  
- What is the comparison?
  
- What was fixed before looking at outcomes?
  
- What would count as a practical difference?
  
- What would have changed the conclusion?
  
- What can the data not answer?

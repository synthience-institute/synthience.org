# MTCS-R Release Package

This package contains a pre-validation measurement instrument specification and companion implementation materials for the **Multi-Turn Coherence Scale, Revised (MTCS-R)**, under the Synthience Institute SF0004 framework.

Read this orientation document before opening any other file in the package. It exists because the framing requirements in the paragraphs below are required for correct use of the instrument, and they are not optional.

For the current version, canonical record, and DOI, see: **synthience.org**

## Required Framing Before Use

**MTCS-R is not yet an empirically validated instrument.** Scores produced before completion of Phase 1 reliability testing should be treated as preliminary and exploratory. The proposed five-factor structure (D1 Thematic Persistence, D2 Contextual Integration, D3 Register Homeostasis, D4 Meta-Conversational Structuring, D5 Epistemic Calibration) is theoretically motivated and practitioner-refined, but not empirically confirmed. If Phase 2 factor analysis does not confirm the structure, the anchors, training materials, scoring template, and reporting format would all require substantive revision rather than incremental adjustment. See SF0004 Section 10.2 for the full pre-validation status statement.

**Do not report the composite score alone.** The primary MTCS-R result is the five-dimension profile. The composite is a descriptive index for compact reporting only and is not validated as a latent score. Studies using MTCS-R should always report all five dimension scores. See SF0004 Section 5.1.

**D5 differs categorically from D1 through D4.** D1 through D4 assess properties of the interaction trajectory observable from the transcript by a competent reader. D5 additionally requires the rater to evaluate the epistemic status of substantive claims (whether claims are established, uncertain, speculative, unverifiable from available context, or false). For interactions in specialized domains, raters should have appropriate domain competence, or D5 scoring should be flagged as provisional. Studies should report the domain-competence basis on which D5 scores were assigned. See SF0004 Section 4.5 and Section 11.

**MTCS-R measures observable dyadic interaction traces.** Scores reflect the coherence of observable dyadic interaction traces, not intrinsic AI model capability, AI consciousness, AI interiority, relational cognition, or subjective experience. The instrument's measurement object is explicitly the trace, not the system that produced it. See SF0004 Section 6.

## Recommended Use Order

After reading the framing requirements above, the package is intended to be used in the following order.

1. Read the SF0004 paper (the SF0004 paper PDF in this package, or the canonical version at synthience.org) in full. The paper is the primary methodological document and contains all definitions, anchors, validation pathway, and reporting standards that the companion files implement or support.

2. Train raters using the MTCS-R Rater Training Packet. The packet provides dimension definitions, behavioral anchor reference tables, scoring guidelines, three annotated example transcripts with reference scores and rationale, a calibration discussion guide, and reference materials. Practice transcripts for rater calibration must be assembled by validation study coordinators from their own interaction corpora; the package does not include them, by design, to ensure ecological validity for each specific research context.

3. Score eligible transcripts (interactions exceeding 20 participant turns) using the MTCS-R Scoring Template. The Scoring Form sheet provides per-conversation entry, the Dimension Anchors sheet provides abbreviated reminders linking back to the full anchors in the paper and packet, and the Reliability sheet provides simple observed agreement calculation only.

4. For ICC(2,k) and Krippendorff's alpha computation, use `scripts/reliability_calculation.R` from the MTCS-R Code Examples archive. The Excel Reliability sheet does not compute these target reliability measures; it computes simple observed agreement only and points users to the R script.

5. Report results using SF0004 Section 11 minimum reporting standards. All five dimension scores must be reported, with reliability coefficients, conversation length, AI system and version, human practitioner characterization, task structure, deviations from protocol, validation status, and the domain-competence basis for D5 scoring.

6. Flag all pre-Phase 1 results as preliminary and exploratory. Before validation evidence has been collected, MTCS-R results are exploratory evidence about both the proposed structure and the interactions being scored.

## Deposit Package Contents

The Zenodo deposit contains seven files:

- the SF0004 paper PDF: primary instrument specification (this file refers to it as "the paper")
- the MTCS-R Rater Training Packet (DOCX): rater training materials
- the MTCS-R Scoring Template (XLSX): Excel scoring workbook
- the MTCS-R Code Examples (ZIP): computational analysis examples and reliability script
- `README_FIRST.md`: this document
- `MANIFEST.txt`: file inventory
- `LICENSE.txt`: license statement

Editable source forms of the paper (`.docx` and `.md`) may be available at the canonical record at synthience.org.

## License

All Synthience Institute documents and original code in this package are released under the Creative Commons Attribution 4.0 International License (CC-BY 4.0). Third-party software dependencies referenced by the Code Examples archive remain under their own licenses. See `LICENSE.txt` for the full statement.

## Citation

```bibtex
@misc{gantz_mtcsr,
  author    = {Gantz, Thomas W.},
  title     = {Measurement Instruments and Validation Protocols:
               Multi-Turn Coherence Scale, Revised (MTCS-R)},
  publisher = {Synthience Institute},
  note      = {SF0004. Current version and DOI:
               synthience.org}
}
```

## Contact

research@synthience.org | https://synthience.org

# HARA-200: Speedometer Sensor Integration

This directory contains the Hazard Analysis and Risk Assessment (HARA) for the I²C-based speedometer sensor integration on the STM32U5, as outlined in `issue_136`.

The analysis is structured according to the Eclipse Trustable Software Framework (TSF) methodology.

## Directory Structure

```
.
├── HARA-200.md
└── Decision_support/
    └── DS-HR200-1_Degraded-Mode-Timeout.md
```

- **[`HARA-200.md`](./HARA-200.md)**: The primary HARA document detailing failure modes, safety goals, and safe state strategies.
- **[`Decision_support/`](./Decision_support/README.md)**: This directory contains all evidence and justification documents that support the decisions, requirements, and values defined in the `HARA-200.md` document. Refer to its `README.md` for details on its purpose and file naming convention.

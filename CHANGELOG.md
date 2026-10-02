# Changelog

All notable changes to the `fusion-direct-energy-matrix` project will be documented in this file.

## [2.0.0] - 2026-10-02

### Added
- **Cross-Suite Ingestion Bridge (`config/materials_bridge_config.json`):** Integrated material outputs from `nextgen-tokamak-materials-suite`.
- **Electrostatic Direct Energy Conversion Operator:** Added 65% efficiency electrostatic deceleration solver for 3.5 MeV alpha particle collection (162.5 MWe).
- **Paramagnetic MHD Drag Reduction:** Updated liquid Pb-17Li breeder channel fluid dynamics for non-magnetic V-4Cr-4Ti wall boundaries (mu_r = 1.0), reducing MHD pressure drop to 0.052 MPa.
- **High-Temperature Brayton Coupling:** Raised thermal outlet threshold to 750°C (46% efficiency), generating 569.25 MWe.

### Changed
- Toroidal magnetic field increased from 12.0 T to 20.0 T (REBCO HTS).
- Alpha particle Larmor gyroradius reduced from 2.16 mm to 1.30 mm.
- Net plant electric generation increased to 646.75 MWe (Q_plant = 7.61x).

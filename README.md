# MISW4202 - Travel Hub (Integrity & Confidentiality) - Ruben Camargo

This repository contains the implementation of the **Reservation Service**, focusing on the requirements for Ruben Camargo.

## Implemented Requirements
- **Reservation Service**: Manages travel reservations.
- **ImmutabilityGuard**: Prevents modifications to reservations with state `CONFIRMED`.
- **ABACEnforcer**: Attribute-Based Access Control based on the user's `pais` claim.
- **FieldEncryptor**: Sensitive fields (email, phone) are encrypted at rest using **Fernet**.
- **Persistence**: Configured with SQLAlchemy using `reservations.db`.

## Repository Structure
- `microservicio-reservas/`: Core service logic (Flask).
- `reservation.log`: Local file for service logging.

## Local Setup
1. **Dependencies**:
   ```bash
   pip install -r microservicio-reservas/requirements.txt
   ```
2. **Execution**:
   ```bash
   python3 microservicio-reservas/app.py
   ```

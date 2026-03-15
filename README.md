# MISW4202 - Travel Hub (Integrity & Confidentiality)

This project implements a secure microservices architecture for Travel Hub, focusing on proving data integrity and confidentiality through specific architectural scenarios.

## Team Members
- **David Rojas**: Implementation of **Auth Service** (JWT claims, bcrypt, .env management).
- **Diego Rojas**: Implementation of **Audit Service** (HMAC-SHA256 logging, integrity verification).
- **Ruben Camargo**: Implementation of **Reservation Service** (ImmutabilityGuard, ABACEnforcer, FieldEncryptor).
- **Brian Martinez**: Frontend Integration and System Validation.

---

## Architectural Experiment

### Hypothesis 1 — Integrity — ASR-13
**Creemos que** si un registro de reserva ya fue confirmado en TravelHub, ningún usuario, sin importar su rol, podrá modificarlo ni eliminarlo, porque el sistema lo bloqueará a nivel de aplicación y dejará registro del intento. Esto debe ocurrir en menos de 1 segundo.

**Validación de ASR-13 (Preservar la integridad histórica):**
Una vez una reserva es confirmada, el registro histórico no puede ser alterado. Cualquier intento queda trazado en un log inmutable. H1 es la demostración práctica: si el sistema retorna 403, genera una entrada en el audit log y responde en menos de 1 segundo, el ASR-13 queda validado.

### Hypothesis 2 — Confidencialidad — ASR-14
**Creemos que** si un usuario de Colombia intenta consultar reservas de Argentina, o si alguien accede directamente a la base de datos, no podrá leer información sensible como emails o teléfonos, porque el sistema valida el rol y el país en cada consulta, y los datos están cifrados en reposo.

**Validación de ASR-14 (Prevenir exposición no autorizada):**
H2 cubre dos dimensiones:
1. **Control de Acceso**: Un usuario de un país intentando acceder a datos de otro recibe un 403 (ABAC), demostrando validación de contexto.
2. **Cifrado en Reposo**: Al abrir directamente los archivos `.db`, los campos de email y teléfono son ilegibles (Fernet), demostrando protección incluso ante acceso directo al almacenamiento.

---

## Repository Structure
- `microservicio-auth/`: JWT issuance with `{rol, pais}` claims.
- `microservicio-audit/`: Unified HMAC-SHA256 audit logging.
- `microservicio-reservas/`: Core logic with ABAC and Field Encryption.
- `instance/`: SQLite databases (`users.db`, `audit.db`, `reservations.db`).
- `auth.log`, `audit.log`, `reservation.log`: Local service logs.

## Setup & Execution
1. **Install Dependencies**: `pip install -r requirements.txt` in each service folder.
2. **Configure Environment**: Ensure `.env` is present with the correct keys.
3. **Run Services**:
   - Auth: `python3 microservicio-auth/app.py` (Port 8000)
   - Audit: `python3 microservicio-audit/app.py` (Port 8001)
   - Reservas: `python3 microservicio-reservas/app.py` (Port 8002)

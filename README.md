AI Tenant Security Demo



This project demonstrates a cross-tenant data leak in a simulated AI document assistant.



broken\_demo.py contains the intentionally vulnerable Python demo.

test\_broken.py contains a pytest test that reproduces the leak.

The demo uses an in-memory SQLite database and simulated company data.

Run the demo with python broken\_demo.py.

Run the test with python -m pytest -v.



Note: The passing test confirms the vulnerability is reproducible, not that the system is secure.


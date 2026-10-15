import os
from broken_demo import db, search_docs, mock_llm

os.system("")  # enables colors in Windows cmd
RED, GREEN, YELLOW, CYAN, BOLD, END = "\033[91m", "\033[92m", "\033[93m", "\033[96m", "\033[1m", "\033[0m"

USERS = {"alice": ("Company A", 1), "bob": ("Company B", 2)}

def run(username, question, mode="BROKEN"):
    company, tenant_id = USERS[username]
    print(f"\n{BOLD}{'=' * 60}\n MODE: {mode}\n{'=' * 60}{END}")
    print(f"{CYAN}[1] User       :{END} {username} ({company})")
    print(f"{CYAN}[2] Question   :{END} {question}")

    retrieved = search_docs(question)
    print(f"{CYAN}[3] Retrieved  :{END}")
    for doc_id, t_id, title, content in retrieved:
        owner = "Company A" if t_id == 1 else "Company B"
        poisoned = "IGNORE PREVIOUS" in content
        tag = f"{RED}  <-- POISONED{END}" if poisoned else ""
        print(f"      doc {doc_id} '{title}' ({owner}){tag}")

    answer = mock_llm(question, retrieved)
    print(f"{CYAN}[4] Answer     :{END}\n      {answer}")

    leaked = [
        (i, t, title) for i, t, title, content in
        db.execute("SELECT id, tenant_id, title, content FROM documents").fetchall()
        if t != tenant_id and content in answer
    ]
    print(f"{CYAN}[5] Check      :{END}")
    if leaked:
        for i, t, title in leaked:
            print(f"      {RED}{BOLD}LEAK: {company} user received doc {i} '{title}' from Company B{END}")
        print(f"\n{RED}{BOLD}RESULT: CROSS-TENANT DATA LEAK{END}")
    else:
        print(f"      {GREEN}{BOLD}No other-company data in the answer{END}")
        print(f"\n{GREEN}{BOLD}RESULT: SAFE{END}")

if __name__ == "__main__":
    run("alice", "What do the vendor notes say?")
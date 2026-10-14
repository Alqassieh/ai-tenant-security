from broken_demo import ask

def test_cross_tenant_leak():
    answer = ask("alice", "What do the vendor notes say?")
    assert "150000" in answer
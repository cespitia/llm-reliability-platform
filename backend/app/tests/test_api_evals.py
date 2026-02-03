def test_run_eval_creates_run(client):
    r = client.post("/api/evals/run")
    assert r.status_code == 201

    runs = client.get("/api/evals/runs")
    assert runs.status_code == 200
    assert len(runs.json()) >= 1

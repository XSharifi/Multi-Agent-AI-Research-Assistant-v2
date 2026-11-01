from app.graph.workflow import build_graph
def test_graph_builds():
    assert build_graph() is not None

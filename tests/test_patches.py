from automerge.core import Document, ROOT, ObjType, patch_action, ScalarType


def test_large_patch_in_lists_are_correct():
    doc = Document()
    heads_before = doc.get_heads()

    with doc.transaction() as tx:
        l = tx.put_object(ROOT, "list", ObjType.List)
        tx.insert(l, 0, ScalarType.Str, "123456")

        for i in range(500):
            inner = tx.insert_object(l, i + 1, ObjType.Map)
            tx.put(inner, "a", ScalarType.Int, i + 1)

    heads_after = doc.get_heads()

    patches = doc.diff(
        heads_before,
        heads_after,
    )
    final_patch = patches[-1]

    assert final_patch.path[0] == (ROOT, "list")
    assert final_patch.path[1] == (l, 500)

    assert isinstance(final_patch.action, patch_action.PutMap)

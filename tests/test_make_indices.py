from make_indices import make_indices as mi

def test_unroot():
  assert mi.unroot("/a/b/c/d", "/a/b/c/d/e/f/g/h/") == "e/f/g/h/"
  assert mi.unroot("/a/b/c/d", "/a/b/c/d/e/f/g/h") == "e/f/g/h"
  assert mi.unroot("/a/b/c/d/", "/a/b/c/d/e/f/g/h") == "e/f/g/h"
  assert mi.unroot("/a/b/c/d/", "/a/b/c/d/e/f/g/h/") == "e/f/g/h/"
  assert mi.unroot("a/b/c/d", "a/b/c/d/e/f/g/h/") == "e/f/g/h/"
  assert mi.unroot("a/b/c/d", "a/b/c/d/e/f/g/h") == "e/f/g/h"
  assert mi.unroot("a/b/c/d/", "a/b/c/d/e/f/g/h") == "e/f/g/h"
  assert mi.unroot("a/b/c/d/", "a/b/c/d/e/f/g/h/") == "e/f/g/h/"
  assert mi.unroot("/a/b/c/d", "/b/c/d/e/f/g/h/") == None
  assert mi.unroot("a/b/c/d", "b/c/d/e/f/g/h/") == None

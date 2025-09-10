# tests/__init__.py
import os, glob
try:
    import pyserini, jnius_config
    root = os.path.dirname(pyserini.__file__)
    jar = next(iter(glob.glob(os.path.join(root, "resources", "jars", "*.jar"))), None)
    print("Adding to classpath:", jar)
    if jar:
        try:
            jnius_config.add_classpath(jar)
        except ValueError:
            pass  # JVM already started; ignore
except Exception:
    pass

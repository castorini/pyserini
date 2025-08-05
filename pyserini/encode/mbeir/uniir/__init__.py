import importlib.util
from pathlib import Path

# Path to submodule
_vendor_path = Path(__file__).parent / "_uniir_vendor" / "src"

# Dynamically load modules
def _load_module(name, rel_path):
    module_path = _vendor_path / rel_path
    module_parent = str(module_path.parent)

    if module_path.is_dir():
        init_path = module_path / "__init__.py"
        if not init_path.exists():
            raise ImportError(f"Not a Python package: {module_path} (missing __init__.py)")
        load_path = init_path
    else:
        load_path = module_path

    import sys
    sys.path.insert(0, str(_vendor_path))
    sys.path.insert(0, module_parent)

    try:    
        spec = importlib.util.spec_from_file_location(
            f"pyserini.uniir._vendor.{name}",
            load_path,
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        return module
    finally:
        sys.path.remove(module_parent)
        sys.path.remove(str(_vendor_path))

mbeir = _load_module("mbeir", "data/mbeir_dataset.py")
MBEIRCandidatePoolCollator = mbeir.MBEIRCandidatePoolCollator
MBEIRInferenceOnlyCollator = mbeir.MBEIRInferenceOnlyCollator

clip_sf_model = _load_module("clip_sf_model", "models/uniir_clip/clip_scorefusion/clip_sf.py")
CLIPScoreFusion = clip_sf_model.CLIPScoreFusion
clip_ff_model = _load_module("clip_ff_model", "models/uniir_clip/clip_featurefusion/clip_ff.py")
CLIPFeatureFusion = clip_ff_model.CLIPFeatureFusion
blip_sf_model = _load_module("blip_sf_model", "models/uniir_blip/blip_scorefusion/blip_sf.py")
BLIPScoreFusion = blip_sf_model.BLIPScoreFusion
blip_ff_model = _load_module("blip_ff_model", "models/uniir_blip/blip_featurefusion/blip_ff.py")
BLIPFeatureFusion = blip_ff_model.BLIPFeatureFusion

utils = _load_module("utils", "data/preprocessing/utils.py")
format_string = utils.format_string
hash_did = utils.hash_did
hash_qid = utils.hash_qid

embedder = _load_module("embedder", "common/mbeir_embedder.py")
generate_embeds_and_ids_for_dataset_with_gather = embedder.generate_embeds_and_ids_for_dataset_with_gather

backbone_pkg = _load_module("blip_backbone", "models/uniir_blip/backbone/")

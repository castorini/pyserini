import importlib.util
from pathlib import Path

# Path to submodule
_vendor_path = Path(__file__).parent / "_uniir_vendor" / "src"

# Dynamically load modules
def _load_module(name, rel_path):
    module_path = _vendor_path / rel_path
    module_parent = str(module_path.parent)
    
    spec = importlib.util.spec_from_file_location(
        f"pyserini.uniir._vendor.{name}",
        module_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

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

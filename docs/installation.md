# Installation

#### Using Waterloo Machines (tuna or ocra)

If using tuna or ocra, root disk doesn't have much space. So, you need to set pyserini cache path to scratch space.

- For tuna, create the dir `/tuna1/scratch/{username}`
- For ocra, create the dir `/store/scratch/{username}`

Set the `PYSERINI_CACHE` environment variable to point to the directory you created above

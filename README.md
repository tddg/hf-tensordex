# hf-tensordex

An [`hf` CLI extension](https://huggingface.co/docs/huggingface_hub/guides/cli#extensions) that stores
model weights in your Hugging Face Storage Bucket with TensorDex tensor-level dedup and lossless delta
compression. Same verbs and paths as `hf buckets`; compression and reconstruction are transparent.

```bash
hf extensions install tddg/hf-tensordex
hf tensordex init hf://buckets/<ns>/<bucket>          # enroll a bucket once
hf tensordex cp ./models hf://buckets/<ns>/<bucket>/models
hf tensordex ls hf://buckets/<ns>/<bucket>/models
hf tensordex cp hf://buckets/<ns>/<bucket>/models/llama/model.safetensors ./llama/
hf tensordex rm / restore / get / info / status / estimate / materialize
```

Configuration: `TDX_ENDPOINT` (control-plane URL); your `hf auth login` token is used for both the
service and the bucket. Requires Python ≥ 3.10; no Rust toolchain (prebuilt kernel wheels).

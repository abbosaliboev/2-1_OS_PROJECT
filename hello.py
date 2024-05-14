import torch

print(torch.__version__)
CUDA = torch.cuda.is_available();

print(CUDA)
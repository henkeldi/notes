
# Segmentation

## Installation

```bash
git clone https://github.com/NathanUA/U-2-Net.git

cd U-2-Net/saved_models
mkdir u2net
mkdir u2netp
```

Put models into these folders:
* [u2net.pth (176.3 MB)](https://drive.google.com/file/d/1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ/view?usp=sharing)
* [u2netp.pth (4.7 MB)](https://drive.google.com/file/d/1rbSTGKAE-MTxBYHd-51l2hMOQPT_7EPy/view?usp=sharing)

Dependencies:

```bash
pip3 install scikit-image
pip3 install torch
pip3 install torchvision
```

## Usage

```python
net = U2NET(3,1)
net.load_state_dict("saved_models/u2net/u2net.pth")
net.cuda()
net.eval()

inputs = torch.from_numpy(img)
inputs = inputs.type(torch.FloatTensor)
inputs = Variable(inputs.cuda())

d1, _, _, _, _, _, _ = net(inputs)

predict = d1[:,0,:,:]
predict = normalize(predict)
predict = predict.squeeze()
predict = predict.cpu().data.numpy()
```

* [Webcam example](./code/segmentation_webcam_example.py)

# Source

* [U-2-Net Github Repo](https://github.com/NathanUA/U-2-Net)

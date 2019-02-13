import numpy as np
from .colorspace import gray2rgb, bgr2rgb


def normalize_grayscale(src, to_float=True, epsilon=1e-7):
    """ Rescale image intensity.

    Rescale an grayscale image's intensity range to [0.0, 1.0].

    Args:
        src (ndarray): image to be intensity rescaled.
        to_float (bool): whether to convert the input image to float
            before processing.
        epsilon: a regularization term to avoid divide by 0 error.

    Return:
        (ndarray): intensity rescaled image.

    """
    if to_float:
        img = src.astype(np.float32)

    min_val, max_val = np.min(img), np.max(img)
    if max_val - min_val < epsilon:
        max_val += epsilon

    return (img - min_val) / (max_val - min_val)


def normalize_to_rgb(img, mean, std):
    """ Normalize an image (support grayscale and BGR image).

    If input image is an grayscale, first rescale intensity to [0.0, 255.0],
    then convert into a RGB image. Otherwise, (an BGR image), convert it to
    a RGB image of float32 type. Then dubtract mean per channel and divide
    by std per channel.

    Args:
        img (ndarray): image to be normalized.
        mean (tuple[float] or float): mean values.
        std (tuple[float] or float): standard deviations.
        to_rgb (bool): whether to convert the image to an uint8 RGB image
            before normalization.

    Return:
        (ndarray): the normalized image.
    """
    img = img.astype(np.float32)

    if img.ndim == 2:
        img = normalize_grayscale(img, to_float=False) * 255.0
        img = gray2rgb(img)
    else:  # img.ndim == 3
        img = bgr2rgb(img)

    return (img - mean) / std

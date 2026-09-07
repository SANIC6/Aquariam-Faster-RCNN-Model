import pytest

def test_bbox_conversion(target):
    boxes = target["boxes"]
    #Check if shape is 4
    assert boxes.shape[1] == 4
    #Check if ALL x_min is smaller than x_max vice versa for y_min and y_max
    assert (boxes[:, 0] < boxes[:, 2]).all()
    assert (boxes[:, 1] < boxes[:, 3]).all()

def test_bbox_in_img(img, target):
    #Check if ALL bounding boxes are within the image
    h, w = img.shape[1], img.shape[2]
    boxes = target["boxes"]
    assert (boxes[:, 0] >= 0).all()
    assert (boxes[:, 1] >= 0).all()
    assert (boxes[:, 2] <= w).all()
    assert (boxes[:, 3] <= h).all()

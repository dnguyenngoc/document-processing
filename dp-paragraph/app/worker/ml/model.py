"""
    @Author by Duy Nguyen Ngoc 
    @email: duynguyenngoc@hotmail.com
    @company-email: duynn_1@digi-texx.vn
    @Date: 2021-09-15
"""

from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model

# import util for keras_frcc
from worker.ml.keras_frcnn import config as frcnn_config
from worker.ml.keras_frcnn import losses as losses
import worker.ml.keras_frcnn.roi_helpers as roi_helpers
from worker.ml.keras_frcnn import resnet as nn
import numpy as np
import tensorflow as tf
import cv2
from settings import ml_config


class CompletedModel(object):
    """[summary] Loading complete model paragraph-frcnn
    Args:
        - Config model:
            {'verbose': True, 
            'network': 'resnet50', 
            'use_horizontal_flips': False, 
            'use_vertical_flips': False, 
            'rot_90': False, 
            'anchor_box_scales': [128, 256, 512], 
            'anchor_box_ratios': [[1, 1], [0.7071067811865475, 1.414213562373095], [1.414213562373095, 0.7071067811865475]], 
            'im_size': 416, 
            'img_channel_mean': [103.939, 116.779, 123.68], 
            'img_scaling_factor': 1.0, 
            'num_rois': 32, 
            'rpn_stride': 16, 
            'balanced_classes': False, 
            'std_scaling': 4.0, 
            'classifier_regr_std': [8.0, 8.0, 4.0, 4.0], 
            'rpn_min_overlap': 0.3, 'rpn_max_overlap': 0.7, 
            'classifier_min_overlap': 0.1, 
            'classifier_max_overlap': 0.5, 
            'class_mapping': {'paragraph': 0, 'bg': 1}, 
            'model_path': './worker/ml/models/ancestry_paragraph_restnet50_20211207.hdf5', 
            'base_net_weights': 
            './resnet50_weights_tf_dim_ordering_tf_kernels.h5'}
    """
    
    def __init__(self):
        self.class_mapping, self.C, self.model_rpn, self.model_classifier, self.model_classifier_only  = self._load_model()
        self.bbox_threshold = ml_config.BBOX_THRESHOLD
        self.overlap_thresh = ml_config.OVERLAP_THRESS
        
    @staticmethod
    def _load_model():
        config = tf.compat.v1.ConfigProto()
        config.log_device_placement = True
        sess = tf.compat.v1.Session(config=config)
        tf.compat.v1.keras.backend.set_session(sess)
        # print("====================================")
        # print('[Model] start ......................')
        C = frcnn_config.Config()
        C.use_horizontal_flips = bool(ml_config.HORIZONTAL_FLIPS)
        C.use_vertical_flips = bool(ml_config.VERTICAL_FLIPS)
        C.rot_90 = bool(ml_config.ROT_90)
        C.num_rois = int(ml_config.NUM_ROIS)
        C.network = ml_config.NETWORK
        C.model_path = ml_config.MODEL_PATH
        C.class_mapping = ml_config.CLASS_MAPPING
        
        class_mapping = C.class_mapping
        if 'bg' not in class_mapping:
            class_mapping['bg'] = len(class_mapping)
        class_mapping = {v: k for k, v in class_mapping.items()}
        
        num_features = int(ml_config.NUM_FEATURE)
        input_shape_img = (None, None, 3)
        input_shape_features = (None, None, num_features)
        img_input = Input(shape=input_shape_img)
        roi_input = Input(shape=(C.num_rois, 4))
        feature_map_input = Input(shape=input_shape_features)
        
        shared_layers = nn.nn_base(img_input, trainable=True)
        num_anchors = len(C.anchor_box_scales) * len(C.anchor_box_ratios)
        rpn_layers = nn.rpn(shared_layers, num_anchors)
        classifier = nn.classifier(feature_map_input, roi_input, C.num_rois, nb_classes=len(class_mapping), trainable=True)
        
        model_rpn = Model(img_input, rpn_layers)
        model_classifier_only = Model([feature_map_input, roi_input], classifier)
        model_classifier = Model([feature_map_input, roi_input], classifier)
        # print(f'Loading weights from {C.model_path}')
        model_rpn.load_weights(C.model_path, by_name=True)
        model_classifier.load_weights(C.model_path, by_name=True)
        model_rpn.compile(optimizer='sgd', loss='mse')
        model_classifier.compile(optimizer='sgd', loss='mse')
        return class_mapping, C, model_rpn, model_classifier, model_classifier_only 
           
    
    # Method to transform the coordinates of the bounding box to its original size
    def get_real_coordinates(self, ratio, x1, y1, x2, y2):
        real_x1 = int(round(x1 // ratio))
        real_y1 = int(round(y1 // ratio))
        real_x2 = int(round(x2 // ratio))
        real_y2 = int(round(y2 // ratio))
        return (real_x1, real_y1, real_x2 ,real_y2)
    
    def format_img_channels(self, img, C):
        """ formats the image channels based on config """
        img = img[:, :, (2, 1, 0)]
        img = img.astype(np.float32)
        img[:, :, 0] -= C.img_channel_mean[0]
        img[:, :, 1] -= C.img_channel_mean[1]
        img[:, :, 2] -= C.img_channel_mean[2]
        img /= C.img_scaling_factor
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0)
        return img

    def format_img_size(self, img, C):
        """ formats the image size based on config """
        img_min_side = float(C.im_size)
        (height,width,_) = img.shape
        if width <= height:
            ratio = img_min_side/width
            new_height = int(ratio * height)
            new_width = int(img_min_side)
        else:
            ratio = img_min_side/height
            new_width = int(ratio * width)
            new_height = int(img_min_side)
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        return img, ratio

    def format_img(self, img, C):
        """ formats an image for model prediction based on config """
        img, ratio = self.format_img_size(img, C)
        img = self.format_img_channels(img, C)
        return img, ratio

    # Method to transform the coordinates of the bounding box to its original size
    def get_real_coordinates(self, ratio, x1, y1, x2, y2):
        real_x1 = int(round(x1 // ratio))
        real_y1 = int(round(y1 // ratio))
        real_x2 = int(round(x2 // ratio))
        real_y2 = int(round(y2 // ratio))
        return (real_x1, real_y1, real_x2 ,real_y2)
            
    
    def predict(self, img):
        X, ratio = self.format_img(img, self.C)
        X = np.transpose(X, (0, 2, 3, 1))
        [Y1, Y2, F] = self.model_rpn.predict(X)
        R = roi_helpers.rpn_to_roi(Y1, Y2, self.C, 'tf', overlap_thresh=0.7) # (IoU) 'tf'
        R[:, 2] -= R[:, 0]
        R[:, 3] -= R[:, 1]
        bboxes = {}
        probs = {}   
        for jk in range(R.shape[0]//self.C.num_rois + 1):
            ROIs = np.expand_dims(R[self.C.num_rois*jk:self.C.num_rois*(jk+1), :], axis=0)
            if ROIs.shape[1] == 0:
                break
            if jk == R.shape[0]//self.C.num_rois:
                curr_shape = ROIs.shape
                target_shape = (curr_shape[0],self.C.num_rois,curr_shape[2])
                ROIs_padded = np.zeros(target_shape).astype(ROIs.dtype)
                ROIs_padded[:, :curr_shape[1], :] = ROIs
                ROIs_padded[0, curr_shape[1]:, :] = ROIs[0, 0, :]
                ROIs = ROIs_padded
            [P_cls, P_regr] = self.model_classifier_only.predict([F, ROIs])
            for ii in range(P_cls.shape[1]):
                if np.max(P_cls[0, ii, :]) < self.bbox_threshold or np.argmax(P_cls[0, ii, :]) == (P_cls.shape[2] - 1):
                    continue
                cls_name = self.class_mapping[np.argmax(P_cls[0, ii, :])]
                if cls_name not in bboxes:
                    bboxes[cls_name] = []
                    probs[cls_name] = []
                (x, y, w, h) = ROIs[0, ii, :]
                cls_num = np.argmax(P_cls[0, ii, :])
                try:
                    (tx, ty, tw, th) = P_regr[0, ii, 4*cls_num:4*(cls_num+1)]
                    tx /= self.C.classifier_regr_std[0]
                    ty /= self.C.classifier_regr_std[1]
                    tw /= self.C.classifier_regr_std[2]
                    th /= self.C.classifier_regr_std[3]
                    x, y, w, h = roi_helpers.apply_regr(x, y, w, h, tx, ty, tw, th)
                except:
                    pass
                bboxes[cls_name].append([self.C.rpn_stride*x, self.C.rpn_stride*y, self.C.rpn_stride*(x+w), self.C.rpn_stride*(y+h)])
                probs[cls_name].append(np.max(P_cls[0, ii, :]))
        all_dets = []
        h, w = img.shape[0:2]
        
        for key in bboxes:
            bbox = np.array(bboxes[key])
            new_boxes, new_probs = roi_helpers.non_max_suppression_fast(bbox, np.array(probs[key]), overlap_thresh=0.3)
            for jk in range(new_boxes.shape[0]):
                (x1, y1, x2, y2) = new_boxes[jk,:]
                (real_x1, real_y1, real_x2, real_y2) = self.get_real_coordinates(ratio, x1, y1, x2, y2)
                obj = {
                    "box": (int(real_x1), int(real_y1), int(real_x2), int(real_y2)), # box is int
                    "class_name": key + "_" + str(jk), # classname with stt
                    "confidence_level": new_probs[jk],  # confidence level with [0:1]
                } 
                all_dets.append(obj)
        return all_dets   
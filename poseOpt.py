import cv2
import numpy as np
from time import time

def pose_coordinate_descend(K, kpts_h, kpts3d, D, max_iters=1000, thresh=1e-3, pnp_int=True):
    '''
    Input
    K: (3, 3) intrinsic camera matrix
    kpts_h: (N, 3) homogeneous keypoint detection
    kpts3d: (N, 3) 3D model keypoints
    D: (N) confidence of each keypoint detection
    '''
    # normalized coordinate
    W = (np.linalg.inv(K) @ kpts_h.T).T
    
    # initialize R, t
    R = np.eye(3)
    t = W.mean(axis=0) * np.std(kpts3d, axis=0).mean() / (np.std(W, axis=0).mean() + 1e-12)
    
    # use PnP to initialize R and t
    conf_idx = (D > 0.3)
    if sum(conf_idx)>3 and pnp_int:
        model_points = np.array(kpts3d, dtype=np.double)[conf_idx]
        image_points = kpts_h[conf_idx,:2].astype(np.double)

        retval, rvec, tvec, inliers = cv2.solvePnPRansac(model_points, image_points, 
                                                         K, np.zeros((4,1)), flags=cv2.SOLVEPNP_P3P) 

        R, _ = cv2.Rodrigues(rvec)
        t = tvec.reshape([3])


    # main coordinate descend procedure    
    residual = np.inf
    for i in range(max_iters):
        # update Z
        X = kpts3d @ R.T + t #(N, 3)
        Z = (W*X).sum(axis=1) / (W**2).sum(axis=1) #(N,)
        
        # update t
        WZ = W * Z[:,None]
        t = ((WZ-kpts3d@R.T) * D[:,None]).sum(axis=0) / (D.sum() + 1e-12)
        
        # update R
        A = ((WZ-t) * D[:,None]).T @ kpts3d
        u,_,vt = np.linalg.svd(A)
        R = u @ vt
        if np.linalg.det(R) < 0:
            u[:, -1] *= -1
            R = u @ vt
            
        
        # update residual
        diff = (WZ - kpts3d@R.T - t) * D[:,None]
        new_residual = np.linalg.norm(diff, axis=1).mean()
        
        if np.abs(residual-new_residual)/(new_residual+1e-12) < thresh:
            break
        else:
            residual = new_residual


    return R, t, Z, residual



package com.jprodevelopment.unscrabble;

import org.opencv.core.MatOfPoint2f;

public class PipelineContext {
    private MatOfPoint2f corners;

    public MatOfPoint2f getCorners() {
        return corners;
    }

    public void setCorners(MatOfPoint2f corners) {
        this.corners = corners;
    }
}

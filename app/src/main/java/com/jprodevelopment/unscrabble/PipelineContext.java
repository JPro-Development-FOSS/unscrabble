package com.jprodevelopment.unscrabble;

import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint2f;

public class PipelineContext {
    private MatOfPoint2f corners;
    private Mat originalBoard;
    private Mat rectifiedBoard;

    public MatOfPoint2f getCorners() {
        return corners;
    }

    public void setCorners(MatOfPoint2f corners) {
        this.corners = corners;
    }

    public Mat getRectifiedBoard() {
        return rectifiedBoard;
    }

    public Mat getOriginalBoard() {
        return originalBoard;
    }

    public void setOriginalBoard(Mat originalBoard) {
        this.originalBoard = originalBoard;
    }

    public void setRectifiedBoard(Mat rectifiedBoard) {
        this.rectifiedBoard = rectifiedBoard;
    }
}

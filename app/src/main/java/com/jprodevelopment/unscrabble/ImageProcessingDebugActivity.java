package com.jprodevelopment.unscrabble;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.CameraBridgeViewBase.CvCameraViewFrame;
import org.opencv.android.LoaderCallbackInterface;
import org.opencv.android.OpenCVLoader;
import org.opencv.core.Mat;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.CameraBridgeViewBase.CvCameraViewListener2;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.WindowManager;

public class ImageProcessingDebugActivity extends Activity implements CvCameraViewListener2 {

    private static final String  TAG                 = "OCVSample::Activity";
    private ImageManipulator imageManipulator = new ImageManipulator();

    private MenuItem mItemPreviewRGBA;
    private MenuItem             mItemPreviewHist;
    private MenuItem             mItemPreviewCanny;
    private MenuItem             mItemPreviewSepia;
    private MenuItem             mItemPreviewSobel;
    private MenuItem             mItemPreviewZoom;
    private MenuItem             mItemPreviewPixelize;
    private MenuItem             mItemPreviewPosterize;

    private BaseLoaderCallback  mLoaderCallback = new BaseLoaderCallback(this) {
        @Override
        public void onManagerConnected(int status) {
            switch (status) {
                case LoaderCallbackInterface.SUCCESS:
                {
                    Log.i(TAG, "OpenCV loaded successfully");
                    imageManipulator.getmOpenCvCameraView().enableView();
                } break;
                default:
                {
                    super.onManagerConnected(status);
                } break;
            }
        }
    };

    public ImageProcessingDebugActivity() {
        Log.i(TAG, "Instantiated new " + this.getClass());
    }

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        Log.i(TAG, "called onCreate");
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        setContentView(R.layout.image_manipulations_surface_view);

        imageManipulator.setmOpenCvCameraView((CameraBridgeViewBase) findViewById(R.id.image_manipulations_activity_surface_view));
        imageManipulator.getmOpenCvCameraView().setVisibility(CameraBridgeViewBase.VISIBLE);
        imageManipulator.getmOpenCvCameraView().setCvCameraViewListener(this);
    }

    @Override
    public void onPause()
    {
        super.onPause();
        if (imageManipulator.getmOpenCvCameraView() != null)
            imageManipulator.getmOpenCvCameraView().disableView();
    }

    @Override
    public void onResume()
    {
        super.onResume();
        if (!OpenCVLoader.initDebug()) {
            Log.d(TAG, "Internal OpenCV library not found. Using OpenCV Manager for initialization");
            OpenCVLoader.initAsync(OpenCVLoader.OPENCV_VERSION_3_0_0, this, mLoaderCallback);
        } else {
            Log.d(TAG, "OpenCV library found inside package. Using it!");
            mLoaderCallback.onManagerConnected(LoaderCallbackInterface.SUCCESS);
        }
    }

    public void onDestroy() {
        super.onDestroy();
        if (imageManipulator.getmOpenCvCameraView() != null)
            imageManipulator.getmOpenCvCameraView().disableView();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        Log.i(TAG, "called onCreateOptionsMenu");
        mItemPreviewRGBA  = menu.add("Preview RGBA");
        mItemPreviewHist  = menu.add("Histograms");
        mItemPreviewCanny = menu.add("Canny");
        mItemPreviewSepia = menu.add("Sepia");
        mItemPreviewSobel = menu.add("Sobel");
        mItemPreviewZoom  = menu.add("Zoom");
        mItemPreviewPixelize  = menu.add("Pixelize");
        mItemPreviewPosterize = menu.add("Posterize");
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        Log.i(TAG, "called onOptionsItemSelected; selected item: " + item);
        if (item == mItemPreviewRGBA)
            ImageManipulator.viewMode = ImageManipulator.VIEW_MODE_RGBA;
        if (item == mItemPreviewHist)
            ImageManipulator.viewMode = ImageManipulator.VIEW_MODE_HIST;
        else if (item == mItemPreviewCanny)
            ImageManipulator.viewMode = ImageManipulator.VIEW_MODE_CANNY;
        else if (item == mItemPreviewSepia)
            ImageManipulator.viewMode = ImageManipulator.VIEW_MODE_SEPIA;
        else if (item == mItemPreviewSobel)
            ImageManipulator.viewMode = ImageManipulator.VIEW_MODE_SOBEL;
        else if (item == mItemPreviewZoom)
            ImageManipulator.viewMode = ImageManipulator.VIEW_MODE_ZOOM;
        else if (item == mItemPreviewPixelize)
            ImageManipulator.viewMode = ImageManipulator.VIEW_MODE_PIXELIZE;
        else if (item == mItemPreviewPosterize)
            ImageManipulator.viewMode = ImageManipulator.VIEW_MODE_POSTERIZE;
        return true;
    }

    public void onCameraViewStarted(int width, int height) {
        imageManipulator.onCameraViewStarted(width, height);
    }

    public void onCameraViewStopped() {
        // Explicitly deallocate Mats
        if (imageManipulator.getmIntermediateMat() != null)
            imageManipulator.getmIntermediateMat().release();

        imageManipulator.setmIntermediateMat(null);
    }

    public Mat onCameraFrame(CvCameraViewFrame inputFrame) {
        return imageManipulator.onCameraFrame(inputFrame);
    }
}

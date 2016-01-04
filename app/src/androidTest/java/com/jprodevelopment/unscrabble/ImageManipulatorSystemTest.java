package com.jprodevelopment.unscrabble;

import android.app.Application;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Environment;
import android.support.annotation.NonNull;
import android.test.ApplicationTestCase;

import org.opencv.android.OpenCVLoader;
import org.opencv.android.Utils;
import org.opencv.core.Mat;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

/**
 * I wish that we could test this via Android unit tests run on the JVM, but there are two
 * problems. One is that it's difficult to load Bitmap resources inside of a JVM based unit test.
 * However, this can be solved with Robolectric mocks. Problem two is that Robolectric can't
 * load and execute arbitrary JNI libs. OpenCV relies on JNI libs. For these reasons, we are
 * forced to make these image manipulation tests full on activity tests (which run on the
 * emulator).
 */
public class ImageManipulatorSystemTest extends ApplicationTestCase<Application> {

    private final String testRunTimestamp;

    /// JUnit3 has no "BeforeClass" facility
    private static boolean firstTest = true;

    public ImageManipulatorSystemTest() {
        super(Application.class);
        OpenCVLoader.initDebug();
        testRunTimestamp = Long.toString(System.currentTimeMillis());
    }

    private ImageManipulator underTest;
    private Bitmap inputBitmap;
    private Mat inputMat;

    public void setUp() {
        if(firstTest) {
            firstTest = false;
            createApplication();
            inputBitmap = BitmapFactory.decodeResource(getApplication().getResources(), R.drawable.test_board_1);
            inputMat = new Mat();
            Utils.bitmapToMat(inputBitmap, inputMat);
        }
        underTest = new ImageManipulator();
        underTest.onCameraViewStarted(inputBitmap.getWidth(), inputBitmap.getHeight());
    }

    public void testCanFilterForCorners() throws Throwable {

        ImageManipulator.viewMode = ImageManipulator.VIEW_MODE_HIST;
        Mat result = underTest.processMat(inputMat, null);

        Bitmap resultBitmap = Bitmap.createBitmap(inputBitmap.getWidth(),
                inputBitmap.getHeight(), Bitmap.Config.ARGB_8888);
        Utils.matToBitmap(result, resultBitmap);

        File file = writeBitmapToStorage(resultBitmap);

        assertNotNull(resultBitmap);
        assertNotNull(file);
    }

    private File writeBitmapToStorage(Bitmap bitmap) throws IOException {
        String file_path = getApplication().getFilesDir().getAbsolutePath() + "/unscrabble";
        File dir = new File(file_path);
        if(!dir.exists())
            dir.mkdirs();
        File file = new File(dir, getName() + testRunTimestamp + ".png");
        FileOutputStream fOut = new FileOutputStream(file);

        bitmap.compress(Bitmap.CompressFormat.PNG, 85, fOut);
        fOut.flush();
        fOut.close();
        return file;
    }
}
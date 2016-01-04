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

    private static Mat inputMat;

    private ImageManipulator underTest;

    public void setUp() {
        createApplication();
        if(firstTest) {
            firstTest = false;

            // get appropriate sample rate
            BitmapFactory.Options options = new BitmapFactory.Options();
            options.inJustDecodeBounds = true;
            BitmapFactory.decodeResource(getApplication().getResources(), R.drawable.test_board_1, options);
            int inSampleSize = calculateInSampleSize(options, 1024, 1024);

            options = new BitmapFactory.Options();
            options.inSampleSize = inSampleSize;
            Bitmap inputBitmap = BitmapFactory.decodeResource(getApplication().getResources(), R.drawable.test_board_1, options);
            inputMat = new Mat();
            Utils.bitmapToMat(inputBitmap, inputMat);
        }
        underTest = new ImageManipulator();
        underTest.onCameraViewStarted(inputMat.width(), inputMat.height());
    }

    public void testCanFilterForCorners() throws Throwable {

        ImageManipulator.viewMode = ImageManipulator.VIEW_MODE_CORNER_FINDER;
        Mat result = underTest.processMat(inputMat, null);


        Bitmap resultBitmap = Bitmap.createBitmap(result.width(),
                result.height(), Bitmap.Config.RGB_565);
        Utils.matToBitmap(result, resultBitmap);

        File file = writeBitmapToStorage(resultBitmap);

        assertNotNull(resultBitmap);
        assertNotNull(file);
    }

    private int calculateInSampleSize(
            BitmapFactory.Options options, int reqWidth, int reqHeight) {
        // Raw height and width of image
        final int height = options.outHeight;
        final int width = options.outWidth;
        int inSampleSize = 1;

        if (height > reqHeight || width > reqWidth) {

            final int halfHeight = height / 2;
            final int halfWidth = width / 2;

            // Calculate the largest inSampleSize value that is a power of 2 and keeps both
            // height and width larger than the requested height and width.
            while ((halfHeight / inSampleSize) > reqHeight
                    && (halfWidth / inSampleSize) > reqWidth) {
                inSampleSize *= 2;
            }
        }

        return inSampleSize;
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
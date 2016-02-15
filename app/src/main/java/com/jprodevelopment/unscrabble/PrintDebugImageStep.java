package com.jprodevelopment.unscrabble;

import android.graphics.Bitmap;
import android.util.Log;

import org.opencv.android.Utils;
import org.opencv.core.Mat;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

public class PrintDebugImageStep extends PipelineStep {

    private final String unscrabbleStorageDir;
    private final String runId;

    /**
     * Saves the image in the input matrix to Android disk storage for debugging purposes. We assume
     * each pipeline step for which we want to save debug images will have a unique step name.
     * @param prevStepName name of the step that we're debugging
     * @param storageDir directory to save images to
     * @param runId unique id for this run of the pipeline (used to group other debug images from
     *              the same run)
     */
    public PrintDebugImageStep(String prevStepName, String storageDir, String runId, PipelineContext context) {
        super(prevStepName + "_debug_print", context);
        this.unscrabbleStorageDir = storageDir + "/unscrabble";
        this.runId = runId;
    }

    @Override
    public Mat process(Mat input) {
        Bitmap resultBitmap =
                Bitmap.createBitmap(input.width(), input.height(), Bitmap.Config.RGB_565);
        Utils.matToBitmap(input, resultBitmap);
        try {
            writeBitmapToStorage(resultBitmap);
        } catch (IOException e) {
            Log.e(this.getClass().getName(), e.getMessage());
        }
        return input;
    }

    private File writeBitmapToStorage(Bitmap bitmap) throws IOException {
        String file_path = unscrabbleStorageDir;
        File dir = new File(file_path);
        if(!dir.exists())
            dir.mkdirs();
        File file = new File(dir, runId + getName() + ".png");
        FileOutputStream fOut = new FileOutputStream(file);

        bitmap.compress(Bitmap.CompressFormat.PNG, 85, fOut);
        fOut.flush();
        fOut.close();
        return file;
    }
}

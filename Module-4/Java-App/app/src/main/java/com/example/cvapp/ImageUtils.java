package com.example.cvapp;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import androidx.exifinterface.media.ExifInterface;

import java.io.IOException;

public class ImageUtils {

    public static Bitmap getCorrectlyOrientedBitmap(String imagePath) {
        Bitmap bitmap = BitmapFactory.decodeFile(imagePath);
        try {
            ExifInterface exif = new ExifInterface(imagePath);
            int orientation = exif.getAttributeInt(ExifInterface.TAG_ORIENTATION, ExifInterface.ORIENTATION_NORMAL);

            int rotation = 0;
            switch (orientation) {
                case ExifInterface.ORIENTATION_ROTATE_90: rotation = 90; break;
                case ExifInterface.ORIENTATION_ROTATE_180: rotation = 180; break;
                case ExifInterface.ORIENTATION_ROTATE_270: rotation = 270; break;
            }

            if (rotation != 0) {
                Matrix matrix = new Matrix();
                matrix.postRotate(rotation);
                return Bitmap.createBitmap(bitmap, 0, 0, bitmap.getWidth(), bitmap.getHeight(), matrix, true);
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
        return bitmap;
    }
}

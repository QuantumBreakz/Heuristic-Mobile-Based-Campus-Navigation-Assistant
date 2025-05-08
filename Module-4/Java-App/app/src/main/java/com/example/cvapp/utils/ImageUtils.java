package com.example.cvapp.utils;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Base64;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

public class ImageUtils {
    private static final int MAX_IMAGE_SIZE = 1024; // Maximum dimension for image
    private static final int COMPRESSION_QUALITY = 80; // JPEG compression quality

    public static String bitmapToBase64(Bitmap bitmap) {
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, COMPRESSION_QUALITY, byteArrayOutputStream);
        byte[] byteArray = byteArrayOutputStream.toByteArray();
        return Base64.encodeToString(byteArray, Base64.DEFAULT);
    }

    public static Bitmap compressImage(Bitmap original) {
        int width = original.getWidth();
        int height = original.getHeight();

        if (width <= MAX_IMAGE_SIZE && height <= MAX_IMAGE_SIZE) {
            return original;
        }

        float ratio = Math.min(
                (float) MAX_IMAGE_SIZE / width,
                (float) MAX_IMAGE_SIZE / height
        );

        int newWidth = Math.round(width * ratio);
        int newHeight = Math.round(height * ratio);

        return Bitmap.createScaledBitmap(original, newWidth, newHeight, true);
    }

    public static File saveBitmapToFile(Bitmap bitmap, File file) throws IOException {
        FileOutputStream fos = new FileOutputStream(file);
        bitmap.compress(Bitmap.CompressFormat.JPEG, COMPRESSION_QUALITY, fos);
        fos.close();
        return file;
    }

    public static Bitmap loadImageFromFile(File file) {
        return BitmapFactory.decodeFile(file.getAbsolutePath());
    }
} 
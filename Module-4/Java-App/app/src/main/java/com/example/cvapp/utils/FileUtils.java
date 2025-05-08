package com.example.cvapp.utils;

import android.util.Base64;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;

public class FileUtils {
    public static String fileToBase64(File file) {
        try {
            byte[] bytes = new byte[(int) file.length()];
            InputStream inputStream = new FileInputStream(file);
            inputStream.read(bytes);
            inputStream.close();
            return Base64.encodeToString(bytes, Base64.DEFAULT);
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    public static File createImageFile(File directory, String prefix, String extension) throws IOException {
        return File.createTempFile(prefix, extension, directory);
    }

    public static boolean deleteFile(File file) {
        return file != null && file.exists() && file.delete();
    }

    public static String getFileExtension(String fileName) {
        if (fileName == null) return "";
        int lastDotIndex = fileName.lastIndexOf('.');
        return lastDotIndex > 0 ? fileName.substring(lastDotIndex + 1) : "";
    }

    public static String getFileNameWithoutExtension(String fileName) {
        if (fileName == null) return "";
        int lastDotIndex = fileName.lastIndexOf('.');
        return lastDotIndex > 0 ? fileName.substring(0, lastDotIndex) : fileName;
    }
} 
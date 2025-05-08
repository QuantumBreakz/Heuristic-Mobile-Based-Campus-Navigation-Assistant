package com.example.cvapp;

import android.content.Context;
import android.database.Cursor;
import android.net.Uri;
import android.provider.OpenableColumns;
import java.io.*;

public class FileUtils {
    public static File uriToFile(Context context, Uri uri) throws IOException {
        String fileName = getFileName(context, uri);
        File file = new File(context.getCacheDir(), fileName);
        InputStream inputStream = context.getContentResolver().openInputStream(uri);
        OutputStream outputStream = new FileOutputStream(file);
        byte[] buf = new byte[1024];
        int len;
        while ((len = inputStream.read(buf)) > 0) {
            outputStream.write(buf, 0, len);
        }
        outputStream.close();
        inputStream.close();
        return file;
    }

    private static String getFileName(Context context, Uri uri) {
        String result = "image.jpg";
        try (Cursor cursor = context.getContentResolver().query(uri, null, null, null, null)) {
            if (cursor != null && cursor.moveToFirst()) {
                int idx = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);
                if (idx != -1) result = cursor.getString(idx);
            }
        }
        return result;
    }
}
